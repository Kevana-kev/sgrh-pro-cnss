<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Department;
use App\Models\Employee;
use App\Services\ActivityLogger;
use App\Support\SpaSerializer;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class DepartmentApiController extends Controller
{
    public function index(): JsonResponse
    {
        $departments = Department::query()->with(['employees.department', 'employees.role', 'employees.user'])->orderBy('name')->get();

        return response()->json($departments->map(fn (Department $d) => SpaSerializer::department($d))->values());
    }

    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'name' => ['required', 'string', 'max:120', 'unique:departments,name'],
            'budget' => ['nullable', 'numeric', 'min:0'],
            'manager_id' => ['nullable', 'exists:employees,id'],
        ]);

        $department = Department::create([
            'name' => $data['name'],
            'budget' => $data['budget'] ?? 0,
            'manager_id' => $data['manager_id'] ?? null,
        ]);

        ActivityLogger::log($request->user()?->username, 'Création département #'.$department->id);

        return response()->json(SpaSerializer::department($department->fresh(['employees'])), 201);
    }

    public function update(Request $request, int $departmentId): JsonResponse
    {
        $department = Department::findOrFail($departmentId);

        $data = $request->validate([
            'name' => ['sometimes', 'string', 'max:120', 'unique:departments,name,'.$department->id],
            'budget' => ['sometimes', 'numeric', 'min:0'],
            'manager_id' => ['nullable', 'exists:employees,id'],
        ]);

        $department->fill($data)->save();
        ActivityLogger::log($request->user()?->username, 'Modification département #'.$department->id);

        return response()->json(SpaSerializer::department($department->fresh(['employees'])));
    }

    public function destroy(Request $request, int $departmentId): JsonResponse
    {
        $department = Department::findOrFail($departmentId);

        if ($department->employees()->exists()) {
            return response()->json(['error' => 'Impossible de supprimer un département avec des employés'], 422);
        }

        $department->delete();
        ActivityLogger::log($request->user()?->username, 'Suppression département #'.$departmentId);

        return response()->json(['message' => 'Département supprimé']);
    }

    public function assignManager(Request $request, int $departmentId, int $managerId): JsonResponse
    {
        $department = Department::findOrFail($departmentId);
        Employee::findOrFail($managerId);

        $department->manager_id = $managerId;
        $department->save();

        ActivityLogger::log($request->user()?->username, "Assignation manager {$managerId} -> département {$departmentId}");

        return response()->json(SpaSerializer::department($department->fresh(['employees'])));
    }
}

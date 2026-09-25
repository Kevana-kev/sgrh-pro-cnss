<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Employee;
use App\Models\Role;
use App\Models\User;
use App\Services\ActivityLogger;
use App\Support\SpaSerializer;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class EmployeeApiController extends Controller
{
    public function index(): JsonResponse
    {
        $employees = Employee::query()
            ->with(['department', 'role', 'user'])
            ->orderBy('last_name')
            ->orderBy('first_name')
            ->get();

        return response()->json($employees->map(fn (Employee $e) => SpaSerializer::employee($e))->values());
    }

    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'first_name' => ['required', 'string', 'max:100'],
            'last_name' => ['required', 'string', 'max:100'],
            'email' => ['required', 'email', 'max:120', 'unique:employees,email'],
            'phone' => ['required', 'string', 'max:30'],
            'address' => ['required', 'string', 'max:255'],
            'hire_date' => ['required', 'date'],
            'status' => ['nullable', 'string', 'max:30'],
            'department_id' => ['nullable', 'exists:departments,id'],
            'role_id' => ['required', 'exists:roles,id'],
            'photo_url' => ['nullable', 'string', 'max:255'],
            'photo_path' => ['nullable', 'string', 'max:255'],
            'matricule' => ['nullable', 'string', 'max:40', 'unique:employees,matricule'],
        ]);

        $role = Role::findOrFail($data['role_id']);
        $matricule = $data['matricule'] ?? $this->generateMatricule($data['department_id'] ?? null, $data['hire_date']);
        $defaultPassword = config('app.default_agent_password', 'Agent@123');

        $result = DB::transaction(function () use ($data, $role, $matricule, $defaultPassword) {
            $employee = Employee::create([
                'first_name' => $data['first_name'],
                'last_name' => $data['last_name'],
                'email' => $data['email'],
                'phone' => $data['phone'],
                'address' => $data['address'],
                'hire_date' => $data['hire_date'],
                'status' => $data['status'] ?? 'Actif',
                'department_id' => $data['department_id'] ?? null,
                'role_id' => $role->id,
                'matricule' => $matricule,
                'photo_path' => $data['photo_path'] ?? $data['photo_url'] ?? null,
            ]);

            $user = User::create([
                'username' => $matricule,
                'password' => $defaultPassword,
                'role_id' => $role->id,
                'employee_id' => $employee->id,
                'must_change_password' => true,
            ]);

            return [$employee->fresh(['department', 'role', 'user']), $user, $defaultPassword];
        });

        [$employee, $user, $defaultPassword] = $result;
        ActivityLogger::log($request->user()?->username, 'Création employé #'.$employee->id);

        return response()->json([
            ...SpaSerializer::employee($employee),
            'generated_account' => [
                'username' => $user->username,
                'must_change_password' => $user->must_change_password,
                'default_password' => $defaultPassword,
            ],
        ], 201);
    }

    public function update(Request $request, int $employeeId): JsonResponse
    {
        $employee = Employee::findOrFail($employeeId);

        $data = $request->validate([
            'first_name' => ['sometimes', 'string', 'max:100'],
            'last_name' => ['sometimes', 'string', 'max:100'],
            'email' => ['sometimes', 'email', 'max:120', 'unique:employees,email,'.$employee->id],
            'phone' => ['sometimes', 'string', 'max:30'],
            'address' => ['sometimes', 'string', 'max:255'],
            'hire_date' => ['sometimes', 'date'],
            'status' => ['sometimes', 'string', 'max:30'],
            'department_id' => ['nullable', 'exists:departments,id'],
            'role_id' => ['sometimes', 'exists:roles,id'],
            'photo_url' => ['nullable', 'string', 'max:255'],
            'photo_path' => ['nullable', 'string', 'max:255'],
            'matricule' => ['sometimes', 'string', 'max:40', 'unique:employees,matricule,'.$employee->id],
        ]);

        if (array_key_exists('photo_url', $data) && ! array_key_exists('photo_path', $data)) {
            $data['photo_path'] = $data['photo_url'];
        }
        unset($data['photo_url']);

        $employee->fill($data);
        $employee->save();

        if ($employee->user && isset($data['role_id'])) {
            $employee->user->role_id = $data['role_id'];
            $employee->user->save();
        }

        ActivityLogger::log($request->user()?->username, 'Modification employé #'.$employee->id);

        return response()->json(SpaSerializer::employee($employee->fresh(['department', 'role', 'user'])));
    }

    public function destroy(Request $request, int $employeeId): JsonResponse
    {
        $employee = Employee::findOrFail($employeeId);
        $employee->user?->delete();
        $employee->delete();

        ActivityLogger::log($request->user()?->username, 'Suppression employé #'.$employeeId);

        return response()->json(['message' => 'Employé supprimé']);
    }

    private function generateMatricule(?int $departmentId, string $hireDate): string
    {
        $year = date('Y', strtotime($hireDate));
        $prefix = 'EMP'.$year.str_pad((string) ($departmentId ?? 0), 2, '0', STR_PAD_LEFT);

        do {
            $matricule = $prefix.Str::upper(Str::random(4));
        } while (Employee::where('matricule', $matricule)->exists());

        return $matricule;
    }
}

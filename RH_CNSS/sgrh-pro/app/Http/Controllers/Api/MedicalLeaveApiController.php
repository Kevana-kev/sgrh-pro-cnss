<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\MedicalLeave;
use App\Services\ActivityLogger;
use App\Support\SpaSerializer;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class MedicalLeaveApiController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $user = $request->user();
        $role = $user->role?->name;

        if (in_array($role, ['SuperAdmin', 'Admin RH', 'RH', 'Administrateur'], true)
            || $user->hasPermission('Voir congés médicaux')) {
            $leaves = MedicalLeave::query()->with('employee')->orderByDesc('created_at')->get();
        } else {
            $leaves = $user->employee_id
                ? MedicalLeave::query()->with('employee')->where('employee_id', $user->employee_id)->get()
                : collect();
        }

        return response()->json($leaves->map(fn (MedicalLeave $ml) => SpaSerializer::medicalLeave($ml))->values());
    }

    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
            'start_date' => ['required', 'date'],
            'end_date' => ['required', 'date'],
            'diagnosis' => ['nullable', 'string', 'max:255'],
            'certificate_path' => ['nullable', 'string', 'max:255'],
            'daily_allowance' => ['nullable', 'numeric'],
            'status' => ['nullable', 'string', 'max:30'],
        ]);

        $ml = MedicalLeave::create([
            'employee_id' => $data['employee_id'],
            'start_date' => $data['start_date'],
            'end_date' => $data['end_date'],
            'diagnosis' => $data['diagnosis'] ?? null,
            'certificate_path' => $data['certificate_path'] ?? null,
            'daily_allowance' => $data['daily_allowance'] ?? 0,
            'status' => $data['status'] ?? 'En attente',
        ]);

        ActivityLogger::log($request->user()?->username, 'Congé médical #'.$ml->id.' créé');

        return response()->json(SpaSerializer::medicalLeave($ml->fresh('employee')), 201);
    }

    public function show(int $mlId): JsonResponse
    {
        $ml = MedicalLeave::with('employee')->findOrFail($mlId);

        return response()->json(SpaSerializer::medicalLeave($ml));
    }

    public function update(Request $request, int $mlId): JsonResponse
    {
        $ml = MedicalLeave::findOrFail($mlId);

        $data = $request->validate([
            'diagnosis' => ['nullable', 'string', 'max:255'],
            'certificate_path' => ['nullable', 'string', 'max:255'],
            'daily_allowance' => ['nullable', 'numeric'],
            'status' => ['sometimes', 'string', 'max:30'],
            'start_date' => ['sometimes', 'date'],
            'end_date' => ['sometimes', 'date'],
        ]);

        $ml->fill($data)->save();
        ActivityLogger::log($request->user()?->username, 'Congé médical #'.$mlId.' mis à jour');

        return response()->json(SpaSerializer::medicalLeave($ml->fresh('employee')));
    }

    public function destroy(int $mlId): JsonResponse
    {
        MedicalLeave::findOrFail($mlId)->delete();

        return response()->json(['message' => 'Congé médical supprimé']);
    }
}

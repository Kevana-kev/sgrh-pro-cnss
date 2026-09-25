<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Leave;
use App\Services\ActivityLogger;
use App\Support\SpaSerializer;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class LeaveApiController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $user = $request->user();
        $query = Leave::query()->orderByDesc('id');

        if (! $user->hasPermission('Valider congés')) {
            $query->where('employee_id', $user->employee_id);
        }

        return response()->json($query->get()->map(fn (Leave $l) => SpaSerializer::leave($l))->values());
    }

    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
            'start_date' => ['required', 'date'],
            'end_date' => ['required', 'date', 'after_or_equal:start_date'],
            'reason' => ['required', 'string', 'max:255'],
            'status' => ['nullable', 'string', 'max:40'],
        ]);

        $leave = Leave::create([
            'employee_id' => $data['employee_id'],
            'start_date' => $data['start_date'],
            'end_date' => $data['end_date'],
            'reason' => $data['reason'],
            'status' => $data['status'] ?? 'En attente',
        ]);

        ActivityLogger::log($request->user()?->username, 'Demande congé #'.$leave->id);

        return response()->json(SpaSerializer::leave($leave), 201);
    }

    public function approval(Request $request, int $leaveId): JsonResponse
    {
        $data = $request->validate([
            'status' => ['required', 'string', 'in:Approuvé,Rejeté,En attente'],
            'decision_comment' => ['nullable', 'string', 'max:500'],
        ]);

        $leave = Leave::findOrFail($leaveId);
        $leave->status = $data['status'];
        $leave->decision_comment = $data['decision_comment'] ?? $leave->decision_comment;
        $leave->save();

        ActivityLogger::log($request->user()?->username, "Validation congé #{$leave->id}: {$leave->status}");

        return response()->json(SpaSerializer::leave($leave));
    }

    public function update(Request $request, int $leaveId): JsonResponse
    {
        $leave = Leave::findOrFail($leaveId);
        $user = $request->user();

        if (! $user->hasPermission('Valider congés') && $user->employee_id !== $leave->employee_id) {
            return response()->json(['error' => 'Accès refusé'], 403);
        }

        $data = $request->validate([
            'start_date' => ['sometimes', 'date'],
            'end_date' => ['sometimes', 'date'],
            'reason' => ['sometimes', 'string', 'max:255'],
            'status' => ['sometimes', 'string', 'max:40'],
            'decision_comment' => ['nullable', 'string', 'max:500'],
        ]);

        $leave->fill($data)->save();
        ActivityLogger::log($user->username, 'Modification congé #'.$leave->id);

        return response()->json(SpaSerializer::leave($leave));
    }

    public function destroy(Request $request, int $leaveId): JsonResponse
    {
        $leave = Leave::findOrFail($leaveId);
        $user = $request->user();

        if (! $user->hasPermission('Valider congés') && $user->employee_id !== $leave->employee_id) {
            return response()->json(['error' => 'Accès refusé'], 403);
        }

        $leave->delete();
        ActivityLogger::log($user->username, 'Suppression congé #'.$leaveId);

        return response()->json(['message' => 'Congé supprimé']);
    }
}

<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\ActivityLog;
use App\Models\Role;
use App\Models\User;
use App\Services\ActivityLogger;
use App\Support\SpaSerializer;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\StreamedResponse;

class AccountApiController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        if (! $this->isAdmin($request)) {
            return response()->json(['error' => 'Accès interdit'], 403);
        }

        $users = User::query()->with(['role', 'employee'])->orderByDesc('id')->get();

        return response()->json($users->map(fn (User $u) => SpaSerializer::account($u))->values());
    }

    public function resetPassword(Request $request, int $userId): JsonResponse
    {
        if (! $this->isAdmin($request)) {
            return response()->json(['error' => 'Accès interdit'], 403);
        }

        $user = User::findOrFail($userId);
        $defaultPassword = config('app.default_agent_password', 'Agent@123');
        $user->password = $defaultPassword;
        $user->must_change_password = true;
        $user->save();
        $user->tokens()->delete();

        ActivityLogger::log($request->user()?->username, 'Reset mot de passe compte #'.$user->id);

        return response()->json([
            'message' => 'Mot de passe réinitialisé',
            'user_id' => $user->id,
            'must_change_password' => true,
        ]);
    }

    public function updateRole(Request $request, int $userId): JsonResponse
    {
        if (! $this->isAdmin($request)) {
            return response()->json(['error' => 'Accès interdit'], 403);
        }

        $data = $request->validate([
            'role_id' => ['required', 'exists:roles,id'],
        ]);

        $user = User::with(['role', 'employee'])->findOrFail($userId);
        $role = Role::findOrFail($data['role_id']);

        $user->role_id = $role->id;
        $user->save();

        if ($user->employee) {
            $user->employee->role_id = $role->id;
            $user->employee->save();
        }

        ActivityLogger::log($request->user()?->username, "Changement rôle compte #{$user->id} -> role #{$role->id}");

        return response()->json([
            'message' => 'Rôle mis à jour',
            'user_id' => $user->id,
            'role' => $role->name,
        ]);
    }

    public function updateStatus(Request $request, int $userId): JsonResponse
    {
        if (! $this->isAdmin($request)) {
            return response()->json(['error' => 'Accès interdit'], 403);
        }

        $data = $request->validate([
            'status' => ['required', 'string', 'in:Actif,Suspendu,Démissionné'],
        ]);

        $user = User::with('employee')->findOrFail($userId);

        if (! $user->employee) {
            return response()->json(['error' => "Ce compte n'est pas lié à un agent"], 422);
        }

        $user->employee->status = $data['status'];
        $user->employee->save();

        ActivityLogger::log($request->user()?->username, "Changement statut compte #{$user->id} -> {$data['status']}");

        return response()->json([
            'message' => 'Statut mis à jour',
            'user_id' => $user->id,
            'status' => $user->employee->status,
        ]);
    }

    public function activity(Request $request): JsonResponse
    {
        if (! $this->isAdmin($request)) {
            return response()->json(['error' => 'Accès interdit'], 403);
        }

        $logs = $this->activityQuery($request)->orderByDesc('created_at')->limit(200)->get();

        return response()->json($logs->map(fn (ActivityLog $log) => [
            'id' => $log->id,
            'username' => $log->username,
            'action' => $log->action,
            'created_at' => optional($log->created_at)?->toIso8601String(),
        ])->values());
    }

    public function exportActivityCsv(Request $request): StreamedResponse|JsonResponse
    {
        if (! $this->isAdmin($request)) {
            return response()->json(['error' => 'Accès interdit'], 403);
        }

        $logs = $this->activityQuery($request)->orderByDesc('created_at')->limit(2000)->get();

        return response()->streamDownload(function () use ($logs) {
            $out = fopen('php://output', 'w');
            fputcsv($out, ['id', 'username', 'action', 'created_at']);
            foreach ($logs as $log) {
                fputcsv($out, [$log->id, $log->username, $log->action, optional($log->created_at)?->toIso8601String()]);
            }
            fclose($out);
        }, 'activity_logs.csv', ['Content-Type' => 'text/csv']);
    }

    private function activityQuery(Request $request)
    {
        $query = ActivityLog::query();

        if ($username = trim((string) $request->query('username', ''))) {
            $query->where('username', 'like', '%'.$username.'%');
        }
        if ($action = trim((string) $request->query('action', ''))) {
            $query->where('action', 'like', '%'.$action.'%');
        }
        if ($start = trim((string) $request->query('start_date', ''))) {
            $query->whereDate('created_at', '>=', $start);
        }
        if ($end = trim((string) $request->query('end_date', ''))) {
            $query->whereDate('created_at', '<=', $end);
        }

        return $query;
    }

    private function isAdmin(Request $request): bool
    {
        $user = $request->user();
        $user?->loadMissing('role');
        $role = $user?->role?->name;

        return in_array($role, ['SuperAdmin', 'Admin RH', 'RH'], true);
    }
}

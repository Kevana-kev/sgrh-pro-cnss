<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Role;
use App\Models\User;
use App\Services\ActivityLogger;
use App\Support\SpaSerializer;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class SpaAuthController extends Controller
{
    public function register(Request $request): JsonResponse
    {
        $data = $request->validate([
            'username' => ['required', 'string', 'max:80', 'unique:users,username'],
            'password' => ['required', 'string', 'min:6'],
            'role_name' => ['required', 'string'],
        ]);

        $role = Role::query()->where('name', $data['role_name'])->first();
        if (! $role) {
            return response()->json(['error' => 'Rôle introuvable'], 404);
        }

        $user = User::create([
            'username' => $data['username'],
            'password' => $data['password'],
            'role_id' => $role->id,
            'must_change_password' => false,
        ]);

        ActivityLogger::log($user->username, 'Inscription utilisateur');

        return response()->json([
            'id' => $user->id,
            'username' => $user->username,
        ], 201);
    }

    public function login(Request $request): JsonResponse
    {
        $data = $request->validate([
            'username' => ['required', 'string'],
            'password' => ['required', 'string'],
        ]);

        $identifier = strtolower(trim($data['username']));

        $user = User::query()
            ->with(['role.permissions', 'employee.role'])
            ->where(function ($q) use ($identifier) {
                $q->whereRaw('LOWER(username) = ?', [$identifier])
                    ->orWhereHas('employee', function ($eq) use ($identifier) {
                        $eq->whereRaw('LOWER(matricule) = ?', [$identifier])
                            ->orWhereRaw('LOWER(email) = ?', [$identifier]);
                    });
            })
            ->first();

        if (! $user || ! Hash::check($data['password'], $user->password)) {
            return response()->json(['error' => 'Identifiants invalides'], 401);
        }

        if ($user->employee && ! $this->isActiveStatus($user->employee->status)) {
            return response()->json(['error' => 'Compte agent non actif'], 401);
        }

        $token = $user->createToken('spa')->plainTextToken;
        ActivityLogger::log($user->username, 'Connexion');

        return response()->json($this->profilePayload($user, $token));
    }

    public function me(Request $request): JsonResponse
    {
        /** @var User $user */
        $user = $request->user();
        $user->loadMissing(['role.permissions', 'employee.role']);

        $holder = SpaSerializer::accountHolder($user);

        return response()->json([
            'username' => $user->username,
            'role' => $user->role?->name,
            'permissions' => $user->permissionNames(),
            'must_change_password' => (bool) $user->must_change_password,
            'account_holder_name' => $holder['account_holder_name'],
            'account_holder_function' => $holder['account_holder_function'],
            'employee_id' => $user->employee_id,
            'employee_name' => $user->employee
                ? trim($user->employee->first_name.' '.$user->employee->last_name)
                : null,
        ]);
    }

    public function changePassword(Request $request): JsonResponse
    {
        $data = $request->validate([
            'current_password' => ['required', 'string'],
            'new_password' => ['required', 'string', 'min:6'],
        ]);

        /** @var User $user */
        $user = $request->user();

        if (! Hash::check($data['current_password'], $user->password)) {
            return response()->json(['error' => 'Mot de passe actuel invalide'], 401);
        }

        if ($data['current_password'] === $data['new_password']) {
            return response()->json(['error' => 'Le nouveau mot de passe doit être différent'], 422);
        }

        $user->password = $data['new_password'];
        $user->must_change_password = false;
        $user->save();

        $user->tokens()->delete();
        $token = $user->createToken('spa')->plainTextToken;

        ActivityLogger::log($user->username, 'Changement mot de passe');

        return response()->json([
            'message' => 'Mot de passe mis à jour',
            'must_change_password' => false,
            'access_token' => $token,
        ]);
    }

    public function logout(Request $request): JsonResponse
    {
        /** @var User $user */
        $user = $request->user();
        $user->currentAccessToken()?->delete();

        ActivityLogger::log($user->username, 'Déconnexion');

        return response()->json(['message' => 'Déconnecté']);
    }

    private function profilePayload(User $user, string $token): array
    {
        $holder = SpaSerializer::accountHolder($user);

        return [
            'access_token' => $token,
            'username' => $user->username,
            'role' => $user->role?->name,
            'permissions' => $user->permissionNames(),
            'must_change_password' => (bool) $user->must_change_password,
            'account_holder_name' => $holder['account_holder_name'],
            'account_holder_function' => $holder['account_holder_function'],
            'employee_id' => $user->employee_id,
            'employee_name' => $user->employee
                ? trim($user->employee->first_name.' '.$user->employee->last_name)
                : null,
        ];
    }

    private function isActiveStatus(?string $status): bool
    {
        $normalized = strtolower(trim((string) $status));

        return in_array($normalized, ['actif', 'act', 'active'], true);
    }
}

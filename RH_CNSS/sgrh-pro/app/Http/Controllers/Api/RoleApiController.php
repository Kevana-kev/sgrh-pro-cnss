<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Permission;
use App\Models\Role;
use App\Services\ActivityLogger;
use App\Support\SpaSerializer;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class RoleApiController extends Controller
{
    public function index(): JsonResponse
    {
        $roles = Role::query()->with('permissions')->orderBy('name')->get();

        return response()->json($roles->map(fn (Role $r) => SpaSerializer::role($r))->values());
    }

    public function permissions(): JsonResponse
    {
        return response()->json(Permission::query()->orderBy('name')->pluck('name')->values());
    }

    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'name' => ['required', 'string', 'max:80', 'unique:roles,name'],
            'permission_names' => ['nullable', 'array'],
            'permission_names.*' => ['string'],
        ]);

        $role = Role::create(['name' => $data['name']]);

        if (! empty($data['permission_names'])) {
            $permissionIds = Permission::query()
                ->whereIn('name', $data['permission_names'])
                ->pluck('id');
            $role->permissions()->sync($permissionIds);
        }

        ActivityLogger::log($request->user()?->username, 'Création rôle #'.$role->id);

        return response()->json(SpaSerializer::role($role->fresh('permissions')), 201);
    }

    public function assignPermissions(Request $request, int $roleId): JsonResponse
    {
        $role = Role::findOrFail($roleId);

        $data = $request->validate([
            'permission_names' => ['required', 'array'],
            'permission_names.*' => ['string'],
        ]);

        $permissionIds = Permission::query()
            ->whereIn('name', $data['permission_names'])
            ->pluck('id');

        $role->permissions()->sync($permissionIds);

        ActivityLogger::log($request->user()?->username, 'Mise à jour permissions rôle #'.$role->id);

        return response()->json(SpaSerializer::role($role->fresh('permissions')));
    }
}

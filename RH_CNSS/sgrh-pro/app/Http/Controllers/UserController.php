<?php

namespace App\Http\Controllers;

use App\Models\Employee;
use App\Models\Role;
use App\Models\User;
use App\Services\ActivityLogger;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\Password;
use Illuminate\View\View;

class UserController extends Controller
{
    public function index(): View
    {
        $users = User::query()
            ->with(['role', 'employee'])
            ->orderBy('username')
            ->paginate(20);

        return view('users.index', compact('users'));
    }

    public function create(): View
    {
        return view('users.create', [
            'roles' => Role::query()->orderBy('name')->get(),
            'employees' => Employee::query()->orderBy('last_name')->orderBy('first_name')->get(),
        ]);
    }

    public function store(Request $request): RedirectResponse
    {
        $validated = $request->validate([
            'username' => ['required', 'string', 'max:80', 'unique:users,username'],
            'password' => ['required', 'confirmed', Password::defaults()],
            'role_id' => ['required', 'exists:roles,id'],
            'employee_id' => ['nullable', 'exists:employees,id'],
            'must_change_password' => ['sometimes', 'boolean'],
        ], [
            'username.required' => 'Le nom d\'utilisateur est obligatoire.',
            'username.unique' => 'Ce nom d\'utilisateur existe déjà.',
            'password.required' => 'Le mot de passe est obligatoire.',
            'role_id.required' => 'Le rôle est obligatoire.',
            'role_id.exists' => 'Le rôle sélectionné est invalide.',
        ]);

        $user = User::create([
            'username' => $validated['username'],
            'password' => $validated['password'],
            'role_id' => $validated['role_id'],
            'employee_id' => $validated['employee_id'] ?? null,
            'must_change_password' => $request->boolean('must_change_password', true),
        ]);

        ActivityLogger::log(
            Auth::user()?->username,
            'Création utilisateur #'.$user->id.' ('.$user->username.')'
        );

        return redirect()->route('users.index')
            ->with('success', 'Utilisateur créé avec succès.');
    }

    public function edit(User $user): View
    {
        return view('users.edit', [
            'user' => $user->load(['role', 'employee']),
            'roles' => Role::query()->orderBy('name')->get(),
            'employees' => Employee::query()->orderBy('last_name')->orderBy('first_name')->get(),
        ]);
    }

    public function update(Request $request, User $user): RedirectResponse
    {
        $validated = $request->validate([
            'username' => [
                'required',
                'string',
                'max:80',
                Rule::unique('users', 'username')->ignore($user->id),
            ],
            'password' => ['nullable', 'confirmed', Password::defaults()],
            'role_id' => ['required', 'exists:roles,id'],
            'employee_id' => ['nullable', 'exists:employees,id'],
            'must_change_password' => ['sometimes', 'boolean'],
        ], [
            'username.required' => 'Le nom d\'utilisateur est obligatoire.',
            'username.unique' => 'Ce nom d\'utilisateur existe déjà.',
            'role_id.required' => 'Le rôle est obligatoire.',
        ]);

        $user->username = $validated['username'];
        $user->role_id = $validated['role_id'];
        $user->employee_id = $validated['employee_id'] ?? null;
        $user->must_change_password = $request->boolean('must_change_password', $user->must_change_password);

        if (! empty($validated['password'])) {
            $user->password = $validated['password'];
            $user->must_change_password = true;
        }

        $user->save();

        ActivityLogger::log(
            Auth::user()?->username,
            'Modification utilisateur #'.$user->id.' ('.$user->username.')'
        );

        return redirect()->route('users.index')
            ->with('success', 'Utilisateur mis à jour avec succès.');
    }

    public function destroy(User $user): RedirectResponse
    {
        if (Auth::id() === $user->id) {
            return redirect()->back()
                ->with('error', 'Vous ne pouvez pas supprimer votre propre compte.');
        }

        $label = $user->username;
        $user->delete();

        ActivityLogger::log(
            Auth::user()?->username,
            'Suppression utilisateur '.$label
        );

        return redirect()->route('users.index')
            ->with('success', 'Utilisateur supprimé avec succès.');
    }
}

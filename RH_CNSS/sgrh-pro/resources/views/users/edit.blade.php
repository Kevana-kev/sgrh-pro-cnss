@extends('layouts.app')

@section('title', 'Modifier utilisateur')

@section('content')
<div class="page-header">
    <div>
        <h1>Modifier l'utilisateur</h1>
        <p class="page-header__meta">{{ $user->username }}</p>
    </div>
    <div class="page-actions">
        <a href="{{ route('users.index') }}" class="btn btn-secondary">Retour</a>
    </div>
</div>

<div class="panel">
    <div class="panel__body">
        <form method="POST" action="{{ route('users.update', $user) }}" autocomplete="off">
            @csrf
            @method('PUT')
            <div class="form-grid">
                <div class="form-group">
                    <label for="username">Nom d'utilisateur</label>
                    <input type="text" id="username" name="username" class="form-control @error('username') is-invalid @enderror" value="{{ old('username', $user->username) }}" required>
                    @error('username')<div class="form-error">{{ $message }}</div>@enderror
                </div>

                <div class="form-group">
                    <label for="role_id">Rôle</label>
                    <select id="role_id" name="role_id" class="form-control @error('role_id') is-invalid @enderror" required>
                        <option value="">— Sélectionner —</option>
                        @foreach($roles as $role)
                            <option value="{{ $role->id }}" @selected(old('role_id', $user->role_id) == $role->id)>{{ $role->name }}</option>
                        @endforeach
                    </select>
                    @error('role_id')<div class="form-error">{{ $message }}</div>@enderror
                </div>

                <div class="form-group">
                    <label for="password">Nouveau mot de passe</label>
                    <input type="password" id="password" name="password" class="form-control @error('password') is-invalid @enderror" autocomplete="new-password">
                    <span class="form-hint">Laisser vide pour ne pas modifier.</span>
                    @error('password')<div class="form-error">{{ $message }}</div>@enderror
                </div>

                <div class="form-group">
                    <label for="password_confirmation">Confirmation</label>
                    <input type="password" id="password_confirmation" name="password_confirmation" class="form-control" autocomplete="new-password">
                </div>

                <div class="form-group form-group--full">
                    <label for="employee_id">Employé lié (optionnel)</label>
                    <select id="employee_id" name="employee_id" class="form-control @error('employee_id') is-invalid @enderror">
                        <option value="">— Aucun —</option>
                        @foreach($employees as $employee)
                            <option value="{{ $employee->id }}" @selected(old('employee_id', $user->employee_id) == $employee->id)>{{ $employee->full_name }}</option>
                        @endforeach
                    </select>
                    @error('employee_id')<div class="form-error">{{ $message }}</div>@enderror
                </div>

                <div class="form-group form-group--full">
                    <div class="form-check">
                        <input type="hidden" name="must_change_password" value="0">
                        <input type="checkbox" id="must_change_password" name="must_change_password" value="1" @checked(old('must_change_password', $user->must_change_password))>
                        <label for="must_change_password">Forcer le changement de mot de passe</label>
                    </div>
                </div>
            </div>

            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Enregistrer</button>
                <a href="{{ route('users.index') }}" class="btn btn-secondary">Annuler</a>
            </div>
        </form>
    </div>
</div>
@endsection

@php
    $e = $employee ?? null;
@endphp
<div class="form-grid">
    <div class="form-group">
        <label for="first_name">Prénom</label>
        <input type="text" id="first_name" name="first_name" class="form-control @error('first_name') is-invalid @enderror" value="{{ old('first_name', $e?->first_name) }}" required>
        @error('first_name')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="last_name">Nom</label>
        <input type="text" id="last_name" name="last_name" class="form-control @error('last_name') is-invalid @enderror" value="{{ old('last_name', $e?->last_name) }}" required>
        @error('last_name')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="matricule">Matricule</label>
        <input type="text" id="matricule" name="matricule" class="form-control @error('matricule') is-invalid @enderror" value="{{ old('matricule', $e?->matricule) }}">
        @error('matricule')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="email">E-mail</label>
        <input type="email" id="email" name="email" class="form-control @error('email') is-invalid @enderror" value="{{ old('email', $e?->email) }}" required>
        @error('email')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="phone">Téléphone</label>
        <input type="text" id="phone" name="phone" class="form-control @error('phone') is-invalid @enderror" value="{{ old('phone', $e?->phone) }}" required>
        @error('phone')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="hire_date">Date d'embauche</label>
        <input type="date" id="hire_date" name="hire_date" class="form-control @error('hire_date') is-invalid @enderror" value="{{ old('hire_date', optional($e?->hire_date)->format('Y-m-d')) }}" required>
        @error('hire_date')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group form-group--full">
        <label for="address">Adresse</label>
        <input type="text" id="address" name="address" class="form-control @error('address') is-invalid @enderror" value="{{ old('address', $e?->address) }}" required>
        @error('address')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="department_id">Département</label>
        <select id="department_id" name="department_id" class="form-control @error('department_id') is-invalid @enderror">
            <option value="">— Aucun —</option>
            @foreach($departments as $department)
                <option value="{{ $department->id }}" @selected(old('department_id', $e?->department_id) == $department->id)>{{ $department->name }}</option>
            @endforeach
        </select>
        @error('department_id')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="role_id">Rôle</label>
        <select id="role_id" name="role_id" class="form-control @error('role_id') is-invalid @enderror" required>
            <option value="">— Sélectionner —</option>
            @foreach($roles as $role)
                <option value="{{ $role->id }}" @selected(old('role_id', $e?->role_id) == $role->id)>{{ $role->name }}</option>
            @endforeach
        </select>
        @error('role_id')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="status">Statut</label>
        <select id="status" name="status" class="form-control @error('status') is-invalid @enderror" required>
            @foreach(['Actif', 'Inactif'] as $st)
                <option value="{{ $st }}" @selected(old('status', $e?->status ?? 'Actif') === $st)>{{ $st }}</option>
            @endforeach
        </select>
        @error('status')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="photo">Photo</label>
        <input type="file" id="photo" name="photo" accept="image/*" class="form-control @error('photo') is-invalid @enderror">
        @error('photo')<div class="form-error">{{ $message }}</div>@enderror
        @if($e?->photo_path)
            <span class="form-hint">Photo actuelle conservée si aucun fichier n'est choisi.</span>
        @endif
    </div>
</div>

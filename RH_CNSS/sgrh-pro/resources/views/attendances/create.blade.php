@extends('layouts.app')

@section('title', 'Nouveau pointage')

@section('content')
<div class="page-header">
    <div>
        <h1>Nouveau pointage</h1>
        <p class="page-header__meta">Saisie manuelle</p>
    </div>
    <div class="page-actions">
        <a href="{{ route('attendances.index') }}" class="btn btn-secondary">Retour</a>
    </div>
</div>

<div class="panel">
    <div class="panel__body">
        <form method="POST" action="{{ route('attendances.store') }}">
            @csrf
            <div class="form-grid">
                <div class="form-group form-group--full">
                    <label for="employee_id">Employé</label>
                    <select id="employee_id" name="employee_id" class="form-control @error('employee_id') is-invalid @enderror" required>
                        <option value="">— Sélectionner —</option>
                        @foreach($employees as $employee)
                            <option value="{{ $employee->id }}" @selected(old('employee_id') == $employee->id)>{{ $employee->full_name }}</option>
                        @endforeach
                    </select>
                    @error('employee_id')<div class="form-error">{{ $message }}</div>@enderror
                </div>
                <div class="form-group">
                    <label for="check_in">Heure d'entrée</label>
                    <input type="datetime-local" id="check_in" name="check_in" class="form-control @error('check_in') is-invalid @enderror" value="{{ old('check_in') }}" required>
                    @error('check_in')<div class="form-error">{{ $message }}</div>@enderror
                </div>
                <div class="form-group">
                    <label for="check_out">Heure de sortie</label>
                    <input type="datetime-local" id="check_out" name="check_out" class="form-control @error('check_out') is-invalid @enderror" value="{{ old('check_out') }}">
                    @error('check_out')<div class="form-error">{{ $message }}</div>@enderror
                </div>
                <div class="form-group">
                    <label for="source">Source</label>
                    <select id="source" name="source" class="form-control @error('source') is-invalid @enderror">
                        <option value="manual" @selected(old('source', 'manual') === 'manual')>Manuel</option>
                        <option value="biometric" @selected(old('source') === 'biometric')>Biométrie</option>
                        <option value="rfid" @selected(old('source') === 'rfid')>RFID</option>
                    </select>
                    @error('source')<div class="form-error">{{ $message }}</div>@enderror
                </div>
                <div class="form-group">
                    <div class="form-check" style="margin-top: 1.75rem;">
                        <input type="checkbox" id="is_absent" name="is_absent" value="1" @checked(old('is_absent'))>
                        <label for="is_absent">Marquer comme absent</label>
                    </div>
                </div>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Enregistrer</button>
                <a href="{{ route('attendances.index') }}" class="btn btn-secondary">Annuler</a>
            </div>
        </form>
    </div>
</div>
@endsection

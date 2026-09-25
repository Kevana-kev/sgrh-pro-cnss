@extends('layouts.app')

@section('title', 'Nouvelle demande de congé')

@section('content')
<div class="page-header">
    <div>
        <h1>Nouvelle demande de congé</h1>
    </div>
    <div class="page-actions">
        <a href="{{ route('leaves.index') }}" class="btn btn-secondary">Retour</a>
    </div>
</div>

<div class="panel">
    <div class="panel__body">
        <form method="POST" action="{{ route('leaves.store') }}">
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
                    <label for="start_date">Date de début</label>
                    <input type="date" id="start_date" name="start_date" class="form-control @error('start_date') is-invalid @enderror" value="{{ old('start_date') }}" required>
                    @error('start_date')<div class="form-error">{{ $message }}</div>@enderror
                </div>
                <div class="form-group">
                    <label for="end_date">Date de fin</label>
                    <input type="date" id="end_date" name="end_date" class="form-control @error('end_date') is-invalid @enderror" value="{{ old('end_date') }}" required>
                    @error('end_date')<div class="form-error">{{ $message }}</div>@enderror
                </div>
                <div class="form-group form-group--full">
                    <label for="reason">Motif</label>
                    <textarea id="reason" name="reason" class="form-control @error('reason') is-invalid @enderror" required>{{ old('reason') }}</textarea>
                    @error('reason')<div class="form-error">{{ $message }}</div>@enderror
                </div>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Soumettre</button>
                <a href="{{ route('leaves.index') }}" class="btn btn-secondary">Annuler</a>
            </div>
        </form>
    </div>
</div>
@endsection

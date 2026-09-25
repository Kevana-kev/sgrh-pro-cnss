@extends('layouts.app')

@section('title', 'Nouveau département')

@section('content')
<div class="page-header">
    <div>
        <h1>Nouveau département</h1>
    </div>
    <div class="page-actions">
        <a href="{{ route('departments.index') }}" class="btn btn-secondary">Retour</a>
    </div>
</div>

<div class="panel">
    <div class="panel__body">
        <form method="POST" action="{{ route('departments.store') }}">
            @csrf
            <div class="form-grid">
                <div class="form-group">
                    <label for="name">Nom</label>
                    <input type="text" id="name" name="name" class="form-control @error('name') is-invalid @enderror" value="{{ old('name') }}" required>
                    @error('name')<div class="form-error">{{ $message }}</div>@enderror
                </div>
                <div class="form-group">
                    <label for="budget">Budget</label>
                    <input type="number" step="0.01" min="0" id="budget" name="budget" class="form-control @error('budget') is-invalid @enderror" value="{{ old('budget', 0) }}">
                    @error('budget')<div class="form-error">{{ $message }}</div>@enderror
                </div>
                <div class="form-group form-group--full">
                    <label for="manager_id">Responsable</label>
                    <select id="manager_id" name="manager_id" class="form-control @error('manager_id') is-invalid @enderror">
                        <option value="">— Aucun —</option>
                        @foreach($employees as $employee)
                            <option value="{{ $employee->id }}" @selected(old('manager_id') == $employee->id)>{{ $employee->full_name }}</option>
                        @endforeach
                    </select>
                    @error('manager_id')<div class="form-error">{{ $message }}</div>@enderror
                </div>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Créer</button>
                <a href="{{ route('departments.index') }}" class="btn btn-secondary">Annuler</a>
            </div>
        </form>
    </div>
</div>
@endsection

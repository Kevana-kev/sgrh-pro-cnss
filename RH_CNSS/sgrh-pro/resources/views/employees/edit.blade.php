@extends('layouts.app')

@section('title', 'Modifier employé')

@section('content')
<div class="page-header">
    <div>
        <h1>Modifier l'employé</h1>
        <p class="page-header__meta">{{ $employee->full_name }}</p>
    </div>
    <div class="page-actions">
        <a href="{{ route('employees.show', $employee) }}" class="btn btn-secondary">Voir la fiche</a>
        <a href="{{ route('employees.index') }}" class="btn btn-secondary">Retour</a>
    </div>
</div>

<div class="panel">
    <div class="panel__body">
        <form method="POST" action="{{ route('employees.update', $employee) }}" enctype="multipart/form-data">
            @csrf
            @method('PUT')
            @include('employees._form', ['employee' => $employee])
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Enregistrer</button>
                <a href="{{ route('employees.index') }}" class="btn btn-secondary">Annuler</a>
            </div>
        </form>
    </div>
</div>
@endsection

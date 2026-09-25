@extends('layouts.app')

@section('title', 'Nouvel employé')

@section('content')
<div class="page-header">
    <div>
        <h1>Nouvel employé</h1>
        <p class="page-header__meta">Fiche personnelle</p>
    </div>
    <div class="page-actions">
        <a href="{{ route('employees.index') }}" class="btn btn-secondary">Retour</a>
    </div>
</div>

<div class="panel">
    <div class="panel__body">
        <form method="POST" action="{{ route('employees.store') }}" enctype="multipart/form-data">
            @csrf
            @include('employees._form')
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Créer</button>
                <a href="{{ route('employees.index') }}" class="btn btn-secondary">Annuler</a>
            </div>
        </form>
    </div>
</div>
@endsection

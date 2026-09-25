@extends('layouts.app')

@section('title', 'Nouvelle évaluation')

@section('content')
<div class="page-header">
    <div>
        <h1>Nouvelle évaluation</h1>
    </div>
    <div class="page-actions">
        <a href="{{ route('evaluations.index') }}" class="btn btn-secondary">Retour</a>
    </div>
</div>

<div class="panel">
    <div class="panel__body">
        <form method="POST" action="{{ route('evaluations.store') }}">
            @csrf
            @include('evaluations._form')
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Créer</button>
                <a href="{{ route('evaluations.index') }}" class="btn btn-secondary">Annuler</a>
            </div>
        </form>
    </div>
</div>
@endsection

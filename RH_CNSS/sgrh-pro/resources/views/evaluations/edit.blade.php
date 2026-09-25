@extends('layouts.app')

@section('title', 'Modifier évaluation')

@section('content')
<div class="page-header">
    <div>
        <h1>Modifier l'évaluation</h1>
        <p class="page-header__meta">{{ $evaluation->employee?->full_name }} — {{ $evaluation->period }}</p>
    </div>
    <div class="page-actions">
        <a href="{{ route('evaluations.index') }}" class="btn btn-secondary">Retour</a>
    </div>
</div>

<div class="panel">
    <div class="panel__body">
        <form method="POST" action="{{ route('evaluations.update', $evaluation) }}">
            @csrf
            @method('PUT')
            @include('evaluations._form', ['evaluation' => $evaluation])
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Enregistrer</button>
                <a href="{{ route('evaluations.index') }}" class="btn btn-secondary">Annuler</a>
            </div>
        </form>
    </div>
</div>
@endsection

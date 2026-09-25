@extends('layouts.app')

@section('title', 'Modifier rémunération')

@section('content')
<div class="page-header">
    <div>
        <h1>Modifier l'élément de rémunération</h1>
        <p class="page-header__meta">Période {{ $remuneration->period }}</p>
    </div>
    <div class="page-actions">
        <a href="{{ route('remunerations.index') }}" class="btn btn-secondary">Retour</a>
    </div>
</div>

<div class="disclaimer">{{ $disclaimer }}</div>

<div class="panel">
    <div class="panel__body">
        <form method="POST" action="{{ route('remunerations.update', $remuneration) }}">
            @csrf
            @method('PUT')
            @include('remunerations._form', ['remuneration' => $remuneration])
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Enregistrer</button>
                <a href="{{ route('remunerations.index') }}" class="btn btn-secondary">Annuler</a>
            </div>
        </form>
    </div>
</div>
@endsection

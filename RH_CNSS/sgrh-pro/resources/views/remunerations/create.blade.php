@extends('layouts.app')

@section('title', 'Nouvelle rémunération')

@section('content')
<div class="page-header">
    <div>
        <h1>Nouvel élément de rémunération</h1>
    </div>
    <div class="page-actions">
        <a href="{{ route('remunerations.index') }}" class="btn btn-secondary">Retour</a>
    </div>
</div>

<div class="disclaimer">{{ $disclaimer }}</div>

<div class="panel">
    <div class="panel__body">
        <form method="POST" action="{{ route('remunerations.store') }}">
            @csrf
            @include('remunerations._form')
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Créer</button>
                <a href="{{ route('remunerations.index') }}" class="btn btn-secondary">Annuler</a>
            </div>
        </form>
    </div>
</div>
@endsection

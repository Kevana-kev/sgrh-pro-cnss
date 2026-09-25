@extends('layouts.app')

@section('title', 'Paramètres')

@section('content')
<div class="page-header">
    <div>
        <h1>Paramètres</h1>
        <p class="page-header__meta">Configuration système SGRH Pro</p>
    </div>
</div>

<div class="panel" style="max-width: 640px;">
    <div class="panel__header">
        <h2 class="panel__title">Horaires & organisation</h2>
    </div>
    <div class="panel__body">
        <form method="POST" action="{{ route('settings.update') }}">
            @csrf
            <div class="form-group mb-1">
                <label for="organization_name">Nom de l'organisation</label>
                <input type="text" id="organization_name" name="organization_name" class="form-control @error('organization_name') is-invalid @enderror" value="{{ old('organization_name', $organization_name) }}">
                @error('organization_name')<div class="form-error">{{ $message }}</div>@enderror
            </div>
            <div class="form-group mb-1">
                <label for="work_start_time">Heure de début de travail</label>
                <input type="time" id="work_start_time" name="work_start_time" class="form-control @error('work_start_time') is-invalid @enderror" value="{{ old('work_start_time', $work_start_time) }}" required>
                @error('work_start_time')<div class="form-error">{{ $message }}</div>@enderror
            </div>
            <div class="form-group mb-1">
                <label for="late_threshold_minutes">Seuil de retard (minutes)</label>
                <input type="number" min="0" max="240" id="late_threshold_minutes" name="late_threshold_minutes" class="form-control @error('late_threshold_minutes') is-invalid @enderror" value="{{ old('late_threshold_minutes', $late_threshold_minutes) }}" required>
                <span class="form-hint">Au-delà de ce seuil, le retard est comptabilisé.</span>
                @error('late_threshold_minutes')<div class="form-error">{{ $message }}</div>@enderror
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Enregistrer</button>
            </div>
        </form>
    </div>
</div>
@endsection

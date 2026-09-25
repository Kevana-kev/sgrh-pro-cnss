@extends('layouts.app')

@section('title', 'Détail évaluation')

@section('content')
<div class="page-header">
  <div>
    <h1>Évaluation #{{ $evaluation->id }}</h1>
    <p class="muted">{{ $evaluation->employee?->full_name }} — {{ $evaluation->period }}</p>
  </div>
  <a href="{{ route('evaluations.edit', $evaluation) }}" class="btn btn-primary">Modifier</a>
</div>
<div class="card">
  <dl class="detail-grid">
    <div><dt>Score</dt><dd>{{ $evaluation->score }}/100</dd></div>
    <div><dt>Évaluateur</dt><dd>{{ $evaluation->evaluator?->full_name ?: '—' }}</dd></div>
    <div><dt>Statut</dt><dd>{{ $evaluation->status }}</dd></div>
    <div><dt>Points forts</dt><dd>{{ $evaluation->strengths ?: '—' }}</dd></div>
    <div><dt>Axes d'amélioration</dt><dd>{{ $evaluation->improvements ?: '—' }}</dd></div>
    <div><dt>Commentaires</dt><dd>{{ $evaluation->comments ?: '—' }}</dd></div>
  </dl>
</div>
@endsection

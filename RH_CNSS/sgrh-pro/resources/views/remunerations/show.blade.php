@extends('layouts.app')

@section('title', 'Détail rémunération')

@section('content')
<div class="page-header">
  <div>
    <h1>Élément de rémunération #{{ $remuneration->id }}</h1>
    <p class="muted">{{ $disclaimer }}</p>
  </div>
  <a href="{{ route('remunerations.edit', $remuneration) }}" class="btn btn-primary">Modifier</a>
</div>
<div class="card">
  <dl class="detail-grid">
    <div><dt>Employé</dt><dd>{{ $remuneration->employee?->full_name }}</dd></div>
    <div><dt>Période</dt><dd>{{ $remuneration->period }}</dd></div>
    <div><dt>Salaire de base</dt><dd>{{ number_format($remuneration->base_salary, 2, ',', ' ') }} CDF</dd></div>
    <div><dt>Primes</dt><dd>{{ number_format($remuneration->bonus, 2, ',', ' ') }} CDF</dd></div>
    <div><dt>Heures supp.</dt><dd>{{ $remuneration->overtime_hours }}</dd></div>
    <div><dt>Montant HS</dt><dd>{{ number_format($remuneration->overtime_amount, 2, ',', ' ') }} CDF</dd></div>
    <div><dt>Retenues</dt><dd>{{ number_format($remuneration->deductions, 2, ',', ' ') }} CDF</dd></div>
    <div><dt>Total indicatif</dt><dd><strong>{{ number_format($remuneration->total_indicative, 2, ',', ' ') }} CDF</strong></dd></div>
    <div><dt>Statut</dt><dd>{{ $remuneration->status }}</dd></div>
    <div><dt>Notes</dt><dd>{{ $remuneration->notes ?: '—' }}</dd></div>
  </dl>
</div>
@endsection

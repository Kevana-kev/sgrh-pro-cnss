@extends('layouts.app')

@section('title', 'Évaluations')

@section('content')
<div class="page-header">
    <div>
        <h1>Évaluations</h1>
        <p class="page-header__meta">Performance et suivi</p>
    </div>
    <div class="page-actions">
        <a href="{{ route('evaluations.create') }}" class="btn btn-primary">Nouvelle évaluation</a>
    </div>
</div>

<form method="GET" action="{{ route('evaluations.index') }}" class="filters">
    <div class="form-group">
        <label for="employee_id">Employé</label>
        <select id="employee_id" name="employee_id" class="form-control">
            <option value="">Tous</option>
            @foreach($employees as $employee)
                <option value="{{ $employee->id }}" @selected(request('employee_id') == $employee->id)>{{ $employee->full_name }}</option>
            @endforeach
        </select>
    </div>
    <div class="form-group">
        <label for="period">Période</label>
        <input type="text" id="period" name="period" class="form-control" value="{{ request('period') }}" placeholder="ex. 2026-T1">
    </div>
    <div class="form-group">
        <label for="status">Statut</label>
        <select id="status" name="status" class="form-control">
            <option value="">Tous</option>
            @foreach(['Brouillon', 'Finalisé'] as $st)
                <option value="{{ $st }}" @selected(request('status') === $st)>{{ $st }}</option>
            @endforeach
        </select>
    </div>
    <div class="form-group form-group--actions">
        <button type="submit" class="btn btn-secondary">Filtrer</button>
    </div>
</form>

<div class="panel">
    <div class="panel__body panel__body--flush">
        @if($evaluations->isEmpty())
            <div class="empty-state">
                <div class="empty-state__title">Aucune évaluation</div>
                <p class="empty-state__text">Créez la première évaluation de performance.</p>
                <a href="{{ route('evaluations.create') }}" class="btn btn-primary">Créer</a>
            </div>
        @else
            <div class="table-wrap">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Employé</th>
                            <th>Évaluateur</th>
                            <th>Période</th>
                            <th>Note</th>
                            <th>Statut</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach($evaluations as $evaluation)
                            <tr>
                                <td><strong>{{ $evaluation->employee?->full_name ?? '—' }}</strong></td>
                                <td>{{ $evaluation->evaluator?->full_name ?? '—' }}</td>
                                <td>{{ $evaluation->period }}</td>
                                <td class="num"><strong>{{ $evaluation->score }}/100</strong></td>
                                <td>
                                    @if($evaluation->status === 'Finalisé')
                                        <span class="badge badge-success">{{ $evaluation->status }}</span>
                                    @else
                                        <span class="badge badge-warning">{{ $evaluation->status }}</span>
                                    @endif
                                </td>
                                <td>
                                    <div class="action-row">
                                        <a href="{{ route('evaluations.edit', $evaluation) }}" class="btn btn-secondary btn-sm">Modifier</a>
                                        <form action="{{ route('evaluations.destroy', $evaluation) }}" method="POST" class="inline-form" onsubmit="return confirm('Supprimer cette évaluation ?');">
                                            @csrf
                                            @method('DELETE')
                                            <button type="submit" class="btn btn-danger btn-sm">Supprimer</button>
                                        </form>
                                    </div>
                                </td>
                            </tr>
                        @endforeach
                    </tbody>
                </table>
            </div>
            <div class="pagination-wrap">{{ $evaluations->links() }}</div>
        @endif
    </div>
</div>
@endsection

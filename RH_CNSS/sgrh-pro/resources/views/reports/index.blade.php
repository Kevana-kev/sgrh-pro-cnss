@extends('layouts.app')

@section('title', 'Rapports')

@section('content')
<div class="page-header">
    <div>
        <h1>Rapports RH</h1>
        <p class="page-header__meta">Synthèse filtrable pour la direction</p>
    </div>
    <div class="page-actions">
        <a href="{{ route('reports.export', $filters) }}" class="btn btn-accent">Export CSV</a>
    </div>
</div>

<form method="GET" action="{{ route('reports.index') }}" class="filters">
    <div class="form-group">
        <label for="date_from">Du</label>
        <input type="date" id="date_from" name="date_from" class="form-control" value="{{ $filters['date_from'] }}" required>
    </div>
    <div class="form-group">
        <label for="date_to">Au</label>
        <input type="date" id="date_to" name="date_to" class="form-control" value="{{ $filters['date_to'] }}" required>
    </div>
    <div class="form-group">
        <label for="department_id">Département</label>
        <select id="department_id" name="department_id" class="form-control">
            <option value="">Tous</option>
            @foreach($departments as $department)
                <option value="{{ $department->id }}" @selected($filters['department_id'] == $department->id)>{{ $department->name }}</option>
            @endforeach
        </select>
    </div>
    <div class="form-group">
        <label for="employee_id">Employé</label>
        <select id="employee_id" name="employee_id" class="form-control">
            <option value="">Tous</option>
            @foreach($employees as $employee)
                <option value="{{ $employee->id }}" @selected($filters['employee_id'] == $employee->id)>{{ $employee->full_name }}</option>
            @endforeach
        </select>
    </div>
    <div class="form-group form-group--actions">
        <button type="submit" class="btn btn-secondary">Actualiser</button>
    </div>
</form>

<div class="kpi-grid">
    <div class="kpi kpi--blue">
        <div class="kpi__label">Effectif actif</div>
        <div class="kpi__value">{{ $summary['employees_active'] }}</div>
    </div>
    <div class="kpi kpi--teal">
        <div class="kpi__label">Pointages</div>
        <div class="kpi__value">{{ $summary['attendances_count'] }}</div>
    </div>
    <div class="kpi kpi--ok">
        <div class="kpi__label">Heures travaillées</div>
        <div class="kpi__value" style="font-size: 1.45rem;">{{ number_format((float) $summary['worked_hours_total'], 1, ',', ' ') }}</div>
    </div>
    <div class="kpi kpi--warn">
        <div class="kpi__label">Minutes de retard</div>
        <div class="kpi__value">{{ $summary['late_minutes_total'] }}</div>
    </div>
</div>

<div class="grid-2">
    <div class="panel">
        <div class="panel__header">
            <h2 class="panel__title">Indicateurs congés & rémunération</h2>
        </div>
        <div class="panel__body">
            <dl class="detail-list">
                <dt>Congés (période)</dt>
                <dd>{{ $summary['leaves_count'] }}</dd>
                <dt>Congés en attente</dt>
                <dd>{{ $summary['leaves_pending'] }}</dd>
                <dt>Rémunération indicative</dt>
                <dd>{{ number_format((float) $summary['remuneration_total'], 2, ',', ' ') }}</dd>
            </dl>
        </div>
    </div>

    <div class="panel">
        <div class="panel__header">
            <h2 class="panel__title">Effectif par département</h2>
        </div>
        <div class="panel__body panel__body--flush">
            @if(empty($summary['by_department']))
                <div class="empty-state">
                    <div class="empty-state__title">Aucune donnée</div>
                </div>
            @else
                <div class="table-wrap">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Département</th>
                                <th class="num">Effectif</th>
                            </tr>
                        </thead>
                        <tbody>
                            @foreach($summary['by_department'] as $row)
                                <tr>
                                    <td>{{ $row['name'] }}</td>
                                    <td class="num">{{ $row['count'] }}</td>
                                </tr>
                            @endforeach
                        </tbody>
                    </table>
                </div>
            @endif
        </div>
    </div>
</div>
@endsection

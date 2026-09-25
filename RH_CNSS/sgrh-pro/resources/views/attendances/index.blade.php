@extends('layouts.app')

@section('title', 'Présences')

@section('content')
<div class="page-header">
    <div>
        <h1>Présences</h1>
        <p class="page-header__meta">Pointages et horaires</p>
    </div>
    <div class="page-actions">
        <a href="{{ route('attendances.create') }}" class="btn btn-primary">Nouveau pointage</a>
    </div>
</div>

<form method="GET" action="{{ route('attendances.index') }}" class="filters">
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
        <label for="date_from">Du</label>
        <input type="date" id="date_from" name="date_from" class="form-control" value="{{ request('date_from') }}">
    </div>
    <div class="form-group">
        <label for="date_to">Au</label>
        <input type="date" id="date_to" name="date_to" class="form-control" value="{{ request('date_to') }}">
    </div>
    <div class="form-group">
        <label for="source">Source</label>
        <select id="source" name="source" class="form-control">
            <option value="">Toutes</option>
            <option value="manual" @selected(request('source') === 'manual')>Manuel</option>
            <option value="biometric" @selected(request('source') === 'biometric')>Biométrie</option>
            <option value="rfid" @selected(request('source') === 'rfid')>RFID</option>
        </select>
    </div>
    <div class="form-group form-group--actions">
        <button type="submit" class="btn btn-secondary">Filtrer</button>
    </div>
</form>

<div class="panel">
    <div class="panel__body panel__body--flush">
        @if($attendances->isEmpty())
            <div class="empty-state">
                <div class="empty-state__title">Aucun pointage</div>
                <p class="empty-state__text">Aucun enregistrement pour ces filtres.</p>
                <a href="{{ route('attendances.create') }}" class="btn btn-primary">Enregistrer un pointage</a>
            </div>
        @else
            <div class="table-wrap">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Employé</th>
                            <th>Entrée</th>
                            <th>Sortie</th>
                            <th>Heures</th>
                            <th>Retard</th>
                            <th>Source</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach($attendances as $attendance)
                            <tr>
                                <td><strong>{{ $attendance->employee?->full_name ?? '—' }}</strong></td>
                                <td>{{ $attendance->check_in?->format('d/m/Y H:i') }}</td>
                                <td>
                                    @if($attendance->check_out)
                                        {{ $attendance->check_out->format('d/m/Y H:i') }}
                                    @elseif($attendance->is_absent)
                                        <span class="badge badge-danger">Absent</span>
                                    @else
                                        <span class="badge badge-warning">En cours</span>
                                    @endif
                                </td>
                                <td class="num">{{ number_format((float) $attendance->worked_hours, 2, ',', ' ') }} h</td>
                                <td class="num">
                                    @if($attendance->late_minutes > 0)
                                        <span class="badge badge-warning">{{ $attendance->late_minutes }} min</span>
                                    @else
                                        —
                                    @endif
                                </td>
                                <td><span class="badge badge-info">{{ $attendance->source }}</span></td>
                                <td>
                                    @if(! $attendance->check_out && ! $attendance->is_absent)
                                        <form action="{{ route('attendances.checkout', $attendance) }}" method="POST" class="inline-form">
                                            @csrf
                                            <button type="submit" class="btn btn-accent btn-sm">Clôturer sortie</button>
                                        </form>
                                    @else
                                        <span class="muted">—</span>
                                    @endif
                                </td>
                            </tr>
                        @endforeach
                    </tbody>
                </table>
            </div>
            <div class="pagination-wrap">{{ $attendances->links() }}</div>
        @endif
    </div>
</div>
@endsection

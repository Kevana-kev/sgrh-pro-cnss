@extends('layouts.app')

@section('title', 'Congés')

@section('content')
<div class="page-header">
    <div>
        <h1>Congés</h1>
        <p class="page-header__meta">Demandes et décisions</p>
    </div>
    <div class="page-actions">
        <a href="{{ route('leaves.create') }}" class="btn btn-primary">Nouvelle demande</a>
    </div>
</div>

<form method="GET" action="{{ route('leaves.index') }}" class="filters">
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
        <label for="status">Statut</label>
        <select id="status" name="status" class="form-control">
            <option value="">Tous</option>
            @foreach(['En attente', 'Approuvé', 'Rejeté'] as $st)
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
        @if($leaves->isEmpty())
            <div class="empty-state">
                <div class="empty-state__title">Aucune demande</div>
                <p class="empty-state__text">Les demandes de congé apparaîtront ici.</p>
                <a href="{{ route('leaves.create') }}" class="btn btn-primary">Créer une demande</a>
            </div>
        @else
            <div class="table-wrap">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Employé</th>
                            <th>Début</th>
                            <th>Fin</th>
                            <th>Motif</th>
                            <th>Statut</th>
                            <th>Décision</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach($leaves as $leave)
                            <tr>
                                <td><strong>{{ $leave->employee?->full_name ?? '—' }}</strong></td>
                                <td>{{ $leave->start_date?->format('d/m/Y') }}</td>
                                <td>{{ $leave->end_date?->format('d/m/Y') }}</td>
                                <td>{{ $leave->reason }}</td>
                                <td>
                                    @if($leave->status === 'Approuvé')
                                        <span class="badge badge-success">{{ $leave->status }}</span>
                                    @elseif($leave->status === 'Rejeté')
                                        <span class="badge badge-danger">{{ $leave->status }}</span>
                                    @else
                                        <span class="badge badge-warning">{{ $leave->status }}</span>
                                    @endif
                                </td>
                                <td>
                                    @if($leave->status === 'En attente' && Auth::user()?->hasPermission('decide_leaves'))
                                        <form method="POST" action="{{ route('leaves.decide', $leave) }}" class="action-row">
                                            @csrf
                                            <input type="text" name="decision_comment" class="form-control" placeholder="Commentaire (optionnel)" style="min-width: 140px; max-width: 200px;">
                                            <button type="submit" name="decision" value="approve" class="btn btn-accent btn-sm">Approuver</button>
                                            <button type="submit" name="decision" value="reject" class="btn btn-danger btn-sm">Rejeter</button>
                                        </form>
                                    @elseif($leave->decision_comment)
                                        <span class="muted">{{ $leave->decision_comment }}</span>
                                    @else
                                        <span class="muted">—</span>
                                    @endif
                                </td>
                            </tr>
                        @endforeach
                    </tbody>
                </table>
            </div>
            <div class="pagination-wrap">{{ $leaves->links() }}</div>
        @endif
    </div>
</div>
@endsection

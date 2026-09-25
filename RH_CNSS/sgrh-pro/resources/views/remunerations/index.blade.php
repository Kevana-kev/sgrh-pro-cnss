@extends('layouts.app')

@section('title', 'Éléments de rémunération')

@section('content')
<div class="page-header">
    <div>
        <h1>Éléments de rémunération</h1>
        <p class="page-header__meta">États indicatifs pour la finance</p>
    </div>
    <div class="page-actions">
        <a href="{{ route('remunerations.export.csv', request()->only(['period', 'status'])) }}" class="btn btn-secondary">Export CSV</a>
        <a href="{{ route('remunerations.create') }}" class="btn btn-primary">Nouvel élément</a>
    </div>
</div>

<div class="disclaimer">{{ $disclaimer }}</div>

<form method="GET" action="{{ route('remunerations.index') }}" class="filters">
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
        <input type="text" id="period" name="period" class="form-control" value="{{ request('period') }}" placeholder="ex. 2026-08">
    </div>
    <div class="form-group">
        <label for="status">Statut</label>
        <select id="status" name="status" class="form-control">
            <option value="">Tous</option>
            @foreach(['Brouillon', 'Validé', 'Exporté'] as $st)
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
        @if($remunerations->isEmpty())
            <div class="empty-state">
                <div class="empty-state__title">Aucun élément</div>
                <p class="empty-state__text">Créez un élément de rémunération indicatif.</p>
                <a href="{{ route('remunerations.create') }}" class="btn btn-primary">Créer</a>
            </div>
        @else
            <div class="table-wrap">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Employé</th>
                            <th>Période</th>
                            <th>Base</th>
                            <th>Prime</th>
                            <th>HS</th>
                            <th>Retenues</th>
                            <th>Total</th>
                            <th>Statut</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach($remunerations as $row)
                            <tr>
                                <td><strong>{{ $row->employee?->full_name ?? '—' }}</strong></td>
                                <td>{{ $row->period }}</td>
                                <td class="num">{{ number_format((float) $row->base_salary, 2, ',', ' ') }}</td>
                                <td class="num">{{ number_format((float) $row->bonus, 2, ',', ' ') }}</td>
                                <td class="num">{{ number_format((float) $row->overtime_amount, 2, ',', ' ') }}</td>
                                <td class="num">{{ number_format((float) $row->deductions, 2, ',', ' ') }}</td>
                                <td class="num"><strong>{{ number_format((float) $row->total_indicative, 2, ',', ' ') }}</strong></td>
                                <td>
                                    @if($row->status === 'Validé')
                                        <span class="badge badge-success">{{ $row->status }}</span>
                                    @elseif($row->status === 'Brouillon')
                                        <span class="badge badge-warning">{{ $row->status }}</span>
                                    @else
                                        <span class="badge badge-info">{{ $row->status }}</span>
                                    @endif
                                </td>
                                <td>
                                    <div class="action-row">
                                        <a href="{{ route('remunerations.edit', $row) }}" class="btn btn-secondary btn-sm">Modifier</a>
                                        <form action="{{ route('remunerations.destroy', $row) }}" method="POST" class="inline-form" onsubmit="return confirm('Supprimer cet élément ?');">
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
            <div class="pagination-wrap">{{ $remunerations->links() }}</div>
        @endif
    </div>
</div>
@endsection

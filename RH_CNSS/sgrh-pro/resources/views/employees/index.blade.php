@extends('layouts.app')

@section('title', 'Employés')

@section('content')
<div class="page-header">
    <div>
        <h1>Employés</h1>
        <p class="page-header__meta">Annuaire du personnel</p>
    </div>
    <div class="page-actions">
        <a href="{{ route('employees.create') }}" class="btn btn-primary">Nouvel employé</a>
    </div>
</div>

<form method="GET" action="{{ route('employees.index') }}" class="filters">
    <div class="form-group">
        <label for="q">Recherche</label>
        <input type="search" id="q" name="q" class="form-control" value="{{ request('q') }}" placeholder="Nom, matricule, e-mail…">
    </div>
    <div class="form-group">
        <label for="department_id">Département</label>
        <select id="department_id" name="department_id" class="form-control">
            <option value="">Tous</option>
            @foreach($departments as $department)
                <option value="{{ $department->id }}" @selected(request('department_id') == $department->id)>{{ $department->name }}</option>
            @endforeach
        </select>
    </div>
    <div class="form-group">
        <label for="status">Statut</label>
        <select id="status" name="status" class="form-control">
            <option value="">Tous</option>
            <option value="Actif" @selected(request('status') === 'Actif')>Actif</option>
            <option value="Inactif" @selected(request('status') === 'Inactif')>Inactif</option>
        </select>
    </div>
    <div class="form-group form-group--actions">
        <button type="submit" class="btn btn-secondary">Filtrer</button>
    </div>
</form>

<div class="panel">
    <div class="panel__body panel__body--flush">
        @if($employees->isEmpty())
            <div class="empty-state">
                <div class="empty-state__title">Aucun employé</div>
                <p class="empty-state__text">Aucun résultat pour ces critères.</p>
                <a href="{{ route('employees.create') }}" class="btn btn-primary">Ajouter un employé</a>
            </div>
        @else
            <div class="table-wrap">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Nom</th>
                            <th>Matricule</th>
                            <th>Département</th>
                            <th>Rôle</th>
                            <th>Statut</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach($employees as $employee)
                            <tr>
                                <td>
                                    <a href="{{ route('employees.show', $employee) }}"><strong>{{ $employee->full_name }}</strong></a>
                                </td>
                                <td>{{ $employee->matricule ?? '—' }}</td>
                                <td>{{ $employee->department?->name ?? '—' }}</td>
                                <td>{{ $employee->role?->name ?? '—' }}</td>
                                <td>
                                    @if($employee->status === 'Actif')
                                        <span class="badge badge-success">{{ $employee->status }}</span>
                                    @else
                                        <span class="badge badge-neutral">{{ $employee->status }}</span>
                                    @endif
                                </td>
                                <td>
                                    <div class="action-row">
                                        <a href="{{ route('employees.show', $employee) }}" class="btn btn-ghost btn-sm">Voir</a>
                                        <a href="{{ route('employees.edit', $employee) }}" class="btn btn-secondary btn-sm">Modifier</a>
                                        <form action="{{ route('employees.destroy', $employee) }}" method="POST" class="inline-form" onsubmit="return confirm('Supprimer cet employé ?');">
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
            <div class="pagination-wrap">{{ $employees->links() }}</div>
        @endif
    </div>
</div>
@endsection

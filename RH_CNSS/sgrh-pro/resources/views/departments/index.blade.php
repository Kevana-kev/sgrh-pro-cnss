@extends('layouts.app')

@section('title', 'Départements')

@section('content')
<div class="page-header">
    <div>
        <h1>Départements</h1>
        <p class="page-header__meta">Organisation structurelle</p>
    </div>
    <div class="page-actions">
        <a href="{{ route('departments.create') }}" class="btn btn-primary">Nouveau département</a>
    </div>
</div>

<div class="panel">
    <div class="panel__body panel__body--flush">
        @if($departments->isEmpty())
            <div class="empty-state">
                <div class="empty-state__title">Aucun département</div>
                <p class="empty-state__text">Créez le premier département.</p>
                <a href="{{ route('departments.create') }}" class="btn btn-primary">Créer</a>
            </div>
        @else
            <div class="table-wrap">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Nom</th>
                            <th>Responsable</th>
                            <th>Budget</th>
                            <th>Effectif</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach($departments as $department)
                            <tr>
                                <td><strong>{{ $department->name }}</strong></td>
                                <td>{{ $department->manager?->full_name ?? '—' }}</td>
                                <td class="num">{{ number_format((float) $department->budget, 2, ',', ' ') }}</td>
                                <td class="num">{{ $department->employees_count }}</td>
                                <td>
                                    <div class="action-row">
                                        <a href="{{ route('departments.edit', $department) }}" class="btn btn-secondary btn-sm">Modifier</a>
                                        <form action="{{ route('departments.destroy', $department) }}" method="POST" class="inline-form" onsubmit="return confirm('Supprimer ce département ?');">
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
            <div class="pagination-wrap">{{ $departments->links() }}</div>
        @endif
    </div>
</div>
@endsection

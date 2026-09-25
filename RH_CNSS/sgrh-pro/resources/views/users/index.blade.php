@extends('layouts.app')

@section('title', 'Utilisateurs')

@section('content')
<div class="page-header">
    <div>
        <h1>Utilisateurs</h1>
        <p class="page-header__meta">Comptes d'accès au système SGRH Pro</p>
    </div>
    <div class="page-actions">
        <a href="{{ route('users.create') }}" class="btn btn-primary">Nouvel utilisateur</a>
    </div>
</div>

<div class="panel">
    <div class="panel__body panel__body--flush">
        @if($users->isEmpty())
            <div class="empty-state">
                <div class="empty-state__title">Aucun utilisateur</div>
                <p class="empty-state__text">Créez le premier compte pour démarrer.</p>
                <a href="{{ route('users.create') }}" class="btn btn-primary">Créer un utilisateur</a>
            </div>
        @else
            <div class="table-wrap">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Nom d'utilisateur</th>
                            <th>Rôle</th>
                            <th>Employé lié</th>
                            <th>Changement MDP</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach($users as $u)
                            <tr>
                                <td><strong>{{ $u->username }}</strong></td>
                                <td>{{ $u->role?->name ?? '—' }}</td>
                                <td>{{ $u->employee?->full_name ?? '—' }}</td>
                                <td>
                                    @if($u->must_change_password)
                                        <span class="badge badge-warning">Requis</span>
                                    @else
                                        <span class="badge badge-success">OK</span>
                                    @endif
                                </td>
                                <td>
                                    <div class="action-row">
                                        <a href="{{ route('users.edit', $u) }}" class="btn btn-secondary btn-sm">Modifier</a>
                                        @if(Auth::id() !== $u->id)
                                            <form action="{{ route('users.destroy', $u) }}" method="POST" class="inline-form" onsubmit="return confirm('Supprimer cet utilisateur ?');">
                                                @csrf
                                                @method('DELETE')
                                                <button type="submit" class="btn btn-danger btn-sm">Supprimer</button>
                                            </form>
                                        @endif
                                    </div>
                                </td>
                            </tr>
                        @endforeach
                    </tbody>
                </table>
            </div>
            <div class="pagination-wrap">{{ $users->links() }}</div>
        @endif
    </div>
</div>
@endsection

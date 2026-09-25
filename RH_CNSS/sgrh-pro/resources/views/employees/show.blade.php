@extends('layouts.app')

@section('title', $employee->full_name)

@section('content')
<div class="page-header">
    <div>
        <h1>{{ $employee->full_name }}</h1>
        <p class="page-header__meta">Fiche employé</p>
    </div>
    <div class="page-actions">
        <a href="{{ route('employees.edit', $employee) }}" class="btn btn-primary">Modifier</a>
        <a href="{{ route('employees.index') }}" class="btn btn-secondary">Retour</a>
    </div>
</div>

<div class="grid-2">
    <div class="panel">
        <div class="panel__header">
            <h2 class="panel__title">Informations</h2>
        </div>
        <div class="panel__body">
            @if($employee->photo_path)
                <p class="mb-2">
                    <img src="{{ asset('storage/'.$employee->photo_path) }}" alt="Photo de {{ $employee->full_name }}" class="avatar">
                </p>
            @endif
            <dl class="detail-list">
                <dt>Matricule</dt>
                <dd>{{ $employee->matricule ?? '—' }}</dd>
                <dt>E-mail</dt>
                <dd>{{ $employee->email }}</dd>
                <dt>Téléphone</dt>
                <dd>{{ $employee->phone }}</dd>
                <dt>Adresse</dt>
                <dd>{{ $employee->address }}</dd>
                <dt>Embauche</dt>
                <dd>{{ $employee->hire_date?->format('d/m/Y') }}</dd>
                <dt>Statut</dt>
                <dd>
                    @if($employee->status === 'Actif')
                        <span class="badge badge-success">{{ $employee->status }}</span>
                    @else
                        <span class="badge badge-neutral">{{ $employee->status }}</span>
                    @endif
                </dd>
                <dt>Département</dt>
                <dd>{{ $employee->department?->name ?? '—' }}</dd>
                <dt>Rôle</dt>
                <dd>{{ $employee->role?->name ?? '—' }}</dd>
                <dt>Compte utilisateur</dt>
                <dd>{{ $employee->user?->username ?? '—' }}</dd>
                <dt>RFID</dt>
                <dd>
                    {{ $employee->rfid_card_id ?? '—' }}
                    @if($employee->rfid_card_id)
                        @if($employee->rfid_card_active)
                            <span class="badge badge-success">Active</span>
                        @else
                            <span class="badge badge-warning">Inactive</span>
                        @endif
                    @endif
                </dd>
                <dt>Empreinte</dt>
                <dd>{{ $employee->fingerprint_template ? 'Enregistrée' : 'Non enregistrée' }}</dd>
            </dl>
        </div>
    </div>
</div>
@endsection

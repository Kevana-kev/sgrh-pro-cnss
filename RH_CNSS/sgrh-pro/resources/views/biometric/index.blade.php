@extends('layouts.app')

@section('title', 'Biométrie ZK-9500')

@section('content')
<div class="page-header">
    <div>
        <h1>Biométrie ZK-9500</h1>
        <p class="page-header__meta">Empreintes et cartes RFID</p>
    </div>
</div>

<div class="alert alert-info">
    Le pont biométrique ZK-9500 doit tourner en local (<strong>localhost:5002</strong>). Sans ce service, l'enrôlement et le scan ne fonctionneront pas.
</div>

@if(session('scan_result'))
    <div class="alert alert-success">
        Résultat du scan&nbsp;:
        <pre class="mb-0" style="white-space: pre-wrap; font-size: 0.85rem;">{{ json_encode(session('scan_result'), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) }}</pre>
    </div>
@endif

<div class="grid-2 mb-2">
    <div class="panel">
        <div class="panel__header">
            <h2 class="panel__title">État du bridge</h2>
        </div>
        <div class="panel__body">
            @if(!empty($bridgeStatus['connected']))
                <p>
                    <span class="status-dot status-dot--on"></span>
                    <span class="badge badge-success">Connecté</span>
                </p>
                <dl class="detail-list">
                    @foreach($bridgeStatus as $key => $value)
                        @if($key !== 'connected')
                            <dt>{{ $key }}</dt>
                            <dd>{{ is_scalar($value) ? $value : json_encode($value) }}</dd>
                        @endif
                    @endforeach
                </dl>
            @else
                <p>
                    <span class="status-dot status-dot--off"></span>
                    <span class="badge badge-danger">Hors ligne</span>
                </p>
                <p class="muted mb-0">{{ $bridgeStatus['message'] ?? 'Bridge non disponible.' }}</p>
            @endif

            <form method="POST" action="{{ route('biometric.scan') }}" class="form-actions" style="border-top: none; padding-top: 0.5rem;">
                @csrf
                <button type="submit" class="btn btn-accent">Lancer un scan</button>
            </form>
        </div>
    </div>

    <div class="panel">
        <div class="panel__header">
            <h2 class="panel__title">Appareils enregistrés</h2>
        </div>
        <div class="panel__body panel__body--flush">
            @if($devices->isEmpty())
                <div class="empty-state">
                    <div class="empty-state__title">Aucun appareil</div>
                    <p class="empty-state__text">Les dispositifs biométriques apparaîtront ici.</p>
                </div>
            @else
                <div class="table-wrap">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Nom</th>
                                <th>Type</th>
                                <th>Emplacement</th>
                                <th>Statut</th>
                            </tr>
                        </thead>
                        <tbody>
                            @foreach($devices as $device)
                                <tr>
                                    <td>{{ $device->name }}</td>
                                    <td>{{ $device->device_type ?? '—' }}</td>
                                    <td>{{ $device->location ?? '—' }}</td>
                                    <td>
                                        @if($device->is_active)
                                            <span class="badge badge-success">Actif</span>
                                        @else
                                            <span class="badge badge-neutral">Inactif</span>
                                        @endif
                                    </td>
                                </tr>
                            @endforeach
                        </tbody>
                    </table>
                </div>
            @endif
        </div>
    </div>
</div>

<div class="grid-2 mb-2">
    <div class="panel">
        <div class="panel__header">
            <h2 class="panel__title">Enrôlement empreinte</h2>
        </div>
        <div class="panel__body">
            <div class="form-group mb-1">
                <label for="enroll_employee_id">Employé</label>
                <select id="enroll_employee_id" class="form-control" required>
                    <option value="">— Sélectionner —</option>
                    @foreach($employees as $employee)
                        <option value="{{ $employee->id }}" data-enroll-url="{{ route('biometric.enroll', $employee) }}">{{ $employee->full_name }}</option>
                    @endforeach
                </select>
            </div>
            <form method="POST" action="" id="enroll-form">
                @csrf
                <div class="form-group mb-1">
                    <label for="template">Gabarit d'empreinte</label>
                    <textarea id="template" name="template" class="form-control @error('template') is-invalid @enderror" rows="4" placeholder="Cliquez sur « Scanner via ZK-9500 » ou collez le template…" required>{{ old('template') }}</textarea>
                    @error('template')<div class="form-error">{{ $message }}</div>@enderror
                    <span class="form-hint">Le template est fourni par le bridge local après scan.</span>
                </div>
                <div class="form-actions" style="border-top:none;padding-top:0;">
                    <button type="button" id="btn-scan-fill" class="btn btn-accent">Scanner via ZK-9500</button>
                    <button type="submit" class="btn btn-primary">Enregistrer l'empreinte</button>
                </div>
            </form>
        </div>
    </div>

    <div class="panel">
        <div class="panel__header">
            <h2 class="panel__title">Assigner une carte RFID</h2>
        </div>
        <div class="panel__body">
            <form method="POST" action="{{ route('biometric.rfid.assign') }}">
                @csrf
                <div class="form-group mb-1">
                    <label for="rfid_employee_id">Employé</label>
                    <select id="rfid_employee_id" name="employee_id" class="form-control @error('employee_id') is-invalid @enderror" required>
                        <option value="">— Sélectionner —</option>
                        @foreach($employees as $employee)
                            <option value="{{ $employee->id }}" @selected(old('employee_id') == $employee->id)>{{ $employee->full_name }}</option>
                        @endforeach
                    </select>
                    @error('employee_id')<div class="form-error">{{ $message }}</div>@enderror
                </div>
                <div class="form-group mb-1">
                    <label for="rfid_card_id">Identifiant RFID</label>
                    <input type="text" id="rfid_card_id" name="rfid_card_id" class="form-control @error('rfid_card_id') is-invalid @enderror" value="{{ old('rfid_card_id') }}" required>
                    @error('rfid_card_id')<div class="form-error">{{ $message }}</div>@enderror
                </div>
                <button type="submit" class="btn btn-accent">Assigner</button>
            </form>
        </div>
    </div>
</div>

<div class="panel">
    <div class="panel__header">
        <h2 class="panel__title">Employés enrôlés</h2>
    </div>
    <div class="panel__body panel__body--flush">
        @if($enrolled->isEmpty())
            <div class="empty-state">
                <div class="empty-state__title">Aucun enrôlement</div>
                <p class="empty-state__text">Aucune empreinte ni carte RFID n'est encore associée.</p>
            </div>
        @else
            <div class="table-wrap">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Employé</th>
                            <th>Empreinte</th>
                            <th>RFID</th>
                            <th>Statut RFID</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach($enrolled as $employee)
                            <tr>
                                <td><strong>{{ $employee->full_name }}</strong></td>
                                <td>
                                    @if($employee->fingerprint_template)
                                        <span class="badge badge-teal">Oui</span>
                                    @else
                                        <span class="badge badge-neutral">Non</span>
                                    @endif
                                </td>
                                <td>{{ $employee->rfid_card_id ?? '—' }}</td>
                                <td>
                                    @if($employee->rfid_card_id)
                                        @if($employee->rfid_card_active)
                                            <span class="badge badge-success">Active</span>
                                        @else
                                            <span class="badge badge-warning">Inactive</span>
                                        @endif
                                    @else
                                        —
                                    @endif
                                </td>
                                <td>
                                    @if($employee->rfid_card_id && $employee->rfid_card_active)
                                        <form method="POST" action="{{ route('biometric.rfid.deactivate') }}" class="inline-form" onsubmit="return confirm('Désactiver la carte RFID ?');">
                                            @csrf
                                            <input type="hidden" name="employee_id" value="{{ $employee->id }}">
                                            <button type="submit" class="btn btn-danger btn-sm">Désactiver RFID</button>
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
        @endif
    </div>
</div>
@endsection

@push('scripts')
<script>
(function () {
    var select = document.getElementById('enroll_employee_id');
    var form = document.getElementById('enroll-form');
    var template = document.getElementById('template');
    var scanBtn = document.getElementById('btn-scan-fill');
    if (!select || !form) return;

    form.addEventListener('submit', function (e) {
        var opt = select.options[select.selectedIndex];
        var url = opt && opt.getAttribute('data-enroll-url');
        if (!url) {
            e.preventDefault();
            alert('Veuillez sélectionner un employé.');
            return;
        }
        form.action = url;
    });

    if (scanBtn) {
        scanBtn.addEventListener('click', async function () {
            scanBtn.disabled = true;
            scanBtn.textContent = 'Scan en cours…';
            try {
                var token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
                var res = await fetch('{{ route('biometric.scan') }}', {
                    method: 'POST',
                    headers: {
                        'X-CSRF-TOKEN': token,
                        'Accept': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                var data = await res.json();
                if (!res.ok) {
                    throw new Error(data.error || data.message || ('HTTP ' + res.status));
                }
                if (!data.template) {
                    throw new Error('Aucun template renvoyé par le bridge.');
                }
                template.value = data.template;
                alert('Template capturé. Sélectionnez un employé puis cliquez sur Enregistrer.');
            } catch (err) {
                alert('Échec du scan : ' + err.message);
            } finally {
                scanBtn.disabled = false;
                scanBtn.textContent = 'Scanner via ZK-9500';
            }
        });
    }
})();
</script>
@endpush

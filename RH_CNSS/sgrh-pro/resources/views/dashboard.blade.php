@extends('layouts.app')

@section('title', 'Tableau de bord')

@section('content')
<div class="page-header">
    <div>
        <h1>Tableau de bord</h1>
        <p class="page-header__meta">Vue d'ensemble des indicateurs RH — CNSS</p>
    </div>
</div>

<div class="kpi-grid">
    <div class="kpi kpi--blue">
        <div class="kpi__label">Employés actifs</div>
        <div class="kpi__value">{{ $employeesCount }}</div>
    </div>
    <div class="kpi kpi--teal">
        <div class="kpi__label">Présences du jour</div>
        <div class="kpi__value">{{ $attendancesToday }}</div>
    </div>
    <div class="kpi kpi--warn">
        <div class="kpi__label">Congés en attente</div>
        <div class="kpi__value">{{ $pendingLeaves }}</div>
    </div>
    <div class="kpi kpi--ok">
        <div class="kpi__label">Rémunérations brouillon</div>
        <div class="kpi__value">{{ $remunerationDrafts }}</div>
    </div>
</div>

<div class="grid-2">
    <div class="panel">
        <div class="panel__header">
            <h2 class="panel__title">Présences — 7 derniers jours</h2>
        </div>
        <div class="panel__body">
            <div class="chart-box">
                <canvas id="attendanceChart" aria-label="Graphique des présences"></canvas>
            </div>
        </div>
    </div>

    <div class="panel">
        <div class="panel__header">
            <h2 class="panel__title">Activité récente</h2>
        </div>
        <div class="panel__body panel__body--flush">
            @if($recentLogs->isEmpty())
                <div class="empty-state">
                    <div class="empty-state__title">Aucune activité</div>
                    <p class="empty-state__text">Les actions utilisateurs apparaîtront ici.</p>
                </div>
            @else
                <div class="table-wrap">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Utilisateur</th>
                                <th>Action</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            @foreach($recentLogs as $log)
                                <tr>
                                    <td>{{ $log->username ?? '—' }}</td>
                                    <td>{{ $log->action }}</td>
                                    <td>{{ $log->created_at?->format('d/m/Y H:i') }}</td>
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

@push('scripts')
<script>
document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('attendanceChart');
    if (!canvas || typeof Chart === 'undefined') return;

    var labels = @json($chartLabels ?? []);
    var data = @json($chartData ?? []);

    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Pointages',
                data: data,
                backgroundColor: 'rgba(13, 148, 136, 0.75)',
                borderColor: '#0D9488',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { precision: 0 }
                }
            }
        }
    });
});
</script>
@endpush

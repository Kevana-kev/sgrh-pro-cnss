<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>@yield('title', 'Tableau de bord') — SGRH Pro · CNSS</title>
    <link rel="stylesheet" href="{{ asset('css/app.css') }}">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js" defer></script>
</head>
<body>
@php
    $user = Auth::user();
@endphp
<div class="app-shell">
    <aside class="sidebar">
        <div class="sidebar-brand">
            <div class="sidebar-brand__name">SGRH Pro</div>
            <span class="sidebar-brand__sub">CNSS</span>
        </div>
        <nav class="sidebar-nav">
            <a href="{{ route('dashboard') }}" class="{{ request()->routeIs('dashboard') ? 'is-active' : '' }}">
                <span class="sidebar-nav__icon">▣</span> Tableau de bord
            </a>

            @if($user?->hasPermission('manage_users'))
                <a href="{{ route('users.index') }}" class="{{ request()->routeIs('users.*') ? 'is-active' : '' }}">
                    <span class="sidebar-nav__icon">◎</span> Utilisateurs
                </a>
            @endif

            @if($user?->hasPermission('manage_employees'))
                <a href="{{ route('employees.index') }}" class="{{ request()->routeIs('employees.*') ? 'is-active' : '' }}">
                    <span class="sidebar-nav__icon">◉</span> Employés
                </a>
            @endif

            @if($user?->hasPermission('manage_departments'))
                <a href="{{ route('departments.index') }}" class="{{ request()->routeIs('departments.*') ? 'is-active' : '' }}">
                    <span class="sidebar-nav__icon">▦</span> Départements
                </a>
            @endif

            @if($user?->hasPermission('manage_biometric'))
                <a href="{{ route('biometric.index') }}" class="{{ request()->routeIs('biometric.*') ? 'is-active' : '' }}">
                    <span class="sidebar-nav__icon">◈</span> Biométrie ZK-9500
                </a>
            @endif

            @if($user?->hasPermission('manage_attendances'))
                <a href="{{ route('attendances.index') }}" class="{{ request()->routeIs('attendances.*') ? 'is-active' : '' }}">
                    <span class="sidebar-nav__icon">◷</span> Présences
                </a>
            @endif

            @if($user?->hasPermission('manage_leaves'))
                <a href="{{ route('leaves.index') }}" class="{{ request()->routeIs('leaves.*') ? 'is-active' : '' }}">
                    <span class="sidebar-nav__icon">☰</span> Congés
                </a>
            @endif

            @if($user?->hasPermission('manage_remuneration'))
                <a href="{{ route('remunerations.index') }}" class="{{ request()->routeIs('remunerations.*') ? 'is-active' : '' }}">
                    <span class="sidebar-nav__icon">₪</span> Éléments de rémunération
                </a>
            @endif

            @if($user?->hasPermission('manage_evaluations'))
                <a href="{{ route('evaluations.index') }}" class="{{ request()->routeIs('evaluations.*') ? 'is-active' : '' }}">
                    <span class="sidebar-nav__icon">★</span> Évaluations
                </a>
            @endif

            @if($user?->hasPermission('view_reports'))
                <a href="{{ route('reports.index') }}" class="{{ request()->routeIs('reports.*') ? 'is-active' : '' }}">
                    <span class="sidebar-nav__icon">▣</span> Rapports
                </a>
            @endif

            @if($user?->hasPermission('manage_settings'))
                <a href="{{ route('settings.edit') }}" class="{{ request()->routeIs('settings.*') ? 'is-active' : '' }}">
                    <span class="sidebar-nav__icon">⚙</span> Paramètres
                </a>
            @endif
        </nav>
    </aside>

    <div class="app-main">
        <header class="topbar">
            <div class="topbar__title">@yield('title', 'Tableau de bord')</div>
            <div class="topbar__user">
                <span class="topbar__name">{{ $user?->username }}</span>
                <form action="{{ route('logout') }}" method="POST" class="inline-form">
                    @csrf
                    <button type="submit" class="btn btn-secondary btn-sm">Déconnexion</button>
                </form>
            </div>
        </header>

        <main class="content">
            @if(session('success'))
                <div class="alert alert-success">{{ session('success') }}</div>
            @endif
            @if(session('error'))
                <div class="alert alert-error">{{ session('error') }}</div>
            @endif
            @if(session('warning'))
                <div class="alert alert-warning">{{ session('warning') }}</div>
            @endif

            @yield('content')
        </main>
    </div>
</div>

@stack('scripts')
</body>
</html>

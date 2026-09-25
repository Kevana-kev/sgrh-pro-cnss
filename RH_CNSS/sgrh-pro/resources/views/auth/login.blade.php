@extends('layouts.guest')

@section('title', 'Connexion')

@section('content')
<div class="guest-shell">
    <section class="guest-hero" aria-label="Présentation SGRH Pro">
        <div class="guest-hero__sub">CNSS</div>
        <h1 class="guest-hero__brand">SGRH Pro</h1>
        <p class="guest-hero__tagline">
            Système de gestion des ressources humaines — présence, congés, rémunération et biométrie ZK-9500.
        </p>
    </section>

    <div class="guest-panel">
        <div class="guest-card">
            <h2 class="guest-card__title">Connexion</h2>
            <p class="guest-card__lead">Accédez à votre espace institutionnel.</p>

            @if(session('success'))
                <div class="alert alert-success">{{ session('success') }}</div>
            @endif
            @if(session('error'))
                <div class="alert alert-error">{{ session('error') }}</div>
            @endif

            <form method="POST" action="{{ route('login.attempt') }}" autocomplete="off">
                @csrf

                <div class="form-group mb-1">
                    <label for="username">Nom d'utilisateur</label>
                    <input
                        type="text"
                        id="username"
                        name="username"
                        class="form-control @error('username') is-invalid @enderror"
                        value="{{ old('username') }}"
                        required
                        autofocus
                        autocomplete="username"
                    >
                    @error('username')
                        <div class="form-error">{{ $message }}</div>
                    @enderror
                </div>

                <div class="form-group mb-1">
                    <label for="password">Mot de passe</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        class="form-control @error('password') is-invalid @enderror"
                        required
                        autocomplete="current-password"
                    >
                    @error('password')
                        <div class="form-error">{{ $message }}</div>
                    @enderror
                </div>

                <div class="form-check mb-2">
                    <input type="checkbox" id="remember" name="remember" value="1" @checked(old('remember'))>
                    <label for="remember">Se souvenir de moi</label>
                </div>

                <button type="submit" class="btn btn-primary btn-block">Se connecter</button>
            </form>

            <p class="guest-footer">SGRH Pro · Caisse Nationale de Sécurité Sociale</p>
        </div>
    </div>
</div>
@endsection

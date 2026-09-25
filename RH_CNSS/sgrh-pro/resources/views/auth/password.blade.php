@extends('layouts.guest')

@section('title', 'Changer le mot de passe')

@section('content')
<div class="guest-shell">
    <section class="guest-hero" aria-label="SGRH Pro">
        <div class="guest-hero__sub">CNSS</div>
        <h1 class="guest-hero__brand">SGRH Pro</h1>
        <p class="guest-hero__tagline">
            Pour la sécurité de votre compte, veuillez définir un nouveau mot de passe avant de continuer.
        </p>
    </section>

    <div class="guest-panel">
        <div class="guest-card">
            <h2 class="guest-card__title">Changer le mot de passe</h2>
            <p class="guest-card__lead">
                Compte&nbsp;: <strong>{{ $user->username }}</strong>
            </p>

            @if(session('warning'))
                <div class="alert alert-warning">{{ session('warning') }}</div>
            @endif
            @if(session('error'))
                <div class="alert alert-error">{{ session('error') }}</div>
            @endif

            <form method="POST" action="{{ route('password.update') }}" autocomplete="off">
                @csrf

                <div class="form-group mb-1">
                    <label for="current_password">Mot de passe actuel</label>
                    <input
                        type="password"
                        id="current_password"
                        name="current_password"
                        class="form-control @error('current_password') is-invalid @enderror"
                        required
                        autocomplete="current-password"
                    >
                    @error('current_password')
                        <div class="form-error">{{ $message }}</div>
                    @enderror
                </div>

                <div class="form-group mb-1">
                    <label for="password">Nouveau mot de passe</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        class="form-control @error('password') is-invalid @enderror"
                        required
                        autocomplete="new-password"
                    >
                    @error('password')
                        <div class="form-error">{{ $message }}</div>
                    @enderror
                </div>

                <div class="form-group mb-2">
                    <label for="password_confirmation">Confirmation</label>
                    <input
                        type="password"
                        id="password_confirmation"
                        name="password_confirmation"
                        class="form-control"
                        required
                        autocomplete="new-password"
                    >
                </div>

                <button type="submit" class="btn btn-accent btn-block">Enregistrer le mot de passe</button>
            </form>

            <p class="guest-footer">
                <form action="{{ route('logout') }}" method="POST" class="inline-form">
                    @csrf
                    <button type="submit" class="btn btn-ghost btn-sm">Se déconnecter</button>
                </form>
            </p>
        </div>
    </div>
</div>
@endsection

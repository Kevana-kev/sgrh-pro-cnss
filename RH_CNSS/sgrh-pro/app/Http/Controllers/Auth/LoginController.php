<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use App\Services\ActivityLogger;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\View\View;

class LoginController extends Controller
{
    public function showLogin(): View|RedirectResponse
    {
        if (Auth::check()) {
            return redirect()->route('dashboard');
        }

        return view('auth.login');
    }

    public function login(Request $request): RedirectResponse
    {
        $credentials = $request->validate([
            'username' => ['required', 'string'],
            'password' => ['required', 'string'],
        ], [
            'username.required' => 'Le nom d\'utilisateur est obligatoire.',
            'password.required' => 'Le mot de passe est obligatoire.',
        ]);

        $remember = $request->boolean('remember');

        if (! Auth::attempt($credentials, $remember)) {
            return back()
                ->withInput($request->only('username', 'remember'))
                ->withErrors(['username' => 'Identifiants incorrects.']);
        }

        $request->session()->regenerate();

        $user = Auth::user();
        ActivityLogger::log($user?->username, 'Connexion réussie');

        if ($user?->must_change_password) {
            return redirect()->route('password.edit')
                ->with('warning', 'Vous devez changer votre mot de passe avant de continuer.');
        }

        return redirect()->intended(route('dashboard'))
            ->with('success', 'Bienvenue, '.$user->username.'.');
    }

    public function logout(Request $request): RedirectResponse
    {
        $username = Auth::user()?->username;

        Auth::logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();

        ActivityLogger::log($username, 'Déconnexion');

        return redirect()->route('login')
            ->with('success', 'Vous êtes déconnecté.');
    }
}

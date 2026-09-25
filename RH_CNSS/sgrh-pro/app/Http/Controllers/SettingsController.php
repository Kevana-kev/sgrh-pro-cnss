<?php

namespace App\Http\Controllers;

use App\Models\SystemParameter;
use App\Services\ActivityLogger;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\View\View;

class SettingsController extends Controller
{
    public function edit(): View
    {
        return view('settings.edit', [
            'work_start_time' => SystemParameter::getValue('work_start_time', '08:00'),
            'late_threshold_minutes' => SystemParameter::getValue('late_threshold_minutes', '15'),
            'organization_name' => SystemParameter::getValue('organization_name', 'CNSS — SGRH Pro'),
        ]);
    }

    public function update(Request $request): RedirectResponse
    {
        $validated = $request->validate([
            'work_start_time' => ['required', 'date_format:H:i'],
            'late_threshold_minutes' => ['required', 'integer', 'min:0', 'max:240'],
            'organization_name' => ['nullable', 'string', 'max:255'],
        ], [
            'work_start_time.required' => 'L\'heure de début est obligatoire.',
            'work_start_time.date_format' => 'Format attendu : HH:MM.',
            'late_threshold_minutes.required' => 'Le seuil de retard est obligatoire.',
            'late_threshold_minutes.integer' => 'Le seuil de retard doit être un entier.',
        ]);

        $this->upsert('work_start_time', $validated['work_start_time']);
        $this->upsert('late_threshold_minutes', (string) $validated['late_threshold_minutes']);

        if (array_key_exists('organization_name', $validated) && $validated['organization_name'] !== null) {
            $this->upsert('organization_name', $validated['organization_name']);
        }

        ActivityLogger::log(
            Auth::user()?->username,
            'Mise à jour des paramètres système'
        );

        return redirect()->back()
            ->with('success', 'Paramètres enregistrés avec succès.');
    }

    private function upsert(string $key, string $value): void
    {
        SystemParameter::query()->updateOrCreate(
            ['key' => $key],
            ['value' => $value]
        );
    }
}

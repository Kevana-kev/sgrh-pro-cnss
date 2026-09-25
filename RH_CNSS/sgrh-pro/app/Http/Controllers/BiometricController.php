<?php

namespace App\Http\Controllers;

use App\Models\BiometricDevice;
use App\Models\Employee;
use App\Services\ActivityLogger;
use App\Services\BiometricBridgeService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Validation\Rule;
use Illuminate\View\View;

class BiometricController extends Controller
{
    public function __construct(
        private readonly BiometricBridgeService $bridge
    ) {}

    public function index(): View
    {
        $bridgeStatus = $this->bridge->status();

        $enrolled = Employee::query()
            ->where(function ($q) {
                $q->whereNotNull('fingerprint_template')
                    ->orWhereNotNull('rfid_card_id');
            })
            ->orderBy('last_name')
            ->orderBy('first_name')
            ->get();

        $devices = BiometricDevice::query()
            ->orderBy('name')
            ->get();

        $employees = Employee::query()
            ->where('status', 'Actif')
            ->orderBy('last_name')
            ->orderBy('first_name')
            ->get();

        return view('biometric.index', compact(
            'bridgeStatus',
            'enrolled',
            'devices',
            'employees'
        ));
    }

    public function enrollFingerprint(Request $request, Employee $employee): RedirectResponse
    {
        $validated = $request->validate([
            'template' => ['required', 'string'],
        ], [
            'template.required' => 'Le gabarit d\'empreinte est obligatoire.',
        ]);

        $employee->fingerprint_template = $validated['template'];
        $employee->save();

        ActivityLogger::log(
            Auth::user()?->username,
            'Empreinte enregistrée employé #'.$employee->id
        );

        return redirect()->back()
            ->with('success', 'Empreinte enregistrée pour '.$employee->full_name.'.');
    }

    public function assignRfid(Request $request): RedirectResponse
    {
        $validated = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
            'rfid_card_id' => [
                'required',
                'string',
                'max:64',
                Rule::unique('employees', 'rfid_card_id')->ignore($request->integer('employee_id')),
            ],
        ], [
            'employee_id.required' => 'L\'employé est obligatoire.',
            'rfid_card_id.required' => 'L\'identifiant RFID est obligatoire.',
            'rfid_card_id.unique' => 'Cette carte RFID est déjà assignée.',
        ]);

        $employee = Employee::findOrFail($validated['employee_id']);
        $employee->rfid_card_id = $validated['rfid_card_id'];
        $employee->rfid_card_active = true;
        $employee->save();

        ActivityLogger::log(
            Auth::user()?->username,
            'RFID assignée à employé #'.$employee->id
        );

        return redirect()->back()
            ->with('success', 'Carte RFID assignée à '.$employee->full_name.'.');
    }

    public function deactivateRfid(Request $request): RedirectResponse
    {
        $validated = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
        ], [
            'employee_id.required' => 'L\'employé est obligatoire.',
        ]);

        $employee = Employee::findOrFail($validated['employee_id']);
        $employee->rfid_card_active = false;
        $employee->save();

        ActivityLogger::log(
            Auth::user()?->username,
            'RFID désactivée employé #'.$employee->id
        );

        return redirect()->back()
            ->with('success', 'Carte RFID désactivée pour '.$employee->full_name.'.');
    }

    public function scanProxy(): JsonResponse|RedirectResponse
    {
        try {
            $data = $this->bridge->scan();

            if (request()->expectsJson()) {
                return response()->json($data);
            }

            return redirect()->back()
                ->with('success', 'Scan effectué.')
                ->with('scan_result', $data);
        } catch (\Throwable $e) {
            if (request()->expectsJson()) {
                return response()->json(['error' => $e->getMessage()], 503);
            }

            return redirect()->back()
                ->with('error', 'Échec du scan : '.$e->getMessage());
        }
    }
}

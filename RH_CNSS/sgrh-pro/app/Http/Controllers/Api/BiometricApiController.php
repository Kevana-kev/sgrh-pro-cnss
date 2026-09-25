<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\BiometricDevice;
use App\Models\Employee;
use App\Services\ActivityLogger;
use App\Services\BiometricBridgeService;
use App\Services\FingerprintTemplateService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Validation\ValidationException;

class BiometricApiController extends Controller
{
    public function __construct(
        private BiometricBridgeService $bridge,
        private FingerprintTemplateService $fingerprints,
    ) {}

    public function scan(): JsonResponse
    {
        try {
            return response()->json($this->bridge->scan());
        } catch (\Throwable $e) {
            return response()->json(['error' => $e->getMessage()], 503);
        }
    }

    public function status(): JsonResponse
    {
        return response()->json($this->bridge->status());
    }

    public function verifyTemplate(Request $request): JsonResponse
    {
        $data = $request->validate([
            'template' => ['required', 'string'],
            'employee_id' => ['nullable', 'integer', 'exists:employees,id'],
            'pending_templates' => ['nullable', 'array', 'max:2'],
            'pending_templates.*' => ['string'],
        ]);

        $duplicate = $this->fingerprints->findDuplicate(
            $data['template'],
            $this->bridge,
            isset($data['employee_id']) ? (int) $data['employee_id'] : null,
            $data['pending_templates'] ?? [],
        );

        if ($duplicate) {
            return response()->json([
                'valid' => false,
                'duplicate' => true,
                'message' => $duplicate['message'],
                'type' => $duplicate['type'],
            ]);
        }

        return response()->json(['valid' => true, 'duplicate' => false]);
    }

    public function enrolled(): JsonResponse
    {
        $employees = Employee::query()->orderBy('last_name')->get();
        $result = [];

        foreach ($employees as $emp) {
            if ($emp->fingerprint_template || $emp->rfid_card_id) {
                $fingerCount = FingerprintTemplateService::count($emp->fingerprint_template);
                $result[] = [
                    'id' => $emp->id,
                    'name' => trim($emp->first_name.' '.$emp->last_name),
                    'has_fingerprint' => $fingerCount > 0,
                    'fingerprint_count' => $fingerCount,
                    'fingerprint_complete' => FingerprintTemplateService::isComplete($emp->fingerprint_template),
                    'rfid_card_id' => $emp->rfid_card_id,
                    'rfid_card_active' => (bool) $emp->rfid_card_active,
                ];
            }
        }

        return response()->json($result);
    }

    public function enroll(Request $request, int $employeeId): JsonResponse
    {
        $employee = Employee::findOrFail($employeeId);

        $data = $request->validate([
            'templates' => ['required', 'array', 'size:'.FingerprintTemplateService::REQUIRED_FINGERS],
            'templates.*' => ['required', 'string'],
        ]);

        try {
            $this->fingerprints->assertEnrollmentValid($data['templates'], $this->bridge, $employeeId);
        } catch (\InvalidArgumentException $e) {
            throw ValidationException::withMessages(['templates' => $e->getMessage()]);
        }

        $employee->fingerprint_template = FingerprintTemplateService::encode($data['templates']);
        $employee->save();

        ActivityLogger::log(
            $request->user()?->username,
            'Empreintes enregistrées (3 doigts) employé #'.$employeeId
        );

        return response()->json([
            'message' => 'Trois empreintes enregistrées avec succès',
            'employee_id' => $employeeId,
            'fingerprint_count' => FingerprintTemplateService::REQUIRED_FINGERS,
        ]);
    }

    public function deleteFingerprint(Request $request): JsonResponse
    {
        $data = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
        ]);

        $employee = Employee::findOrFail($data['employee_id']);
        $employee->fingerprint_template = null;
        $employee->save();

        ActivityLogger::log($request->user()?->username, 'Empreintes supprimées employé #'.$employee->id);

        return response()->json(['message' => 'Empreintes supprimées']);
    }

    public function assignRfid(Request $request): JsonResponse
    {
        $data = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
            'rfid_card_id' => ['required', 'string', 'max:64'],
        ]);

        $exists = Employee::query()
            ->where('rfid_card_id', $data['rfid_card_id'])
            ->where('id', '!=', $data['employee_id'])
            ->exists();

        if ($exists) {
            throw ValidationException::withMessages([
                'rfid_card_id' => 'Cette carte RFID est déjà attribuée à un autre employé.',
            ]);
        }

        $employee = Employee::findOrFail($data['employee_id']);
        $employee->rfid_card_id = $data['rfid_card_id'];
        $employee->rfid_card_active = true;
        $employee->save();

        ActivityLogger::log($request->user()?->username, 'RFID assignée à employé #'.$employee->id);

        return response()->json([
            'message' => 'RFID assignée',
            'employee_id' => $employee->id,
            'rfid_card_id' => $employee->rfid_card_id,
        ]);
    }

    public function updateRfid(Request $request): JsonResponse
    {
        $data = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
            'rfid_card_id' => ['required', 'string', 'max:64'],
        ]);

        $exists = Employee::query()
            ->where('rfid_card_id', $data['rfid_card_id'])
            ->where('id', '!=', $data['employee_id'])
            ->exists();

        if ($exists) {
            throw ValidationException::withMessages([
                'rfid_card_id' => 'Cette carte RFID est déjà attribuée à un autre employé.',
            ]);
        }

        $employee = Employee::findOrFail($data['employee_id']);
        $employee->rfid_card_id = $data['rfid_card_id'];
        $employee->rfid_card_active = true;
        $employee->save();

        ActivityLogger::log($request->user()?->username, 'RFID modifiée employé #'.$employee->id);

        return response()->json(['message' => 'Carte RFID mise à jour']);
    }

    public function deactivateRfid(Request $request): JsonResponse
    {
        $data = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
        ]);

        $employee = Employee::findOrFail($data['employee_id']);
        $employee->rfid_card_active = false;
        $employee->save();

        return response()->json(['message' => 'RFID désactivée']);
    }

    public function reactivateRfid(Request $request): JsonResponse
    {
        $data = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
        ]);

        $employee = Employee::findOrFail($data['employee_id']);

        if (! $employee->rfid_card_id) {
            throw ValidationException::withMessages([
                'employee_id' => 'Aucune carte RFID enregistrée pour cet employé.',
            ]);
        }

        $employee->rfid_card_active = true;
        $employee->save();

        return response()->json(['message' => 'RFID réactivée']);
    }

    public function deleteRfid(Request $request): JsonResponse
    {
        $data = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
        ]);

        $employee = Employee::findOrFail($data['employee_id']);
        $employee->rfid_card_id = null;
        $employee->rfid_card_active = false;
        $employee->save();

        ActivityLogger::log($request->user()?->username, 'RFID supprimée employé #'.$employee->id);

        return response()->json(['message' => 'Carte RFID supprimée']);
    }

    public function devices(): JsonResponse
    {
        $devices = BiometricDevice::query()->orderBy('name')->get();

        return response()->json($devices->map(fn (BiometricDevice $d) => [
            'id' => $d->id,
            'name' => $d->name,
            'device_type' => $d->device_type,
            'location' => $d->location,
            'is_active' => (bool) $d->is_active,
            'last_seen' => optional($d->last_seen)?->toIso8601String(),
        ])->values());
    }
}

<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Attendance;
use App\Models\Employee;
use App\Models\SystemParameter;
use App\Services\ActivityLogger;
use Carbon\Carbon;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class BiometricCheckinController extends Controller
{
    public function checkinRfid(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'rfid_card_id' => ['required', 'string', 'max:64'],
        ]);

        $employee = Employee::query()
            ->where('rfid_card_id', $validated['rfid_card_id'])
            ->where('rfid_card_active', true)
            ->first();

        if (! $employee) {
            return response()->json(['error' => 'Carte non reconnue ou inactive.'], 404);
        }

        return $this->registerPunch($employee, 'rfid');
    }

    public function checkinFingerprint(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
        ]);

        $employee = Employee::findOrFail($validated['employee_id']);

        if (! $employee->fingerprint_template) {
            return response()->json(['error' => 'Aucune empreinte enregistrée pour cet employé.'], 422);
        }

        return $this->registerPunch($employee, 'fingerprint');
    }

    private function registerPunch(Employee $employee, string $source): JsonResponse
    {
        $open = Attendance::query()
            ->where('employee_id', $employee->id)
            ->whereNull('check_out')
            ->orderByDesc('check_in')
            ->first();

        if ($open) {
            $checkOut = Carbon::now();
            $open->check_out = $checkOut;
            $open->worked_hours = round(
                max(($checkOut->getTimestamp() - $open->check_in->getTimestamp()) / 3600, 0),
                2
            );
            $open->save();

            ActivityLogger::log('system', 'Sortie biométrique ('.$source.') employé #'.$employee->id);

            return response()->json([
                'message' => 'Sortie enregistrée.',
                'action' => 'checkout',
                'employee' => $employee->full_name,
                'worked_hours' => $open->worked_hours,
                'attendance_id' => $open->id,
            ]);
        }

        $checkIn = Carbon::now();
        $attendance = Attendance::create([
            'employee_id' => $employee->id,
            'check_in' => $checkIn,
            'worked_hours' => 0,
            'late_minutes' => $this->computeLateMinutes($checkIn),
            'is_absent' => false,
            'source' => $source,
        ]);

        ActivityLogger::log('system', 'Entrée biométrique ('.$source.') employé #'.$employee->id);

        return response()->json([
            'message' => 'Pointage enregistré.',
            'action' => 'checkin',
            'employee' => $employee->full_name,
            'attendance_id' => $attendance->id,
            'late_minutes' => $attendance->late_minutes,
        ], 201);
    }

    private function computeLateMinutes(Carbon $checkIn): int
    {
        $workStart = SystemParameter::getValue('work_start_time', '08:00') ?: '08:00';
        $threshold = (int) (SystemParameter::getValue('late_threshold_minutes', '15') ?: 15);

        $expected = $checkIn->copy()->setTimeFromTimeString($workStart);
        $diff = $expected->diffInMinutes($checkIn, false);

        if ($diff <= $threshold) {
            return 0;
        }

        return (int) $diff;
    }
}

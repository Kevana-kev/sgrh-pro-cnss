<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Attendance;
use App\Models\Employee;
use App\Services\ActivityLogger;
use App\Support\SpaSerializer;
use Carbon\Carbon;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class AttendanceApiController extends Controller
{
    public function index(): JsonResponse
    {
        $items = Attendance::query()->orderByDesc('check_in')->limit(500)->get();

        return response()->json($items->map(fn (Attendance $a) => SpaSerializer::attendance($a))->values());
    }

    public function checkin(Request $request): JsonResponse
    {
        $data = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
            'check_in' => ['nullable', 'date'],
            'worked_hours' => ['nullable', 'numeric'],
            'late_minutes' => ['nullable', 'integer'],
            'is_absent' => ['nullable', 'boolean'],
            'source' => ['nullable', 'string', 'max:20'],
        ]);

        $attendance = Attendance::create([
            'employee_id' => $data['employee_id'],
            'check_in' => $data['check_in'] ?? now(),
            'worked_hours' => $data['worked_hours'] ?? 0,
            'late_minutes' => $data['late_minutes'] ?? 0,
            'is_absent' => $data['is_absent'] ?? false,
            'source' => $data['source'] ?? 'manual',
        ]);

        ActivityLogger::log($request->user()?->username, 'Check-in employé #'.$attendance->employee_id);

        return response()->json(SpaSerializer::attendance($attendance), 201);
    }

    public function checkout(Request $request): JsonResponse
    {
        $data = $request->validate([
            'attendance_id' => ['required', 'exists:attendances,id'],
            'check_out' => ['nullable', 'date'],
        ]);

        $attendance = Attendance::findOrFail($data['attendance_id']);
        $checkOut = isset($data['check_out']) ? Carbon::parse($data['check_out']) : now();
        $attendance->check_out = $checkOut;
        $attendance->worked_hours = round(max(($checkOut->getTimestamp() - $attendance->check_in->getTimestamp()) / 3600, 0), 2);
        $attendance->save();

        ActivityLogger::log($request->user()?->username, 'Check-out employé #'.$attendance->employee_id);

        return response()->json(SpaSerializer::attendance($attendance));
    }

    public function checkoutEmployee(Request $request): JsonResponse
    {
        $data = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
            'check_out' => ['nullable', 'date'],
        ]);

        $attendance = Attendance::query()
            ->where('employee_id', $data['employee_id'])
            ->whereNull('check_out')
            ->orderByDesc('check_in')
            ->first();

        if (! $attendance) {
            return response()->json(['error' => 'Aucun pointage ouvert pour cet employé'], 404);
        }

        $checkOut = isset($data['check_out']) ? Carbon::parse($data['check_out']) : now();
        $attendance->check_out = $checkOut;
        $attendance->worked_hours = round(max(($checkOut->getTimestamp() - $attendance->check_in->getTimestamp()) / 3600, 0), 2);
        $attendance->save();

        ActivityLogger::log($request->user()?->username, 'Check-out employé #'.$attendance->employee_id);

        return response()->json(SpaSerializer::attendance($attendance));
    }

    public function monthlySummary(Request $request): JsonResponse
    {
        $month = trim((string) $request->query('month', ''));
        if (! preg_match('/^\d{4}-\d{2}$/', $month)) {
            return response()->json(['error' => "Paramètre 'month' requis (YYYY-MM)"], 400);
        }

        [$year, $monthValue] = array_map('intval', explode('-', $month));
        $start = Carbon::create($year, $monthValue, 1)->startOfDay();
        $end = $start->copy()->endOfMonth();

        $employees = Employee::query()->orderBy('first_name')->orderBy('last_name')->get();
        $summaries = [];

        foreach ($employees as $employee) {
            $records = Attendance::query()
                ->where('employee_id', $employee->id)
                ->whereBetween('check_in', [$start, $end])
                ->get();

            $summaries[] = [
                'employee_id' => $employee->id,
                'employee_name' => trim($employee->first_name.' '.$employee->last_name),
                'month' => $month,
                'presence_days' => $records->where('is_absent', false)->count(),
                'absence_days' => $records->where('is_absent', true)->count(),
                'worked_hours' => round((float) $records->sum('worked_hours'), 2),
                'late_minutes' => (int) $records->sum('late_minutes'),
            ];
        }

        return response()->json($summaries);
    }

    public function update(Request $request, int $attendanceId): JsonResponse
    {
        $attendance = Attendance::findOrFail($attendanceId);

        $data = $request->validate([
            'check_in' => ['sometimes', 'date'],
            'check_out' => ['nullable', 'date'],
            'worked_hours' => ['sometimes', 'numeric'],
            'late_minutes' => ['sometimes', 'integer'],
            'is_absent' => ['sometimes', 'boolean'],
            'source' => ['sometimes', 'string', 'max:20'],
        ]);

        $attendance->fill($data)->save();
        ActivityLogger::log($request->user()?->username, 'Modification pointage #'.$attendance->id);

        return response()->json(SpaSerializer::attendance($attendance));
    }

    public function destroy(Request $request, int $attendanceId): JsonResponse
    {
        Attendance::findOrFail($attendanceId)->delete();
        ActivityLogger::log($request->user()?->username, 'Suppression pointage #'.$attendanceId);

        return response()->json(['message' => 'Pointage supprimé']);
    }
}

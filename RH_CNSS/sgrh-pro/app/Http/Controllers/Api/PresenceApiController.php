<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Attendance;
use App\Models\Contract;
use App\Models\Department;
use App\Models\Employee;
use App\Models\EmployeeSkill;
use App\Models\Leave;
use App\Models\Message;
use App\Models\Notification;
use App\Models\Payroll;
use App\Models\PerformanceEvaluation;
use App\Models\SystemParameter;
use App\Models\TrainingEnrollment;
use App\Models\User;
use App\Services\ActivityLogger;
use App\Services\BiometricBridgeService;
use App\Services\FingerprintTemplateService;
use App\Support\SpaSerializer;
use Carbon\Carbon;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class PresenceApiController extends Controller
{
    public function __construct(private BiometricBridgeService $bridge) {}

    public function today(): JsonResponse
    {
        $today = Carbon::today();
        $now = Carbon::now();
        $workStart = SystemParameter::getValue('work_start_time', '08:00') ?: '08:00';
        $dayEnded = $now->hour >= 18;

        $employees = Employee::query()
            ->with('department')
            ->where(function ($q) {
                $q->whereRaw('LOWER(TRIM(status)) IN (?, ?, ?)', ['actif', 'act', 'active']);
            })
            ->orderBy('last_name')
            ->orderBy('first_name')
            ->get();

        $attendances = Attendance::query()
            ->with('employee')
            ->whereDate('check_in', $today)
            ->orderByDesc('check_in')
            ->get()
            ->groupBy('employee_id');

        $board = [];
        $stats = [
            'expected' => $employees->count(),
            'present' => 0,
            'completed' => 0,
            'late' => 0,
            'absent' => 0,
        ];

        foreach ($employees as $employee) {
            $dayRecords = $attendances->get($employee->id, collect());
            /** @var Attendance|null $primary */
            $primary = $dayRecords->first(fn (Attendance $a) => ! $a->is_absent)
                ?? $dayRecords->first();

            $checkIn = $primary?->check_in;
            $checkOut = $primary?->check_out;
            $lateMinutes = (int) ($primary?->late_minutes ?? 0);
            $workedHours = (float) ($primary?->worked_hours ?? 0);
            $source = $primary?->source;
            $markedAbsent = (bool) ($primary?->is_absent ?? false);

            if ($markedAbsent || (! $checkIn && $dayEnded)) {
                $status = 'absent';
                $stats['absent']++;
            } elseif (! $checkIn) {
                $status = 'not_arrived';
            } elseif ($checkIn && ! $checkOut) {
                $status = 'present';
                $stats['present']++;
                if ($lateMinutes > 0) {
                    $stats['late']++;
                }
            } else {
                $status = 'completed';
                $stats['completed']++;
                if ($lateMinutes > 0) {
                    $stats['late']++;
                }
            }

            $board[] = [
                'employee_id' => $employee->id,
                'matricule' => $employee->matricule,
                'full_name' => $employee->full_name,
                'department' => $employee->department?->name,
                'has_fingerprint' => ! empty($employee->fingerprint_template),
                'has_rfid' => ! empty($employee->rfid_card_id) && (bool) $employee->rfid_card_active,
                'status' => $status,
                'check_in' => optional($checkIn)?->toIso8601String(),
                'check_out' => optional($checkOut)?->toIso8601String(),
                'worked_hours' => $workedHours,
                'late_minutes' => $lateMinutes,
                'source' => $source,
            ];
        }

        $liveFeed = $this->buildLiveFeed($today);

        return response()->json([
            'date' => $today->toDateString(),
            'work_start_time' => $workStart,
            'stats' => $stats,
            'live_feed' => $liveFeed,
            'board' => $board,
        ]);
    }

    public function punch(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'method' => ['required', 'in:rfid,fingerprint'],
            'rfid_card_id' => ['nullable', 'string', 'max:64'],
            'employee_id' => ['nullable', 'integer', 'exists:employees,id'],
            'template' => ['nullable', 'string'],
        ]);

        $method = $validated['method'];
        $employee = null;

        if ($method === 'rfid') {
            if (empty($validated['rfid_card_id'])) {
                return response()->json(['error' => 'rfid_card_id est requis pour le pointage RFID.'], 422);
            }

            $employee = Employee::query()
                ->where('rfid_card_id', $validated['rfid_card_id'])
                ->where('rfid_card_active', true)
                ->first();

            if (! $employee) {
                return response()->json(['error' => 'Carte RFID non reconnue ou inactive.'], 404);
            }
        } else {
            if (! empty($validated['employee_id'])) {
                $employee = Employee::find($validated['employee_id']);
            } elseif (! empty($validated['template'])) {
                $employee = $this->identifyByFingerprint($validated['template']);
            } else {
                return response()->json([
                    'error' => 'Pour le pointage empreinte, fournissez employee_id ou template.',
                ], 422);
            }

            if (! $employee) {
                return response()->json(['error' => 'Empreinte non reconnue. Aucun agent enrôlé ne correspond.'], 404);
            }
        }

        return $this->registerPunch($employee, $method, $request->user()?->username);
    }

    private function identifyByFingerprint(string $template): ?Employee
    {
        $employees = Employee::query()
            ->whereNotNull('fingerprint_template')
            ->where('fingerprint_template', '!=', '')
            ->get(['id', 'fingerprint_template']);

        foreach ($employees as $employee) {
            foreach (FingerprintTemplateService::decode($employee->fingerprint_template) as $stored) {
                if ($stored === $template) {
                    return $employee;
                }
            }
        }

        if ($employees->isEmpty()) {
            return null;
        }

        $gallery = [];
        foreach ($employees as $employee) {
            foreach (FingerprintTemplateService::decode($employee->fingerprint_template) as $stored) {
                $gallery[] = [
                    'id' => (int) $employee->id,
                    'template_b64' => $stored,
                ];
            }
        }

        try {
            $match = $this->bridge->match($template, $gallery);
        } catch (\Throwable) {
            return null;
        }

        $matched = (bool) ($match['matched'] ?? false);
        $employeeId = (int) ($match['empreinte_id'] ?? -1);
        $score = (int) ($match['score'] ?? 0);
        $threshold = (int) (SystemParameter::getValue('fingerprint_match_threshold', '40') ?: 40);

        if (! $matched || $employeeId <= 0 || $score < $threshold) {
            return null;
        }

        return Employee::find($employeeId);
    }

    public function me(Request $request): JsonResponse
    {
        /** @var User $user */
        $user = $request->user();
        $user->loadMissing(['employee.department', 'employee.role']);

        if (! $user->employee_id || ! $user->employee) {
            return response()->json([
                'error' => 'Aucun employé lié à ce compte utilisateur.',
            ], 404);
        }

        $employee = $user->employee;
        $today = Carbon::today();
        $monthStart = Carbon::now()->startOfMonth();
        $monthEnd = Carbon::now()->endOfMonth();

        $todayAttendance = Attendance::query()
            ->where('employee_id', $employee->id)
            ->whereDate('check_in', $today)
            ->where('is_absent', false)
            ->orderByDesc('check_in')
            ->first();

        $todayStatus = 'not_arrived';
        if ($todayAttendance) {
            $todayStatus = $todayAttendance->check_out ? 'completed' : 'present';
        } elseif (Carbon::now()->hour >= 18) {
            $todayStatus = 'absent';
        }

        $monthRecords = Attendance::query()
            ->where('employee_id', $employee->id)
            ->whereBetween('check_in', [$monthStart, $monthEnd])
            ->get();

        $presentDays = $monthRecords->where('is_absent', false)->filter(fn (Attendance $a) => $a->check_in !== null)->count();
        $lateDays = $monthRecords->where('is_absent', false)->where('late_minutes', '>', 0)->count();
        $totalHours = round((float) $monthRecords->sum('worked_hours'), 2);
        $absenceDays = $monthRecords->where('is_absent', true)->count();

        $recentAttendances = Attendance::query()
            ->where('employee_id', $employee->id)
            ->where('check_in', '>=', Carbon::today()->subDays(30)->startOfDay())
            ->orderByDesc('check_in')
            ->limit(60)
            ->get()
            ->map(fn (Attendance $a) => SpaSerializer::attendance($a))
            ->values()
            ->all();

        $leaves = Leave::query()
            ->where('employee_id', $employee->id)
            ->orderByDesc('start_date')
            ->limit(10)
            ->get()
            ->map(fn (Leave $l) => SpaSerializer::leave($l))
            ->values()
            ->all();

        $evaluations = PerformanceEvaluation::query()
            ->where('employee_id', $employee->id)
            ->orderByDesc('created_at')
            ->limit(10)
            ->get()
            ->map(fn (PerformanceEvaluation $e) => SpaSerializer::evaluation($e))
            ->values()
            ->all();

        $series = $this->buildSeries($employee->id, 14);

        $usedLeaveDays = Leave::query()
            ->where('employee_id', $employee->id)
            ->where('status', 'Approuvé')
            ->whereYear('start_date', now()->year)
            ->get()
            ->sum(function (Leave $leave) {
                if (! $leave->start_date || ! $leave->end_date) {
                    return 0;
                }

                return $leave->start_date->diffInDays($leave->end_date) + 1;
            });

        $leaveAllowance = 30;
        $remainingLeave = max(0, $leaveAllowance - (int) $usedLeaveDays);

        $lastPayroll = Payroll::query()
            ->where('employee_id', $employee->id)
            ->orderByDesc('paid_at')
            ->first();

        $contract = Contract::query()
            ->where('employee_id', $employee->id)
            ->orderByDesc('start_date')
            ->first();

        $trainings = TrainingEnrollment::query()
            ->with('training')
            ->where('employee_id', $employee->id)
            ->orderByDesc('enrolled_at')
            ->limit(6)
            ->get()
            ->map(fn (TrainingEnrollment $e) => SpaSerializer::enrollment($e))
            ->values()
            ->all();

        $skills = EmployeeSkill::query()
            ->with('skill')
            ->where('employee_id', $employee->id)
            ->orderByDesc('level')
            ->limit(8)
            ->get()
            ->map(fn (EmployeeSkill $s) => SpaSerializer::employeeSkill($s))
            ->values()
            ->all();

        $notifications = Notification::query()
            ->where('user_id', $user->id)
            ->orderByDesc('created_at')
            ->limit(6)
            ->get()
            ->map(fn (Notification $n) => SpaSerializer::notification($n))
            ->values()
            ->all();

        $unreadNotifications = Notification::query()
            ->where('user_id', $user->id)
            ->where('is_read', false)
            ->count();

        $unreadMessages = Message::query()
            ->where('recipient_user_id', $user->id)
            ->whereNull('read_at')
            ->count();

        return response()->json([
            'employee' => SpaSerializer::employee($employee),
            'today' => [
                'status' => $todayStatus,
                'check_in' => optional($todayAttendance?->check_in)?->toIso8601String(),
                'check_out' => optional($todayAttendance?->check_out)?->toIso8601String(),
                'late_minutes' => (int) ($todayAttendance?->late_minutes ?? 0),
                'worked_hours' => (float) ($todayAttendance?->worked_hours ?? 0),
            ],
            'month' => [
                'present_days' => $presentDays,
                'late_days' => $lateDays,
                'total_hours' => $totalHours,
                'absence_days' => $absenceDays,
            ],
            'leave_balance' => [
                'annual_allowance' => $leaveAllowance,
                'used_days' => (int) $usedLeaveDays,
                'remaining_days' => $remainingLeave,
            ],
            'last_payroll' => $lastPayroll ? SpaSerializer::payroll($lastPayroll) : null,
            'contract' => $contract ? SpaSerializer::contract($contract) : null,
            'trainings' => $trainings,
            'skills' => $skills,
            'notifications' => $notifications,
            'unread_notifications' => $unreadNotifications,
            'unread_messages' => $unreadMessages,
            'recent_attendances' => $recentAttendances,
            'leaves' => $leaves,
            'evaluations' => $evaluations,
            'series' => $series,
        ]);
    }

    public function teamOverview(Request $request): JsonResponse
    {
        /** @var User $user */
        $user = $request->user();
        $user->loadMissing(['employee', 'role']);

        if (! $user->employee_id) {
            return response()->json(['error' => 'Profil employé requis.'], 403);
        }

        $roleName = $user->role?->name ?? '';
        $isHrAdmin = in_array($roleName, ['SuperAdmin', 'Admin RH', 'RH'], true);

        $managedDepartments = Department::query()
            ->with('employees.role')
            ->when(! $isHrAdmin, fn ($q) => $q->where('manager_id', $user->employee_id))
            ->when($isHrAdmin, fn ($q) => $q->orderBy('name'))
            ->get();

        if ($managedDepartments->isEmpty() && $isHrAdmin) {
            $managedDepartments = Department::with('employees.role')->orderBy('name')->get();
        }

        $today = Carbon::today();
        $memberIds = $managedDepartments
            ->flatMap(fn (Department $d) => $d->employees->pluck('id'))
            ->unique()
            ->values();

        $todayAttendances = Attendance::query()
            ->whereIn('employee_id', $memberIds)
            ->whereDate('check_in', $today)
            ->get()
            ->groupBy('employee_id');

        $pendingLeaves = Leave::query()
            ->whereIn('employee_id', $memberIds)
            ->where('status', 'En attente')
            ->count();

        $departments = [];
        $stats = [
            'members' => 0,
            'present' => 0,
            'late' => 0,
            'absent' => 0,
            'pending_leaves' => $pendingLeaves,
        ];

        foreach ($managedDepartments as $department) {
            $members = [];
            foreach ($department->employees as $employee) {
                if (! in_array(strtolower(trim($employee->status)), ['actif', 'active'], true) && $employee->status !== 'Actif') {
                    continue;
                }

                $record = $todayAttendances->get($employee->id)?->first();
                $status = 'not_arrived';
                if ($record?->is_absent) {
                    $status = 'absent';
                    $stats['absent']++;
                } elseif ($record?->check_in && ! $record->check_out) {
                    $status = 'present';
                    $stats['present']++;
                    if ($record->late_minutes > 0) {
                        $stats['late']++;
                    }
                } elseif ($record?->check_out) {
                    $status = 'completed';
                    $stats['present']++;
                }

                $stats['members']++;
                $members[] = [
                    'employee' => SpaSerializer::employee($employee),
                    'today_status' => $status,
                    'check_in' => optional($record?->check_in)?->toIso8601String(),
                    'late_minutes' => (int) ($record?->late_minutes ?? 0),
                ];
            }

            if ($members !== [] || $isHrAdmin) {
                $departments[] = [
                    'department' => SpaSerializer::department($department),
                    'members' => $members,
                ];
            }
        }

        return response()->json([
            'manager' => SpaSerializer::employee($user->employee),
            'is_hr_view' => $isHrAdmin,
            'stats' => $stats,
            'departments' => $departments,
        ]);
    }

    private function registerPunch(Employee $employee, string $source, ?string $actor = null): JsonResponse
    {
        $today = Carbon::today();

        $open = Attendance::query()
            ->where('employee_id', $employee->id)
            ->whereDate('check_in', $today)
            ->whereNull('check_out')
            ->where('is_absent', false)
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

            ActivityLogger::log(
                $actor ?? 'system',
                'Sortie présence ('.$source.') employé #'.$employee->id
            );

            return response()->json([
                'action' => 'checkout',
                'message' => 'Sortie enregistrée. Bonne soirée '.$employee->full_name.' !',
                'employee' => [
                    'id' => $employee->id,
                    'full_name' => $employee->full_name,
                    'matricule' => $employee->matricule,
                ],
                'attendance' => SpaSerializer::attendance($open),
                'day_status' => 'completed',
            ]);
        }

        $closed = Attendance::query()
            ->where('employee_id', $employee->id)
            ->whereDate('check_in', $today)
            ->whereNotNull('check_out')
            ->where('is_absent', false)
            ->orderByDesc('check_in')
            ->first();

        if ($closed) {
            return response()->json([
                'error' => 'Journée déjà clôturée pour '.$employee->full_name.'. Un seul couple entrée/sortie est autorisé par jour.',
                'action' => 'blocked',
                'day_status' => 'completed',
                'attendance' => SpaSerializer::attendance($closed),
            ], 409);
        }

        $checkIn = Carbon::now();
        $lateMinutes = $this->computeLateMinutes($checkIn);

        $attendance = Attendance::create([
            'employee_id' => $employee->id,
            'check_in' => $checkIn,
            'worked_hours' => 0,
            'late_minutes' => $lateMinutes,
            'is_absent' => false,
            'source' => $source,
        ]);

        ActivityLogger::log(
            $actor ?? 'system',
            'Entrée présence ('.$source.') employé #'.$employee->id
        );

        $message = $lateMinutes > 0
            ? 'Arrivée enregistrée avec '.$lateMinutes.' min de retard.'
            : 'Arrivée enregistrée. Bonne journée '.$employee->full_name.' !';

        return response()->json([
            'action' => 'checkin',
            'message' => $message,
            'employee' => [
                'id' => $employee->id,
                'full_name' => $employee->full_name,
                'matricule' => $employee->matricule,
            ],
            'attendance' => SpaSerializer::attendance($attendance),
            'day_status' => 'present',
        ], 201);
    }

    private function buildLiveFeed(Carbon $today): array
    {
        $records = Attendance::query()
            ->with('employee')
            ->whereDate('check_in', $today)
            ->where('is_absent', false)
            ->get();

        $events = [];

        foreach ($records as $attendance) {
            if ($attendance->check_in) {
                $events[] = [
                    'employee_id' => $attendance->employee_id,
                    'employee_name' => $attendance->employee?->full_name,
                    'action' => 'checkin',
                    'at' => $attendance->check_in->toIso8601String(),
                    'source' => $attendance->source,
                    'late_minutes' => (int) $attendance->late_minutes,
                    '_ts' => $attendance->check_in->timestamp,
                ];
            }

            if ($attendance->check_out) {
                $events[] = [
                    'employee_id' => $attendance->employee_id,
                    'employee_name' => $attendance->employee?->full_name,
                    'action' => 'checkout',
                    'at' => $attendance->check_out->toIso8601String(),
                    'source' => $attendance->source,
                    'late_minutes' => (int) $attendance->late_minutes,
                    '_ts' => $attendance->check_out->timestamp,
                ];
            }
        }

        usort($events, fn ($a, $b) => $b['_ts'] <=> $a['_ts']);

        return array_map(function (array $e) {
            unset($e['_ts']);

            return $e;
        }, array_slice($events, 0, 20));
    }

    private function buildSeries(int $employeeId, int $days): array
    {
        $labels = [];
        $hours = [];
        $late = [];

        for ($i = $days - 1; $i >= 0; $i--) {
            $day = Carbon::today()->subDays($i);
            $labels[] = $day->format('d/m');

            $dayRecords = Attendance::query()
                ->where('employee_id', $employeeId)
                ->whereDate('check_in', $day)
                ->where('is_absent', false)
                ->get();

            $hours[] = round((float) $dayRecords->sum('worked_hours'), 2);
            $late[] = (int) $dayRecords->sum('late_minutes');
        }

        return [
            'labels' => $labels,
            'hours' => $hours,
            'late' => $late,
        ];
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

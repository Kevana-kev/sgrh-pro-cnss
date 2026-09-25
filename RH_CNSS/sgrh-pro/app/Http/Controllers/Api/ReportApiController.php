<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Attendance;
use App\Models\Contract;
use App\Models\Department;
use App\Models\Employee;
use App\Models\JobApplication;
use App\Models\JobOffer;
use App\Models\Leave;
use App\Models\Notification;
use App\Models\Payroll;
use App\Models\PerformanceEvaluation;
use App\Models\Training;
use App\Models\TrainingEnrollment;
use Carbon\Carbon;
use Illuminate\Http\JsonResponse;

class ReportApiController extends Controller
{
    public function stats(): JsonResponse
    {
        $payrolls = Payroll::with('employee.department')->get();

        if ($payrolls->isEmpty()) {
            return response()->json([
                'total_payroll' => 0,
                'average_salary' => 0,
                'employees_by_department' => [],
                'absence_rate' => 0,
            ]);
        }

        $attendances = Attendance::all();
        $absenceRate = $attendances->isEmpty()
            ? 0
            : round(($attendances->where('is_absent', true)->count() / $attendances->count()) * 100, 2);

        $employeesByDepartment = [];
        foreach ($payrolls->groupBy(fn ($p) => $p->employee?->department?->name ?? 'Non assigné') as $dept => $group) {
            $employeesByDepartment[$dept] = $group->pluck('employee_id')->unique()->count();
        }

        return response()->json([
            'total_payroll' => round((float) $payrolls->sum('net_salary'), 2),
            'average_salary' => round((float) $payrolls->avg('net_salary'), 2),
            'employees_by_department' => $employeesByDepartment,
            'absence_rate' => $absenceRate,
        ]);
    }

    public function accounting(): JsonResponse
    {
        $payrolls = Payroll::with('employee.department')->orderBy('paid_at')->get();

        if ($payrolls->isEmpty()) {
            return response()->json([
                'totals' => [
                    'gross_payroll' => 0,
                    'net_payroll' => 0,
                    'taxes' => 0,
                    'deductions' => 0,
                    'bonuses' => 0,
                    'overtime_hours' => 0,
                    'records' => 0,
                ],
                'monthly' => [
                    'labels' => [],
                    'gross' => [],
                    'net' => [],
                    'taxes' => [],
                    'deductions' => [],
                    'bonuses' => [],
                ],
                'department_net' => ['labels' => [], 'values' => []],
                'cost_structure' => [
                    'labels' => ['Salaires nets', 'Impôts', 'Déductions', 'Primes'],
                    'values' => [0, 0, 0, 0],
                ],
            ]);
        }

        $monthlyMap = [];
        $departmentNet = [];
        $totalGross = $totalNet = $totalTaxes = $totalDeductions = $totalBonuses = $totalOvertime = 0.0;

        foreach ($payrolls as $payroll) {
            $base = (float) $payroll->base_salary;
            $bonus = (float) $payroll->bonus;
            $overtime = (float) $payroll->overtime_hours;
            $deductions = (float) $payroll->deductions;
            $taxes = (float) $payroll->taxes;
            $net = (float) $payroll->net_salary;
            $gross = $base + $bonus + $overtime;

            $monthKey = optional($payroll->paid_at)?->format('Y-m') ?? 'unknown';
            $monthlyMap[$monthKey] ??= ['gross' => 0.0, 'net' => 0.0, 'taxes' => 0.0, 'deductions' => 0.0, 'bonuses' => 0.0];
            $monthlyMap[$monthKey]['gross'] += $gross;
            $monthlyMap[$monthKey]['net'] += $net;
            $monthlyMap[$monthKey]['taxes'] += $taxes;
            $monthlyMap[$monthKey]['deductions'] += $deductions;
            $monthlyMap[$monthKey]['bonuses'] += $bonus;

            $dept = $payroll->employee?->department?->name ?? 'Non assigné';
            $departmentNet[$dept] = ($departmentNet[$dept] ?? 0) + $net;

            $totalGross += $gross;
            $totalNet += $net;
            $totalTaxes += $taxes;
            $totalDeductions += $deductions;
            $totalBonuses += $bonus;
            $totalOvertime += $overtime;
        }

        ksort($monthlyMap);
        $labels = array_keys($monthlyMap);

        return response()->json([
            'totals' => [
                'gross_payroll' => round($totalGross, 2),
                'net_payroll' => round($totalNet, 2),
                'taxes' => round($totalTaxes, 2),
                'deductions' => round($totalDeductions, 2),
                'bonuses' => round($totalBonuses, 2),
                'overtime_hours' => round($totalOvertime, 2),
                'records' => $payrolls->count(),
            ],
            'monthly' => [
                'labels' => $labels,
                'gross' => array_map(fn ($k) => round($monthlyMap[$k]['gross'], 2), $labels),
                'net' => array_map(fn ($k) => round($monthlyMap[$k]['net'], 2), $labels),
                'taxes' => array_map(fn ($k) => round($monthlyMap[$k]['taxes'], 2), $labels),
                'deductions' => array_map(fn ($k) => round($monthlyMap[$k]['deductions'], 2), $labels),
                'bonuses' => array_map(fn ($k) => round($monthlyMap[$k]['bonuses'], 2), $labels),
            ],
            'department_net' => [
                'labels' => array_keys($departmentNet),
                'values' => array_map(fn ($v) => round($v, 2), array_values($departmentNet)),
            ],
            'cost_structure' => [
                'labels' => ['Salaires nets', 'Impôts', 'Déductions', 'Primes'],
                'values' => [round($totalNet, 2), round($totalTaxes, 2), round($totalDeductions, 2), round($totalBonuses, 2)],
            ],
        ]);
    }

    public function dashboard(): JsonResponse
    {
        $today = Carbon::today();
        $firstDayMonth = $today->copy()->startOfMonth();
        $last12 = [];
        for ($i = 11; $i >= 0; $i--) {
            $last12[] = $today->copy()->startOfMonth()->subMonths($i)->format('Y-m');
        }

        $employees = Employee::with(['department', 'payrolls'])->get();
        $active = $employees->filter(fn (Employee $e) => in_array(strtolower(trim($e->status)), ['actif', 'act', 'active'], true))->count();
        $newThisMonth = $employees->filter(fn (Employee $e) => $e->hire_date && $e->hire_date->gte($firstDayMonth))->count();

        $payrolls = Payroll::all();
        $totalPayroll = (float) $payrolls->sum('net_salary');
        $avgSalary = $payrolls->count() ? round($totalPayroll / $payrolls->count(), 2) : 0;
        $payrollByMonth = array_fill_keys($last12, 0.0);
        foreach ($payrolls as $p) {
            $mk = optional($p->paid_at)?->format('Y-m');
            if ($mk && isset($payrollByMonth[$mk])) {
                $payrollByMonth[$mk] += (float) $p->net_salary;
            }
        }

        $leaves = Leave::all();
        $leaveStatus = ['En attente' => 0, 'Approuvé' => 0, 'Rejeté' => 0];
        foreach ($leaves as $lv) {
            if (isset($leaveStatus[$lv->status])) {
                $leaveStatus[$lv->status]++;
            }
        }

        $attendances = Attendance::all();
        $totalAtt = $attendances->count();
        $absentAtt = $attendances->where('is_absent', true)->count();
        $absenceRate = $totalAtt > 0 ? round(($absentAtt / $totalAtt) * 100, 1) : 0;
        $attByMonth = array_fill_keys($last12, 0);
        $absByMonth = array_fill_keys($last12, 0);
        foreach ($attendances as $a) {
            $mk = optional($a->check_in)?->format('Y-m');
            if ($mk && isset($attByMonth[$mk])) {
                $attByMonth[$mk]++;
                if ($a->is_absent) {
                    $absByMonth[$mk]++;
                }
            }
        }

        $departments = Department::with('employees.payrolls')->orderBy('name')->get();
        $deptNames = [];
        $deptCounts = [];
        $deptPayroll = [];
        foreach ($departments as $dept) {
            $deptNames[] = $dept->name;
            $deptCounts[] = $dept->employees->count();
            $deptPayroll[] = round((float) $dept->employees->sum(fn ($e) => $e->payrolls->sum('net_salary')), 2);
        }

        $trainings = Training::all();
        $enrollments = TrainingEnrollment::all();
        $evaluations = PerformanceEvaluation::all();
        $avgScore = $evaluations->count() ? round((float) $evaluations->avg('score'), 1) : 0;
        $scoreDist = ['Excellent (9-10)' => 0, 'Bon (7-8)' => 0, 'Moyen (5-6)' => 0, 'Insuffisant (<5)' => 0];
        foreach ($evaluations as $ev) {
            $s = (float) ($ev->score ?? 0);
            if ($s >= 9) {
                $scoreDist['Excellent (9-10)']++;
            } elseif ($s >= 7) {
                $scoreDist['Bon (7-8)']++;
            } elseif ($s >= 5) {
                $scoreDist['Moyen (5-6)']++;
            } else {
                $scoreDist['Insuffisant (<5)']++;
            }
        }

        $jobOffers = JobOffer::all();
        $applications = JobApplication::all();
        $appStatus = ['Reçue' => 0, 'En cours' => 0, 'Retenu' => 0, 'Rejeté' => 0];
        foreach ($applications as $app) {
            $s = $app->status ?: 'Reçue';
            if (isset($appStatus[$s])) {
                $appStatus[$s]++;
            }
        }

        $contracts = Contract::all();
        $expiringSoon = $contracts->filter(function (Contract $c) use ($today) {
            return $c->end_date && $c->end_date->between($today, $today->copy()->addDays(60));
        })->count();
        $contractTypes = [];
        foreach ($contracts as $c) {
            $t = $c->contract_type ?: 'Autre';
            $contractTypes[$t] = ($contractTypes[$t] ?? 0) + 1;
        }

        return response()->json([
            'employees' => [
                'total' => $employees->count(),
                'active' => $active,
                'new_this_month' => $newThisMonth,
                'gender' => ['N/A' => $employees->count()],
            ],
            'payroll' => [
                'total' => round($totalPayroll, 2),
                'average' => $avgSalary,
                'by_month' => [
                    'labels' => $last12,
                    'values' => array_map(fn ($m) => round($payrollByMonth[$m], 2), $last12),
                ],
            ],
            'leaves' => [
                'status' => $leaveStatus,
                'total' => $leaves->count(),
            ],
            'attendance' => [
                'total' => $totalAtt,
                'absences' => $absentAtt,
                'absence_rate' => $absenceRate,
                'by_month' => [
                    'labels' => $last12,
                    'present' => array_map(fn ($m) => $attByMonth[$m] - $absByMonth[$m], $last12),
                    'absent' => array_map(fn ($m) => $absByMonth[$m], $last12),
                ],
            ],
            'departments' => [
                'names' => $deptNames,
                'counts' => $deptCounts,
                'payroll' => $deptPayroll,
            ],
            'training' => [
                'total' => $trainings->count(),
                'completed' => $enrollments->where('status', 'Terminé')->count(),
                'in_progress' => $enrollments->where('status', 'En cours')->count(),
                'enrollments' => $enrollments->count(),
            ],
            'performance' => [
                'average_score' => $avgScore,
                'total_evaluations' => $evaluations->count(),
                'score_distribution' => $scoreDist,
            ],
            'recruitment' => [
                'open_offers' => $jobOffers->where('status', 'ouvert')->count() + $jobOffers->where('status', 'Ouverte')->count(),
                'total_applications' => $applications->count(),
                'application_status' => $appStatus,
            ],
            'contracts' => [
                'total' => $contracts->count(),
                'expiring_soon' => $expiringSoon,
                'by_type' => $contractTypes,
            ],
            'notifications' => [
                'unread' => Notification::query()->where('is_read', false)->count(),
            ],
        ]);
    }
}

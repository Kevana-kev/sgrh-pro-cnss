<?php

namespace App\Http\Controllers;

use App\Models\Attendance;
use App\Models\Department;
use App\Models\Employee;
use App\Models\Leave;
use App\Models\RemunerationElement;
use App\Services\ActivityLogger;
use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\View\View;
use Symfony\Component\HttpFoundation\StreamedResponse;

class ReportController extends Controller
{
    public function index(Request $request): View
    {
        $filters = $this->resolveFilters($request);
        $summary = $this->buildSummary($filters);

        return view('reports.index', [
            'filters' => $filters,
            'summary' => $summary,
            'departments' => Department::query()->orderBy('name')->get(),
            'employees' => Employee::query()->orderBy('last_name')->orderBy('first_name')->get(),
        ]);
    }

    public function export(Request $request): StreamedResponse
    {
        $filters = $this->resolveFilters($request);
        $summary = $this->buildSummary($filters);

        ActivityLogger::log(
            Auth::user()?->username,
            'Export rapport RH '.$filters['date_from'].' → '.$filters['date_to']
        );

        $filename = 'rapport-rh-'.now()->format('Ymd-His').'.csv';

        return response()->streamDownload(function () use ($summary, $filters) {
            $handle = fopen('php://output', 'w');
            fwrite($handle, "\xEF\xBB\xBF");

            fputcsv($handle, ['Rapport RH SGRH Pro'], ';');
            fputcsv($handle, ['Du', $filters['date_from'], 'Au', $filters['date_to']], ';');
            fputcsv($handle, [], ';');

            fputcsv($handle, ['Indicateur', 'Valeur'], ';');
            fputcsv($handle, ['Effectif actif', $summary['employees_active']], ';');
            fputcsv($handle, ['Pointages', $summary['attendances_count']], ';');
            fputcsv($handle, ['Heures travaillées', $summary['worked_hours_total']], ';');
            fputcsv($handle, ['Minutes de retard', $summary['late_minutes_total']], ';');
            fputcsv($handle, ['Congés (période)', $summary['leaves_count']], ';');
            fputcsv($handle, ['Congés en attente', $summary['leaves_pending']], ';');
            fputcsv($handle, ['Total rémunération indicative', $summary['remuneration_total']], ';');

            fputcsv($handle, [], ';');
            fputcsv($handle, ['Par département', 'Effectif'], ';');
            foreach ($summary['by_department'] as $row) {
                fputcsv($handle, [$row['name'], $row['count']], ';');
            }

            fclose($handle);
        }, $filename, [
            'Content-Type' => 'text/csv; charset=UTF-8',
        ]);
    }

    /**
     * @return array{date_from: string, date_to: string, department_id: ?int, employee_id: ?int}
     */
    private function resolveFilters(Request $request): array
    {
        $dateFrom = $request->input('date_from', now()->startOfMonth()->toDateString());
        $dateTo = $request->input('date_to', now()->toDateString());

        return [
            'date_from' => Carbon::parse($dateFrom)->toDateString(),
            'date_to' => Carbon::parse($dateTo)->toDateString(),
            'department_id' => $request->filled('department_id') ? $request->integer('department_id') : null,
            'employee_id' => $request->filled('employee_id') ? $request->integer('employee_id') : null,
        ];
    }

    /**
     * @param  array{date_from: string, date_to: string, department_id: ?int, employee_id: ?int}  $filters
     * @return array<string, mixed>
     */
    private function buildSummary(array $filters): array
    {
        $employeesQuery = Employee::query()->where('status', 'Actif');
        if ($filters['department_id']) {
            $employeesQuery->where('department_id', $filters['department_id']);
        }
        if ($filters['employee_id']) {
            $employeesQuery->where('id', $filters['employee_id']);
        }
        $employeeIds = $employeesQuery->pluck('id');

        $attendances = Attendance::query()
            ->whereIn('employee_id', $employeeIds)
            ->whereDate('check_in', '>=', $filters['date_from'])
            ->whereDate('check_in', '<=', $filters['date_to'])
            ->get();

        $leaves = Leave::query()
            ->whereIn('employee_id', $employeeIds)
            ->whereDate('start_date', '<=', $filters['date_to'])
            ->whereDate('end_date', '>=', $filters['date_from'])
            ->get();

        $remunerations = RemunerationElement::query()
            ->whereIn('employee_id', $employeeIds)
            ->whereBetween('period', [
                Carbon::parse($filters['date_from'])->format('Y-m'),
                Carbon::parse($filters['date_to'])->format('Y-m'),
            ])
            ->get();

        $byDepartment = Department::query()
            ->withCount(['employees' => function ($q) use ($filters) {
                $q->where('status', 'Actif');
                if ($filters['employee_id']) {
                    $q->where('id', $filters['employee_id']);
                }
            }])
            ->orderBy('name')
            ->get()
            ->map(fn (Department $d) => [
                'name' => $d->name,
                'count' => $d->employees_count,
            ])
            ->all();

        return [
            'employees_active' => $employeeIds->count(),
            'attendances_count' => $attendances->count(),
            'worked_hours_total' => round((float) $attendances->sum('worked_hours'), 2),
            'late_minutes_total' => (int) $attendances->sum('late_minutes'),
            'leaves_count' => $leaves->count(),
            'leaves_pending' => $leaves->where('status', 'En attente')->count(),
            'remuneration_total' => round((float) $remunerations->sum('total_indicative'), 2),
            'by_department' => $byDepartment,
        ];
    }
}

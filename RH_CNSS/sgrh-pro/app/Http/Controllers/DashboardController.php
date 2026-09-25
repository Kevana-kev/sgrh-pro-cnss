<?php

namespace App\Http\Controllers;

use App\Models\ActivityLog;
use App\Models\Attendance;
use App\Models\Employee;
use App\Models\Leave;
use App\Models\RemunerationElement;
use Carbon\Carbon;
use Illuminate\View\View;

class DashboardController extends Controller
{
    public function index(): View
    {
        $today = Carbon::today();

        $employeesCount = Employee::query()->where('status', 'Actif')->count();
        $attendancesToday = Attendance::query()
            ->whereDate('check_in', $today)
            ->count();
        $pendingLeaves = Leave::query()
            ->where('status', 'En attente')
            ->count();
        $remunerationDrafts = RemunerationElement::query()
            ->where('status', 'Brouillon')
            ->count();

        $recentLogs = ActivityLog::query()
            ->orderByDesc('id')
            ->limit(10)
            ->get();

        $chartLabels = [];
        $chartData = [];

        for ($i = 6; $i >= 0; $i--) {
            $day = $today->copy()->subDays($i);
            $chartLabels[] = $day->translatedFormat('D d/m');
            $chartData[] = Attendance::query()
                ->whereDate('check_in', $day)
                ->count();
        }

        return view('dashboard', [
            'employeesCount' => $employeesCount,
            'attendancesToday' => $attendancesToday,
            'pendingLeaves' => $pendingLeaves,
            'remunerationDrafts' => $remunerationDrafts,
            'recentLogs' => $recentLogs,
            'chartLabels' => $chartLabels,
            'chartData' => $chartData,
        ]);
    }
}

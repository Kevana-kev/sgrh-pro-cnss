<?php

namespace App\Http\Controllers;

use App\Models\Attendance;
use App\Models\Employee;
use App\Models\SystemParameter;
use App\Services\ActivityLogger;
use Carbon\Carbon;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\View\View;

class AttendanceController extends Controller
{
    public function index(Request $request): View
    {
        $query = Attendance::query()->with('employee');

        if ($request->filled('employee_id')) {
            $query->where('employee_id', $request->integer('employee_id'));
        }

        if ($request->filled('date_from')) {
            $query->whereDate('check_in', '>=', $request->date('date_from'));
        }

        if ($request->filled('date_to')) {
            $query->whereDate('check_in', '<=', $request->date('date_to'));
        }

        if ($request->filled('source')) {
            $query->where('source', $request->string('source')->toString());
        }

        $attendances = $query->orderByDesc('check_in')->paginate(25)->withQueryString();

        return view('attendances.index', [
            'attendances' => $attendances,
            'employees' => Employee::query()->orderBy('last_name')->orderBy('first_name')->get(),
        ]);
    }

    public function create(): View
    {
        return view('attendances.create', [
            'employees' => Employee::query()
                ->where('status', 'Actif')
                ->orderBy('last_name')
                ->orderBy('first_name')
                ->get(),
        ]);
    }

    public function store(Request $request): RedirectResponse
    {
        $validated = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
            'check_in' => ['required', 'date'],
            'check_out' => ['nullable', 'date', 'after:check_in'],
            'is_absent' => ['sometimes', 'boolean'],
            'source' => ['nullable', 'string', 'max:20'],
        ], [
            'employee_id.required' => 'L\'employé est obligatoire.',
            'check_in.required' => 'L\'heure d\'entrée est obligatoire.',
            'check_out.after' => 'La sortie doit être postérieure à l\'entrée.',
        ]);

        $checkIn = Carbon::parse($validated['check_in']);
        $checkOut = isset($validated['check_out']) ? Carbon::parse($validated['check_out']) : null;
        $workedHours = 0.0;

        if ($checkOut) {
            $workedHours = round(max(($checkOut->getTimestamp() - $checkIn->getTimestamp()) / 3600, 0), 2);
        }

        $attendance = Attendance::create([
            'employee_id' => $validated['employee_id'],
            'check_in' => $checkIn,
            'check_out' => $checkOut,
            'worked_hours' => $workedHours,
            'late_minutes' => $this->computeLateMinutes($checkIn),
            'is_absent' => $request->boolean('is_absent'),
            'source' => $validated['source'] ?? 'manual',
        ]);

        ActivityLogger::log(
            Auth::user()?->username,
            'Création pointage #'.$attendance->id.' (employé #'.$attendance->employee_id.')'
        );

        return redirect()->route('attendances.index')
            ->with('success', 'Pointage enregistré avec succès.');
    }

    public function checkout(Request $request, Attendance $attendance): RedirectResponse
    {
        if ($attendance->check_out) {
            return redirect()->back()
                ->with('error', 'Ce pointage est déjà clôturé.');
        }

        $validated = $request->validate([
            'check_out' => ['nullable', 'date', 'after:'.$attendance->check_in->toDateTimeString()],
        ], [
            'check_out.after' => 'La sortie doit être postérieure à l\'entrée.',
        ]);

        $checkOut = isset($validated['check_out'])
            ? Carbon::parse($validated['check_out'])
            : Carbon::now();

        $attendance->check_out = $checkOut;
        $attendance->worked_hours = round(
            max(($checkOut->getTimestamp() - $attendance->check_in->getTimestamp()) / 3600, 0),
            2
        );
        $attendance->save();

        ActivityLogger::log(
            Auth::user()?->username,
            'Sortie pointage #'.$attendance->id
        );

        return redirect()->back()
            ->with('success', 'Sortie enregistrée ('.$attendance->worked_hours.' h).');
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

<?php

namespace App\Http\Controllers;

use App\Models\Employee;
use App\Models\Leave;
use App\Services\ActivityLogger;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\View\View;

class LeaveController extends Controller
{
    public function index(Request $request): View
    {
        $query = Leave::query()->with('employee');

        if ($request->filled('status')) {
            $query->where('status', $request->string('status')->toString());
        }

        if ($request->filled('employee_id')) {
            $query->where('employee_id', $request->integer('employee_id'));
        }

        $leaves = $query->orderByDesc('start_date')->paginate(20)->withQueryString();

        return view('leaves.index', [
            'leaves' => $leaves,
            'employees' => Employee::query()->orderBy('last_name')->orderBy('first_name')->get(),
        ]);
    }

    public function create(): View
    {
        return view('leaves.create', [
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
            'start_date' => ['required', 'date'],
            'end_date' => ['required', 'date', 'after_or_equal:start_date'],
            'reason' => ['required', 'string', 'max:255'],
        ], [
            'employee_id.required' => 'L\'employé est obligatoire.',
            'start_date.required' => 'La date de début est obligatoire.',
            'end_date.required' => 'La date de fin est obligatoire.',
            'end_date.after_or_equal' => 'La date de fin doit être postérieure ou égale au début.',
            'reason.required' => 'Le motif est obligatoire.',
        ]);

        $leave = Leave::create([
            ...$validated,
            'status' => 'En attente',
        ]);

        ActivityLogger::log(
            Auth::user()?->username,
            'Demande de congé #'.$leave->id.' créée'
        );

        return redirect()->route('leaves.index')
            ->with('success', 'Demande de congé enregistrée.');
    }

    public function decide(Request $request, Leave $leave): RedirectResponse
    {
        if ($leave->status !== 'En attente') {
            return redirect()->back()
                ->with('error', 'Cette demande a déjà été traitée.');
        }

        $validated = $request->validate([
            'decision' => ['required', 'in:approve,reject'],
            'decision_comment' => ['nullable', 'string', 'max:500'],
        ], [
            'decision.required' => 'La décision est obligatoire.',
            'decision.in' => 'Décision invalide.',
        ]);

        $leave->status = $validated['decision'] === 'approve' ? 'Approuvé' : 'Rejeté';
        $leave->decision_comment = $validated['decision_comment'] ?? null;
        $leave->save();

        ActivityLogger::log(
            Auth::user()?->username,
            'Décision congé #'.$leave->id.' : '.$leave->status
        );

        return redirect()->back()
            ->with('success', 'Décision enregistrée : '.$leave->status.'.');
    }
}

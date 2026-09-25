<?php

namespace App\Http\Controllers;

use App\Models\Employee;
use App\Models\PerformanceEvaluation;
use App\Services\ActivityLogger;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\View\View;

class EvaluationController extends Controller
{
    public function index(Request $request): View
    {
        $query = PerformanceEvaluation::query()->with(['employee', 'evaluator']);

        if ($request->filled('employee_id')) {
            $query->where('employee_id', $request->integer('employee_id'));
        }

        if ($request->filled('period')) {
            $query->where('period', $request->string('period')->toString());
        }

        if ($request->filled('status')) {
            $query->where('status', $request->string('status')->toString());
        }

        $evaluations = $query->orderByDesc('id')->paginate(20)->withQueryString();

        return view('evaluations.index', [
            'evaluations' => $evaluations,
            'employees' => Employee::query()->orderBy('last_name')->orderBy('first_name')->get(),
        ]);
    }

    public function create(): View
    {
        $employees = Employee::query()
            ->where('status', 'Actif')
            ->orderBy('last_name')
            ->orderBy('first_name')
            ->get();

        return view('evaluations.create', compact('employees'));
    }

    public function store(Request $request): RedirectResponse
    {
        $validated = $this->validatedData($request);
        $evaluation = PerformanceEvaluation::create($validated);

        ActivityLogger::log(
            Auth::user()?->username,
            'Création évaluation #'.$evaluation->id
        );

        return redirect()->route('evaluations.index')
            ->with('success', 'Évaluation créée avec succès.');
    }

    public function show(PerformanceEvaluation $evaluation): View
    {
        $evaluation->load(['employee', 'evaluator']);

        return view('evaluations.show', compact('evaluation'));
    }

    public function edit(PerformanceEvaluation $evaluation): View
    {
        $employees = Employee::query()
            ->orderBy('last_name')
            ->orderBy('first_name')
            ->get();

        return view('evaluations.edit', compact('evaluation', 'employees'));
    }

    public function update(Request $request, PerformanceEvaluation $evaluation): RedirectResponse
    {
        $validated = $this->validatedData($request);
        $evaluation->update($validated);

        ActivityLogger::log(
            Auth::user()?->username,
            'Modification évaluation #'.$evaluation->id
        );

        return redirect()->route('evaluations.index')
            ->with('success', 'Évaluation mise à jour avec succès.');
    }

    public function destroy(PerformanceEvaluation $evaluation): RedirectResponse
    {
        $id = $evaluation->id;
        $evaluation->delete();

        ActivityLogger::log(
            Auth::user()?->username,
            'Suppression évaluation #'.$id
        );

        return redirect()->route('evaluations.index')
            ->with('success', 'Évaluation supprimée.');
    }

    /**
     * @return array<string, mixed>
     */
    private function validatedData(Request $request): array
    {
        $validated = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
            'evaluator_id' => ['nullable', 'exists:employees,id'],
            'period' => ['required', 'string', 'max:40'],
            'score' => ['required', 'integer', 'min:0', 'max:100'],
            'strengths' => ['nullable', 'string'],
            'improvements' => ['nullable', 'string'],
            'comments' => ['nullable', 'string'],
            'status' => ['nullable', 'string', 'max:40'],
        ], [
            'employee_id.required' => 'L\'employé est obligatoire.',
            'period.required' => 'La période est obligatoire.',
            'score.required' => 'La note est obligatoire.',
            'score.max' => 'La note ne peut pas dépasser 100.',
        ]);

        $validated['status'] = $validated['status'] ?? 'Brouillon';

        return $validated;
    }
}

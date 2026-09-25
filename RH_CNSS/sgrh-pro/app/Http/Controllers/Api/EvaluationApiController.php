<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\PerformanceEvaluation;
use App\Services\ActivityLogger;
use App\Support\SpaSerializer;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class EvaluationApiController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $user = $request->user();
        $role = $user->role?->name;

        if ($user->hasPermission('Voir performances') || $user->hasPermission('Gérer évaluations')
            || in_array($role, ['SuperAdmin', 'Admin RH', 'RH', 'Administrateur'], true)) {
            $evals = PerformanceEvaluation::query()->with(['employee', 'evaluator'])->orderByDesc('created_at')->get();
        } else {
            $evals = $user->employee_id
                ? PerformanceEvaluation::query()->with(['employee', 'evaluator'])->where('employee_id', $user->employee_id)->get()
                : collect();
        }

        return response()->json($evals->map(fn (PerformanceEvaluation $e) => SpaSerializer::evaluation($e))->values());
    }

    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
            'evaluator_id' => ['nullable', 'exists:employees,id'],
            'period' => ['required', 'string', 'max:40'],
            'score' => ['nullable', 'numeric'],
            'objectives' => ['nullable', 'string'],
            'comments' => ['nullable', 'string'],
            'status' => ['nullable', 'string', 'max:40'],
        ]);

        $ev = PerformanceEvaluation::create([
            'employee_id' => $data['employee_id'],
            'evaluator_id' => $data['evaluator_id'] ?? null,
            'period' => $data['period'],
            'score' => $data['score'] ?? 0,
            'objectives' => $data['objectives'] ?? null,
            'comments' => $data['comments'] ?? null,
            'status' => $data['status'] ?? 'en cours',
        ]);

        ActivityLogger::log($request->user()?->username, 'Évaluation créée employé #'.$ev->employee_id);

        return response()->json(SpaSerializer::evaluation($ev->fresh(['employee', 'evaluator'])), 201);
    }

    public function show(int $evalId): JsonResponse
    {
        $ev = PerformanceEvaluation::with(['employee', 'evaluator'])->findOrFail($evalId);

        return response()->json(SpaSerializer::evaluation($ev));
    }

    public function update(Request $request, int $evalId): JsonResponse
    {
        $ev = PerformanceEvaluation::findOrFail($evalId);

        $data = $request->validate([
            'period' => ['sometimes', 'string', 'max:40'],
            'score' => ['nullable', 'numeric'],
            'objectives' => ['nullable', 'string'],
            'comments' => ['nullable', 'string'],
            'status' => ['sometimes', 'string', 'max:40'],
        ]);

        $ev->fill($data)->save();

        return response()->json(SpaSerializer::evaluation($ev->fresh(['employee', 'evaluator'])));
    }

    public function destroy(int $evalId): JsonResponse
    {
        PerformanceEvaluation::findOrFail($evalId)->delete();

        return response()->json(['message' => 'Évaluation supprimée']);
    }

    public function stats(): JsonResponse
    {
        $scored = PerformanceEvaluation::query()->whereNotNull('score')->get();
        if ($scored->isEmpty()) {
            return response()->json(['avg_score' => 0, 'total' => 0, 'by_status' => []]);
        }

        $byStatus = [];
        foreach (PerformanceEvaluation::all() as $e) {
            $byStatus[$e->status] = ($byStatus[$e->status] ?? 0) + 1;
        }

        return response()->json([
            'avg_score' => round($scored->avg('score'), 2),
            'total' => PerformanceEvaluation::count(),
            'by_status' => $byStatus,
        ]);
    }
}

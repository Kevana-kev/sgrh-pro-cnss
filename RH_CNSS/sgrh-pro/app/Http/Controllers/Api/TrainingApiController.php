<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Employee;
use App\Models\EmployeeSkill;
use App\Models\Skill;
use App\Models\Training;
use App\Models\TrainingEnrollment;
use App\Services\ActivityLogger;
use App\Support\SpaSerializer;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class TrainingApiController extends Controller
{
    public function index(): JsonResponse
    {
        $trainings = Training::query()->with('enrollments')->orderByDesc('start_date')->get();

        return response()->json($trainings->map(fn (Training $t) => SpaSerializer::training($t))->values());
    }

    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'title' => ['required', 'string', 'max:200'],
            'description' => ['nullable', 'string'],
            'trainer' => ['nullable', 'string', 'max:120'],
            'start_date' => ['required', 'date'],
            'end_date' => ['required', 'date'],
            'max_participants' => ['nullable', 'integer', 'min:1'],
            'status' => ['nullable', 'string', 'max:30'],
        ]);

        $training = Training::create([
            'title' => $data['title'],
            'description' => $data['description'] ?? null,
            'trainer' => $data['trainer'] ?? null,
            'start_date' => $data['start_date'],
            'end_date' => $data['end_date'],
            'max_participants' => $data['max_participants'] ?? 20,
            'status' => $data['status'] ?? 'planifié',
        ]);

        ActivityLogger::log($request->user()?->username, 'Formation créée: '.$training->title);

        return response()->json(SpaSerializer::training($training), 201);
    }

    public function show(int $trainingId): JsonResponse
    {
        $training = Training::with(['enrollments.employee'])->findOrFail($trainingId);
        $result = SpaSerializer::training($training);
        $result['enrollments'] = $training->enrollments
            ->map(fn (TrainingEnrollment $e) => SpaSerializer::enrollment($e))
            ->values()
            ->all();

        return response()->json($result);
    }

    public function update(Request $request, int $trainingId): JsonResponse
    {
        $training = Training::findOrFail($trainingId);

        $data = $request->validate([
            'title' => ['sometimes', 'string', 'max:200'],
            'description' => ['nullable', 'string'],
            'trainer' => ['nullable', 'string', 'max:120'],
            'start_date' => ['sometimes', 'date'],
            'end_date' => ['sometimes', 'date'],
            'max_participants' => ['sometimes', 'integer', 'min:1'],
            'status' => ['sometimes', 'string', 'max:30'],
        ]);

        $training->fill($data)->save();

        return response()->json(SpaSerializer::training($training->fresh('enrollments')));
    }

    public function destroy(int $trainingId): JsonResponse
    {
        Training::findOrFail($trainingId)->delete();

        return response()->json(['message' => 'Formation supprimée']);
    }

    public function enroll(Request $request, int $trainingId): JsonResponse
    {
        Training::findOrFail($trainingId);

        $data = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
        ]);

        $existing = TrainingEnrollment::query()
            ->where('training_id', $trainingId)
            ->where('employee_id', $data['employee_id'])
            ->first();

        if ($existing) {
            return response()->json(['error' => 'Déjà inscrit'], 409);
        }

        $enrollment = TrainingEnrollment::create([
            'training_id' => $trainingId,
            'employee_id' => $data['employee_id'],
            'status' => 'inscrit',
            'enrolled_at' => now(),
        ]);

        return response()->json(SpaSerializer::enrollment($enrollment->fresh('employee')), 201);
    }

    public function updateEnrollment(Request $request, int $enrollmentId): JsonResponse
    {
        $enrollment = TrainingEnrollment::findOrFail($enrollmentId);

        $data = $request->validate([
            'status' => ['sometimes', 'string', 'max:30'],
            'score' => ['nullable', 'numeric'],
        ]);

        $enrollment->fill($data)->save();

        return response()->json(SpaSerializer::enrollment($enrollment->fresh('employee')));
    }

    public function listSkills(): JsonResponse
    {
        $skills = Skill::query()->orderBy('category')->orderBy('name')->get();

        return response()->json($skills->map(fn (Skill $s) => [
            'id' => $s->id,
            'name' => $s->name,
            'category' => $s->category,
        ])->values());
    }

    public function createSkill(Request $request): JsonResponse
    {
        $data = $request->validate([
            'name' => ['required', 'string', 'max:120', 'unique:skills,name'],
            'category' => ['nullable', 'string', 'max:80'],
        ]);

        $skill = Skill::create($data);

        return response()->json([
            'id' => $skill->id,
            'name' => $skill->name,
            'category' => $skill->category,
        ], 201);
    }

    public function employeeSkills(int $employeeId): JsonResponse
    {
        Employee::findOrFail($employeeId);
        $skills = EmployeeSkill::query()->with('skill')->where('employee_id', $employeeId)->get();

        return response()->json($skills->map(fn (EmployeeSkill $es) => SpaSerializer::employeeSkill($es))->values());
    }

    public function addEmployeeSkill(Request $request, int $employeeId): JsonResponse
    {
        Employee::findOrFail($employeeId);

        $data = $request->validate([
            'skill_id' => ['required', 'exists:skills,id'],
            'level' => ['nullable', 'integer', 'min:1', 'max:10'],
            'certified_at' => ['nullable', 'date'],
        ]);

        $es = EmployeeSkill::query()
            ->where('employee_id', $employeeId)
            ->where('skill_id', $data['skill_id'])
            ->first();

        if ($es) {
            $es->level = $data['level'] ?? $es->level;
            $es->save();
        } else {
            $es = EmployeeSkill::create([
                'employee_id' => $employeeId,
                'skill_id' => $data['skill_id'],
                'level' => $data['level'] ?? 1,
                'certified_at' => $data['certified_at'] ?? null,
            ]);
        }

        return response()->json(SpaSerializer::employeeSkill($es->fresh('skill')), 201);
    }
}

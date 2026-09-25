<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\JobApplication;
use App\Models\JobOffer;
use App\Services\ActivityLogger;
use App\Support\SpaSerializer;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class RecruitmentApiController extends Controller
{
    public function listOffers(): JsonResponse
    {
        $offers = JobOffer::query()->with(['department', 'applications'])->orderByDesc('created_at')->get();

        return response()->json($offers->map(fn (JobOffer $o) => SpaSerializer::jobOffer($o))->values());
    }

    public function createOffer(Request $request): JsonResponse
    {
        $data = $request->validate([
            'title' => ['required', 'string', 'max:200'],
            'department_id' => ['nullable', 'exists:departments,id'],
            'description' => ['nullable', 'string'],
            'requirements' => ['nullable', 'string'],
            'status' => ['nullable', 'string', 'max:30'],
        ]);

        $offer = JobOffer::create([
            'title' => $data['title'],
            'department_id' => $data['department_id'] ?? null,
            'description' => $data['description'] ?? null,
            'requirements' => $data['requirements'] ?? null,
            'status' => $data['status'] ?? 'ouvert',
        ]);

        ActivityLogger::log($request->user()?->username, 'Offre recrutement créée: '.$offer->title);

        return response()->json(SpaSerializer::jobOffer($offer->fresh(['department', 'applications'])), 201);
    }

    public function showOffer(int $offerId): JsonResponse
    {
        $offer = JobOffer::with(['department', 'applications'])->findOrFail($offerId);
        $result = SpaSerializer::jobOffer($offer);
        $result['applications'] = $offer->applications
            ->map(fn (JobApplication $a) => SpaSerializer::jobApplication($a))
            ->values()
            ->all();

        return response()->json($result);
    }

    public function updateOffer(Request $request, int $offerId): JsonResponse
    {
        $offer = JobOffer::findOrFail($offerId);

        $data = $request->validate([
            'title' => ['sometimes', 'string', 'max:200'],
            'description' => ['nullable', 'string'],
            'requirements' => ['nullable', 'string'],
            'status' => ['sometimes', 'string', 'max:30'],
            'department_id' => ['nullable', 'exists:departments,id'],
        ]);

        $offer->fill($data)->save();

        return response()->json(SpaSerializer::jobOffer($offer->fresh(['department', 'applications'])));
    }

    public function destroyOffer(int $offerId): JsonResponse
    {
        JobOffer::findOrFail($offerId)->delete();

        return response()->json(['message' => 'Offre supprimée']);
    }

    public function listApplications(): JsonResponse
    {
        $apps = JobApplication::query()->with('jobOffer')->orderByDesc('created_at')->get();

        return response()->json($apps->map(fn (JobApplication $a) => SpaSerializer::jobApplication($a))->values());
    }

    public function submitApplication(Request $request, int $offerId): JsonResponse
    {
        JobOffer::findOrFail($offerId);

        $data = $request->validate([
            'applicant_name' => ['required', 'string', 'max:150'],
            'applicant_email' => ['required', 'email', 'max:120'],
            'cv_path' => ['nullable', 'string', 'max:255'],
            'status' => ['nullable', 'string', 'max:30'],
            'notes' => ['nullable', 'string'],
            'interview_date' => ['nullable', 'date'],
        ]);

        $app = JobApplication::create([
            'job_offer_id' => $offerId,
            'applicant_name' => $data['applicant_name'],
            'applicant_email' => $data['applicant_email'],
            'cv_path' => $data['cv_path'] ?? null,
            'status' => $data['status'] ?? 'reçu',
            'notes' => $data['notes'] ?? null,
            'interview_date' => $data['interview_date'] ?? null,
        ]);

        ActivityLogger::log($request->user()?->username, 'Candidature reçue: '.$app->applicant_name);

        return response()->json(SpaSerializer::jobApplication($app->fresh('jobOffer')), 201);
    }

    public function updateApplication(Request $request, int $appId): JsonResponse
    {
        $app = JobApplication::findOrFail($appId);

        $data = $request->validate([
            'status' => ['sometimes', 'string', 'max:30'],
            'notes' => ['nullable', 'string'],
            'cv_path' => ['nullable', 'string', 'max:255'],
            'interview_date' => ['nullable', 'date'],
        ]);

        $app->fill($data)->save();

        return response()->json(SpaSerializer::jobApplication($app->fresh('jobOffer')));
    }

    public function destroyApplication(int $appId): JsonResponse
    {
        JobApplication::findOrFail($appId)->delete();

        return response()->json(['message' => 'Candidature supprimée']);
    }

    public function stats(): JsonResponse
    {
        $byStatus = [];
        foreach (JobApplication::all() as $a) {
            $byStatus[$a->status] = ($byStatus[$a->status] ?? 0) + 1;
        }

        return response()->json([
            'total_offers' => JobOffer::count(),
            'open_offers' => JobOffer::query()->where('status', 'ouvert')->count(),
            'total_applications' => JobApplication::count(),
            'by_status' => $byStatus,
        ]);
    }
}

<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Contract;
use App\Services\ActivityLogger;
use App\Support\SpaSerializer;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class ContractApiController extends Controller
{
    public function index(): JsonResponse
    {
        $contracts = Contract::query()->orderByDesc('id')->get();

        return response()->json($contracts->map(fn (Contract $c) => SpaSerializer::contract($c))->values());
    }

    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
            'contract_type' => ['required', 'string', 'max:20'],
            'start_date' => ['required', 'date'],
            'end_date' => ['nullable', 'date'],
            'contractual_salary' => ['required', 'numeric', 'min:0'],
            'document_path' => ['nullable', 'string', 'max:255'],
        ]);

        $contract = Contract::create($data);
        ActivityLogger::log($request->user()?->username, 'Création contrat #'.$contract->id);

        return response()->json(SpaSerializer::contract($contract), 201);
    }

    public function update(Request $request, int $contractId): JsonResponse
    {
        $contract = Contract::findOrFail($contractId);

        $data = $request->validate([
            'contract_type' => ['sometimes', 'string', 'max:20'],
            'start_date' => ['sometimes', 'date'],
            'end_date' => ['nullable', 'date'],
            'contractual_salary' => ['sometimes', 'numeric', 'min:0'],
            'document_path' => ['nullable', 'string', 'max:255'],
        ]);

        $contract->fill($data)->save();
        ActivityLogger::log($request->user()?->username, 'Modification contrat #'.$contract->id);

        return response()->json(SpaSerializer::contract($contract));
    }

    public function destroy(Request $request, int $contractId): JsonResponse
    {
        Contract::findOrFail($contractId)->delete();
        ActivityLogger::log($request->user()?->username, 'Suppression contrat #'.$contractId);

        return response()->json(['message' => 'Contrat supprimé']);
    }
}

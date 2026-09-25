<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Payroll;
use App\Services\ActivityLogger;
use App\Support\SpaSerializer;
use Carbon\Carbon;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class PayrollApiController extends Controller
{
    public function index(): JsonResponse
    {
        $payrolls = Payroll::query()->with('employee')->orderByDesc('paid_at')->get();

        return response()->json($payrolls->map(fn (Payroll $p) => SpaSerializer::payroll($p))->values());
    }

    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
            'base_salary' => ['required', 'numeric'],
            'bonus' => ['nullable', 'numeric'],
            'overtime_hours' => ['nullable', 'numeric'],
            'deductions' => ['nullable', 'numeric'],
            'taxes' => ['nullable', 'numeric'],
            'paid_at' => ['nullable', 'date'],
            'payroll_month' => ['nullable', 'string'],
        ]);

        $bonus = (float) ($data['bonus'] ?? 0);
        $overtime = (float) ($data['overtime_hours'] ?? 0);
        $deductions = (float) ($data['deductions'] ?? 0);
        $taxes = (float) ($data['taxes'] ?? 0);
        $base = (float) $data['base_salary'];
        $net = round($base + $bonus + $overtime - $deductions - $taxes, 2);

        $paidAt = isset($data['paid_at'])
            ? Carbon::parse($data['paid_at'])
            : (isset($data['payroll_month']) && preg_match('/^\d{4}-\d{2}$/', $data['payroll_month'])
                ? Carbon::createFromFormat('Y-m', $data['payroll_month'])->endOfMonth()
                : now());

        $payroll = Payroll::create([
            'employee_id' => $data['employee_id'],
            'base_salary' => $base,
            'bonus' => $bonus,
            'overtime_hours' => $overtime,
            'deductions' => $deductions,
            'taxes' => $taxes,
            'net_salary' => $net,
            'paid_at' => $paidAt,
        ]);

        ActivityLogger::log($request->user()?->username, 'Création paie #'.$payroll->id);

        return response()->json(SpaSerializer::payroll($payroll->fresh('employee')), 201);
    }

    public function update(Request $request, int $payrollId): JsonResponse
    {
        $payroll = Payroll::with('employee')->findOrFail($payrollId);

        $data = $request->validate([
            'base_salary' => ['sometimes', 'numeric'],
            'bonus' => ['sometimes', 'numeric'],
            'overtime_hours' => ['sometimes', 'numeric'],
            'deductions' => ['sometimes', 'numeric'],
            'taxes' => ['sometimes', 'numeric'],
            'paid_at' => ['sometimes', 'date'],
        ]);

        $payroll->fill($data);
        $payroll->net_salary = round(
            (float) $payroll->base_salary
            + (float) $payroll->bonus
            + (float) $payroll->overtime_hours
            - (float) $payroll->deductions
            - (float) $payroll->taxes,
            2
        );
        $payroll->save();

        ActivityLogger::log($request->user()?->username, 'Modification paie #'.$payroll->id);

        return response()->json(SpaSerializer::payroll($payroll));
    }

    public function destroy(Request $request, int $payrollId): JsonResponse
    {
        Payroll::findOrFail($payrollId)->delete();
        ActivityLogger::log($request->user()?->username, 'Suppression paie #'.$payrollId);

        return response()->json(['message' => 'Paie supprimée']);
    }

    public function payslip(Request $request, int $payrollId): JsonResponse
    {
        $payroll = Payroll::with('employee')->findOrFail($payrollId);

        ActivityLogger::log($request->user()?->username, 'Export fiche de paie #'.$payrollId);

        return response()->json([
            'message' => 'PDF généré',
            'file_path' => null,
            'payroll' => SpaSerializer::payroll($payroll),
        ]);
    }
}

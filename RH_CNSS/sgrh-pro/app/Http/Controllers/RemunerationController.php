<?php

namespace App\Http\Controllers;

use App\Models\Employee;
use App\Models\RemunerationElement;
use App\Services\ActivityLogger;
use Barryvdh\DomPDF\Facade\Pdf;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\View\View;
use Symfony\Component\HttpFoundation\StreamedResponse;

class RemunerationController extends Controller
{
    private const DISCLAIMER = 'État pour la finance, pas un bulletin de paie.';

    public function index(Request $request): View
    {
        $query = RemunerationElement::query()->with('employee');

        if ($request->filled('employee_id')) {
            $query->where('employee_id', $request->integer('employee_id'));
        }

        if ($request->filled('period')) {
            $query->where('period', $request->string('period')->toString());
        }

        if ($request->filled('status')) {
            $query->where('status', $request->string('status')->toString());
        }

        $remunerations = $query->orderByDesc('period')->paginate(20)->withQueryString();

        return view('remunerations.index', [
            'remunerations' => $remunerations,
            'employees' => Employee::query()->orderBy('last_name')->orderBy('first_name')->get(),
            'disclaimer' => self::DISCLAIMER,
        ]);
    }

    public function create(): View
    {
        return view('remunerations.create', [
            'employees' => Employee::query()
                ->where('status', 'Actif')
                ->orderBy('last_name')
                ->orderBy('first_name')
                ->get(),
            'disclaimer' => self::DISCLAIMER,
        ]);
    }

    public function store(Request $request): RedirectResponse
    {
        $data = $this->preparePayload($request);
        $remuneration = RemunerationElement::create($data);

        ActivityLogger::log(
            Auth::user()?->username,
            'Création rémunération #'.$remuneration->id
        );

        return redirect()->route('remunerations.index')
            ->with('success', 'Élément de rémunération créé. '.self::DISCLAIMER);
    }

    public function show(RemunerationElement $remuneration): View
    {
        $remuneration->load('employee');

        return view('remunerations.show', [
            'remuneration' => $remuneration,
            'disclaimer' => self::DISCLAIMER,
        ]);
    }

    public function edit(RemunerationElement $remuneration): View
    {
        return view('remunerations.edit', [
            'remuneration' => $remuneration,
            'employees' => Employee::query()->orderBy('last_name')->orderBy('first_name')->get(),
            'disclaimer' => self::DISCLAIMER,
        ]);
    }

    public function update(Request $request, RemunerationElement $remuneration): RedirectResponse
    {
        $data = $this->preparePayload($request, $remuneration);
        $remuneration->update($data);

        ActivityLogger::log(
            Auth::user()?->username,
            'Modification rémunération #'.$remuneration->id
        );

        return redirect()->route('remunerations.index')
            ->with('success', 'Rémunération mise à jour. '.self::DISCLAIMER);
    }

    public function destroy(RemunerationElement $remuneration): RedirectResponse
    {
        $id = $remuneration->id;
        $remuneration->delete();

        ActivityLogger::log(
            Auth::user()?->username,
            'Suppression rémunération #'.$id
        );

        return redirect()->route('remunerations.index')
            ->with('success', 'Rémunération supprimée.');
    }

    public function exportPdf(RemunerationElement $remuneration)
    {
        $remuneration->load('employee');

        $pdf = Pdf::loadView('remunerations.pdf', [
            'remuneration' => $remuneration,
            'disclaimer' => self::DISCLAIMER,
        ]);

        ActivityLogger::log(
            Auth::user()?->username,
            'Export PDF rémunération #'.$remuneration->id
        );

        $filename = 'remuneration-'.$remuneration->id.'-'.$remuneration->period.'.pdf';

        return $pdf->download($filename);
    }

    public function exportCsv(Request $request): StreamedResponse
    {
        $query = RemunerationElement::query()->with('employee');

        if ($request->filled('period')) {
            $query->where('period', $request->string('period')->toString());
        }

        if ($request->filled('status')) {
            $query->where('status', $request->string('status')->toString());
        }

        $rows = $query->orderBy('period')->get();

        ActivityLogger::log(
            Auth::user()?->username,
            'Export CSV rémunérations ('.$rows->count().' lignes)'
        );

        $filename = 'remunerations-'.now()->format('Ymd-His').'.csv';

        return response()->streamDownload(function () use ($rows) {
            $handle = fopen('php://output', 'w');
            fwrite($handle, "\xEF\xBB\xBF");
            fputcsv($handle, [
                'ID',
                'Employé',
                'Période',
                'Salaire de base',
                'Prime',
                'Heures supp.',
                'Montant HS',
                'Retenues',
                'Total indicatif',
                'Statut',
                'Notes',
                'Avertissement',
            ], ';');

            foreach ($rows as $row) {
                fputcsv($handle, [
                    $row->id,
                    $row->employee?->full_name,
                    $row->period,
                    $row->base_salary,
                    $row->bonus,
                    $row->overtime_hours,
                    $row->overtime_amount,
                    $row->deductions,
                    $row->total_indicative,
                    $row->status,
                    $row->notes,
                    self::DISCLAIMER,
                ], ';');
            }

            fclose($handle);
        }, $filename, [
            'Content-Type' => 'text/csv; charset=UTF-8',
        ]);
    }

    /**
     * @return array<string, mixed>
     */
    private function preparePayload(Request $request, ?RemunerationElement $existing = null): array
    {
        $validated = $request->validate([
            'employee_id' => ['required', 'exists:employees,id'],
            'period' => ['required', 'string', 'max:20'],
            'base_salary' => ['required', 'numeric', 'min:0'],
            'bonus' => ['nullable', 'numeric', 'min:0'],
            'overtime_hours' => ['nullable', 'numeric', 'min:0'],
            'overtime_amount' => ['nullable', 'numeric', 'min:0'],
            'deductions' => ['nullable', 'numeric', 'min:0'],
            'status' => ['nullable', 'string', 'max:40'],
            'notes' => ['nullable', 'string'],
        ], [
            'employee_id.required' => 'L\'employé est obligatoire.',
            'period.required' => 'La période est obligatoire.',
            'base_salary.required' => 'Le salaire de base est obligatoire.',
        ]);

        $base = (float) $validated['base_salary'];
        $bonus = (float) ($validated['bonus'] ?? 0);
        $overtimeHours = (float) ($validated['overtime_hours'] ?? 0);
        $deductions = (float) ($validated['deductions'] ?? 0);

        if ($request->filled('overtime_amount')) {
            $overtimeAmount = (float) $validated['overtime_amount'];
        } else {
            $overtimeAmount = round($overtimeHours * ($base / 160), 2);
        }

        $notes = $validated['notes'] ?? null;
        if ($notes === null || $notes === '') {
            $notes = self::DISCLAIMER;
        } elseif (! str_contains($notes, 'pas un bulletin')) {
            $notes .= ' — '.self::DISCLAIMER;
        }

        return [
            'employee_id' => $validated['employee_id'],
            'period' => $validated['period'],
            'base_salary' => $base,
            'bonus' => $bonus,
            'overtime_hours' => $overtimeHours,
            'overtime_amount' => $overtimeAmount,
            'deductions' => $deductions,
            'total_indicative' => RemunerationElement::computeTotal($base, $bonus, $overtimeAmount, $deductions),
            'status' => $validated['status'] ?? ($existing?->status ?? 'Brouillon'),
            'notes' => $notes,
        ];
    }
}

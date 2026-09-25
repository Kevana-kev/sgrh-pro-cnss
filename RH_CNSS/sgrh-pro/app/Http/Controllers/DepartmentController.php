<?php

namespace App\Http\Controllers;

use App\Models\Department;
use App\Models\Employee;
use App\Services\ActivityLogger;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Validation\Rule;
use Illuminate\View\View;

class DepartmentController extends Controller
{
    public function index(): View
    {
        $departments = Department::query()
            ->with('manager')
            ->withCount('employees')
            ->orderBy('name')
            ->paginate(20);

        return view('departments.index', compact('departments'));
    }

    public function create(): View
    {
        return view('departments.create', [
            'employees' => Employee::query()->orderBy('last_name')->orderBy('first_name')->get(),
        ]);
    }

    public function store(Request $request): RedirectResponse
    {
        $validated = $this->validatedData($request);
        $validated['budget'] = $validated['budget'] ?? 0;

        $department = Department::create($validated);

        ActivityLogger::log(
            Auth::user()?->username,
            'Création département #'.$department->id.' ('.$department->name.')'
        );

        return redirect()->route('departments.index')
            ->with('success', 'Département créé avec succès.');
    }

    public function edit(Department $department): View
    {
        return view('departments.edit', [
            'department' => $department,
            'employees' => Employee::query()->orderBy('last_name')->orderBy('first_name')->get(),
        ]);
    }

    public function update(Request $request, Department $department): RedirectResponse
    {
        $validated = $this->validatedData($request, $department);
        $department->update($validated);

        ActivityLogger::log(
            Auth::user()?->username,
            'Modification département #'.$department->id.' ('.$department->name.')'
        );

        return redirect()->route('departments.index')
            ->with('success', 'Département mis à jour avec succès.');
    }

    public function destroy(Department $department): RedirectResponse
    {
        if ($department->employees()->exists()) {
            return redirect()->back()
                ->with('error', 'Impossible de supprimer un département qui contient des employés.');
        }

        $label = $department->name;
        $department->delete();

        ActivityLogger::log(
            Auth::user()?->username,
            'Suppression département '.$label
        );

        return redirect()->route('departments.index')
            ->with('success', 'Département supprimé avec succès.');
    }

    /**
     * @return array<string, mixed>
     */
    private function validatedData(Request $request, ?Department $department = null): array
    {
        return $request->validate([
            'name' => [
                'required',
                'string',
                'max:120',
                Rule::unique('departments', 'name')->ignore($department?->id),
            ],
            'budget' => ['nullable', 'numeric', 'min:0'],
            'manager_id' => ['nullable', 'exists:employees,id'],
        ], [
            'name.required' => 'Le nom du département est obligatoire.',
            'name.unique' => 'Ce département existe déjà.',
            'budget.numeric' => 'Le budget doit être un nombre.',
            'manager_id.exists' => 'Le responsable sélectionné est invalide.',
        ]);
    }
}

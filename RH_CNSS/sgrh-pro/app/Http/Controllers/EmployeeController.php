<?php

namespace App\Http\Controllers;

use App\Models\Department;
use App\Models\Employee;
use App\Models\Role;
use App\Services\ActivityLogger;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Storage;
use Illuminate\Validation\Rule;
use Illuminate\View\View;

class EmployeeController extends Controller
{
    public function index(Request $request): View
    {
        $query = Employee::query()->with(['department', 'role']);

        if ($search = $request->string('q')->trim()->toString()) {
            $query->where(function ($q) use ($search) {
                $q->where('first_name', 'like', "%{$search}%")
                    ->orWhere('last_name', 'like', "%{$search}%")
                    ->orWhere('matricule', 'like', "%{$search}%")
                    ->orWhere('email', 'like', "%{$search}%");
            });
        }

        if ($request->filled('department_id')) {
            $query->where('department_id', $request->integer('department_id'));
        }

        if ($request->filled('status')) {
            $query->where('status', $request->string('status')->toString());
        }

        $employees = $query->orderBy('last_name')->orderBy('first_name')->paginate(20)->withQueryString();

        return view('employees.index', [
            'employees' => $employees,
            'departments' => Department::query()->orderBy('name')->get(),
        ]);
    }

    public function create(): View
    {
        return view('employees.create', [
            'departments' => Department::query()->orderBy('name')->get(),
            'roles' => Role::query()->orderBy('name')->get(),
        ]);
    }

    public function store(Request $request): RedirectResponse
    {
        $validated = $this->validatedData($request);
        unset($validated['photo']);
        $validated['photo_path'] = $this->storePhoto($request);

        $employee = Employee::create($validated);

        ActivityLogger::log(
            Auth::user()?->username,
            'Création employé #'.$employee->id.' ('.$employee->full_name.')'
        );

        return redirect()->route('employees.index')
            ->with('success', 'Employé créé avec succès.');
    }

    public function show(Employee $employee): View
    {
        $employee->load(['department', 'role', 'user']);

        return view('employees.show', compact('employee'));
    }

    public function edit(Employee $employee): View
    {
        return view('employees.edit', [
            'employee' => $employee,
            'departments' => Department::query()->orderBy('name')->get(),
            'roles' => Role::query()->orderBy('name')->get(),
        ]);
    }

    public function update(Request $request, Employee $employee): RedirectResponse
    {
        $validated = $this->validatedData($request, $employee);
        unset($validated['photo']);

        if ($request->hasFile('photo')) {
            if ($employee->photo_path) {
                Storage::disk('public')->delete($employee->photo_path);
            }
            $validated['photo_path'] = $this->storePhoto($request);
        }

        $employee->update($validated);

        ActivityLogger::log(
            Auth::user()?->username,
            'Modification employé #'.$employee->id.' ('.$employee->full_name.')'
        );

        return redirect()->route('employees.index')
            ->with('success', 'Employé mis à jour avec succès.');
    }

    public function destroy(Employee $employee): RedirectResponse
    {
        if ($employee->photo_path) {
            Storage::disk('public')->delete($employee->photo_path);
        }

        $label = $employee->full_name;
        $employee->delete();

        ActivityLogger::log(
            Auth::user()?->username,
            'Suppression employé '.$label
        );

        return redirect()->route('employees.index')
            ->with('success', 'Employé supprimé avec succès.');
    }

    /**
     * @return array<string, mixed>
     */
    private function validatedData(Request $request, ?Employee $employee = null): array
    {
        return $request->validate([
            'first_name' => ['required', 'string', 'max:100'],
            'last_name' => ['required', 'string', 'max:100'],
            'matricule' => [
                'nullable',
                'string',
                'max:40',
                Rule::unique('employees', 'matricule')->ignore($employee?->id),
            ],
            'email' => [
                'required',
                'email',
                'max:120',
                Rule::unique('employees', 'email')->ignore($employee?->id),
            ],
            'phone' => ['required', 'string', 'max:30'],
            'address' => ['required', 'string', 'max:255'],
            'hire_date' => ['required', 'date'],
            'status' => ['required', 'string', 'max:30'],
            'department_id' => ['nullable', 'exists:departments,id'],
            'role_id' => ['required', 'exists:roles,id'],
            'photo' => ['nullable', 'image', 'max:2048'],
        ], [
            'first_name.required' => 'Le prénom est obligatoire.',
            'last_name.required' => 'Le nom est obligatoire.',
            'email.required' => 'L\'e-mail est obligatoire.',
            'email.unique' => 'Cet e-mail est déjà utilisé.',
            'phone.required' => 'Le téléphone est obligatoire.',
            'address.required' => 'L\'adresse est obligatoire.',
            'hire_date.required' => 'La date d\'embauche est obligatoire.',
            'role_id.required' => 'Le rôle est obligatoire.',
            'photo.image' => 'Le fichier photo doit être une image.',
        ]);
    }

    private function storePhoto(Request $request): ?string
    {
        if (! $request->hasFile('photo')) {
            return null;
        }

        return $request->file('photo')->store('employees', 'public');
    }
}

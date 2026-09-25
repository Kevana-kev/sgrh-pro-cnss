@php
    $r = $remuneration ?? null;
@endphp
<div class="form-grid">
    <div class="form-group form-group--full">
        <label for="employee_id">Employé</label>
        <select id="employee_id" name="employee_id" class="form-control @error('employee_id') is-invalid @enderror" required>
            <option value="">— Sélectionner —</option>
            @foreach($employees as $employee)
                <option value="{{ $employee->id }}" @selected(old('employee_id', $r?->employee_id) == $employee->id)>{{ $employee->full_name }}</option>
            @endforeach
        </select>
        @error('employee_id')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="period">Période</label>
        <input type="text" id="period" name="period" class="form-control @error('period') is-invalid @enderror" value="{{ old('period', $r?->period) }}" placeholder="YYYY-MM" required>
        @error('period')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="status">Statut</label>
        <select id="status" name="status" class="form-control @error('status') is-invalid @enderror">
            @foreach(['Brouillon', 'Validé', 'Exporté'] as $st)
                <option value="{{ $st }}" @selected(old('status', $r?->status ?? 'Brouillon') === $st)>{{ $st }}</option>
            @endforeach
        </select>
        @error('status')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="base_salary">Salaire de base</label>
        <input type="number" step="0.01" min="0" id="base_salary" name="base_salary" class="form-control @error('base_salary') is-invalid @enderror" value="{{ old('base_salary', $r?->base_salary) }}" required>
        @error('base_salary')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="bonus">Prime</label>
        <input type="number" step="0.01" min="0" id="bonus" name="bonus" class="form-control @error('bonus') is-invalid @enderror" value="{{ old('bonus', $r?->bonus ?? 0) }}">
        @error('bonus')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="overtime_hours">Heures supplémentaires</label>
        <input type="number" step="0.01" min="0" id="overtime_hours" name="overtime_hours" class="form-control @error('overtime_hours') is-invalid @enderror" value="{{ old('overtime_hours', $r?->overtime_hours ?? 0) }}">
        @error('overtime_hours')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="overtime_amount">Montant heures supp.</label>
        <input type="number" step="0.01" min="0" id="overtime_amount" name="overtime_amount" class="form-control @error('overtime_amount') is-invalid @enderror" value="{{ old('overtime_amount', $r?->overtime_amount) }}">
        <span class="form-hint">Laisser vide pour calcul automatique.</span>
        @error('overtime_amount')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="deductions">Retenues</label>
        <input type="number" step="0.01" min="0" id="deductions" name="deductions" class="form-control @error('deductions') is-invalid @enderror" value="{{ old('deductions', $r?->deductions ?? 0) }}">
        @error('deductions')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group form-group--full">
        <label for="notes">Notes</label>
        <textarea id="notes" name="notes" class="form-control @error('notes') is-invalid @enderror">{{ old('notes', $r?->notes) }}</textarea>
        @error('notes')<div class="form-error">{{ $message }}</div>@enderror
    </div>
</div>

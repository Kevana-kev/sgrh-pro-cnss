@php
    $ev = $evaluation ?? null;
@endphp
<div class="form-grid">
    <div class="form-group">
        <label for="employee_id">Employé évalué</label>
        <select id="employee_id" name="employee_id" class="form-control @error('employee_id') is-invalid @enderror" required>
            <option value="">— Sélectionner —</option>
            @foreach($employees as $employee)
                <option value="{{ $employee->id }}" @selected(old('employee_id', $ev?->employee_id) == $employee->id)>{{ $employee->full_name }}</option>
            @endforeach
        </select>
        @error('employee_id')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="evaluator_id">Évaluateur</label>
        <select id="evaluator_id" name="evaluator_id" class="form-control @error('evaluator_id') is-invalid @enderror">
            <option value="">— Aucun —</option>
            @foreach($employees as $employee)
                <option value="{{ $employee->id }}" @selected(old('evaluator_id', $ev?->evaluator_id) == $employee->id)>{{ $employee->full_name }}</option>
            @endforeach
        </select>
        @error('evaluator_id')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="period">Période</label>
        <input type="text" id="period" name="period" class="form-control @error('period') is-invalid @enderror" value="{{ old('period', $ev?->period) }}" required>
        @error('period')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="score">Note (0–100)</label>
        <input type="number" min="0" max="100" id="score" name="score" class="form-control @error('score') is-invalid @enderror" value="{{ old('score', $ev?->score) }}" required>
        @error('score')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group">
        <label for="status">Statut</label>
        <select id="status" name="status" class="form-control @error('status') is-invalid @enderror">
            @foreach(['Brouillon', 'Finalisé'] as $st)
                <option value="{{ $st }}" @selected(old('status', $ev?->status ?? 'Brouillon') === $st)>{{ $st }}</option>
            @endforeach
        </select>
        @error('status')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group form-group--full">
        <label for="strengths">Points forts</label>
        <textarea id="strengths" name="strengths" class="form-control @error('strengths') is-invalid @enderror">{{ old('strengths', $ev?->strengths) }}</textarea>
        @error('strengths')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group form-group--full">
        <label for="improvements">Axes d'amélioration</label>
        <textarea id="improvements" name="improvements" class="form-control @error('improvements') is-invalid @enderror">{{ old('improvements', $ev?->improvements) }}</textarea>
        @error('improvements')<div class="form-error">{{ $message }}</div>@enderror
    </div>
    <div class="form-group form-group--full">
        <label for="comments">Commentaires</label>
        <textarea id="comments" name="comments" class="form-control @error('comments') is-invalid @enderror">{{ old('comments', $ev?->comments) }}</textarea>
        @error('comments')<div class="form-error">{{ $message }}</div>@enderror
    </div>
</div>

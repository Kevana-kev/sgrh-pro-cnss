<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\HasOne;

class Employee extends Model
{
    protected $fillable = [
        'first_name', 'last_name', 'matricule', 'photo_path', 'email', 'phone',
        'address', 'hire_date', 'status', 'department_id', 'role_id',
        'fingerprint_template', 'rfid_card_id', 'rfid_card_active',
    ];

    protected function casts(): array
    {
        return [
            'hire_date' => 'date',
            'rfid_card_active' => 'boolean',
        ];
    }

    public function getFullNameAttribute(): string
    {
        return trim($this->first_name.' '.$this->last_name);
    }

    public function department(): BelongsTo
    {
        return $this->belongsTo(Department::class);
    }

    public function role(): BelongsTo
    {
        return $this->belongsTo(Role::class);
    }

    public function user(): HasOne
    {
        return $this->hasOne(User::class);
    }

    public function attendances(): HasMany
    {
        return $this->hasMany(Attendance::class);
    }

    public function leaves(): HasMany
    {
        return $this->hasMany(Leave::class);
    }

    public function remunerationElements(): HasMany
    {
        return $this->hasMany(RemunerationElement::class);
    }

    public function evaluations(): HasMany
    {
        return $this->hasMany(PerformanceEvaluation::class);
    }

    public function contracts(): HasMany
    {
        return $this->hasMany(Contract::class);
    }

    public function payrolls(): HasMany
    {
        return $this->hasMany(Payroll::class);
    }

    public function medicalLeaves(): HasMany
    {
        return $this->hasMany(MedicalLeave::class);
    }

    public function employeeSkills(): HasMany
    {
        return $this->hasMany(EmployeeSkill::class);
    }
}

<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class RemunerationElement extends Model
{
    protected $fillable = [
        'employee_id', 'period', 'base_salary', 'bonus', 'overtime_hours',
        'overtime_amount', 'deductions', 'total_indicative', 'status', 'notes',
    ];

    protected function casts(): array
    {
        return [
            'base_salary' => 'decimal:2',
            'bonus' => 'decimal:2',
            'overtime_hours' => 'decimal:2',
            'overtime_amount' => 'decimal:2',
            'deductions' => 'decimal:2',
            'total_indicative' => 'decimal:2',
        ];
    }

    public function employee(): BelongsTo
    {
        return $this->belongsTo(Employee::class);
    }

    public static function computeTotal(
        float $base,
        float $bonus,
        float $overtimeAmount,
        float $deductions
    ): float {
        return round($base + $bonus + $overtimeAmount - $deductions, 2);
    }
}

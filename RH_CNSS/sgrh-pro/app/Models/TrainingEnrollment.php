<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class TrainingEnrollment extends Model
{
    protected $fillable = [
        'training_id', 'employee_id', 'status', 'score', 'enrolled_at',
    ];

    protected function casts(): array
    {
        return [
            'score' => 'decimal:2',
            'enrolled_at' => 'datetime',
        ];
    }

    public function training(): BelongsTo
    {
        return $this->belongsTo(Training::class);
    }

    public function employee(): BelongsTo
    {
        return $this->belongsTo(Employee::class);
    }
}

<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class JobApplication extends Model
{
    protected $fillable = [
        'job_offer_id', 'applicant_name', 'applicant_email', 'cv_path',
        'status', 'interview_date', 'notes',
    ];

    protected function casts(): array
    {
        return [
            'interview_date' => 'datetime',
        ];
    }

    public function jobOffer(): BelongsTo
    {
        return $this->belongsTo(JobOffer::class);
    }
}

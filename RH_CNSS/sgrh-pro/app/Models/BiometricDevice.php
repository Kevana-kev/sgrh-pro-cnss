<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class BiometricDevice extends Model
{
    protected $fillable = ['name', 'device_type', 'location', 'is_active', 'last_seen'];

    protected function casts(): array
    {
        return [
            'is_active' => 'boolean',
            'last_seen' => 'datetime',
        ];
    }
}

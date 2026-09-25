<?php

namespace App\Services;

use App\Models\ActivityLog;

class ActivityLogger
{
    public static function log(?string $username, string $action): void
    {
        ActivityLog::create([
            'username' => $username ?: 'system',
            'action' => $action,
        ]);
    }
}

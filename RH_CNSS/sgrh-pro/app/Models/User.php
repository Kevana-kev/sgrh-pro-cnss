<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, Notifiable;

    protected $fillable = [
        'username',
        'password',
        'must_change_password',
        'employee_id',
        'role_id',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];

    protected function casts(): array
    {
        return [
            'password' => 'hashed',
            'must_change_password' => 'boolean',
        ];
    }

    public function role(): BelongsTo
    {
        return $this->belongsTo(Role::class);
    }

    public function employee(): BelongsTo
    {
        return $this->belongsTo(Employee::class);
    }

    public function sentMessages(): HasMany
    {
        return $this->hasMany(Message::class, 'sender_user_id');
    }

    public function receivedMessages(): HasMany
    {
        return $this->hasMany(Message::class, 'recipient_user_id');
    }

    public function hasPermission(string $name): bool
    {
        $this->loadMissing('role.permissions');

        if (! $this->role) {
            return false;
        }

        if ($this->role->name === 'SuperAdmin') {
            return true;
        }

        return $this->role->hasPermission($name);
    }

    public function hasAnyRole(array $roles): bool
    {
        return $this->role && in_array($this->role->name, $roles, true);
    }

    public function permissionNames(): array
    {
        $this->loadMissing('role.permissions');

        if (! $this->role) {
            return [];
        }

        if ($this->role->name === 'SuperAdmin') {
            return \App\Models\Permission::query()->orderBy('name')->pluck('name')->all();
        }

        return $this->role->permissions->pluck('name')->values()->all();
    }
}

<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Skill extends Model
{
    protected $fillable = ['name', 'category'];

    public function employeeSkills(): HasMany
    {
        return $this->hasMany(EmployeeSkill::class);
    }
}

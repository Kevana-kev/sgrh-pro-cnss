<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('roles', function (Blueprint $table) {
            $table->id();
            $table->string('name', 80)->unique();
            $table->timestamps();
        });

        Schema::create('permissions', function (Blueprint $table) {
            $table->id();
            $table->string('name', 120)->unique();
            $table->timestamps();
        });

        Schema::create('role_permission', function (Blueprint $table) {
            $table->foreignId('role_id')->constrained('roles')->cascadeOnDelete();
            $table->foreignId('permission_id')->constrained('permissions')->cascadeOnDelete();
            $table->primary(['role_id', 'permission_id']);
        });

        Schema::create('departments', function (Blueprint $table) {
            $table->id();
            $table->string('name', 120)->unique();
            $table->decimal('budget', 14, 2)->default(0);
            $table->unsignedBigInteger('manager_id')->nullable();
            $table->timestamps();
        });

        Schema::create('employees', function (Blueprint $table) {
            $table->id();
            $table->string('first_name', 100);
            $table->string('last_name', 100);
            $table->string('matricule', 40)->nullable()->unique();
            $table->string('photo_path', 255)->nullable();
            $table->string('email', 120)->unique();
            $table->string('phone', 30);
            $table->string('address', 255);
            $table->date('hire_date');
            $table->string('status', 30)->default('Actif');
            $table->foreignId('department_id')->nullable()->constrained('departments')->nullOnDelete();
            $table->foreignId('role_id')->constrained('roles');
            $table->longText('fingerprint_template')->nullable();
            $table->string('rfid_card_id', 64)->nullable()->unique();
            $table->boolean('rfid_card_active')->default(true);
            $table->timestamps();
        });

        Schema::table('departments', function (Blueprint $table) {
            $table->foreign('manager_id')->references('id')->on('employees')->nullOnDelete();
        });

        Schema::create('users', function (Blueprint $table) {
            $table->id();
            $table->string('username', 80)->unique();
            $table->string('password');
            $table->boolean('must_change_password')->default(true);
            $table->foreignId('employee_id')->nullable()->constrained('employees')->nullOnDelete();
            $table->foreignId('role_id')->constrained('roles');
            $table->rememberToken();
            $table->timestamps();
        });

        Schema::create('activity_logs', function (Blueprint $table) {
            $table->id();
            $table->string('username', 80);
            $table->string('action', 255);
            $table->timestamps();
        });

        Schema::create('attendances', function (Blueprint $table) {
            $table->id();
            $table->foreignId('employee_id')->constrained('employees')->cascadeOnDelete();
            $table->dateTime('check_in');
            $table->dateTime('check_out')->nullable();
            $table->decimal('worked_hours', 8, 2)->default(0);
            $table->unsignedInteger('late_minutes')->default(0);
            $table->boolean('is_absent')->default(false);
            $table->string('source', 20)->default('manual');
            $table->timestamps();
        });

        Schema::create('leaves', function (Blueprint $table) {
            $table->id();
            $table->foreignId('employee_id')->constrained('employees')->cascadeOnDelete();
            $table->date('start_date');
            $table->date('end_date');
            $table->string('reason', 255);
            $table->string('status', 40)->default('En attente');
            $table->string('decision_comment', 500)->nullable();
            $table->timestamps();
        });

        Schema::create('holidays', function (Blueprint $table) {
            $table->id();
            $table->string('name', 120);
            $table->date('date');
            $table->timestamps();
        });

        Schema::create('biometric_devices', function (Blueprint $table) {
            $table->id();
            $table->string('name', 120);
            $table->string('device_type', 60)->default('ZK-9500');
            $table->string('location', 120)->nullable();
            $table->boolean('is_active')->default(true);
            $table->dateTime('last_seen')->nullable();
            $table->timestamps();
        });

        Schema::create('remuneration_elements', function (Blueprint $table) {
            $table->id();
            $table->foreignId('employee_id')->constrained('employees')->cascadeOnDelete();
            $table->string('period', 20);
            $table->decimal('base_salary', 14, 2);
            $table->decimal('bonus', 14, 2)->default(0);
            $table->decimal('overtime_hours', 8, 2)->default(0);
            $table->decimal('overtime_amount', 14, 2)->default(0);
            $table->decimal('deductions', 14, 2)->default(0);
            $table->decimal('total_indicative', 14, 2);
            $table->string('status', 40)->default('Brouillon');
            $table->text('notes')->nullable();
            $table->timestamps();
        });

        Schema::create('performance_evaluations', function (Blueprint $table) {
            $table->id();
            $table->foreignId('employee_id')->constrained('employees')->cascadeOnDelete();
            $table->foreignId('evaluator_id')->nullable()->constrained('employees')->nullOnDelete();
            $table->string('period', 40);
            $table->unsignedTinyInteger('score')->default(0);
            $table->text('strengths')->nullable();
            $table->text('improvements')->nullable();
            $table->text('comments')->nullable();
            $table->string('status', 40)->default('Brouillon');
            $table->timestamps();
        });

        Schema::create('system_parameters', function (Blueprint $table) {
            $table->id();
            $table->string('key', 100)->unique();
            $table->text('value')->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('system_parameters');
        Schema::dropIfExists('performance_evaluations');
        Schema::dropIfExists('remuneration_elements');
        Schema::dropIfExists('biometric_devices');
        Schema::dropIfExists('holidays');
        Schema::dropIfExists('leaves');
        Schema::dropIfExists('attendances');
        Schema::dropIfExists('activity_logs');
        Schema::dropIfExists('users');
        Schema::table('departments', function (Blueprint $table) {
            $table->dropForeign(['manager_id']);
        });
        Schema::dropIfExists('employees');
        Schema::dropIfExists('departments');
        Schema::dropIfExists('role_permission');
        Schema::dropIfExists('permissions');
        Schema::dropIfExists('roles');
    }
};

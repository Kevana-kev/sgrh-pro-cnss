<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        if (! Schema::hasTable('contracts')) {
            Schema::create('contracts', function (Blueprint $table) {
                $table->id();
                $table->foreignId('employee_id')->constrained('employees')->cascadeOnDelete();
                $table->string('contract_type', 20);
                $table->date('start_date');
                $table->date('end_date')->nullable();
                $table->decimal('contractual_salary', 14, 2);
                $table->string('document_path', 255)->nullable();
                $table->timestamps();
            });
        }

        if (! Schema::hasTable('messages')) {
            Schema::create('messages', function (Blueprint $table) {
                $table->id();
                $table->foreignId('sender_user_id')->constrained('users')->cascadeOnDelete();
                $table->foreignId('recipient_user_id')->constrained('users')->cascadeOnDelete();
                $table->string('subject', 160)->nullable();
                $table->string('content', 2000);
                $table->dateTime('sent_at');
                $table->dateTime('edited_at')->nullable();
                $table->dateTime('read_at')->nullable();
                $table->timestamps();
            });
        }

        if (! Schema::hasTable('trainings')) {
            Schema::create('trainings', function (Blueprint $table) {
                $table->id();
                $table->string('title', 200);
                $table->text('description')->nullable();
                $table->string('trainer', 120)->nullable();
                $table->date('start_date');
                $table->date('end_date');
                $table->unsignedInteger('max_participants')->default(20);
                $table->string('status', 30)->default('planifié');
                $table->timestamps();
            });
        }

        if (! Schema::hasTable('training_enrollments')) {
            Schema::create('training_enrollments', function (Blueprint $table) {
                $table->id();
                $table->foreignId('training_id')->constrained('trainings')->cascadeOnDelete();
                $table->foreignId('employee_id')->constrained('employees')->cascadeOnDelete();
                $table->string('status', 30)->default('inscrit');
                $table->decimal('score', 8, 2)->nullable();
                $table->dateTime('enrolled_at');
                $table->timestamps();
                $table->unique(['training_id', 'employee_id']);
            });
        }

        if (! Schema::hasTable('skills')) {
            Schema::create('skills', function (Blueprint $table) {
                $table->id();
                $table->string('name', 120)->unique();
                $table->string('category', 80)->nullable();
                $table->timestamps();
            });
        }

        if (! Schema::hasTable('employee_skills')) {
            Schema::create('employee_skills', function (Blueprint $table) {
                $table->id();
                $table->foreignId('employee_id')->constrained('employees')->cascadeOnDelete();
                $table->foreignId('skill_id')->constrained('skills')->cascadeOnDelete();
                $table->unsignedTinyInteger('level')->default(1);
                $table->date('certified_at')->nullable();
                $table->timestamps();
                $table->unique(['employee_id', 'skill_id']);
            });
        }

        if (! Schema::hasTable('medical_leaves')) {
            Schema::create('medical_leaves', function (Blueprint $table) {
                $table->id();
                $table->foreignId('employee_id')->constrained('employees')->cascadeOnDelete();
                $table->date('start_date');
                $table->date('end_date');
                $table->string('diagnosis', 255)->nullable();
                $table->string('certificate_path', 255)->nullable();
                $table->decimal('daily_allowance', 14, 2)->default(0);
                $table->string('status', 30)->default('En attente');
                $table->timestamps();
            });
        }

        if (! Schema::hasTable('notifications')) {
            Schema::create('notifications', function (Blueprint $table) {
                $table->id();
                $table->foreignId('user_id')->nullable()->constrained('users')->nullOnDelete();
                $table->string('type', 50)->default('info');
                $table->string('title', 160);
                $table->string('message', 1000);
                $table->boolean('is_read')->default(false);
                $table->timestamps();
            });
        }

        if (! Schema::hasTable('job_offers')) {
            Schema::create('job_offers', function (Blueprint $table) {
                $table->id();
                $table->string('title', 200);
                $table->foreignId('department_id')->nullable()->constrained('departments')->nullOnDelete();
                $table->text('description')->nullable();
                $table->text('requirements')->nullable();
                $table->string('status', 30)->default('ouvert');
                $table->timestamps();
            });
        }

        if (! Schema::hasTable('job_applications')) {
            Schema::create('job_applications', function (Blueprint $table) {
                $table->id();
                $table->foreignId('job_offer_id')->constrained('job_offers')->cascadeOnDelete();
                $table->string('applicant_name', 150);
                $table->string('applicant_email', 120);
                $table->string('cv_path', 255)->nullable();
                $table->string('status', 30)->default('reçu');
                $table->dateTime('interview_date')->nullable();
                $table->text('notes')->nullable();
                $table->timestamps();
            });
        }

        if (! Schema::hasTable('payrolls')) {
            Schema::create('payrolls', function (Blueprint $table) {
                $table->id();
                $table->foreignId('employee_id')->constrained('employees')->cascadeOnDelete();
                $table->decimal('base_salary', 14, 2);
                $table->decimal('bonus', 14, 2)->default(0);
                $table->decimal('overtime_hours', 8, 2)->default(0);
                $table->decimal('deductions', 14, 2)->default(0);
                $table->decimal('taxes', 14, 2)->default(0);
                $table->decimal('net_salary', 14, 2);
                $table->dateTime('paid_at');
                $table->timestamps();
            });
        }

        if (Schema::hasTable('holidays') && ! Schema::hasColumn('holidays', 'is_recurring')) {
            Schema::table('holidays', function (Blueprint $table) {
                $table->boolean('is_recurring')->default(false)->after('date');
            });
        }

        if (Schema::hasTable('system_parameters') && ! Schema::hasColumn('system_parameters', 'description')) {
            Schema::table('system_parameters', function (Blueprint $table) {
                $table->string('description', 255)->nullable()->after('value');
            });
        }

        if (Schema::hasTable('performance_evaluations') && ! Schema::hasColumn('performance_evaluations', 'objectives')) {
            Schema::table('performance_evaluations', function (Blueprint $table) {
                $table->text('objectives')->nullable()->after('score');
            });
        }
    }

    public function down(): void
    {
        Schema::dropIfExists('payrolls');
        Schema::dropIfExists('job_applications');
        Schema::dropIfExists('job_offers');
        Schema::dropIfExists('notifications');
        Schema::dropIfExists('medical_leaves');
        Schema::dropIfExists('employee_skills');
        Schema::dropIfExists('skills');
        Schema::dropIfExists('training_enrollments');
        Schema::dropIfExists('trainings');
        Schema::dropIfExists('messages');
        Schema::dropIfExists('contracts');

        if (Schema::hasTable('holidays') && Schema::hasColumn('holidays', 'is_recurring')) {
            Schema::table('holidays', function (Blueprint $table) {
                $table->dropColumn('is_recurring');
            });
        }

        if (Schema::hasTable('system_parameters') && Schema::hasColumn('system_parameters', 'description')) {
            Schema::table('system_parameters', function (Blueprint $table) {
                $table->dropColumn('description');
            });
        }

        if (Schema::hasTable('performance_evaluations') && Schema::hasColumn('performance_evaluations', 'objectives')) {
            Schema::table('performance_evaluations', function (Blueprint $table) {
                $table->dropColumn('objectives');
            });
        }
    }
};

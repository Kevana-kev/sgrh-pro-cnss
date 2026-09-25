<?php

namespace App\Support;

use App\Models\Attendance;
use App\Models\Contract;
use App\Models\Department;
use App\Models\Employee;
use App\Models\EmployeeSkill;
use App\Models\Holiday;
use App\Models\JobApplication;
use App\Models\JobOffer;
use App\Models\Leave;
use App\Models\MedicalLeave;
use App\Models\Message;
use App\Models\Notification;
use App\Models\Payroll;
use App\Models\PerformanceEvaluation;
use App\Models\Role;
use App\Models\SystemParameter;
use App\Models\Training;
use App\Models\TrainingEnrollment;
use App\Models\User;
use Illuminate\Support\Facades\Storage;

class SpaSerializer
{
    public static function photoUrl(?string $photoPath): ?string
    {
        if (! $photoPath) {
            return null;
        }

        if (str_starts_with($photoPath, 'http://') || str_starts_with($photoPath, 'https://') || str_starts_with($photoPath, '/')) {
            return $photoPath;
        }

        return Storage::disk('public')->url($photoPath);
    }

    public static function employee(Employee $employee): array
    {
        $employee->loadMissing(['department', 'role', 'user']);

        return [
            'id' => $employee->id,
            'matricule' => $employee->matricule,
            'first_name' => $employee->first_name,
            'last_name' => $employee->last_name,
            'photo_url' => self::photoUrl($employee->photo_path),
            'email' => $employee->email,
            'phone' => $employee->phone,
            'address' => $employee->address,
            'hire_date' => optional($employee->hire_date)?->format('Y-m-d'),
            'status' => $employee->status,
            'department_id' => $employee->department_id,
            'role_id' => $employee->role_id,
            'department' => $employee->department?->name,
            'role' => $employee->role?->name,
            'account_username' => $employee->user?->username,
        ];
    }

    public static function department(Department $department): array
    {
        $department->loadMissing('employees.department', 'employees.role', 'employees.user');

        return [
            'id' => $department->id,
            'name' => $department->name,
            'budget' => (float) $department->budget,
            'manager_id' => $department->manager_id,
            'employees' => $department->employees->map(fn (Employee $e) => self::employee($e))->values()->all(),
        ];
    }

    public static function role(Role $role): array
    {
        $role->loadMissing('permissions');

        return [
            'id' => $role->id,
            'name' => $role->name,
            'permissions' => $role->permissions->pluck('name')->values()->all(),
        ];
    }

    public static function payroll(Payroll $payroll): array
    {
        $payroll->loadMissing('employee');

        return [
            'id' => $payroll->id,
            'employee_id' => $payroll->employee_id,
            'employee_name' => $payroll->employee
                ? trim($payroll->employee->first_name.' '.$payroll->employee->last_name)
                : null,
            'base_salary' => (float) $payroll->base_salary,
            'bonus' => (float) $payroll->bonus,
            'overtime_hours' => (float) $payroll->overtime_hours,
            'deductions' => (float) $payroll->deductions,
            'taxes' => (float) $payroll->taxes,
            'net_salary' => (float) $payroll->net_salary,
            'payroll_month' => optional($payroll->paid_at)?->format('Y-m'),
            'paid_at' => optional($payroll->paid_at)?->toIso8601String(),
        ];
    }

    public static function attendance(Attendance $attendance): array
    {
        return [
            'id' => $attendance->id,
            'employee_id' => $attendance->employee_id,
            'check_in' => optional($attendance->check_in)?->toIso8601String(),
            'check_out' => optional($attendance->check_out)?->toIso8601String(),
            'worked_hours' => (float) $attendance->worked_hours,
            'late_minutes' => (int) $attendance->late_minutes,
            'is_absent' => (bool) $attendance->is_absent,
            'source' => $attendance->source,
        ];
    }

    public static function leave(Leave $leave): array
    {
        return [
            'id' => $leave->id,
            'employee_id' => $leave->employee_id,
            'start_date' => optional($leave->start_date)?->format('Y-m-d'),
            'end_date' => optional($leave->end_date)?->format('Y-m-d'),
            'reason' => $leave->reason,
            'status' => $leave->status,
            'decision_comment' => $leave->decision_comment,
        ];
    }

    public static function contract(Contract $contract): array
    {
        return [
            'id' => $contract->id,
            'employee_id' => $contract->employee_id,
            'contract_type' => $contract->contract_type,
            'start_date' => optional($contract->start_date)?->format('Y-m-d'),
            'end_date' => optional($contract->end_date)?->format('Y-m-d'),
            'contractual_salary' => (float) $contract->contractual_salary,
            'document_path' => $contract->document_path,
        ];
    }

    public static function message(Message $message): array
    {
        $message->loadMissing(['sender.employee', 'recipient.employee']);

        $sender = $message->sender;
        $recipient = $message->recipient;
        $senderEmployee = $sender?->employee;
        $recipientEmployee = $recipient?->employee;

        $senderName = $senderEmployee
            ? trim($senderEmployee->first_name.' '.$senderEmployee->last_name)
            : ($sender?->username ?? '-');
        $recipientName = $recipientEmployee
            ? trim($recipientEmployee->first_name.' '.$recipientEmployee->last_name)
            : ($recipient?->username ?? '-');

        return [
            'id' => $message->id,
            'sender_user_id' => $message->sender_user_id,
            'recipient_user_id' => $message->recipient_user_id,
            'sender_username' => $sender?->username,
            'recipient_username' => $recipient?->username,
            'sender_name' => $senderName,
            'recipient_name' => $recipientName,
            'subject' => $message->subject,
            'content' => $message->content,
            'sent_at' => optional($message->sent_at)?->toIso8601String(),
            'edited_at' => optional($message->edited_at)?->toIso8601String(),
            'read_at' => optional($message->read_at)?->toIso8601String(),
            'is_read' => $message->read_at !== null,
        ];
    }

    public static function account(User $user): array
    {
        $user->loadMissing(['role', 'employee']);

        return [
            'id' => $user->id,
            'username' => $user->username,
            'role_id' => $user->role_id,
            'role' => $user->role?->name,
            'must_change_password' => (bool) $user->must_change_password,
            'employee_id' => $user->employee_id,
            'employee_name' => $user->employee
                ? trim($user->employee->first_name.' '.$user->employee->last_name)
                : null,
            'matricule' => $user->employee?->matricule,
            'status' => $user->employee?->status,
        ];
    }

    public static function training(Training $training): array
    {
        $training->loadMissing('enrollments');

        return [
            'id' => $training->id,
            'title' => $training->title,
            'description' => $training->description,
            'trainer' => $training->trainer,
            'start_date' => optional($training->start_date)?->format('Y-m-d'),
            'end_date' => optional($training->end_date)?->format('Y-m-d'),
            'max_participants' => (int) $training->max_participants,
            'status' => $training->status,
            'enrolled_count' => $training->enrollments->count(),
            'created_at' => optional($training->created_at)?->toIso8601String(),
        ];
    }

    public static function enrollment(TrainingEnrollment $enrollment): array
    {
        $enrollment->loadMissing(['employee', 'training']);

        return [
            'id' => $enrollment->id,
            'training_id' => $enrollment->training_id,
            'training_title' => $enrollment->training?->title,
            'employee_id' => $enrollment->employee_id,
            'employee_name' => $enrollment->employee
                ? trim($enrollment->employee->first_name.' '.$enrollment->employee->last_name)
                : null,
            'status' => $enrollment->status,
            'score' => $enrollment->score !== null ? (float) $enrollment->score : null,
            'enrolled_at' => optional($enrollment->enrolled_at)?->toIso8601String(),
        ];
    }

    public static function employeeSkill(EmployeeSkill $es): array
    {
        $es->loadMissing('skill');

        return [
            'id' => $es->id,
            'employee_id' => $es->employee_id,
            'skill_id' => $es->skill_id,
            'skill_name' => $es->skill?->name,
            'category' => $es->skill?->category,
            'level' => (int) $es->level,
            'certified_at' => optional($es->certified_at)?->format('Y-m-d'),
        ];
    }

    public static function evaluation(PerformanceEvaluation $ev): array
    {
        $ev->loadMissing(['employee', 'evaluator']);

        return [
            'id' => $ev->id,
            'employee_id' => $ev->employee_id,
            'employee_name' => $ev->employee
                ? trim($ev->employee->first_name.' '.$ev->employee->last_name)
                : null,
            'evaluator_id' => $ev->evaluator_id,
            'evaluator_name' => $ev->evaluator
                ? trim($ev->evaluator->first_name.' '.$ev->evaluator->last_name)
                : null,
            'period' => $ev->period,
            'score' => $ev->score !== null ? (float) $ev->score : null,
            'objectives' => $ev->objectives ?? $ev->strengths,
            'comments' => $ev->comments,
            'status' => $ev->status,
            'created_at' => optional($ev->created_at)?->toIso8601String(),
        ];
    }

    public static function medicalLeave(MedicalLeave $ml): array
    {
        $ml->loadMissing('employee');

        return [
            'id' => $ml->id,
            'employee_id' => $ml->employee_id,
            'employee_name' => $ml->employee
                ? trim($ml->employee->first_name.' '.$ml->employee->last_name)
                : null,
            'start_date' => optional($ml->start_date)?->format('Y-m-d'),
            'end_date' => optional($ml->end_date)?->format('Y-m-d'),
            'diagnosis' => $ml->diagnosis,
            'certificate_path' => $ml->certificate_path,
            'daily_allowance' => (float) $ml->daily_allowance,
            'status' => $ml->status,
            'created_at' => optional($ml->created_at)?->toIso8601String(),
        ];
    }

    public static function notification(Notification $n): array
    {
        return [
            'id' => $n->id,
            'user_id' => $n->user_id,
            'type' => $n->type,
            'title' => $n->title,
            'message' => $n->message,
            'is_read' => (bool) $n->is_read,
            'created_at' => optional($n->created_at)?->toIso8601String(),
        ];
    }

    public static function jobOffer(JobOffer $o): array
    {
        $o->loadMissing(['department', 'applications']);

        return [
            'id' => $o->id,
            'title' => $o->title,
            'department_id' => $o->department_id,
            'department_name' => $o->department?->name,
            'description' => $o->description,
            'requirements' => $o->requirements,
            'status' => $o->status,
            'application_count' => $o->applications->count(),
            'created_at' => optional($o->created_at)?->toIso8601String(),
        ];
    }

    public static function jobApplication(JobApplication $a): array
    {
        $a->loadMissing('jobOffer');

        return [
            'id' => $a->id,
            'job_offer_id' => $a->job_offer_id,
            'offer_title' => $a->jobOffer?->title,
            'applicant_name' => $a->applicant_name,
            'applicant_email' => $a->applicant_email,
            'cv_path' => $a->cv_path,
            'status' => $a->status,
            'interview_date' => optional($a->interview_date)?->toIso8601String(),
            'notes' => $a->notes,
            'created_at' => optional($a->created_at)?->toIso8601String(),
        ];
    }

    public static function parameter(SystemParameter $p): array
    {
        return [
            'id' => $p->id,
            'key' => $p->key,
            'value' => $p->value,
            'description' => $p->description ?? null,
            'updated_at' => optional($p->updated_at)?->toIso8601String(),
        ];
    }

    public static function holiday(Holiday $h): array
    {
        return [
            'id' => $h->id,
            'name' => $h->name,
            'date' => optional($h->date)?->format('Y-m-d'),
            'is_recurring' => (bool) ($h->is_recurring ?? false),
            'created_at' => optional($h->created_at)?->toIso8601String(),
        ];
    }

    public static function accountHolder(?User $user): array
    {
        if (! $user) {
            return [
                'account_holder_name' => 'Utilisateur',
                'account_holder_function' => 'Fonction non définie',
            ];
        }

        $user->loadMissing(['employee.role', 'role']);

        if ($user->employee) {
            $fullName = trim(($user->employee->first_name ?? '').' '.($user->employee->last_name ?? ''));
            $function = $user->employee->role?->name ?: ($user->role?->name ?? '');

            return [
                'account_holder_name' => $fullName !== '' ? $fullName : $user->username,
                'account_holder_function' => $function !== '' ? $function : 'Fonction non définie',
            ];
        }

        return [
            'account_holder_name' => $user->username,
            'account_holder_function' => $user->role?->name ?: 'Fonction non définie',
        ];
    }
}

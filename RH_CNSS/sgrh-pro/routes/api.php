<?php

use App\Http\Controllers\Api\AccountApiController;
use App\Http\Controllers\Api\AttendanceApiController;
use App\Http\Controllers\Api\BiometricApiController;
use App\Http\Controllers\Api\BiometricCheckinController;
use App\Http\Controllers\Api\ContractApiController;
use App\Http\Controllers\Api\DepartmentApiController;
use App\Http\Controllers\Api\EmployeeApiController;
use App\Http\Controllers\Api\EvaluationApiController;
use App\Http\Controllers\Api\LeaveApiController;
use App\Http\Controllers\Api\MedicalLeaveApiController;
use App\Http\Controllers\Api\MessageApiController;
use App\Http\Controllers\Api\NotificationApiController;
use App\Http\Controllers\Api\PayrollApiController;
use App\Http\Controllers\Api\PresenceApiController;
use App\Http\Controllers\Api\RecruitmentApiController;
use App\Http\Controllers\Api\ReportApiController;
use App\Http\Controllers\Api\RoleApiController;
use App\Http\Controllers\Api\SettingsApiController;
use App\Http\Controllers\Api\SpaAuthController;
use App\Http\Controllers\Api\TrainingApiController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Flask-compatible SPA JSON API
|--------------------------------------------------------------------------
*/

Route::prefix('auth')->group(function () {
    Route::post('/register', [SpaAuthController::class, 'register']);
    Route::post('/login', [SpaAuthController::class, 'login']);

    Route::middleware('auth:sanctum')->group(function () {
        Route::get('/me', [SpaAuthController::class, 'me']);
        Route::post('/change-password', [SpaAuthController::class, 'changePassword']);
        Route::post('/logout', [SpaAuthController::class, 'logout']);
    });
});

// Public biometric check-in (device endpoints)
Route::post('/biometric/checkin/rfid', [BiometricCheckinController::class, 'checkinRfid']);
Route::post('/biometric/checkin/fingerprint', [BiometricCheckinController::class, 'checkinFingerprint']);

// Public presence punch for kiosk devices (no JWT)
Route::post('/presence/punch-public', [PresenceApiController::class, 'punch']);

Route::middleware('auth:sanctum')->group(function () {
    // Presence (revolutionary attendance board + personal view)
    Route::get('/presence/today', [PresenceApiController::class, 'today']);
    Route::post('/presence/punch', [PresenceApiController::class, 'punch']);
    Route::get('/presence/me', [PresenceApiController::class, 'me']);
    Route::get('/team/overview', [PresenceApiController::class, 'teamOverview']);

    // Employees
    Route::get('/employees', [EmployeeApiController::class, 'index']);
    Route::post('/employees', [EmployeeApiController::class, 'store']);
    Route::put('/employees/{employeeId}', [EmployeeApiController::class, 'update']);
    Route::delete('/employees/{employeeId}', [EmployeeApiController::class, 'destroy']);

    // Departments
    Route::get('/departments', [DepartmentApiController::class, 'index']);
    Route::post('/departments', [DepartmentApiController::class, 'store']);
    Route::put('/departments/{departmentId}', [DepartmentApiController::class, 'update']);
    Route::delete('/departments/{departmentId}', [DepartmentApiController::class, 'destroy']);
    Route::patch('/departments/{departmentId}/manager/{managerId}', [DepartmentApiController::class, 'assignManager']);

    // Roles
    Route::get('/roles', [RoleApiController::class, 'index']);
    Route::get('/roles/permissions', [RoleApiController::class, 'permissions']);
    Route::post('/roles', [RoleApiController::class, 'store']);
    Route::patch('/roles/{roleId}/permissions', [RoleApiController::class, 'assignPermissions']);

    // Accounts
    Route::get('/accounts', [AccountApiController::class, 'index']);
    Route::get('/accounts/activity', [AccountApiController::class, 'activity']);
    Route::get('/accounts/activity/export.csv', [AccountApiController::class, 'exportActivityCsv']);
    Route::patch('/accounts/{userId}/reset-password', [AccountApiController::class, 'resetPassword']);
    Route::patch('/accounts/{userId}/role', [AccountApiController::class, 'updateRole']);
    Route::patch('/accounts/{userId}/status', [AccountApiController::class, 'updateStatus']);

    // Attendances
    Route::get('/attendances', [AttendanceApiController::class, 'index']);
    Route::post('/attendances/checkin', [AttendanceApiController::class, 'checkin']);
    Route::post('/attendances/checkout', [AttendanceApiController::class, 'checkout']);
    Route::post('/attendances/checkout-employee', [AttendanceApiController::class, 'checkoutEmployee']);
    Route::get('/attendances/summary/monthly', [AttendanceApiController::class, 'monthlySummary']);
    Route::put('/attendances/{attendanceId}', [AttendanceApiController::class, 'update']);
    Route::delete('/attendances/{attendanceId}', [AttendanceApiController::class, 'destroy']);

    // Leaves
    Route::get('/leaves', [LeaveApiController::class, 'index']);
    Route::post('/leaves', [LeaveApiController::class, 'store']);
    Route::patch('/leaves/{leaveId}/approval', [LeaveApiController::class, 'approval']);
    Route::put('/leaves/{leaveId}', [LeaveApiController::class, 'update']);
    Route::delete('/leaves/{leaveId}', [LeaveApiController::class, 'destroy']);

    // Contracts
    Route::get('/contracts', [ContractApiController::class, 'index']);
    Route::post('/contracts', [ContractApiController::class, 'store']);
    Route::put('/contracts/{contractId}', [ContractApiController::class, 'update']);
    Route::delete('/contracts/{contractId}', [ContractApiController::class, 'destroy']);

    // Payrolls
    Route::get('/payrolls', [PayrollApiController::class, 'index']);
    Route::post('/payrolls', [PayrollApiController::class, 'store']);
    Route::put('/payrolls/{payrollId}', [PayrollApiController::class, 'update']);
    Route::delete('/payrolls/{payrollId}', [PayrollApiController::class, 'destroy']);
    Route::get('/payrolls/{payrollId}/payslip', [PayrollApiController::class, 'payslip']);

    // Messages
    Route::get('/messages/recipients', [MessageApiController::class, 'recipients']);
    Route::get('/messages', [MessageApiController::class, 'inbox']);
    Route::get('/messages/sent', [MessageApiController::class, 'sent']);
    Route::get('/messages/unread-count', [MessageApiController::class, 'unreadCount']);
    Route::get('/messages/conversations', [MessageApiController::class, 'conversations']);
    Route::get('/messages/thread/{otherUserId}', [MessageApiController::class, 'thread']);
    Route::post('/messages/thread/{otherUserId}', [MessageApiController::class, 'sendThread']);
    Route::post('/messages', [MessageApiController::class, 'store']);
    Route::patch('/messages/{messageId}/read', [MessageApiController::class, 'markRead']);
    Route::patch('/messages/{messageId}', [MessageApiController::class, 'update']);
    Route::delete('/messages/{messageId}', [MessageApiController::class, 'destroy']);

    // Biometric (authenticated)
    Route::post('/biometric/scan', [BiometricApiController::class, 'scan']);
    Route::get('/biometric/status', [BiometricApiController::class, 'status']);
    Route::get('/biometric/match-gallery', [BiometricApiController::class, 'matchGallery']);
    Route::post('/biometric/verify-template', [BiometricApiController::class, 'verifyTemplate']);
    Route::get('/biometric/enrolled', [BiometricApiController::class, 'enrolled']);
    Route::post('/biometric/enroll/{employeeId}', [BiometricApiController::class, 'enroll']);
    Route::post('/biometric/fingerprint/delete', [BiometricApiController::class, 'deleteFingerprint']);
    Route::post('/biometric/rfid/assign', [BiometricApiController::class, 'assignRfid']);
    Route::post('/biometric/rfid/update', [BiometricApiController::class, 'updateRfid']);
    Route::post('/biometric/rfid/deactivate', [BiometricApiController::class, 'deactivateRfid']);
    Route::post('/biometric/rfid/reactivate', [BiometricApiController::class, 'reactivateRfid']);
    Route::post('/biometric/rfid/delete', [BiometricApiController::class, 'deleteRfid']);
    Route::get('/biometric/devices', [BiometricApiController::class, 'devices']);

    // Trainings
    Route::get('/trainings', [TrainingApiController::class, 'index']);
    Route::post('/trainings', [TrainingApiController::class, 'store']);
    Route::get('/trainings/skills', [TrainingApiController::class, 'listSkills']);
    Route::post('/trainings/skills', [TrainingApiController::class, 'createSkill']);
    Route::get('/trainings/employees/{employeeId}/skills', [TrainingApiController::class, 'employeeSkills']);
    Route::post('/trainings/employees/{employeeId}/skills', [TrainingApiController::class, 'addEmployeeSkill']);
    Route::put('/trainings/enrollments/{enrollmentId}', [TrainingApiController::class, 'updateEnrollment']);
    Route::get('/trainings/{trainingId}', [TrainingApiController::class, 'show']);
    Route::put('/trainings/{trainingId}', [TrainingApiController::class, 'update']);
    Route::delete('/trainings/{trainingId}', [TrainingApiController::class, 'destroy']);
    Route::post('/trainings/{trainingId}/enroll', [TrainingApiController::class, 'enroll']);

    // Evaluations
    Route::get('/evaluations', [EvaluationApiController::class, 'index']);
    Route::post('/evaluations', [EvaluationApiController::class, 'store']);
    Route::get('/evaluations/stats', [EvaluationApiController::class, 'stats']);
    Route::get('/evaluations/{evalId}', [EvaluationApiController::class, 'show']);
    Route::put('/evaluations/{evalId}', [EvaluationApiController::class, 'update']);
    Route::delete('/evaluations/{evalId}', [EvaluationApiController::class, 'destroy']);

    // Medical leaves
    Route::get('/medical-leaves', [MedicalLeaveApiController::class, 'index']);
    Route::post('/medical-leaves', [MedicalLeaveApiController::class, 'store']);
    Route::get('/medical-leaves/{mlId}', [MedicalLeaveApiController::class, 'show']);
    Route::put('/medical-leaves/{mlId}', [MedicalLeaveApiController::class, 'update']);
    Route::delete('/medical-leaves/{mlId}', [MedicalLeaveApiController::class, 'destroy']);

    // Notifications
    Route::get('/notifications', [NotificationApiController::class, 'index']);
    Route::get('/notifications/unread-count', [NotificationApiController::class, 'unreadCount']);
    Route::put('/notifications/read-all', [NotificationApiController::class, 'markAllRead']);
    Route::put('/notifications/{notifId}/read', [NotificationApiController::class, 'markRead']);
    Route::post('/notifications', [NotificationApiController::class, 'store']);
    Route::delete('/notifications/{notifId}', [NotificationApiController::class, 'destroy']);
    Route::post('/notifications/generate-alerts', [NotificationApiController::class, 'generateAlerts']);

    // Recruitment
    Route::get('/recruitment/offers', [RecruitmentApiController::class, 'listOffers']);
    Route::post('/recruitment/offers', [RecruitmentApiController::class, 'createOffer']);
    Route::get('/recruitment/offers/{offerId}', [RecruitmentApiController::class, 'showOffer']);
    Route::put('/recruitment/offers/{offerId}', [RecruitmentApiController::class, 'updateOffer']);
    Route::delete('/recruitment/offers/{offerId}', [RecruitmentApiController::class, 'destroyOffer']);
    Route::get('/recruitment/applications', [RecruitmentApiController::class, 'listApplications']);
    Route::post('/recruitment/offers/{offerId}/applications', [RecruitmentApiController::class, 'submitApplication']);
    Route::put('/recruitment/applications/{appId}', [RecruitmentApiController::class, 'updateApplication']);
    Route::delete('/recruitment/applications/{appId}', [RecruitmentApiController::class, 'destroyApplication']);
    Route::get('/recruitment/stats', [RecruitmentApiController::class, 'stats']);

    // Reports
    Route::get('/reports/stats', [ReportApiController::class, 'stats']);
    Route::get('/reports/accounting', [ReportApiController::class, 'accounting']);
    Route::get('/reports/dashboard', [ReportApiController::class, 'dashboard']);

    // Settings
    Route::get('/settings/parameters', [SettingsApiController::class, 'listParameters']);
    Route::get('/settings/parameters/{key}', [SettingsApiController::class, 'getParameter']);
    Route::put('/settings/parameters/{key}', [SettingsApiController::class, 'upsertParameter']);
    Route::post('/settings/parameters/bulk', [SettingsApiController::class, 'bulkUpsertParameters']);
    Route::get('/settings/holidays', [SettingsApiController::class, 'listHolidays']);
    Route::post('/settings/holidays', [SettingsApiController::class, 'createHoliday']);
    Route::put('/settings/holidays/{holidayId}', [SettingsApiController::class, 'updateHoliday']);
    Route::delete('/settings/holidays/{holidayId}', [SettingsApiController::class, 'destroyHoliday']);
});

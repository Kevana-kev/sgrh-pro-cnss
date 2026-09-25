<?php

use App\Http\Controllers\AttendanceController;
use App\Http\Controllers\Auth\LoginController;
use App\Http\Controllers\Auth\PasswordController;
use App\Http\Controllers\BiometricController;
use App\Http\Controllers\DashboardController;
use App\Http\Controllers\DepartmentController;
use App\Http\Controllers\EmployeeController;
use App\Http\Controllers\EvaluationController;
use App\Http\Controllers\LeaveController;
use App\Http\Controllers\RemunerationController;
use App\Http\Controllers\ReportController;
use App\Http\Controllers\SettingsController;
use App\Http\Controllers\UserController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| UI principale = ancienne SPA 14 modules (dashboard Flask)
| Backend = API Laravel JSON sous /api/*
| Anciennes pages Blade conservées sous /classic/*
|--------------------------------------------------------------------------
*/

Route::get('/', fn () => view('spa'))->name('spa');
Route::get('/dashboard', fn () => view('spa'))->name('spa.dashboard');

Route::prefix('classic')->group(function () {
    Route::get('/', fn () => auth()->check() ? redirect()->route('dashboard') : redirect()->route('login'));

    Route::middleware('guest')->group(function () {
        Route::get('/login', [LoginController::class, 'showLogin'])->name('login');
        Route::post('/login', [LoginController::class, 'login'])->name('login.attempt');
    });

    Route::middleware('auth')->group(function () {
        Route::post('/logout', [LoginController::class, 'logout'])->name('logout');
        Route::get('/password/change', [PasswordController::class, 'edit'])->name('password.edit');
        Route::post('/password/change', [PasswordController::class, 'update'])->name('password.update');

        Route::middleware('password.force')->group(function () {
            Route::get('/dashboard', [DashboardController::class, 'index'])->name('dashboard');

            Route::middleware('permission:manage_users')->group(function () {
                Route::resource('users', UserController::class)->except(['show']);
            });

            Route::middleware('permission:manage_employees')->group(function () {
                Route::resource('employees', EmployeeController::class);
            });

            Route::middleware('permission:manage_departments')->group(function () {
                Route::resource('departments', DepartmentController::class)->except(['show']);
            });

            Route::middleware('permission:manage_attendances')->group(function () {
                Route::get('/attendances', [AttendanceController::class, 'index'])->name('attendances.index');
                Route::get('/attendances/create', [AttendanceController::class, 'create'])->name('attendances.create');
                Route::post('/attendances', [AttendanceController::class, 'store'])->name('attendances.store');
                Route::post('/attendances/{attendance}/checkout', [AttendanceController::class, 'checkout'])->name('attendances.checkout');
            });

            Route::middleware('permission:manage_leaves')->group(function () {
                Route::get('/leaves', [LeaveController::class, 'index'])->name('leaves.index');
                Route::get('/leaves/create', [LeaveController::class, 'create'])->name('leaves.create');
                Route::post('/leaves', [LeaveController::class, 'store'])->name('leaves.store');
            });

            Route::middleware('permission:decide_leaves')->group(function () {
                Route::post('/leaves/{leave}/decide', [LeaveController::class, 'decide'])->name('leaves.decide');
            });

            Route::middleware('permission:manage_biometric')->group(function () {
                Route::get('/biometric', [BiometricController::class, 'index'])->name('biometric.index');
                Route::post('/biometric/scan', [BiometricController::class, 'scanProxy'])->name('biometric.scan');
                Route::post('/biometric/enroll/{employee}', [BiometricController::class, 'enrollFingerprint'])->name('biometric.enroll');
                Route::post('/biometric/rfid/assign', [BiometricController::class, 'assignRfid'])->name('biometric.rfid.assign');
                Route::post('/biometric/rfid/deactivate', [BiometricController::class, 'deactivateRfid'])->name('biometric.rfid.deactivate');
            });

            Route::middleware('permission:manage_remuneration')->group(function () {
                Route::resource('remunerations', RemunerationController::class)->except(['show']);
                Route::get('/remunerations-export/pdf', [RemunerationController::class, 'exportPdf'])->name('remunerations.export.pdf');
                Route::get('/remunerations-export/csv', [RemunerationController::class, 'exportCsv'])->name('remunerations.export.csv');
            });

            Route::middleware('permission:manage_evaluations')->group(function () {
                Route::resource('evaluations', EvaluationController::class)->except(['show']);
            });

            Route::middleware('permission:view_reports')->group(function () {
                Route::get('/reports', [ReportController::class, 'index'])->name('reports.index');
                Route::get('/reports/export', [ReportController::class, 'export'])->name('reports.export');
            });

            Route::middleware('permission:manage_settings')->group(function () {
                Route::get('/settings', [SettingsController::class, 'edit'])->name('settings.edit');
                Route::post('/settings', [SettingsController::class, 'update'])->name('settings.update');
            });
        });
    });
});

<?php

namespace Database\Seeders;

use App\Models\Attendance;
use App\Models\BiometricDevice;
use App\Models\Department;
use App\Models\Employee;
use App\Models\Holiday;
use App\Models\Leave;
use App\Models\Permission;
use App\Models\PerformanceEvaluation;
use App\Models\RemunerationElement;
use App\Models\Role;
use App\Models\SystemParameter;
use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $permissions = [
            'Voir employés',
            'Modifier employés',
            'Voir salaires',
            'Exporter rapports',
            'Valider congés',
            'Voir comptabilité',
            'Voir équipe',
            'Valider congés équipe',
            'Attribuer tâches',
            'Gérer objectifs',
            'Gérer évaluations',
            'Voir performances',
            'Exporter rapports équipe',
            'Modifier formations',
        ];

        foreach ($permissions as $name) {
            Permission::firstOrCreate(['name' => $name]);
        }

        $all = Permission::query()->whereIn('name', $permissions)->get();

        $super = Role::firstOrCreate(['name' => 'SuperAdmin']);
        $adminRh = Role::firstOrCreate(['name' => 'Admin RH']);
        $rh = Role::firstOrCreate(['name' => 'RH']);
        $manager = Role::firstOrCreate(['name' => 'Manager']);
        $employeeRole = Role::firstOrCreate(['name' => 'Employé']);
        $comptable = Role::firstOrCreate(['name' => 'Comptable']);

        $super->permissions()->sync($all->pluck('id'));
        $adminRh->permissions()->sync(
            $all->whereIn('name', [
                'Voir employés', 'Modifier employés', 'Voir salaires',
                'Exporter rapports', 'Valider congés', 'Gérer évaluations',
                'Voir performances', 'Modifier formations',
            ])->pluck('id')
        );
        $rh->permissions()->sync(
            $all->whereIn('name', [
                'Voir employés', 'Modifier employés', 'Valider congés',
                'Gérer évaluations', 'Voir performances',
            ])->pluck('id')
        );
        $manager->permissions()->sync(
            $all->whereIn('name', [
                'Voir employés', 'Voir équipe', 'Voir salaires',
                'Valider congés équipe', 'Attribuer tâches',
                'Voir performances', 'Exporter rapports équipe',
            ])->pluck('id')
        );
        $employeeRole->permissions()->sync(
            $all->whereIn('name', ['Voir employés'])->pluck('id')
        );
        $comptable->permissions()->sync(
            $all->whereIn('name', [
                'Voir employés', 'Voir salaires', 'Exporter rapports', 'Voir comptabilité',
            ])->pluck('id')
        );

        $deptRh = Department::firstOrCreate(['name' => 'Ressources Humaines'], ['budget' => 50000]);
        $deptIt = Department::firstOrCreate(['name' => 'Informatique'], ['budget' => 80000]);
        $deptFin = Department::firstOrCreate(['name' => 'Finance'], ['budget' => 120000]);

        $adminEmp = Employee::firstOrCreate(
            ['email' => 'admin@cnss.cd'],
            [
                'first_name' => 'Admin',
                'last_name' => 'SGRH',
                'matricule' => 'CNSS-001',
                'phone' => '+243900000001',
                'address' => 'Kinshasa, Gombe',
                'hire_date' => now()->subYears(5)->toDateString(),
                'status' => 'Actif',
                'department_id' => $deptRh->id,
                'role_id' => $super->id,
                'rfid_card_id' => 'RFID-ADMIN-001',
                'rfid_card_active' => true,
            ]
        );

        $rhEmp = Employee::firstOrCreate(
            ['email' => 'rh@cnss.cd'],
            [
                'first_name' => 'Marie',
                'last_name' => 'Kabila',
                'matricule' => 'CNSS-002',
                'phone' => '+243900000002',
                'address' => 'Kinshasa, Limete',
                'hire_date' => now()->subYears(3)->toDateString(),
                'status' => 'Actif',
                'department_id' => $deptRh->id,
                'role_id' => $adminRh->id,
                'rfid_card_id' => 'RFID-RH-002',
                'rfid_card_active' => true,
            ]
        );

        $mgrEmp = Employee::firstOrCreate(
            ['email' => 'manager@cnss.cd'],
            [
                'first_name' => 'Jean',
                'last_name' => 'Mwamba',
                'matricule' => 'CNSS-003',
                'phone' => '+243900000003',
                'address' => 'Kinshasa, Ngaliema',
                'hire_date' => now()->subYears(2)->toDateString(),
                'status' => 'Actif',
                'department_id' => $deptIt->id,
                'role_id' => $manager->id,
            ]
        );

        $agentEmp = Employee::firstOrCreate(
            ['email' => 'agent@cnss.cd'],
            [
                'first_name' => 'Grace',
                'last_name' => 'Ilunga',
                'matricule' => 'CNSS-004',
                'phone' => '+243900000004',
                'address' => 'Kinshasa, Kalamu',
                'hire_date' => now()->subYear()->toDateString(),
                'status' => 'Actif',
                'department_id' => $deptFin->id,
                'role_id' => $employeeRole->id,
            ]
        );

        $deptRh->update(['manager_id' => $rhEmp->id]);
        $deptIt->update(['manager_id' => $mgrEmp->id]);

        // Passwords alignés avec l'ancienne UI SPA
        User::updateOrCreate(
            ['username' => 'superadmin'],
            [
                'password' => Hash::make('superadmin123'),
                'must_change_password' => false,
                'employee_id' => $adminEmp->id,
                'role_id' => $super->id,
            ]
        );

        User::updateOrCreate(
            ['username' => 'adminrh'],
            [
                'password' => Hash::make('adminrh123'),
                'must_change_password' => false,
                'employee_id' => $rhEmp->id,
                'role_id' => $adminRh->id,
            ]
        );

        User::updateOrCreate(
            ['username' => 'manager'],
            [
                'password' => Hash::make('manager123'),
                'must_change_password' => false,
                'employee_id' => $mgrEmp->id,
                'role_id' => $manager->id,
            ]
        );

        User::updateOrCreate(
            ['username' => 'agent'],
            [
                'password' => Hash::make('Agent@123'),
                'must_change_password' => true,
                'employee_id' => $agentEmp->id,
                'role_id' => $employeeRole->id,
            ]
        );

        BiometricDevice::firstOrCreate(
            ['name' => 'ZK-9500 Accueil'],
            [
                'device_type' => 'ZK-9500',
                'location' => 'Hall principal CNSS',
                'is_active' => true,
                'last_seen' => now(),
            ]
        );

        SystemParameter::firstOrCreate(['key' => 'work_start_time'], ['value' => '08:00']);
        SystemParameter::firstOrCreate(['key' => 'late_threshold_minutes'], ['value' => '15']);
        SystemParameter::firstOrCreate(['key' => 'fingerprint_match_threshold'], ['value' => '40']);
        SystemParameter::firstOrCreate(['key' => 'organization_name'], ['value' => 'CNSS — SGRH Pro']);

        Holiday::firstOrCreate(
            ['date' => now()->startOfYear()->toDateString()],
            ['name' => 'Nouvel An']
        );

        // Historique de présence (14 jours) pour graphiques espace agent / jury
        foreach ([$agentEmp, $rhEmp, $mgrEmp, $adminEmp] as $idx => $emp) {
            for ($d = 13; $d >= 0; $d--) {
                $day = now()->copy()->subDays($d)->startOfDay();
                // Week-end ignoré sauf aujourd'hui (utile pour démo jury)
                if ($day->isWeekend() && ! $day->isSameDay(now())) {
                    continue;
                }

                $late = ($d % 5 === 0 && $emp->id === $agentEmp->id) ? 18 : 0;
                $checkIn = $day->copy()->setTime(8, $late > 0 ? 20 : 2 + ($idx * 3));
                $checkOut = $day->copy()->setTime(16, 45 - $idx);
                $hours = round(($checkOut->getTimestamp() - $checkIn->getTimestamp()) / 3600, 2);

                $existing = Attendance::query()
                    ->where('employee_id', $emp->id)
                    ->whereDate('check_in', $day->toDateString())
                    ->first();

                $payload = [
                    'employee_id' => $emp->id,
                    'check_in' => $checkIn,
                    'check_out' => $d === 0 ? null : $checkOut,
                    'worked_hours' => $d === 0 ? 0 : $hours,
                    'late_minutes' => $late,
                    'is_absent' => false,
                    'source' => $d % 2 === 0 ? 'fingerprint' : 'rfid',
                ];

                if ($existing) {
                    $existing->update($payload);
                } else {
                    Attendance::create($payload);
                }
            }
        }

        $agentEmp->update([
            'rfid_card_id' => $agentEmp->rfid_card_id ?: 'RFID-AGENT-004',
            'rfid_card_active' => true,
        ]);

        Leave::firstOrCreate(
            [
                'employee_id' => $agentEmp->id,
                'start_date' => now()->addDays(10)->toDateString(),
                'end_date' => now()->addDays(12)->toDateString(),
            ],
            [
                'reason' => 'Congé annuel',
                'status' => 'En attente',
            ]
        );

        RemunerationElement::firstOrCreate(
            [
                'employee_id' => $agentEmp->id,
                'period' => now()->format('Y-m'),
            ],
            [
                'base_salary' => 450000,
                'bonus' => 25000,
                'overtime_hours' => 4,
                'overtime_amount' => 11250,
                'deductions' => 15000,
                'total_indicative' => 471250,
                'status' => 'Brouillon',
                'notes' => 'État indicatif à transmettre à la finance.',
            ]
        );

        PerformanceEvaluation::firstOrCreate(
            [
                'employee_id' => $agentEmp->id,
                'period' => now()->format('Y').'-S1',
            ],
            [
                'evaluator_id' => $mgrEmp->id,
                'score' => 78,
                'strengths' => 'Ponctualité et collaboration',
                'improvements' => 'Renforcer le reporting',
                'comments' => 'Bonne progression',
                'status' => 'Validé',
            ]
        );

        $this->call(DemoDataSeeder::class);
    }
}

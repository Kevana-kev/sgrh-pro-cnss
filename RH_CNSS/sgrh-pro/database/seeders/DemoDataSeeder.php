<?php

namespace Database\Seeders;

use App\Models\ActivityLog;
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
use App\Models\Skill;
use App\Models\Training;
use App\Models\TrainingEnrollment;
use App\Models\User;
use Carbon\Carbon;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DemoDataSeeder extends Seeder
{
    public function run(): void
    {
        if (Employee::query()->where('matricule', 'CNSS-005')->exists()) {
            $this->command?->info('Données démo déjà présentes — mise à jour partielle…');
        }

        $employeeRole = Role::firstOrCreate(['name' => 'Employé']);
        $managerRole = Role::firstOrCreate(['name' => 'Manager']);
        $rhRole = Role::firstOrCreate(['name' => 'RH']);

        $deptRh = Department::firstOrCreate(['name' => 'Ressources Humaines'], ['budget' => 850000]);
        $deptIt = Department::firstOrCreate(['name' => 'Informatique'], ['budget' => 1200000]);
        $deptFin = Department::firstOrCreate(['name' => 'Finance'], ['budget' => 1500000]);
        $deptJur = Department::firstOrCreate(['name' => 'Juridique'], ['budget' => 620000]);
        $deptCom = Department::firstOrCreate(['name' => 'Communication'], ['budget' => 480000]);
        $deptCot = Department::firstOrCreate(['name' => 'Cotisations & Recouvrement'], ['budget' => 2100000]);

        $mgrEmp = Employee::where('email', 'manager@cnss.cd')->first();
        $rhEmp = Employee::where('email', 'rh@cnss.cd')->first();
        $agentEmp = Employee::where('email', 'agent@cnss.cd')->first();

        $staff = [
            ['CNSS-005', 'Patrick', 'Mbuyi', 'patrick.mbuyi@cnss.cd', $deptIt, 680000, 'Actif', '+243810000005'],
            ['CNSS-006', 'Chantal', 'Tshibanda', 'chantal.tshibanda@cnss.cd', $deptIt, 720000, 'Actif', '+243810000006'],
            ['CNSS-007', 'David', 'Kabongo', 'david.kabongo@cnss.cd', $deptIt, 590000, 'Actif', '+243810000007'],
            ['CNSS-008', 'Esther', 'Mpunga', 'esther.mpunga@cnss.cd', $deptFin, 750000, 'Actif', '+243810000008'],
            ['CNSS-009', 'Fabrice', 'Ngoy', 'fabrice.ngoy@cnss.cd', $deptFin, 810000, 'Actif', '+243810000009'],
            ['CNSS-010', 'Hortense', 'Kalonji', 'hortense.kalonji@cnss.cd', $deptFin, 640000, 'Actif', '+243810000010'],
            ['CNSS-011', 'Ibrahim', 'Beya', 'ibrahim.beya@cnss.cd', $deptCot, 920000, 'Actif', '+243810000011'],
            ['CNSS-012', 'Joséphine', 'Mukendi', 'josephine.mukendi@cnss.cd', $deptCot, 880000, 'Actif', '+243810000012'],
            ['CNSS-013', 'Kevin', 'Kasongo', 'kevin.kasongo@cnss.cd', $deptCot, 710000, 'Actif', '+243810000013'],
            ['CNSS-014', 'Lydia', 'Mutombo', 'lydia.mutombo@cnss.cd', $deptRh, 650000, 'Actif', '+243810000014'],
            ['CNSS-015', 'Marc', 'Ilunga', 'marc.ilunga@cnss.cd', $deptRh, 620000, 'Actif', '+243810000015'],
            ['CNSS-016', 'Nathalie', 'Kabasele', 'nathalie.kabasele@cnss.cd', $deptJur, 980000, 'Actif', '+243810000016'],
            ['CNSS-017', 'Olivier', 'Mwanza', 'olivier.mwanza@cnss.cd', $deptJur, 1050000, 'Actif', '+243810000017'],
            ['CNSS-018', 'Prisca', 'Luboya', 'prisca.luboya@cnss.cd', $deptCom, 580000, 'Actif', '+243810000018'],
            ['CNSS-019', 'Roger', 'Tshilombo', 'roger.tshilombo@cnss.cd', $deptCom, 560000, 'Actif', '+243810000019'],
            ['CNSS-020', 'Sandra', 'Mpiana', 'sandra.mpiana@cnss.cd', $deptIt, 540000, 'Suspendu', '+243810000020'],
            ['CNSS-021', 'Thierry', 'Kabeya', 'thierry.kabeya@cnss.cd', $deptCot, 600000, 'Démissionné', '+243810000021'],
            ['CNSS-022', 'Vanessa', 'Nsimba', 'vanessa.nsimba@cnss.cd', $deptFin, 670000, 'Actif', '+243810000022'],
            ['CNSS-023', 'William', 'Kazadi', 'william.kazadi@cnss.cd', $deptIt, 830000, 'Actif', '+243810000023'],
            ['CNSS-024', 'Yvette', 'Banza', 'yvette.banza@cnss.cd', $deptRh, 610000, 'Actif', '+243810000024'],
        ];

        $createdEmployees = [];
        foreach ($staff as [$mat, $first, $last, $email, $dept, $salary, $status, $phone]) {
            $emp = Employee::updateOrCreate(
                ['matricule' => $mat],
                [
                    'first_name' => $first,
                    'last_name' => $last,
                    'email' => $email,
                    'phone' => $phone,
                    'address' => 'Kinshasa, RDC',
                    'hire_date' => now()->subMonths(rand(6, 48))->toDateString(),
                    'status' => $status,
                    'department_id' => $dept->id,
                    'role_id' => $employeeRole->id,
                    'rfid_card_id' => 'RFID-'.$mat,
                    'rfid_card_active' => $status === 'Actif',
                ]
            );
            $createdEmployees[] = ['emp' => $emp, 'salary' => $salary];
        }

        if ($mgrEmp) {
            $deptIt->update(['manager_id' => $mgrEmp->id]);
        }
        $finMgr = Employee::where('matricule', 'CNSS-009')->first();
        if ($finMgr) {
            $finMgr->update(['role_id' => $managerRole->id]);
            $deptFin->update(['manager_id' => $finMgr->id]);
        }
        $cotMgr = Employee::where('matricule', 'CNSS-011')->first();
        if ($cotMgr) {
            $cotMgr->update(['role_id' => $managerRole->id]);
            $deptCot->update(['manager_id' => $cotMgr->id]);
        }
        if ($rhEmp) {
            $deptRh->update(['manager_id' => $rhEmp->id]);
        }

        $allActive = Employee::query()
            ->where(function ($q) {
                $q->where('status', 'Actif')
                    ->orWhereRaw('LOWER(TRIM(status)) IN (?, ?)', ['actif', 'active']);
            })
            ->get();

        foreach ($allActive as $emp) {
            $base = 450000 + (($emp->id % 7) * 85000);
            for ($m = 5; $m >= 0; $m--) {
                $paidAt = now()->subMonths($m)->endOfMonth()->setTime(14, 0);
                $bonus = ($m % 3 === 0) ? 35000 : 15000;
                $deductions = 22000 + ($emp->id % 5) * 1200;
                $taxes = round($base * 0.08, 2);
                $net = $base + $bonus - $deductions - $taxes;

                Payroll::updateOrCreate(
                    [
                        'employee_id' => $emp->id,
                        'paid_at' => $paidAt,
                    ],
                    [
                        'base_salary' => $base,
                        'bonus' => $bonus,
                        'overtime_hours' => ($m % 2) * 3,
                        'deductions' => $deductions,
                        'taxes' => $taxes,
                        'net_salary' => $net,
                    ]
                );
            }

            Contract::updateOrCreate(
                ['employee_id' => $emp->id, 'contract_type' => 'CDI'],
                [
                    'start_date' => $emp->hire_date ?? now()->subYear(),
                    'end_date' => null,
                    'contractual_salary' => $base,
                ]
            );
        }

        $cddEmployees = Employee::whereIn('matricule', ['CNSS-020', 'CNSS-023'])->get();
        foreach ($cddEmployees as $emp) {
            Contract::updateOrCreate(
                ['employee_id' => $emp->id, 'contract_type' => 'CDD'],
                [
                    'start_date' => now()->subMonths(8),
                    'end_date' => now()->addMonths(2),
                    'contractual_salary' => 520000,
                ]
            );
        }

        $trainings = [
            ['Sécurité sociale — module avancé', 'Dr. Mwamba', 'Planifiée', 25],
            ['Excel & reporting RH', 'FormaPro Kinshasa', 'En cours', 20],
            ['Gestion du stress au travail', 'CNSS — Service médical', 'Terminée', 30],
            ['DSP2 & protection des données', 'Cabinet Juridique LMC', 'En cours', 15],
            ['Accueil & relation assuré', 'Direction Communication', 'Planifiée', 40],
        ];

        foreach ($trainings as [$title, $trainer, $status, $max]) {
            $training = Training::updateOrCreate(
                ['title' => $title],
                [
                    'description' => 'Formation interne CNSS — programme '.$title,
                    'trainer' => $trainer,
                    'start_date' => now()->subDays($status === 'Terminée' ? 45 : 5)->toDateString(),
                    'end_date' => now()->addDays($status === 'Terminée' ? -10 : 12)->toDateString(),
                    'max_participants' => $max,
                    'status' => $status,
                ]
            );

            $pick = $allActive->random(min(8, $allActive->count()));
            foreach ($pick as $idx => $emp) {
                TrainingEnrollment::updateOrCreate(
                    ['training_id' => $training->id, 'employee_id' => $emp->id],
                    [
                        'status' => match ($status) {
                            'Terminée' => 'Terminé',
                            'En cours' => $idx % 2 === 0 ? 'En cours' : 'Inscrit',
                            default => 'Inscrit',
                        },
                        'score' => $status === 'Terminée' ? rand(72, 96) : null,
                        'enrolled_at' => now()->subDays(rand(3, 20)),
                    ]
                );
            }
        }

        if ($agentEmp) {
            TrainingEnrollment::updateOrCreate(
                [
                    'training_id' => Training::where('title', 'Excel & reporting RH')->value('id'),
                    'employee_id' => $agentEmp->id,
                ],
                ['status' => 'En cours', 'enrolled_at' => now()->subDays(4)]
            );
        }

        $skills = [
            ['Comptabilité publique', 'Finance'],
            ['Paie & cotisations', 'Finance'],
            ['Laravel / PHP', 'Technique'],
            ['Réseaux & sécurité', 'Technique'],
            ['Communication institutionnelle', 'Soft skills'],
            ['Droit du travail', 'Juridique'],
            ['Gestion de projet', 'Management'],
            ['Anglais professionnel', 'Langues'],
        ];
        foreach ($skills as [$name, $cat]) {
            Skill::firstOrCreate(['name' => $name], ['category' => $cat]);
        }

        foreach ($allActive->take(12) as $emp) {
            $skillIds = Skill::inRandomOrder()->limit(3)->pluck('id');
            foreach ($skillIds as $skillId) {
                EmployeeSkill::updateOrCreate(
                    ['employee_id' => $emp->id, 'skill_id' => $skillId],
                    [
                        'level' => rand(1, 4),
                        'certified_at' => rand(0, 1) ? now()->subMonths(rand(1, 18)) : null,
                    ]
                );
            }
        }

        $leaveReasons = ['Congé annuel', 'Raisons familiales', 'Mariage', 'Décès proche', 'Formation'];
        $leaveStatuses = ['Approuvé', 'Approuvé', 'Approuvé', 'En attente', 'Rejeté'];
        foreach ($allActive->take(14) as $i => $emp) {
            Leave::updateOrCreate(
                [
                    'employee_id' => $emp->id,
                    'start_date' => now()->addDays(5 + $i * 3)->toDateString(),
                ],
                [
                    'end_date' => now()->addDays(7 + $i * 3)->toDateString(),
                    'reason' => $leaveReasons[$i % count($leaveReasons)],
                    'status' => $leaveStatuses[$i % count($leaveStatuses)],
                ]
            );
        }

        if ($agentEmp) {
            Leave::updateOrCreate(
                ['employee_id' => $agentEmp->id, 'status' => 'En attente'],
                [
                    'start_date' => now()->addDays(10)->toDateString(),
                    'end_date' => now()->addDays(12)->toDateString(),
                    'reason' => 'Congé annuel',
                ]
            );
            Leave::updateOrCreate(
                ['employee_id' => $agentEmp->id, 'status' => 'Approuvé'],
                [
                    'start_date' => now()->subMonths(2)->toDateString(),
                    'end_date' => now()->subMonths(2)->addDays(3)->toDateString(),
                    'reason' => 'Congé annuel',
                ]
            );
        }

        foreach ($allActive->take(4) as $i => $emp) {
            MedicalLeave::updateOrCreate(
                ['employee_id' => $emp->id, 'start_date' => now()->subDays(20 - $i * 5)->toDateString()],
                [
                    'end_date' => now()->subDays(14 - $i * 5)->toDateString(),
                    'diagnosis' => ['Grippe', 'Lombalgie', 'Consultation', 'Repos médical'][$i],
                    'daily_allowance' => 18500,
                    'status' => $i < 2 ? 'Clôturé' : 'En cours',
                ]
            );
        }

        $offers = [
            ['Analyste cotisations senior', $deptCot, 'Publiée'],
            ['Développeur full-stack', $deptIt, 'Publiée'],
            ['Chargé de communication', $deptCom, 'Brouillon'],
            ['Juriste social', $deptJur, 'Publiée'],
            ['Comptable paie', $deptFin, 'Clôturée'],
        ];
        foreach ($offers as [$title, $dept, $status]) {
            $offer = JobOffer::updateOrCreate(
                ['title' => $title],
                [
                    'department_id' => $dept->id,
                    'description' => 'Poste ouvert à la CNSS Kinshasa — '.$title,
                    'requirements' => 'Bac+3 minimum, expérience 2 ans, maîtrise du français.',
                    'status' => $status,
                ]
            );

            $applicants = [
                ['Aline Mujinga', 'aline.mujinga@gmail.com', 'Reçue'],
                ['Bruno Kabamba', 'bruno.k@gmail.com', 'Présélection'],
                ['Cynthia Nzeba', 'cynthia.nzeba@yahoo.fr', 'Entretien'],
                ['Didier Tshisekedi', 'didier.t@outlook.com', 'Rejetée'],
            ];
            foreach ($applicants as $j => [$name, $email, $appStatus]) {
                JobApplication::updateOrCreate(
                    ['job_offer_id' => $offer->id, 'applicant_email' => $email],
                    [
                        'applicant_name' => $name,
                        'status' => $appStatus,
                        'interview_date' => $appStatus === 'Entretien' ? now()->addDays(3) : null,
                        'notes' => 'Candidature reçue via portail CNSS.',
                    ]
                );
            }
        }

        $adminUser = User::where('username', 'superadmin')->first();
        $rhUser = User::where('username', 'adminrh')->first();
        $mgrUser = User::where('username', 'manager')->first();
        $agentUser = User::where('username', 'agent')->first();

        if ($agentUser) {
            $agentUser->update(['must_change_password' => false]);
        }

        $notifTemplates = [
            ['BUDGET_ALERT', 'Budget formation', 'Le budget formation Q3 atteint 82% du plafond.'],
            ['MONTHLY_SUMMARY', 'Résumé RH disponible', 'Le rapport mensuel d\'août est prêt à consulter.'],
            ['LEAVE_ALERT', 'Congé à valider', 'Grace Ilunga a soumis une demande de congé.'],
            ['TRAINING', 'Formation demain', 'Rappel : Excel & reporting RH démarre à 09h00.'],
            ['CONTRACT', 'Contrat CDD', 'Le contrat de Sandra Mpiana expire dans 60 jours.'],
        ];

        foreach ([$adminUser, $rhUser, $mgrUser, $agentUser] as $uIdx => $user) {
            if (! $user) {
                continue;
            }
            foreach ($notifTemplates as $nIdx => [$type, $title, $message]) {
                Notification::updateOrCreate(
                    ['user_id' => $user->id, 'title' => $title],
                    [
                        'type' => $type,
                        'message' => $message,
                        'is_read' => ($uIdx + $nIdx) % 3 === 0,
                    ]
                );
            }
        }

        if ($rhUser && $agentUser) {
            Message::updateOrCreate(
                ['sender_user_id' => $rhUser->id, 'recipient_user_id' => $agentUser->id, 'subject' => 'Documents manquants'],
                [
                    'content' => 'Bonjour Grace, merci de déposer votre certificat médical avant vendredi.',
                    'sent_at' => now()->subDays(2),
                    'read_at' => null,
                ]
            );
            Message::updateOrCreate(
                ['sender_user_id' => $agentUser->id, 'recipient_user_id' => $rhUser->id, 'subject' => 'Demande attestation'],
                [
                    'content' => 'Bonjour, pourriez-vous me transmettre une attestation de travail ?',
                    'sent_at' => now()->subDay(),
                    'read_at' => now()->subHours(6),
                ]
            );
        }

        if ($mgrEmp) {
            foreach ($allActive->where('department_id', $deptIt->id)->take(5) as $i => $emp) {
                PerformanceEvaluation::updateOrCreate(
                    ['employee_id' => $emp->id, 'period' => now()->format('Y').'-S1'],
                    [
                        'evaluator_id' => $mgrEmp->id,
                        'score' => rand(68, 94),
                        'strengths' => 'Rigueur et esprit d\'équipe',
                        'improvements' => 'Renforcer la communication transverse',
                        'comments' => 'Évaluation semestrielle CNSS',
                        'status' => $i % 4 === 0 ? 'Brouillon' : 'Validé',
                    ]
                );
            }
        }

        $holidays = [
            ['Fête du Travail', '05-01'],
            ['Fête de l\'Indépendance', '06-30'],
            ['Noël', '12-25'],
        ];
        foreach ($holidays as [$name, $md]) {
            Holiday::firstOrCreate(
                ['date' => now()->year.'-'.$md],
                ['name' => $name]
            );
        }

        $logs = [
            ['adminrh', 'Validation congé employé #'.$agentEmp?->id],
            ['manager', 'Consultation tableau de bord équipe IT'],
            ['superadmin', 'Mise à jour paramètre seuil biométrique'],
            ['adminrh', 'Publication offre Analyste cotisations'],
            ['manager', 'Évaluation performance S1 enregistrée'],
        ];
        if (ActivityLog::query()->count() < 5) {
            foreach ($logs as [$user, $action]) {
                ActivityLog::create(['username' => $user, 'action' => $action]);
            }
        }

        $today = Carbon::today();
        $scenario = ['present', 'present', 'present', 'late', 'late', 'present', 'completed', 'not_arrived', 'absent'];
        $idx = 0;
        foreach ($allActive->take(18) as $emp) {
            $kind = $scenario[$idx % count($scenario)];
            $idx++;

            Attendance::query()
                ->where('employee_id', $emp->id)
                ->whereDate('check_in', $today)
                ->delete();

            if ($kind === 'not_arrived') {
                continue;
            }
            if ($kind === 'absent') {
                Attendance::create([
                    'employee_id' => $emp->id,
                    'check_in' => $today->copy()->setTime(8, 0),
                    'check_out' => null,
                    'worked_hours' => 0,
                    'late_minutes' => 0,
                    'is_absent' => true,
                    'source' => 'system',
                ]);
                continue;
            }

            $late = $kind === 'late' ? rand(12, 35) : 0;
            $checkIn = $today->copy()->setTime(8, $late > 0 ? 25 : rand(0, 8));
            $checkOut = in_array($kind, ['completed'], true)
                ? $today->copy()->setTime(16, rand(40, 55))
                : null;
            $hours = $checkOut
                ? round(max($checkOut->diffInMinutes($checkIn), 0) / 60, 2)
                : 0;

            Attendance::create([
                'employee_id' => $emp->id,
                'check_in' => $checkIn,
                'check_out' => $checkOut,
                'worked_hours' => $hours,
                'late_minutes' => $late,
                'is_absent' => false,
                'source' => $idx % 2 === 0 ? 'fingerprint' : 'rfid',
            ]);
        }

        if ($agentEmp) {
            Attendance::query()
                ->where('employee_id', $agentEmp->id)
                ->whereDate('check_in', $today)
                ->delete();
            Attendance::create([
                'employee_id' => $agentEmp->id,
                'check_in' => $today->copy()->setTime(8, 5),
                'check_out' => null,
                'worked_hours' => 0,
                'late_minutes' => 5,
                'is_absent' => false,
                'source' => 'fingerprint',
            ]);
        }

        $this->command?->info('Données démo CNSS chargées : '.Employee::count().' employés, '.Payroll::count().' bulletins.');
    }
}

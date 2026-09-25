<?php

namespace App\Services;

use App\Models\Employee;
use App\Models\SystemParameter;

class FingerprintTemplateService
{
    public const REQUIRED_FINGERS = 3;

    public static function decode(?string $raw): array
    {
        if (! $raw || trim($raw) === '') {
            return [];
        }

        $trim = trim($raw);
        if (str_starts_with($trim, '[')) {
            $decoded = json_decode($trim, true);

            return is_array($decoded)
                ? array_values(array_filter($decoded, fn ($t) => is_string($t) && $t !== ''))
                : [];
        }

        return [$trim];
    }

    public static function encode(array $templates): string
    {
        return json_encode(array_values($templates), JSON_UNESCAPED_SLASHES);
    }

    public static function count(?string $raw): int
    {
        return count(self::decode($raw));
    }

    public static function isComplete(?string $raw): bool
    {
        return self::count($raw) >= self::REQUIRED_FINGERS;
    }

    public function matchThreshold(): int
    {
        return (int) (SystemParameter::getValue('fingerprint_match_threshold', '40') ?: 40);
    }

    /**
     * @return array<int, array{id:int, template_b64:string}>
     */
    public function buildMatchGallery(?int $excludeEmployeeId = null): array
    {
        $gallery = [];

        $employees = Employee::query()
            ->whereNotNull('fingerprint_template')
            ->where('fingerprint_template', '!=', '')
            ->get(['id', 'fingerprint_template']);

        foreach ($employees as $employee) {
            if ($excludeEmployeeId && (int) $employee->id === $excludeEmployeeId) {
                continue;
            }

            foreach (self::decode($employee->fingerprint_template) as $template) {
                $gallery[] = [
                    'id' => (int) $employee->id,
                    'template_b64' => $template,
                ];
            }
        }

        return $gallery;
    }

    /**
     * @return array<int, array{id:int, template_b64:string}>
     */
    public function buildEmployeeGallery(Employee $employee): array
    {
        $gallery = [];

        foreach (self::decode($employee->fingerprint_template) as $template) {
            $gallery[] = [
                'id' => (int) $employee->id,
                'template_b64' => $template,
            ];
        }

        return $gallery;
    }

    /**
     * @param  array<int, string>  $pendingTemplates
     * @return array{message:string, type:string, employee_name?:string}|null
     */
    public function findDuplicate(
        string $probeTemplate,
        BiometricBridgeService $bridge,
        ?int $employeeId = null,
        array $pendingTemplates = [],
    ): ?array {
        foreach ($pendingTemplates as $pending) {
            if ($pending === $probeTemplate) {
                return [
                    'message' => 'Ce doigt a déjà été scanné dans cette session.',
                    'type' => 'session_duplicate',
                ];
            }
        }

        $employees = Employee::query()
            ->whereNotNull('fingerprint_template')
            ->where('fingerprint_template', '!=', '')
            ->get();

        foreach ($employees as $employee) {
            foreach (self::decode($employee->fingerprint_template) as $stored) {
                if ($stored !== $probeTemplate) {
                    continue;
                }

                if ($employeeId && (int) $employee->id === $employeeId) {
                    return [
                        'message' => 'Cette empreinte est déjà enregistrée pour cet employé.',
                        'type' => 'self_duplicate',
                    ];
                }

                return [
                    'message' => 'Empreinte déjà enregistrée pour '.$employee->full_name.'.',
                    'type' => 'cross_duplicate',
                    'employee_name' => $employee->full_name,
                ];
            }
        }

        $gallery = [];
        foreach ($employees as $employee) {
            foreach (self::decode($employee->fingerprint_template) as $stored) {
                $gallery[] = [
                    'id' => (int) $employee->id,
                    'template_b64' => $stored,
                ];
            }
        }

        foreach ($pendingTemplates as $stored) {
            $gallery[] = [
                'id' => $employeeId ?? -1,
                'template_b64' => $stored,
            ];
        }

        if ($gallery === []) {
            return null;
        }

        try {
            $match = $bridge->match($probeTemplate, $gallery);
        } catch (\Throwable) {
            return null;
        }

        if (! ($match['matched'] ?? false)) {
            return null;
        }

        $score = (int) ($match['score'] ?? 0);
        $matchedId = (int) ($match['empreinte_id'] ?? -1);

        if ($score < $this->matchThreshold()) {
            return null;
        }

        if ($employeeId && $matchedId === $employeeId) {
            return [
                'message' => 'Cette empreinte correspond à un doigt déjà enregistré pour cet employé.',
                'type' => 'self_fuzzy',
            ];
        }

        $matchedEmployee = Employee::find($matchedId);
        if ($matchedEmployee) {
            return [
                'message' => 'Empreinte déjà associée à '.$matchedEmployee->full_name.' (score '.$score.').',
                'type' => 'cross_fuzzy',
                'employee_name' => $matchedEmployee->full_name,
            ];
        }

        return null;
    }

    /**
     * @param  array<int, string>  $templates
     */
    public function assertEnrollmentValid(array $templates, BiometricBridgeService $bridge, int $employeeId): void
    {
        if (count($templates) !== self::REQUIRED_FINGERS) {
            throw new \InvalidArgumentException(
                'Trois empreintes distinctes sont requises (reçu : '.count($templates).').'
            );
        }

        if (count(array_unique($templates)) !== count($templates)) {
            throw new \InvalidArgumentException('Chaque doigt doit être différent.');
        }

        $pending = [];
        foreach ($templates as $template) {
            $duplicate = $this->findDuplicate($template, $bridge, $employeeId, $pending);
            if ($duplicate) {
                throw new \InvalidArgumentException($duplicate['message']);
            }
            $pending[] = $template;
        }
    }
}

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <title>Rémunération #{{ $remuneration->id }} — {{ $remuneration->period }}</title>
    <style>
        body { font-family: DejaVu Sans, sans-serif; font-size: 12px; color: #1a2332; }
        h1 { color: #0B3D91; font-size: 18px; margin: 0 0 4px; }
        .sub { color: #5a6a7e; margin-bottom: 16px; }
        .disclaimer { background: #fffaeb; border: 1px solid #fedf89; padding: 8px 10px; margin-bottom: 16px; font-weight: bold; color: #b54708; }
        table { width: 100%; border-collapse: collapse; margin-top: 12px; }
        th, td { border: 1px solid #d8e0ec; padding: 8px 10px; text-align: left; }
        th { background: #e8eef8; color: #0B3D91; }
        .right { text-align: right; }
        .total { font-weight: bold; background: #e6f7f5; }
        .footer { margin-top: 24px; font-size: 10px; color: #5a6a7e; }
    </style>
</head>
<body>
    <h1>SGRH Pro — CNSS</h1>
    <div class="sub">Élément de rémunération indicatif #{{ $remuneration->id }}</div>

    <div class="disclaimer">{{ $disclaimer }}</div>

    <p>
        <strong>Employé :</strong> {{ $remuneration->employee?->full_name ?? '—' }}<br>
        <strong>Période :</strong> {{ $remuneration->period }}<br>
        <strong>Statut :</strong> {{ $remuneration->status }}
    </p>

    <table>
        <thead>
            <tr>
                <th>Rubrique</th>
                <th class="right">Montant</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Salaire de base</td>
                <td class="right">{{ number_format((float) $remuneration->base_salary, 2, ',', ' ') }}</td>
            </tr>
            <tr>
                <td>Prime</td>
                <td class="right">{{ number_format((float) $remuneration->bonus, 2, ',', ' ') }}</td>
            </tr>
            <tr>
                <td>Heures supplémentaires ({{ number_format((float) $remuneration->overtime_hours, 2, ',', ' ') }} h)</td>
                <td class="right">{{ number_format((float) $remuneration->overtime_amount, 2, ',', ' ') }}</td>
            </tr>
            <tr>
                <td>Retenues</td>
                <td class="right">− {{ number_format((float) $remuneration->deductions, 2, ',', ' ') }}</td>
            </tr>
            <tr class="total">
                <td>Total indicatif</td>
                <td class="right">{{ number_format((float) $remuneration->total_indicative, 2, ',', ' ') }}</td>
            </tr>
        </tbody>
    </table>

    @if($remuneration->notes)
        <p style="margin-top: 16px;"><strong>Notes :</strong> {{ $remuneration->notes }}</p>
    @endif

    <div class="footer">
        Document généré le {{ now()->format('d/m/Y H:i') }} — SGRH Pro · CNSS<br>
        {{ $disclaimer }}
    </div>
</body>
</html>

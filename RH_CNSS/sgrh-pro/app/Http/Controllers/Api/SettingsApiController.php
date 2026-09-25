<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Holiday;
use App\Models\SystemParameter;
use App\Services\ActivityLogger;
use App\Support\SpaSerializer;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class SettingsApiController extends Controller
{
    public function listParameters(): JsonResponse
    {
        $params = SystemParameter::query()->orderBy('key')->get();

        return response()->json($params->map(fn (SystemParameter $p) => SpaSerializer::parameter($p))->values());
    }

    public function getParameter(string $key): JsonResponse
    {
        $param = SystemParameter::query()->where('key', $key)->firstOrFail();

        return response()->json(SpaSerializer::parameter($param));
    }

    public function upsertParameter(Request $request, string $key): JsonResponse
    {
        $data = $request->validate([
            'value' => ['nullable'],
            'description' => ['nullable', 'string', 'max:255'],
        ]);

        $param = SystemParameter::query()->where('key', $key)->first();
        if ($param) {
            if (array_key_exists('value', $data)) {
                $param->value = is_string($data['value']) || $data['value'] === null
                    ? $data['value']
                    : json_encode($data['value']);
            }
            if (array_key_exists('description', $data)) {
                $param->description = $data['description'];
            }
            $param->save();
        } else {
            $param = SystemParameter::create([
                'key' => $key,
                'value' => array_key_exists('value', $data)
                    ? (is_string($data['value']) || $data['value'] === null ? $data['value'] : json_encode($data['value']))
                    : null,
                'description' => $data['description'] ?? null,
            ]);
        }

        ActivityLogger::log($request->user()?->username, 'Paramètre mis à jour: '.$key);

        return response()->json(SpaSerializer::parameter($param));
    }

    public function bulkUpsertParameters(Request $request): JsonResponse
    {
        $data = $request->validate([
            'parameters' => ['required', 'array'],
            'parameters.*.key' => ['required', 'string'],
            'parameters.*.value' => ['nullable'],
            'parameters.*.description' => ['nullable', 'string'],
        ]);

        $updated = [];
        foreach ($data['parameters'] as $item) {
            $param = SystemParameter::query()->where('key', $item['key'])->first();
            if ($param) {
                if (array_key_exists('value', $item)) {
                    $param->value = is_string($item['value']) || $item['value'] === null
                        ? $item['value']
                        : json_encode($item['value']);
                }
                $param->save();
            } else {
                SystemParameter::create([
                    'key' => $item['key'],
                    'value' => array_key_exists('value', $item)
                        ? (is_string($item['value']) || $item['value'] === null ? $item['value'] : json_encode($item['value']))
                        : null,
                    'description' => $item['description'] ?? null,
                ]);
            }
            $updated[] = $item['key'];
        }

        ActivityLogger::log($request->user()?->username, 'Paramètres mis à jour en masse: '.implode(', ', $updated));

        return response()->json(['updated' => $updated]);
    }

    public function listHolidays(): JsonResponse
    {
        $holidays = Holiday::query()->orderBy('date')->get();

        return response()->json($holidays->map(fn (Holiday $h) => SpaSerializer::holiday($h))->values());
    }

    public function createHoliday(Request $request): JsonResponse
    {
        $data = $request->validate([
            'name' => ['required', 'string', 'max:120'],
            'date' => ['required', 'date'],
            'is_recurring' => ['nullable', 'boolean'],
        ]);

        $holiday = Holiday::create([
            'name' => $data['name'],
            'date' => $data['date'],
            'is_recurring' => $data['is_recurring'] ?? false,
        ]);

        ActivityLogger::log($request->user()?->username, 'Jour férié créé: '.$holiday->name);

        return response()->json(SpaSerializer::holiday($holiday), 201);
    }

    public function updateHoliday(Request $request, int $holidayId): JsonResponse
    {
        $holiday = Holiday::findOrFail($holidayId);

        $data = $request->validate([
            'name' => ['sometimes', 'string', 'max:120'],
            'date' => ['sometimes', 'date'],
            'is_recurring' => ['sometimes', 'boolean'],
        ]);

        $holiday->fill($data)->save();

        return response()->json(SpaSerializer::holiday($holiday));
    }

    public function destroyHoliday(int $holidayId): JsonResponse
    {
        Holiday::findOrFail($holidayId)->delete();

        return response()->json(['message' => 'Jour férié supprimé']);
    }
}

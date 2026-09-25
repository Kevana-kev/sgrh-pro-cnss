<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;

class BiometricBridgeService
{
    public function baseUrl(): string
    {
        return rtrim(config('services.biometric.bridge_url', 'http://127.0.0.1:5002'), '/');
    }

    public function apiKey(): string
    {
        return (string) config('services.biometric.bridge_api_key', 'local-secret-key');
    }

    public function status(): array
    {
        try {
            $response = Http::timeout(2)->withOptions(['proxy' => ''])->get($this->baseUrl().'/status');

            if ($response->successful()) {
                $data = $response->json() ?? [];
                $data['connected'] = true;

                return $data;
            }
        } catch (\Throwable) {
            // Bridge offline
        }

        return ['connected' => false, 'message' => 'Bridge ZK-9500 non disponible (localhost:5002)'];
    }

    public function scan(): array
    {
        $response = Http::timeout(30)
            ->withOptions(['proxy' => ''])
            ->withHeaders([
                'X-API-KEY' => $this->apiKey(),
                'Content-Type' => 'application/json',
            ])
            ->post($this->baseUrl().'/scan', []);

        if (! $response->successful()) {
            throw new \RuntimeException($response->json('error') ?? 'Échec scan bridge (HTTP '.$response->status().')');
        }

        return $response->json() ?? [];
    }

    /**
     * 1:N match against enrolled templates via ZK SDK (bridge /match).
     *
     * @param  array<int, array{id:int, template_b64:string}>  $gallery
     */
    public function match(string $probeTemplate, array $gallery): array
    {
        $response = Http::timeout(30)
            ->withOptions(['proxy' => ''])
            ->withHeaders([
                'X-API-KEY' => $this->apiKey(),
                'Content-Type' => 'application/json',
            ])
            ->post($this->baseUrl().'/match', [
                'probe_template' => $probeTemplate,
                'gallery' => $gallery,
            ]);

        if (! $response->successful()) {
            throw new \RuntimeException($response->json('detail') ?? $response->json('error') ?? 'Échec match bridge (HTTP '.$response->status().')');
        }

        return $response->json() ?? ['matched' => false, 'empreinte_id' => -1, 'score' => 0];
    }
}

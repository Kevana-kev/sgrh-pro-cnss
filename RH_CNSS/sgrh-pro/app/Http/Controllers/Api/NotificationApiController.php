<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Contract;
use App\Models\Leave;
use App\Models\Notification;
use App\Support\SpaSerializer;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class NotificationApiController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $userId = $request->user()->id;

        $notifs = Notification::query()
            ->where(function ($q) use ($userId) {
                $q->where('user_id', $userId)->orWhereNull('user_id');
            })
            ->orderByDesc('created_at')
            ->limit(50)
            ->get();

        return response()->json($notifs->map(fn (Notification $n) => SpaSerializer::notification($n))->values());
    }

    public function unreadCount(Request $request): JsonResponse
    {
        $userId = $request->user()->id;

        $count = Notification::query()
            ->where(function ($q) use ($userId) {
                $q->where('user_id', $userId)->orWhereNull('user_id');
            })
            ->where('is_read', false)
            ->count();

        return response()->json(['count' => $count]);
    }

    public function markRead(int $notifId): JsonResponse
    {
        $notif = Notification::findOrFail($notifId);
        $notif->is_read = true;
        $notif->save();

        return response()->json(['message' => 'Marquée comme lue']);
    }

    public function markAllRead(Request $request): JsonResponse
    {
        $userId = $request->user()->id;

        Notification::query()
            ->where(function ($q) use ($userId) {
                $q->where('user_id', $userId)->orWhereNull('user_id');
            })
            ->update(['is_read' => true]);

        return response()->json(['message' => 'Toutes marquées comme lues']);
    }

    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'title' => ['required', 'string', 'max:160'],
            'message' => ['required', 'string', 'max:1000'],
            'user_id' => ['nullable', 'exists:users,id'],
            'type' => ['nullable', 'string', 'max:50'],
        ]);

        $notif = Notification::create([
            'user_id' => $data['user_id'] ?? null,
            'type' => $data['type'] ?? 'info',
            'title' => $data['title'],
            'message' => $data['message'],
        ]);

        return response()->json(SpaSerializer::notification($notif), 201);
    }

    public function destroy(int $notifId): JsonResponse
    {
        Notification::findOrFail($notifId)->delete();

        return response()->json(['message' => 'Notification supprimée']);
    }

    public function generateAlerts(): JsonResponse
    {
        $today = now()->startOfDay();
        $in30 = now()->addDays(30)->endOfDay();
        $created = 0;

        $contracts = Contract::query()
            ->with('employee')
            ->whereNotNull('end_date')
            ->whereBetween('end_date', [$today, $in30])
            ->get();

        foreach ($contracts as $c) {
            $emp = $c->employee;
            if (! $emp) {
                continue;
            }

            $title = 'Contrat expirant bientôt — '.$emp->first_name.' '.$emp->last_name;
            $exists = Notification::query()
                ->where('type', 'contract_expiry')
                ->where('title', $title)
                ->whereDate('created_at', $today)
                ->exists();

            if (! $exists) {
                Notification::create([
                    'type' => 'contract_expiry',
                    'title' => $title,
                    'message' => "Le contrat de {$emp->first_name} {$emp->last_name} expire le {$c->end_date->format('Y-m-d')}.",
                ]);
                $created++;
            }
        }

        $pendingLeaves = Leave::query()->where('status', 'En attente')->get();
        foreach ($pendingLeaves as $lv) {
            $age = $lv->created_at ? $lv->created_at->diffInDays(now()) : 0;
            if ($age <= 3) {
                continue;
            }

            $title = 'Congé en attente — Employé #'.$lv->employee_id;
            $exists = Notification::query()
                ->where('type', 'leave_pending')
                ->where('title', $title)
                ->whereDate('created_at', $today)
                ->exists();

            if (! $exists) {
                Notification::create([
                    'type' => 'leave_pending',
                    'title' => $title,
                    'message' => 'Une demande de congé est en attente depuis plus de 3 jours.',
                ]);
                $created++;
            }
        }

        return response()->json(['message' => "{$created} alerte(s) générée(s)"]);
    }
}

<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Message;
use App\Models\User;
use App\Services\ActivityLogger;
use App\Support\SpaSerializer;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class MessageApiController extends Controller
{
    private const EDIT_WINDOW_MINUTES = 15;

    public function recipients(Request $request): JsonResponse
    {
        $userId = $request->user()->id;

        $recipients = User::query()
            ->with('employee')
            ->where('id', '!=', $userId)
            ->orderBy('username')
            ->get()
            ->map(function (User $u) {
                $name = $u->employee
                    ? trim($u->employee->first_name.' '.$u->employee->last_name)
                    : $u->username;

                return [
                    'id' => $u->id,
                    'username' => $u->username,
                    'name' => $name !== '' ? $name : $u->username,
                    'employee_id' => $u->employee_id,
                ];
            })
            ->values();

        return response()->json($recipients);
    }

    public function inbox(Request $request): JsonResponse
    {
        $userId = $request->user()->id;
        $limit = (int) ($request->query('limit', 100) ?: 100);

        $messages = Message::query()
            ->with(['sender.employee', 'recipient.employee'])
            ->where('recipient_user_id', $userId)
            ->orderByDesc('sent_at')
            ->limit($limit)
            ->get();

        return response()->json($messages->map(fn (Message $m) => $this->serializeForUser($m, $userId))->values());
    }

    public function sent(Request $request): JsonResponse
    {
        $userId = $request->user()->id;
        $limit = (int) ($request->query('limit', 100) ?: 100);

        $messages = Message::query()
            ->with(['sender.employee', 'recipient.employee'])
            ->where('sender_user_id', $userId)
            ->orderByDesc('sent_at')
            ->limit($limit)
            ->get();

        return response()->json($messages->map(fn (Message $m) => $this->serializeForUser($m, $userId))->values());
    }

    public function unreadCount(Request $request): JsonResponse
    {
        $count = Message::query()
            ->where('recipient_user_id', $request->user()->id)
            ->whereNull('read_at')
            ->count();

        return response()->json(['unread_count' => $count]);
    }

    public function conversations(Request $request): JsonResponse
    {
        $userId = $request->user()->id;
        $q = trim((string) $request->query('q', ''));

        $messages = Message::query()
            ->with(['sender.employee', 'recipient.employee'])
            ->where(function ($query) use ($userId) {
                $query->where('sender_user_id', $userId)->orWhere('recipient_user_id', $userId);
            })
            ->orderByDesc('sent_at')
            ->get();

        $conversations = [];
        foreach ($messages as $message) {
            $otherId = $message->sender_user_id === $userId
                ? $message->recipient_user_id
                : $message->sender_user_id;

            if (isset($conversations[$otherId])) {
                continue;
            }

            $other = $message->sender_user_id === $userId ? $message->recipient : $message->sender;
            $name = $other?->employee
                ? trim($other->employee->first_name.' '.$other->employee->last_name)
                : ($other?->username ?? '-');

            if ($q !== '' && ! str_contains(strtolower($name.' '.$other?->username), strtolower($q))) {
                continue;
            }

            $conversations[$otherId] = [
                'user_id' => $otherId,
                'username' => $other?->username,
                'name' => $name,
                'last_message' => $message->content,
                'last_sent_at' => optional($message->sent_at)?->toIso8601String(),
                'unread_count' => Message::query()
                    ->where('sender_user_id', $otherId)
                    ->where('recipient_user_id', $userId)
                    ->whereNull('read_at')
                    ->count(),
            ];
        }

        return response()->json(array_values($conversations));
    }

    public function thread(Request $request, int $otherUserId): JsonResponse
    {
        $userId = $request->user()->id;
        $limit = (int) ($request->query('limit', 200) ?: 200);
        $beforeId = $request->query('before_id');

        Message::query()
            ->where('sender_user_id', $otherUserId)
            ->where('recipient_user_id', $userId)
            ->whereNull('read_at')
            ->update(['read_at' => now()]);

        $query = Message::query()
            ->with(['sender.employee', 'recipient.employee'])
            ->where(function ($q) use ($userId, $otherUserId) {
                $q->where(function ($inner) use ($userId, $otherUserId) {
                    $inner->where('sender_user_id', $userId)->where('recipient_user_id', $otherUserId);
                })->orWhere(function ($inner) use ($userId, $otherUserId) {
                    $inner->where('sender_user_id', $otherUserId)->where('recipient_user_id', $userId);
                });
            })
            ->orderByDesc('id');

        if ($beforeId && ctype_digit((string) $beforeId)) {
            $query->where('id', '<', (int) $beforeId);
        }

        $messages = $query->limit($limit)->get()->sortBy('id')->values();

        return response()->json($messages->map(fn (Message $m) => $this->serializeForUser($m, $userId))->values());
    }

    public function sendThread(Request $request, int $otherUserId): JsonResponse
    {
        $data = $request->validate([
            'content' => ['required', 'string', 'max:2000'],
            'subject' => ['nullable', 'string', 'max:160'],
        ]);

        User::findOrFail($otherUserId);

        $message = Message::create([
            'sender_user_id' => $request->user()->id,
            'recipient_user_id' => $otherUserId,
            'subject' => $data['subject'] ?? null,
            'content' => $data['content'],
            'sent_at' => now(),
        ]);

        ActivityLogger::log($request->user()?->username, 'Envoi message thread #'.$message->id);

        return response()->json($this->serializeForUser($message->fresh(['sender.employee', 'recipient.employee']), $request->user()->id), 201);
    }

    public function store(Request $request): JsonResponse
    {
        $data = $request->validate([
            'recipient_user_id' => ['required', 'exists:users,id'],
            'content' => ['required', 'string', 'max:2000'],
            'subject' => ['nullable', 'string', 'max:160'],
        ]);

        $message = Message::create([
            'sender_user_id' => $request->user()->id,
            'recipient_user_id' => $data['recipient_user_id'],
            'subject' => $data['subject'] ?? null,
            'content' => $data['content'],
            'sent_at' => now(),
        ]);

        ActivityLogger::log($request->user()?->username, 'Envoi message #'.$message->id);

        return response()->json($this->serializeForUser($message->fresh(['sender.employee', 'recipient.employee']), $request->user()->id), 201);
    }

    public function markRead(Request $request, int $messageId): JsonResponse
    {
        $message = Message::findOrFail($messageId);

        if ($message->recipient_user_id !== $request->user()->id) {
            return response()->json(['error' => 'Accès refusé'], 403);
        }

        if (! $message->read_at) {
            $message->read_at = now();
            $message->save();
        }

        return response()->json($this->serializeForUser($message, $request->user()->id));
    }

    public function update(Request $request, int $messageId): JsonResponse
    {
        $message = Message::findOrFail($messageId);
        $userId = $request->user()->id;

        if ($this->remainingSeconds($userId, $message) <= 0) {
            return response()->json(['error' => 'Délai de modification dépassé'], 403);
        }

        $data = $request->validate([
            'content' => ['sometimes', 'string', 'max:2000'],
            'subject' => ['nullable', 'string', 'max:160'],
        ]);

        $message->fill($data);
        $message->edited_at = now();
        $message->save();

        return response()->json($this->serializeForUser($message, $userId));
    }

    public function destroy(Request $request, int $messageId): JsonResponse
    {
        $message = Message::findOrFail($messageId);
        $userId = $request->user()->id;

        if ($this->remainingSeconds($userId, $message) <= 0) {
            return response()->json(['error' => 'Délai de suppression dépassé'], 403);
        }

        $message->delete();

        return response()->json(['message' => 'Message supprimé']);
    }

    private function serializeForUser(Message $message, int $userId): array
    {
        $payload = SpaSerializer::message($message);
        $remaining = $this->remainingSeconds($userId, $message);
        $payload['can_edit'] = $remaining > 0;
        $payload['can_delete'] = $remaining > 0;
        $payload['edit_delete_remaining_seconds'] = $remaining;
        $payload['edit_delete_window_minutes'] = self::EDIT_WINDOW_MINUTES;

        return $payload;
    }

    private function remainingSeconds(int $userId, Message $message): int
    {
        if ($message->sender_user_id !== $userId) {
            return 0;
        }

        $deadline = $message->sent_at->copy()->addMinutes(self::EDIT_WINDOW_MINUTES);

        return max(0, $deadline->getTimestamp() - now()->getTimestamp());
    }
}

# SGRH Pro — CNSS (Laravel)

Application de gestion des ressources humaines pour la **CNSS** (Kinshasa).

## Interface

L’UI principale est l’**ancienne SPA 14 modules** (`dashboard.html` / CSS / JS), servie par Laravel :

- **URL :** http://127.0.0.1:8000/
- **API JSON :** `/api/*` (compatible Flask + Sanctum Bearer token)

Les pages Blade « classiques » restent sous `/classic/...` si besoin.

## Modules UI (comme avant)

Employés, départements, rôles, contrats, présences, congés, biométrie ZK-9500, congés médicaux, formations, évaluations, recrutement, paie, comptabilité, messages, notifications, comptes, rapports, paramètres.

## Comptes de démonstration

| Utilisateur   | Mot de passe     | Rôle        |
|---------------|------------------|-------------|
| `superadmin`  | `superadmin123`  | SuperAdmin  |
| `adminrh`     | `adminrh123`     | Admin RH    |
| `manager`     | `manager123`     | Manager     |
| `agent`       | `Agent@123`      | Employé     |

## Installation locale

```bash
cd RH_CNSS/sgrh-pro
composer install
copy .env.example .env
php artisan key:generate
php artisan migrate --seed
php artisan storage:link
php artisan serve
```

Ouvrir : http://127.0.0.1:8000

## Biométrie ZK-9500

Bridge local : `RH_CNSS/fingerprint-service/` sur le port **5002**.

```bash
cd fingerprint-service/APP_DESK/bin/Release/net7.0-windows
set FINGERPRINT_BRIDGE_API_KEY=local-secret-key
set FINGERPRINT_BRIDGE_FORCE_DEVICE=1
dotnet FingerprintBridge.dll --headless
```

Ne pas activer `FINGERPRINT_BRIDGE_ALLOW_MOCK` si le lecteur est branché.

## Hostinger

Document root = dossier `public/`. Configurer MySQL via `.env` (voir `.env.example`).

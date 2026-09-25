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

## Railway.com

Le dépôt GitHub est déployable. **Root Directory** à indiquer dans Railway :

```
RH_CNSS/sgrh-pro
```

### Étapes

1. Nouveau projet Railway → **Deploy from GitHub** → `Kevana-kev/sgrh-pro-cnss`
2. Settings → **Root Directory** = `RH_CNSS/sgrh-pro`
3. Ajouter un plugin **MySQL**
4. Variables d’environnement (Variables) :

| Variable | Valeur |
|----------|--------|
| `APP_NAME` | `SGRH Pro` |
| `APP_ENV` | `production` |
| `APP_DEBUG` | `false` |
| `APP_KEY` | générer localement : `php artisan key:generate --show` |
| `APP_URL` | URL Railway (ex. `https://….up.railway.app`) |
| `DB_CONNECTION` | `mysql` |
| `DB_HOST` | `${{MySQL.MYSQLHOST}}` |
| `DB_PORT` | `${{MySQL.MYSQLPORT}}` |
| `DB_DATABASE` | `${{MySQL.MYSQLDATABASE}}` |
| `DB_USERNAME` | `${{MySQL.MYSQLUSER}}` |
| `DB_PASSWORD` | `${{MySQL.MYSQLPASSWORD}}` |
| `SEED_ON_BOOT` | `true` **une seule fois** (premier déploiement), puis `false` |

5. Deploy. Les migrations tournent au démarrage (`Dockerfile` + `docker/railway-start.sh`).

### Limite importante

Le **bridge biométrique ZK-9500** (Windows + USB, port 5002) **ne tourne pas sur Railway**.  
L’app web (login, RH, congés, dashboard…) fonctionne ; le pointage empreinte reste sur un **PC local** connecté au lecteur.

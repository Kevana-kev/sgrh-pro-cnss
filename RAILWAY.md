# Déploiement Railway — SGRH Pro

Repo : https://github.com/Kevana-kev/sgrh-pro-cnss

## Pourquoi le build a échoué

Railway a tenté **Railpack** sur la **racine** du dépôt (mémoire + scripts + app).
Sans `Dockerfile` à la racine, il ne détecte pas Laravel → `Railpack failed to prepare the build`.

De plus : **0 Variables** → même un build réussi ne démarrerait pas sans `APP_KEY` + MySQL.

## Correction (déjà poussée)

- `Dockerfile` à la **racine**
- `railway.toml` force `builder = "DOCKERFILE"`

## Étapes dans Railway (à faire maintenant)

### 1. Settings du service `sgrh-pro-cnss`

- **Root Directory** : laisser **vide** (racine du repo)  
  OU mettre `RH_CNSS/sgrh-pro` si tu utilises le Dockerfile interne
- **Builder** : Docker (détecté via `railway.toml`)

### 2. Ajouter MySQL

Add → Database → MySQL

### 3. Variables (Variables) — obligatoire

| Variable | Valeur |
|----------|--------|
| `APP_NAME` | `SGRH Pro` |
| `APP_ENV` | `production` |
| `APP_DEBUG` | `false` |
| `APP_KEY` | `base64:E5ke1YNgPSEspJIu085MZspWZB48ko2Bb5HRkuvkawk=` |
| `APP_URL` | ton URL Railway (après premier deploy) |
| `DB_CONNECTION` | `mysql` |
| `DB_HOST` | `${{MySQL.MYSQLHOST}}` |
| `DB_PORT` | `${{MySQL.MYSQLPORT}}` |
| `DB_DATABASE` | `${{MySQL.MYSQLDATABASE}}` |
| `DB_USERNAME` | `${{MySQL.MYSQLUSER}}` |
| `DB_PASSWORD` | `${{MySQL.MYSQLPASSWORD}}` |
| `SEED_ON_BOOT` | `true` (1er deploy), puis `false` |

### 4. Redeploy

Deployments → Redeploy (ou push sur `main`)

## Limite

Le lecteur **ZK-9500** ne tourne pas sur Railway (USB Windows local uniquement).

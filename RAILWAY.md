# Déploiement Railway — SGRH Pro
# Repo : https://github.com/Kevana-kev/sgrh-pro-cnss

## Erreur « Railpack could not determine how to build »

Railway analyse la **racine** du monorepo (MEMOIRE, scripts…) et ne trouve pas Laravel.
**Correction poussée** : `railpack.json` + `composer.json` + `start.sh` à la racine.

## Action OBLIGATOIRE dans l’interface Railway

### Option A (recommandée) — Root Directory

1. Service `sgrh-pro-cnss` → **Settings**
2. **Root Directory** = `RH_CNSS/sgrh-pro`
3. **Builder** = Railpack **ou** Dockerfile
4. **Redeploy**

Avec ce Root Directory, Railway ne voit que l’app Laravel.

### Option B — Docker à la racine

1. Settings → **Builder** = **Dockerfile** (pas Railpack)
2. Dockerfile path = `Dockerfile`
3. Root Directory = **vide**
4. Redeploy

### Variables (toujours)

| Variable | Valeur |
|----------|--------|
| `APP_KEY` | `base64:E5ke1YNgPSEspJIu085MZspWZB48ko2Bb5HRkuvkawk=` |
| `APP_ENV` | `production` |
| `APP_DEBUG` | `false` |
| `APP_URL` | URL `.up.railway.app` |
| `DB_CONNECTION` | `mysql` |
| `DB_HOST` | `${{MySQL.MYSQLHOST}}` |
| `DB_PORT` | `${{MySQL.MYSQLPORT}}` |
| `DB_DATABASE` | `${{MySQL.MYSQLDATABASE}}` |
| `DB_USERNAME` | `${{MySQL.MYSQLUSER}}` |
| `DB_PASSWORD` | `${{MySQL.MYSQLPASSWORD}}` |
| `SEED_ON_BOOT` | `true` puis `false` |

Ajoute aussi un plugin **MySQL**.

## Limite

ZK-9500 (USB) ne tourne pas sur Railway.

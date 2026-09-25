# Déploiement Railway — SGRH Pro

**App en ligne :** https://sgrh-pro-cnss-production.up.railway.app  
**Repo :** https://github.com/Kevana-kev/sgrh-pro-cnss  
**Projet Railway :** `alluring-vitality` / service `sgrh-pro-cnss`

## Configuration qui fonctionne

| Setting | Valeur |
|---------|--------|
| Root Directory | `RH_CNSS` |
| Builder | Dockerfile |
| Dockerfile | `Dockerfile` (racine du repo, chemins relatifs à `RH_CNSS/`) |
| MySQL | plugin Railway attaché |

Le Dockerfile racine fait `COPY sgrh-pro/ /app/` car le contexte Docker = dossier `RH_CNSS`.

## Variables requises

| Variable | Valeur |
|----------|--------|
| `APP_KEY` | (généré, déjà défini sur Railway) |
| `APP_ENV` | `production` |
| `APP_DEBUG` | `false` |
| `APP_URL` | `https://sgrh-pro-cnss-production.up.railway.app` |
| `DB_*` | refs `${{MySQL.*}}` |
| `SEED_ON_BOOT` | `false` (mettre `true` une fois pour recharger la démo) |

## Biométrie en ligne (Railway)

L’app cloud ne peut pas voir le USB. Le **navigateur** parle au bridge local :

1. Branchez le ZK-9500 sur le PC de démo
2. Démarrez `Fingerprint Bridge` (port **5002**) — rebuild recommandé après CORS
3. Ouvrez https://sgrh-pro-cnss-production.up.railway.app sur **ce même PC**
4. Enrôlement / pointage empreinte fonctionnent via `localhost:5002`

Variable utile : `BIOMETRIC_BRIDGE_API_KEY=local-secret-key` (app + bridge).

## Limite

Sans bridge démarré sur le PC qui ouvre le site, l’empreinte reste indisponible (RFID OK).

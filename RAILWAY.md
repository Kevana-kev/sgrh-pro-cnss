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

1. Sur le PC Windows du terminal : lancer **`RH_CNSS/fingerprint-service/installer/INSTALLER.bat`**
2. Brancher le ZK-9500
3. Ouvrir https://sgrh-pro-cnss-production.up.railway.app **sur ce PC**
4. Clic **Empreinte** → le site déclenche `sgrhbridge://start` → bridge en arrière-plan → scan

L’installeur enregistre le protocole, le démarrage auto et la clé `local-secret-key`.

## Limite

Sans l’installeur Windows sur le PC qui ouvre le site, l’empreinte ne peut pas parler au lecteur USB (RFID OK).

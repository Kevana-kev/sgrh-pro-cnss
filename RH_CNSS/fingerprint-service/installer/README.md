# SGRH Pro — Fingerprint Bridge (installation one-touch)

## Objectif

Sur **chaque PC Windows** du terminal de pointage (accueil CNSS) :

1. Brancher le lecteur **ZK-9500**
2. Double-cliquer **`INSTALLER.bat`**
3. C’est tout — le bridge démarre, se relance à chaque ouverture de session, et écoute sur `http://127.0.0.1:5002`

## Contenu du dossier `installer/`

| Fichier | Rôle |
|---|---|
| `INSTALLER.bat` | **One-touch** (élévation UAC + install) |
| `Install-SgrhBridge.ps1` | Script d’installation |
| `Uninstall-SgrhBridge.ps1` | Désinstallation |
| `Build-Payload.ps1` | Rebuild du payload self-contained |
| `payload/` | Binaires bridge (générés) |
| `vendor/zk/` | **DLL SDK ZKFinger** à déposer ici |

## Préparation (une seule fois chez le développeur)

1. Installer le **SDK / driver ZKFinger** sur le PC de build (pour récupérer les DLL).
2. Copier dans `vendor/zk/` au minimum :
   - `libzkfpcsharp.dll`
   - `libzkfp.dll` (et dépendances natives fournies par ZK)
3. Lancer `Build-Payload.ps1` **ou** laisser `INSTALLER.bat` le faire.
4. Zipper tout le dossier `installer/` → distribution aux postes CNSS.

> Les DLL ZKTeco sont propriétaires : on ne les commit pas dans Git. Elles doivent être dans `vendor/zk/` avant distribution.

## Sur chaque PC de pointage

1. Windows 10/11 (x64 OK — le bridge est publié en **win-x86** pour le SDK ZK).
2. Brancher le ZK-9500 (driver USB déjà inclus si `vendor/zk` + install SDK fait, sinon installer le driver ZK une fois).
3. Exécuter `INSTALLER.bat` en admin.
4. Vérifier : navigateur → [http://127.0.0.1:5002/status](http://127.0.0.1:5002/status) → `{"status":"ok"}`

## Ce que l’installateur configure automatiquement

- Copie dans `C:\Program Files\SGRH Pro\FingerprintBridge`
- Variables machine :
  - `FINGERPRINT_BRIDGE_API_KEY=local-secret-key`
  - `FINGERPRINT_BRIDGE_FORCE_DEVICE=1`
- Démarrage auto (Startup + tâche planifiée ONLOGON)
- Pare-feu TCP **5002**
- Raccourcis bureau / menu Démarrer
- Lancement immédiat du mode `--headless`

## Alignement Laravel (SGRH Pro)

Dans `.env` du serveur / PC app :

```env
BIOMETRIC_BRIDGE_URL=http://127.0.0.1:5002
BIOMETRIC_BRIDGE_API_KEY=local-secret-key
```

Le navigateur qui fait le pointage doit tourner **sur le même PC** que le bridge (localhost).

## Désinstallation

Exécuter `Uninstall-SgrhBridge.ps1` en administrateur, ou le script copié dans le dossier d’installation.

## Limites honnêtes

- **Windows uniquement** (pas Mac/Linux).
- Le **driver USB ZK** doit être présent (souvent fourni avec le SDK ZKFinger Explorer).
- Sans DLL dans `vendor/zk` / SysWOW64, l’app s’installe quand même mais le **scan échouera** jusqu’à ajout des DLL + réinstall.

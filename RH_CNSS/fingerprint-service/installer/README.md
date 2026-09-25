# SGRH Pro — Fingerprint Bridge (installation one-touch)

## Objectif

Sur **chaque PC Windows** du terminal de pointage :

1. Brancher le lecteur **ZK-9500**
2. Double-cliquer **`INSTALLER.bat`**
3. Ouvrir le site SGRH (local ou Railway) **sur ce PC**
4. Clic **Empreinte digitale** → le bridge démarre tout seul en arrière-plan (`sgrhbridge://`)

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

1. Installer le **SDK / driver ZKFinger** sur le PC de build.
2. Copier dans `vendor/zk/` : `libzkfpcsharp.dll`, `libzkfp.dll`, etc.
3. Lancer `Build-Payload.ps1` **ou** laisser `INSTALLER.bat` le faire.
4. Zipper le dossier `installer/` → distribution postes CNSS.

## Sur chaque PC de pointage

1. Windows 10/11 + ZK-9500 branché
2. Exécuter `INSTALLER.bat` en admin
3. Vérifier : [http://127.0.0.1:5002/status](http://127.0.0.1:5002/status) → `{"status":"ok"}`
4. Site web : clic Empreinte → le navigateur ouvre `sgrhbridge://start` → bridge headless

## Ce que l’installateur configure

- Copie dans `C:\Program Files\SGRH Pro\FingerprintBridge`
- `FINGERPRINT_BRIDGE_API_KEY=local-secret-key`
- Démarrage auto (Startup + tâche ONLOGON)
- Pare-feu TCP **5002**
- Protocoles URL : **`sgrhbridge://`** et **`sgrh-fingerprint://`**
- Lancement immédiat en `--headless`

## Alignement site web (Railway / local)

```env
BIOMETRIC_BRIDGE_URL=http://127.0.0.1:5002
BIOMETRIC_BRIDGE_API_KEY=local-secret-key
```

Le **navigateur** doit être sur le **même PC** que le bridge (localhost + protocole).

## Désinstallation

`Uninstall-SgrhBridge.ps1` (admin) — retire aussi les protocoles URL.

## Limites

- Windows uniquement
- Driver USB ZK requis
- Chrome/Edge peut demander « Ouvrir FingerprintBridge ? » la première fois → cocher « Toujours autoriser »

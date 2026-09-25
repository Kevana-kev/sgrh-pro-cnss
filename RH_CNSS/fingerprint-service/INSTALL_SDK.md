Installation du SDK ZKFinger pour le bridge d'empreintes

But : retirer les gros binaires du dépôt et documenter l'installation locale du SDK nécessaire pour que l'application desktop `APP_DESK` fonctionne.

Prérequis
- Windows (l'application bridge est WinForms/.NET)
- Accès au SDK ZKTeco (ZKFinger Standard SDK) fourni par le fabricant. Le SDK n'est pas contenu dans ce dépôt pour éviter de committer des binaires/vendor.

Étapes d'installation (manuelle)
1. Téléchargez le SDK ZKFinger (ou le SDK ZKTeco fourni) depuis le fournisseur officiel ou votre archive interne.
2. Sur la machine où sera exécuté le bridge, copiez les fichiers nécessaires dans le répertoire de l'application bridge `fingerprint_service/APP_DESK/` (ou dans le dossier de sortie de build, ex. `bin/Debug/` après compilation). Les fichiers typiquement nécessaires :
   - `Interop.ZKFPEngXControl.dll` (interop/ActiveX)
   - `AxInterop.ZKFPEngXControl.dll` (le cas échéant)
   - `libzkfpcsharp.dll` (wrapper natif .NET) ou tout autre DLL natif fourni par le SDK
   - Eventuellement d'autres DLLs fournis par le SDK (vérifiez la documentation du SDK)


3. Construisez l'application bridge (Visual Studio recommandé) ou utilisez le script fourni pour créer une distribution prête à l'emploi.

Build & packaging (maintainers)
--------------------------------
Placez les DLL du SDK dans `fingerprint_service/vendor/` (ce dossier est ignoré par Git). Ensuite, exécutez le script suivant depuis la racine du dépôt pour créer une archive ZIP plug-and-play :

```powershell
cd <repo-root>\fingerprint_service\installer
.\build_distribution.ps1
```

Le script réalisera un `dotnet publish` du projet WinForms et copiera les DLL du dossier `vendor/` dans la distribution, puis créera `fingerprint_service\dist\FingerprintBridge-<timestamp>.zip`.

4. Déploiement sur la machine cible

Copiez le ZIP sur la machine cible et exécutez le script d'installation (nécessite PowerShell) :

```powershell
cd C:\où\vous\avez\copié\le\zip
Expand-Archive -Path FingerprintBridge-<timestamp>.zip -DestinationPath 'C:\Program Files\FingerprintBridge'
# ou utilisez le script d'installation fourni
\path\to\repo\fingerprint_service\installer\install.ps1 -ZipPath 'C:\path\to\FingerprintBridge-<timestamp>.zip' -CreateStartupShortcut
```

Le script `install.ps1` peut aussi copier des DLL depuis un partage réseau si vous fournissez `-SdkShare`.

5. Configurez la connexion au backend (exemple pour enregistrer tokens) :

```powershell
# Remplacez les valeurs ci-dessous
curl -X POST http://localhost:5002/configure-server \
  -H "X-API-KEY: <LOCAL_API_KEY>" -H "Content-Type: application/json" \
  -d '{"serverUrl":"https://your-backend","accessToken":"<ACCESS>","refreshToken":"<REFRESH>","userId":3}'
```

Notes & sécurité
- Ne commitez jamais le SDK ou ses installeurs dans le dépôt. Utilisez des artefacts internes ou un stockage sécurisé (artifactory, sharepoint interne) pour distribuer le SDK.
- Par défaut, les mock-templates et auto-mode sont désactivés. N'activez les flags `FINGERPRINT_BRIDGE_ALLOW_*` qu'en développement.
- La clé API locale et la config serveur sont stockées chiffrées via DPAPI (CurrentUser). Si vous prévoyez d'exécuter le bridge en tant que service système, envisagez une autre méthode de stockage (Machine scope ou KeyVault).

Déploiement recommandé
- Installer le SDK et les DLLs via un installeur (MSI) ou script d'installation pour chaque machine.
- Packager l'application bridge en MSI/EXE via un outil de packaging (WiX, InnoSetup) et inclure une étape qui copie les DLL nécessaires.

Support
- Si vous avez besoin que j'automatise l'installation (script PowerShell pour copier les DLL depuis un emplacement réseau), dites-le et je peux ajouter un script `fingerprint_service/scripts/install_sdk.ps1`.

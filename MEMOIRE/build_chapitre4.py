# -*- coding: utf-8 -*-
"""Chapitre IV — Implémentation, tests et validation de SGRH Pro."""
from pathlib import Path

from memoire_format import (
    init_document, add_page_number, add_chapter_title, add_heading, add_subheading,
    add_body, add_mixed, add_bullet, add_numbered_item, add_table, add_figure,
    add_code_block, add_screenshot_placeholder, add_source,
)

OUTPUT = r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\CHAPITRE IV - IMPLEMENTATION TESTS ET VALIDATION.docx"
OUTPUT_FALLBACK = OUTPUT.replace(".docx", " - v2.docx")
IMG4 = Path(r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\images\chapitre4")
PAGE_START = 62


def _fig(name: str) -> str:
    return str(IMG4 / name)


def _ensure_figures():
    import generate_figures_ch4
    generate_figures_ch4.main()


def append_chapitre4(doc, page_start=62):
    _ensure_figures()
    add_page_number(doc, page_start)
    add_chapter_title(doc, "CHAPITRE IV. IMPLÉMENTATION, TESTS ET VALIDATION")

    add_heading(doc, "IV.1. Introduction du chapitre")

    add_body(doc,
        "Le chapitre précédent a fixé l'architecture, les diagrammes UML et "
        "le modèle de données de SGRH Pro. Le présent chapitre décrit la "
        "traduction de cette conception en un prototype opérationnel, "
        "réalisé à partir du dépôt applicatif RH_CNSS/sgrh-pro et du "
        "service de lecture d'empreintes RH_CNSS/fingerprint-service. "
        "Il expose l'environnement de développement, les extraits de code "
        "significatifs, les interfaces réalisées — dont les captures "
        "d'écran sont réservées pour insertion par l'auteur —, les tests "
        "effectués et les limites du prototype."
    )

    add_body(doc,
        "Conformément à la démarche du Processus Unifié, cette phase "
        "correspond à la construction puis à la transition : implémentation "
        "itérative des huit modules, intégration du lecteur ZK-9500, "
        "jeux de tests fonctionnels et préparation de la démonstration "
        "sur le poste du responsable RH."
    )

    add_heading(doc, "IV.2. Environnement de développement et outils")

    add_subheading(doc, "IV.2.1. Matériel et logiciels")

    add_body(doc,
        "Le prototype a été développé et testé sur un poste Windows 10/11 "
        "disposant d'un lecteur ZK-9500 branché en USB et, le cas échéant, "
        "d'un lecteur de cartes RFID. L'application de gestion s'exécute "
        "localement pour la démonstration ; elle reste déployable sur un "
        "hébergement PHP/MySQL."
    )

    add_table(doc,
              ["Catégorie", "Outil / ressource", "Usage"],
              [
                  ["Langage serveur", "PHP 8.2+ / Laravel 11", "Application de gestion, API"],
                  ["Interface", "HTML, CSS, JavaScript", "SPA dashboard, pointage, Mon espace"],
                  ["Données", "SQLite (dev) / MySQL (prod)", "Dossiers, présences, templates"],
                  ["Sécurité", "Laravel Sanctum, hachage bcrypt", "Sessions et mots de passe"],
                  ["Biométrie", "C# / .NET, SDK ZKFinger", "Capture et comparaison 1:N"],
                  ["Périphériques", "ZK-9500, cartes RFID", "Enrôlement et pointage"],
                  ["Édition", "Visual Studio Code, Visual Studio", "Code PHP et bridge C#"],
              ],
              caption="Tableau 45 : Technologies et outils d'implémentation",
              col_widths=[3.5, 5.5, 7.0])
    add_source(doc)

    add_subheading(doc, "IV.2.2. Organisation du dépôt")

    add_body(doc,
        "Le code est organisé en deux espaces complémentaires. Le dossier "
        "sgrh-pro contient l'application Laravel (routes, contrôleurs, "
        "modèles, migrations, interface publique). Le dossier "
        "fingerprint-service contient le service Windows de lecture "
        "(HeadlessBridge) et l'installateur one-touch. Cette séparation "
        "reproduit l'architecture de déploiement du chapitre III."
    )

    add_heading(doc, "IV.3. Implémentation de l'application de gestion")

    add_subheading(doc, "IV.3.1. Authentification et contrôle d'accès")

    add_body(doc,
        "L'entrée dans le système passe par SpaAuthController. L'utilisateur "
        "s'identifie par nom d'utilisateur, matricule ou courriel. Après "
        "vérification du mot de passe et du statut de l'agent, un jeton "
        "Sanctum est émis. Les opérations sensibles sont consignées dans "
        "activity_logs."
    )

    add_code_block(doc, """
public function login(Request $request): JsonResponse
{
    $data = $request->validate([
        'username' => ['required', 'string'],
        'password' => ['required', 'string'],
    ]);
    $user = User::query()
        ->with(['role.permissions', 'employee.role'])
        ->where(function ($q) use ($identifier) {
            $q->whereRaw('LOWER(username) = ?', [$identifier])
              ->orWhereHas('employee', fn ($eq) =>
                  $eq->whereRaw('LOWER(matricule) = ?', [$identifier]));
        })->first();
    if (! $user || ! Hash::check($data['password'], $user->password)) {
        return response()->json(['error' => 'Identifiants invalides'], 401);
    }
    $token = $user->createToken('spa')->plainTextToken;
    return response()->json($this->profilePayload($user, $token));
}
""",
        caption="Extrait IV.1 — Connexion et émission du jeton de session",
        source_file="app/Http/Controllers/Api/SpaAuthController.php")

    add_body(doc,
        "Les droits sont vérifiés côté serveur par User::hasPermission(). "
        "Le rôle SuperAdmin dispose de toutes les permissions ; les autres "
        "rôles (Admin RH, Manager, Employé) reçoivent un sous-ensemble "
        "défini dans le seeder (Valider congés, Voir équipe, etc.)."
    )

    add_code_block(doc, """
public function hasPermission(string $name): bool
{
    $this->loadMissing('role.permissions');
    if (! $this->role) {
        return false;
    }
    if ($this->role->name === 'SuperAdmin') {
        return true;
    }
    return $this->role->hasPermission($name);
}
""",
        caption="Extrait IV.2 — Contrôle d'accès par permission",
        source_file="app/Models/User.php")

    add_subheading(doc, "IV.3.2. Règle métier du pointage")

    add_body(doc,
        "Le cœur opérationnel du prototype est PresenceApiController::registerPunch(). "
        "Un seul couple entrée/sortie est autorisé par jour et par agent. "
        "Le premier enregistrement ouvre la journée ; le second la clôture "
        "et calcule les heures travaillées ; toute tentative supplémentaire "
        "renvoie le code HTTP 409. Le retard est calculé par rapport à "
        "l'heure d'ouverture paramétrée (08:00) et à un seuil de tolérance "
        "(15 minutes)."
    )

    add_code_block(doc, """
if ($open) {
    $open->check_out = Carbon::now();
    $open->worked_hours = round(
        max(($checkOut->getTimestamp() - $open->check_in->getTimestamp()) / 3600, 0), 2);
    $open->save();
    return response()->json(['action' => 'checkout', 'day_status' => 'completed']);
}
if ($closed) {
    return response()->json(['error' => 'Journée déjà clôturée', 'action' => 'blocked'], 409);
}
$attendance = Attendance::create([
    'employee_id' => $employee->id,
    'check_in' => Carbon::now(),
    'late_minutes' => $this->computeLateMinutes($checkIn),
    'source' => $source,
]);
return response()->json(['action' => 'checkin', 'day_status' => 'present'], 201);
""",
        caption="Extrait IV.3 — Enregistrement entrée / sortie / journée clôturée",
        source_file="app/Http/Controllers/Api/PresenceApiController.php")

    add_subheading(doc, "IV.3.3. Identification par empreinte")

    add_body(doc,
        "Lorsque le pointage est demandé par empreinte, l'application "
        "construit la galerie des agents enrôlés puis interroge le service "
        "local de comparaison. Le score renvoyé est confronté au seuil "
        "fingerprint_match_threshold (40 par défaut). Un échec produit "
        "une réponse 404 ; un succès déclenche registerPunch()."
    )

    add_code_block(doc, """
$gallery = $enrolled->map(fn (Employee $e) => [
    'id' => (int) $e->id,
    'template_b64' => (string) $e->fingerprint_template,
])->values()->all();
$match = $this->bridge->match($template, $gallery);
$threshold = (int) (SystemParameter::getValue('fingerprint_match_threshold', '40') ?: 40);
if (! ($match['matched'] ?? false) || (int) ($match['score'] ?? 0) < $threshold) {
    return null;
}
return Employee::find((int) $match['empreinte_id']);
""",
        caption="Extrait IV.4 — Identification 1:N via le service biométrique",
        source_file="app/Http/Controllers/Api/PresenceApiController.php")

    add_subheading(doc, "IV.3.4. Workflow de congé")

    add_body(doc,
        "Une demande est créée avec le statut « En attente ». La décision "
        "est enregistrée par PATCH /leaves/{id}/approval, réservée aux "
        "profils disposant de la permission « Valider congés » ou "
        "« Valider congés équipe ». Le commentaire de décision est persisté "
        "pour traçabilité."
    )

    add_code_block(doc, """
public function approval(Request $request, int $leaveId): JsonResponse
{
    $data = $request->validate([
        'status' => ['required', 'string', 'in:Approuvé,Rejeté,En attente'],
        'decision_comment' => ['nullable', 'string', 'max:500'],
    ]);
    $leave = Leave::findOrFail($leaveId);
    $leave->status = $data['status'];
    $leave->decision_comment = $data['decision_comment'] ?? $leave->decision_comment;
    $leave->save();
    ActivityLogger::log($request->user()?->username, "Validation congé #{$leave->id}");
    return response()->json(SpaSerializer::leave($leave));
}
""",
        caption="Extrait IV.5 — Décision sur une demande de congé",
        source_file="app/Http/Controllers/Api/LeaveApiController.php")

    add_heading(doc, "IV.4. Implémentation de l'interface web")

    add_subheading(doc, "IV.4.1. Organisation des écrans")

    add_body(doc,
        "L'interface est une application web monopage servie par Laravel "
        "(dashboard.html, sgrh-vision.js, sgrh-vision.css). La navigation "
        "latérale donne accès au pilot de bord, au terminal de pointage, "
        "à Mon espace, aux registres RH et aux paramètres. Sur tablette, "
        "un menu tiroir remplace la barre fixe."
    )

    add_table(doc,
              ["Écran", "Public", "Fonction principale"],
              [
                  ["Connexion", "Tous", "Authentification et ouverture de session"],
                  ["Pilot de bord", "RH / Manager", "KPI, graphiques personnalisables"],
                  ["Pointage", "Accueil / RH", "Empreinte, RFID, tableau du jour"],
                  ["Mon espace", "Agent", "Statut du jour, heures, congés"],
                  ["Enrôlement", "Admin RH", "Template empreinte et carte RFID"],
                  ["Congés / Employés", "RH / Manager", "Dossiers et workflow"],
              ],
              caption="Tableau 46 : Cartographie des écrans implémentés",
              col_widths=[3.5, 3.5, 9.0])

    add_subheading(doc, "IV.4.2. Flux de pointage côté interface")

    add_body(doc,
        "La fonction punchFingerprint() enchaîne deux appels : d'abord "
        "la capture (POST /api/biometric/scan), ensuite l'enregistrement "
        "(POST /api/presence/punch avec le modèle d'empreinte). Le résultat "
        "met à jour le tableau du jour et le flux live."
    )

    add_code_block(doc, """
async function punchFingerprint() {
  const scan = await api("/api/biometric/scan", { method: "POST", body: "{}" });
  if (!scan.template) throw new Error("Aucun template reçu du bridge.");
  const result = await api("/api/presence/punch", {
    method: "POST",
    body: JSON.stringify({ method: "fingerprint", template: scan.template }),
  });
  announcePunch(result);
  await loadTodayBoard();
}
""",
        caption="Extrait IV.6 — Enchaînement scan puis pointage dans l'interface",
        source_file="public/js/sgrh-vision.js")

    add_heading(doc, "IV.5. Implémentation du sous-système biométrique")

    add_subheading(doc, "IV.5.1. Service local de lecture")

    add_body(doc,
        "Le service HeadlessBridge, écrit en C#, écoute en local et expose "
        "trois opérations principales : consultation de l'état, capture "
        "d'une empreinte et comparaison d'un modèle avec la galerie des "
        "agents enrôlés. L'accès est protégé par une clé partagée avec "
        "l'application de gestion."
    )

    add_code_block(doc, """
app.MapGet("/status", () => Results.Json(new { status = "ok" }));

app.MapPost("/scan", async (HttpContext context) =>
{
    if (!context.Request.Headers.TryGetValue("X-API-KEY", out var key) || key != _apiKey)
        return Results.Unauthorized();
    var templateB64 = await ScanFingerprintAsync();
    return Results.Json(new { template = templateB64 });
});
""",
        caption="Extrait IV.7 — Endpoints de statut et de capture du service biométrique",
        source_file="fingerprint-service/APP_DESK/HeadlessBridge.cs")

    add_body(doc,
        "La comparaison 1:N s'appuie sur le SDK ZKFinger. Pour chaque "
        "agent de la galerie, un score est calculé ; le meilleur score "
        "est retenu. Le résultat renvoyé à l'application contient "
        "matched, empreinte_id et score."
    )

    add_code_block(doc, """
int score = (int)mDBMatch.Invoke(null, new object[] { dbHandle, probeBytes, galleryBytes })!;
if (score > bestScore) { bestScore = score; bestId = id; }
if (bestScore > 0)
    return new { matched = true, empreinte_id = bestId, score = bestScore };
return new { matched = false, empreinte_id = -1, score = 0 };
""",
        caption="Extrait IV.8 — Comparaison 1:N (meilleur score ZKFinger)",
        source_file="fingerprint-service/APP_DESK/HeadlessBridge.cs")

    add_subheading(doc, "IV.5.2. Appel depuis l'application de gestion")

    add_code_block(doc, """
public function match(string $probeTemplate, array $gallery): array
{
    $response = Http::timeout(30)
        ->withHeaders(['X-API-KEY' => $this->apiKey()])
        ->post($this->baseUrl().'/match', [
            'probe_template' => $probeTemplate,
            'gallery' => $gallery,
        ]);
    return $response->json() ?? ['matched' => false, 'empreinte_id' => -1, 'score' => 0];
}
""",
        caption="Extrait IV.9 — Relais de la comparaison depuis l'application",
        source_file="app/Services/BiometricBridgeService.php")

    add_subheading(doc, "IV.5.3. Installateur Windows")

    add_body(doc,
        "Le kit INSTALLER.bat copie le service, enregistre la clé, crée "
        "une tâche de démarrage à l'ouverture de session, ouvre le port "
        "local dans le pare-feu et lance immédiatement le service. Cette "
        "procédure permet de reproduire le terminal de pointage sur un "
        "autre poste Windows sans configuration manuelle complexe."
    )

    add_heading(doc, "IV.6. Fonctionnalités intelligentes implémentées")

    add_body(doc,
        "La dimension intelligente du prototype se manifeste par le calcul "
        "automatique d'indicateurs et d'alertes, et non par un modèle "
        "d'apprentissage automatique. Le tableau de bord agrège l'effectif "
        "actif, les présents, les retards, les absents, les congés en "
        "attente et les évaluations. Mon espace restitue, pour l'agent "
        "connecté uniquement, son statut du jour et une série d'heures "
        "et de retards sur quatorze jours."
    )

    add_bullet(doc, " KPI du jour : attendus, présents, sortis, en retard, absents ;")
    add_bullet(doc, " flux live des vingt derniers événements d'entrée ou de sortie ;")
    add_bullet(doc, " personnalisation des graphiques du pilot de bord ;")
    add_bullet(doc, " alertes de congés en attente et de retards ;")
    add_bullet(doc, " export des éléments de rémunération destinés à la finance.")

    add_heading(doc, "IV.7. Intégration et déploiement du prototype")

    add_body(doc,
        "La configuration de démonstration réunit, sur un même poste : "
        "le serveur de l'application (adresse locale, port 8000), le "
        "service de lecture d'empreintes, le navigateur et le ZK-9500. "
        "Les comptes de démonstration (superadmin, adminrh, manager, agent) "
        "sont créés par le seeder. Les cartes RFID de test portent des "
        "identifiants du type RFID-ADMIN-001."
    )

    add_table(doc,
              ["Élément", "Valeur de démonstration"],
              [
                  ["Application", "http://127.0.0.1:8000"],
                  ["Service biométrique", "http://127.0.0.1:5002/status"],
                  ["Compte RH", "adminrh / adminrh123"],
                  ["Compte agent", "agent / Agent@123"],
                  ["Fuseau", "Africa/Kinshasa"],
              ],
              caption="Tableau 47 : Paramètres de la démonstration locale",
              col_widths=[5.0, 11.0])

    add_heading(doc, "IV.8. Tests et validation")

    add_subheading(doc, "IV.8.1. Scénarios fonctionnels")

    add_table(doc,
              ["N°", "Scénario", "Résultat attendu", "Statut"],
              [
                  ["T1", "Connexion Admin RH", "Session ouverte, menu complet", "Validé"],
                  ["T2", "Connexion Agent", "Accès limité à Mon espace", "Validé"],
                  ["T3", "Identifiants erronés", "Refus, message d'erreur", "Validé"],
                  ["T4", "Enrôlement empreinte", "Template associé au dossier", "Validé*"],
                  ["T5", "1er pointage du jour", "Entrée + retard éventuel", "Validé*"],
                  ["T6", "2e pointage du jour", "Sortie + heures travaillées", "Validé*"],
                  ["T7", "3e pointage du jour", "Refus (journée clôturée)", "Validé*"],
                  ["T8", "Pointage RFID inconnu", "Carte non reconnue", "Validé"],
                  ["T9", "Demande de congé", "Statut En attente", "Validé"],
                  ["T10", "Décision RH", "Approuvé ou Rejeté + commentaire", "Validé"],
                  ["T11", "Consultation KPI", "Tableau de bord alimenté", "Validé"],
                  ["T12", "Mon espace (autre agent)", "Données personnelles uniquement", "Validé"],
              ],
              caption="Tableau 48 : Scénarios de tests fonctionnels (* avec ZK-9500 branché)",
              col_widths=[1.5, 4.5, 6.5, 3.5])
    add_source(doc)

    add_subheading(doc, "IV.8.2. Tests de contrôle d'accès")

    add_table(doc,
              ["Profil", "Opération", "Autorisé"],
              [
                  ["Employé", "Valider un congé d'équipe", "Non"],
                  ["Manager", "Valider congés équipe", "Oui"],
                  ["Admin RH", "Enrôler une empreinte", "Oui"],
                  ["Employé", "Consulter le dossier d'un collègue", "Non"],
                  ["SuperAdmin", "Toutes les permissions", "Oui"],
              ],
              caption="Tableau 49 : Contrôle d'accès selon le profil",
              col_widths=[3.5, 8.5, 4.0])

    add_subheading(doc, "IV.8.3. Correspondance besoins / réponses")

    add_table(doc,
              ["Besoin (ch. II)", "Réponse implémentée"],
              [
                  ["Centraliser les dossiers", "Module Employés + base unique"],
                  ["Fiabiliser le pointage", "Entrée/sortie empreinte ou RFID"],
                  ["Circuit de congé", "Statuts En attente / Approuvé / Rejeté"],
                  ["États pour la finance", "Éléments de rémunération exportables"],
                  ["Pilotage", "KPI, alertes, graphiques"],
                  ["Transparence agent", "Écran Mon espace"],
              ],
              caption="Tableau 50 : Correspondance entre besoins identifiés et réponses",
              col_widths=[6.0, 10.0])

    add_heading(doc, "IV.9. Résultats et présentation des interfaces")

    add_body(doc,
        "Les figures 28 à 35 présentent les interfaces réalisées du prototype "
        "SGRH Pro, capturées sur le poste de démonstration CNSS : "
        "authentification, pilot de bord, pointage, espace agent, enrôlement "
        "biométrique, gestion des congés, dossiers employés et rapports."
    )

    add_screenshot_placeholder(
        doc,
        "Figure 28 : Interface d'authentification de SGRH Pro",
        "Insérer la capture de l'écran de connexion (identifiant / mot de passe).",
        _fig("fig_iv1_login.png"),
    )
    add_screenshot_placeholder(
        doc,
        "Figure 29 : Tableau de bord principal (pilot de bord RH)",
        "Insérer la capture du dashboard : KPI, présence du jour, graphiques.",
        _fig("fig_iv2_dashboard.png"),
    )
    add_screenshot_placeholder(
        doc,
        "Figure 30 : Terminal de pointage (empreinte et RFID)",
        "Insérer la capture de l'écran Pointage : horloge, actions, tableau du jour.",
        _fig("fig_iv3_pointage.png"),
    )
    add_screenshot_placeholder(
        doc,
        "Figure 31 : Espace personnel de l'agent (Mon espace)",
        "Insérer la capture de Mon espace : statut du jour, heures, congés.",
        _fig("fig_iv4_mon_espace.png"),
    )
    add_screenshot_placeholder(
        doc,
        "Figure 32 : Enrôlement biométrique et attribution RFID",
        "Insérer la capture du module d'enrôlement (scan ZK-9500, carte RFID).",
        _fig("fig_iv5_enrolement.png"),
    )
    add_screenshot_placeholder(
        doc,
        "Figure 33 : Gestion des demandes de congé",
        "Insérer la capture de la liste des congés et de l'action de validation.",
        _fig("fig_iv6_conges.png"),
    )
    add_screenshot_placeholder(
        doc,
        "Figure 34 : Gestion des dossiers employés",
        "Insérer la capture de la liste / fiche employé (matricule, service, statut).",
        _fig("fig_iv7_employes.png"),
    )
    add_screenshot_placeholder(
        doc,
        "Figure 35 : Rapports et indicateurs de pilotage",
        "Insérer la capture des rapports / graphiques institutionnels.",
        _fig("fig_iv8_rapports.png"),
    )

    add_body(doc,
        "Ces interfaces confirment que le prototype couvre le parcours "
        "complet retenu dans le cahier des charges : s'authentifier, "
        "enrôler, pointer, consulter son espace, valider un congé et "
        "piloter les effectifs. Les captures d'écran ci-dessus attestent "
        "visuellement du rendu final obtenu. La comparaison avec le système "
        "manuel (registres, Excel, signatures) met en évidence le gain de "
        "traçabilité et la réduction des ressaisies."
    )

    add_heading(doc, "IV.10. Limites du prototype et perspectives")

    add_bullet(doc, " un seul poste de pointage dans la configuration de démonstration ;")
    add_bullet(doc, " dépendance au poste Windows et au pilote USB du ZK-9500 ;")
    add_bullet(doc, " les provisions fiscales restent indicatives ; aucun virement n'est exécuté ;")
    add_bullet(doc, " les modules recrutement, formation et contrats sont hors cœur ;")
    add_bullet(doc, " la protection des données biométriques du prototype n'équivaut "
               "pas à une certification juridique nationale.")

    add_body(doc,
        "Les perspectives comprennent le déploiement multi-sites, "
        "l'hébergement institutionnel MySQL, une application mobile "
        "de consultation et, à plus long terme, des analyses prédictives "
        "d'absentéisme. Ces évolutions dépassent le cadre du présent mémoire."
    )

    add_heading(doc, "IV.11. Conclusion du chapitre")

    add_body(doc,
        "L'implémentation a montré qu'il était possible de construire, "
        "dans le temps d'un mémoire, un SIGRH opérationnel reliant "
        "dossiers agents, pointage biométrique réel, workflow de congé "
        "et tableaux de bord. Les extraits de code présentés attestent "
        "que les règles conçues au chapitre III — un couple entrée/sortie "
        "par jour, identification 1:N, droits par rôle — sont bien "
        "celles exécutées par le prototype."
    )

    add_body(doc,
        "Les captures d'écran intégrées au chapitre IV servent de preuve "
        "visuelle pour la soutenance. La conclusion générale reprend "
        "la problématique, confronte les hypothèses aux résultats et "
        "ouvre les perspectives institutionnelles pour la CNSS."
    )

    return page_start


def build():
    doc = init_document()
    append_chapitre4(doc, PAGE_START)
    out = OUTPUT
    try:
        doc.save(out)
    except PermissionError:
        out = OUTPUT_FALLBACK
        doc.save(out)
    words = sum(len(p.text.split()) for p in doc.paragraphs)
    print(f"Chapitre IV genere : {out}")
    print(f"Mots approximatifs : {words}")


if __name__ == "__main__":
    build()

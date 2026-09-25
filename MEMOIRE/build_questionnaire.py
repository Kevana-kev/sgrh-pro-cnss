# -*- coding: utf-8 -*-
"""Questionnaire Q/R — Introduction + Chapitres I et II (SGRH Pro / CNSS).
Réponses simples, y compris notions informatiques de base.
"""
from pathlib import Path

from memoire_format import (
    init_document, add_chapter_title, add_heading, add_subheading,
    add_body, add_mixed, add_bullet, add_numbered_item,
)

OUTPUT = Path(r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\QUESTIONNAIRE - INTRO CHAPITRES I ET II.docx")
OUTPUT_FALLBACK = OUTPUT.with_name(OUTPUT.stem + " - v2.docx")


def qa(doc, q: str, a: str):
    add_mixed(doc, [("Q. ", True, False), (q, True, False)])
    add_body(doc, "R. " + a)


def build():
    doc = init_document()
    add_chapter_title(
        doc,
        "QUESTIONNAIRE DE PRÉPARATION — INTRODUCTION, CHAPITRES I ET II\n"
        "SGRH Pro — CNSS (Kinshasa)",
    )
    add_body(doc,
        "Ce document regroupe des questions susceptibles d'être posées à l'oral "
        "(soutenance, encadreur, jury) sur la partie déjà rédigée du mémoire. "
        "Les réponses sont volontairement simples et claires, y compris pour "
        "les notions techniques de base. Apprenez d'abord les réponses courtes ; "
        "les détails servent si le jury approfondit.")

    # ═══════════════════════════════════════════════════════════
    add_heading(doc, "1. Présentation générale du travail (à savoir par cœur)")

    qa(doc,
       "Quel est le titre / le sujet de votre mémoire ?",
       "Conception et implémentation d'un système d'information intelligent "
       "de gestion des ressources humaines (SGRH Pro) intégrant la biométrie "
       "(lecteur ZK-9500) et les cartes RFID, pour le suivi du personnel "
       "au siège central de la CNSS en RDC.")

    qa(doc,
       "Qu'est-ce que SGRH Pro ?",
       "C'est le nom du logiciel que je propose. SGRH Pro signifie Système de "
       "Gestion des Ressources Humaines Professionnel. C'est une application "
       "web qui centralise les dossiers agents, les présences, les congés, "
       "les éléments de rémunération (états pour la finance), l'évaluation "
       "et les tableaux de bord.")

    qa(doc,
       "Pourquoi ce sujet ?",
       "Pendant le stage à la CNSS, j'ai observé que le RH utilise encore "
       "beaucoup le papier et Excel : pointage peu fiable, états de présence "
       "longs à produire, pas de tableau de bord. Le sujet répond à un vrai "
       "problème de terrain, pas à un sujet inventé.")

    qa(doc,
       "Quel est le problème principal ?",
       "Comment concevoir un SIGRH fiable pour la CNSS, basé surtout sur un "
       "logiciel modulaire, complété par la biométrie (empreinte) et le RFID "
       "(carte), pour mieux suivre le personnel au siège central.")

    qa(doc,
       "Quel est l'objectif général ?",
       "Concevoir et implémenter SGRH Pro pour améliorer le suivi administratif "
       "du personnel (présences, biométrie, évaluation, états de rémunération).")

    qa(doc,
       "Combien de modules le système contient-il ?",
       "Huit modules : M1 Accès, M2 Employés, M3 Biométrie, M4 Présences, "
       "M5 Congés, M6 Rémunération (états admin), M7 Évaluation, M8 Rapports.")

    qa(doc,
       "Pourquoi seulement huit modules et pas plus ?",
       "Le directeur a demandé un périmètre réaliste. On a recentré le travail "
       "sur ce qui compte vraiment : présences, biométrie, évaluation et "
       "rémunération. On a exclu contrats, recrutement, formation et congés "
       "médicaux pour garder un prototype démontrable et de qualité.")

    qa(doc,
       "Le système fait-il la paie (virements bancaires) ?",
       "Non. À la CNSS, c'est la direction financière qui paie les agents par "
       "virement bancaire. SGRH Pro produit seulement les états administratifs "
       "(présences, absences, éléments variables) que la finance utilise. "
       "Le logiciel ne calcule pas le salaire net et ne fait pas les virements.")

    # ═══════════════════════════════════════════════════════════
    add_heading(doc, "2. Notions informatiques de base (questions très simples)")

    add_body(doc,
        "Ces questions paraissent « trop faciles », mais un jury peut les poser "
        "pour vérifier que vous comprenez vraiment ce que vous avez écrit.")

    qa(doc,
       "Qu'est-ce qu'un logiciel ?",
       "Un programme informatique qui fait des tâches pour l'utilisateur. "
       "Exemple : Word, Excel, ou SGRH Pro.")

    qa(doc,
       "Qu'est-ce qu'une application web ?",
       "Un logiciel qu'on utilise dans un navigateur Internet (Chrome, Edge…) "
       "sans installer un gros programme sur chaque PC. On tape une adresse "
       "et on se connecte. SGRH Pro est une application web.")

    qa(doc,
       "Quelle est la différence entre frontend et backend ?",
       "Le frontend, c'est ce que l'utilisateur voit (écrans, boutons, formulaires). "
       "Le backend, c'est la partie « moteur » cachée qui traite les données, "
       "vérifie les droits et parle à la base de données. Chez nous : frontend = "
       "pages HTML/CSS/JavaScript ; backend = API Laravel en PHP.")

    qa(doc,
       "Qu'est-ce qu'une base de données ?",
       "Un endroit organisé pour stocker durablement les informations "
       "(agents, pointages, congés…). Comme un classeur intelligent. "
       "Nous utilisons SQLite pour le prototype local (un fichier), et MySQL "
       "pour l'hébergement de production.")

    qa(doc,
       "Qu'est-ce qu'une API ?",
       "Une interface de communication entre programmes. Le frontend demande "
       "au backend : « donne-moi la liste des agents » ; le backend répond "
       "avec des données. C'est l'API REST.")

    qa(doc,
       "Que veut dire REST / API REST ?",
       "REST est une façon standard de concevoir une API web. On utilise des "
       "adresses (URL) et des méthodes HTTP : GET (lire), POST (créer), "
       "PUT/PATCH (modifier), DELETE (supprimer). Les réponses sont souvent "
       "en JSON (format texte lisible par les programmes).")

    qa(doc,
       "Qu'est-ce que JSON ?",
       "Un format simple pour échanger des données entre programmes, "
       "par exemple : {\"nom\": \"Mukendi\", \"matricule\": \"A123\"}.")

    qa(doc,
       "Qu'est-ce que PHP ? Laravel ?",
       "PHP est un langage de programmation très utilisé pour le web. "
       "Laravel est un framework PHP (boîte à outils) pour créer une "
       "application structurée : routes, contrôleurs, base de données, "
       "sécurité. C'est le moteur de SGRH Pro.")

    qa(doc,
       "Qu'est-ce que C# ? Pourquoi l'utiliser pour la biométrie ?",
       "C# est un langage Microsoft, bien adapté à Windows. Le SDK du lecteur "
       "ZK-9500 fonctionne surtout sous Windows : on a donc créé un petit "
       "programme local en C# (le Bridge) qui parle au capteur USB.")

    qa(doc,
       "Qu'est-ce que le Bridge biométrique ?",
       "Un service local installé sur le PC du responsable RH. Il relie le "
       "lecteur d'empreintes ZK-9500 au logiciel SGRH Pro. Sans ce bridge, "
       "le navigateur web ne peut pas piloter directement le capteur USB.")

    qa(doc,
       "Qu'est-ce qu'un serveur ?",
       "Un ordinateur (ou un programme) qui répond aux demandes des clients. "
       "Dans le prototype, le PC du responsable RH peut jouer le rôle de "
       "serveur local pour l'API et le bridge.")

    qa(doc,
       "Qu'est-ce qu'un client ?",
       "Le programme qui demande un service au serveur. Ici, le navigateur "
       "web (frontend) est un client de l'API.")

    qa(doc,
       "Qu'est-ce qu'un navigateur ?",
       "Le logiciel pour ouvrir des sites/applications web : Chrome, Edge, "
       "Firefox…")

    qa(doc,
       "Qu'est-ce que HTTP / HTTPS ?",
       "HTTP est le protocole de communication sur le web. HTTPS est la "
       "version sécurisée (données chiffrées). En production on vise HTTPS.")

    qa(doc,
       "Qu'est-ce qu'un login / une authentification ?",
       "Vérifier qui vous êtes avant d'entrer dans le système "
       "(matricule + mot de passe).")

    qa(doc,
       "Qu'est-ce qu'un mot de passe hashé (bcrypt) ?",
       "On ne stocke pas le mot de passe en clair. On le transforme en une "
       "empreinte (hash) avec bcrypt. Même si quelqu'un vole la base, "
       "il ne lit pas directement les mots de passe.")

    qa(doc,
       "Qu'est-ce que Laravel Sanctum ?",
       "Un mécanisme de tickets de session (tokens Bearer) après connexion. "
       "À chaque requête, le frontend envoie ce ticket pour prouver que "
       "l'utilisateur est bien connecté, sans renvoyer le mot de passe.")

    qa(doc,
       "Qu'est-ce que RBAC ?",
       "Role-Based Access Control : contrôle d'accès par rôles. "
       "Admin RH, Responsable, Agent n'ont pas les mêmes droits. "
       "Un agent ne peut pas modifier les dossiers de tout le monde.")

    qa(doc,
       "Qu'est-ce qu'un rôle utilisateur ?",
       "Un profil de droits. Exemple : l'Agent consulte ses présences ; "
       "le Responsable valide les congés de son équipe ; l'Admin RH gère tout.")

    qa(doc,
       "Qu'est-ce qu'un journal d'audit ?",
       "Un historique des actions sensibles : qui a créé un agent, qui a "
       "modifié un dossier, quand. Utile pour la traçabilité dans une "
       "institution publique.")

    qa(doc,
       "Qu'est-ce que USB ?",
       "Un port/câble pour brancher un périphérique (ici le ZK-9500) "
       "sur l'ordinateur.")

    qa(doc,
       "Quelle différence entre logiciel et matériel ?",
       "Le matériel, c'est le physique (PC, lecteur d'empreintes, cartes). "
       "Le logiciel, c'est le programme. Dans mon mémoire, le logiciel "
       "est prioritaire ; le matériel biométrique/RFID sert à alimenter "
       "le système en données de pointage.")

    qa(doc,
       "Qu'est-ce qu'un prototype ?",
       "Une version démontrable du système, pas encore un déploiement "
       "national. Il prouve que la solution fonctionne (enrôlement, "
       "pointage, états, évaluations).")

    qa(doc,
       "Qu'est-ce que UML ?",
       "Un langage de modélisation avec des diagrammes (cas d'utilisation, "
       "classes, séquences…). Ça aide à concevoir avant de coder. "
       "Les diagrammes détaillés sont prévus au chapitre III.")

    qa(doc,
       "Qu'est-ce qu'un KPI ?",
       "Key Performance Indicator : indicateur de performance. "
       "Exemples : taux d'absentéisme, effectif, retards, score moyen "
       "d'évaluation. Affichés sur le tableau de bord.")

    qa(doc,
       "Qu'est-ce qu'un workflow ?",
       "Un circuit de validation étape par étape. Exemple congé : "
       "Agent demande → Responsable donne son avis → Admin RH décide.")

    qa(doc,
       "Qu'est-ce que PDF / CSV ?",
       "Des formats de fichiers. PDF pour un document imprimable ; "
       "CSV pour un tableau ouvrable dans Excel. SGRH Pro exporte "
       "les états administratifs dans ces formats pour la finance.")

    # ═══════════════════════════════════════════════════════════
    add_heading(doc, "3. Questions sur l'Introduction")

    qa(doc,
       "Où se situe votre étude (périmètre géographique) ?",
       "Siège central de la CNSS à Kinshasa (commune de la Gombe). "
       "Pas les agences provinciales dans ce mémoire.")

    qa(doc,
       "Qu'est-ce qui est hors périmètre ?",
       "Gestion des assurés sociaux et cotisations ; virements bancaires ; "
       "calcul fiscal IRG ; application mobile native ; reconnaissance "
       "faciale ; contrats, recrutement, formation, congés médicaux ; "
       "déploiement multi-sites.")

    qa(doc,
       "Quelles méthodes avez-vous utilisées ?",
       "Analyse du système actuel (observation, entretiens, documents), "
       "approche structuro-fonctionnelle (découpage en modules), "
       "développement itératif, planification PERT/Gantt.")

    qa(doc,
       "Quelles techniques de collecte ?",
       "Observation participante au service RH, entretiens semi-directifs "
       "(responsable RH, gestionnaires, agents), analyse documentaire "
       "(registres, Excel, procédures).")

    qa(doc,
       "Que signifie « intelligent » dans votre titre ?",
       "Pas de l'intelligence artificielle (machine learning). "
       "Ça veut dire : tableaux de bord, KPI, alertes automatiques "
       "(absences, retards, congés en attente) pour aider à décider.")

    qa(doc,
       "Citez une hypothèse de recherche.",
       "Si on centralise les données et qu'on automatise les présences "
       "et congés, on réduira les incohérences et on accélérera les états "
       "transmis à la finance. La biométrie fiabilisera le pointage.")

    # ═══════════════════════════════════════════════════════════
    add_heading(doc, "4. Questions sur le Chapitre I (théorie)")

    qa(doc,
       "Qu'est-ce que la GRH ?",
       "Gestion des Ressources Humaines : ensemble des pratiques pour "
       "attirer, administrer, développer et suivre le personnel "
       "(Dessler, etc.).")

    qa(doc,
       "Qu'est-ce qu'un SIGRH / SIRH ?",
       "Système d'Information des Ressources Humaines : logiciel qui "
       "collecte, stocke, traite et restitue les infos RH "
       "(dossiers, présences, congés, reporting…).")

    qa(doc,
       "Quelles sont les trois couches fonctionnelles d'un SIGRH ?",
       "1) Acquisition (saisies, pointage biométrique, RFID) ; "
       "2) Traitement (règles métier, workflows, calculs) ; "
       "3) Restitution (tableaux de bord, rapports, exports).")

    qa(doc,
       "Qu'est-ce que la biométrie ?",
       "Techniques qui utilisent une caractéristique du corps pour "
       "identifier une personne. Chez nous : l'empreinte digitale.")

    qa(doc,
       "Pourquoi l'empreinte digitale et pas le visage ?",
       "L'empreinte est courante, relativement peu chère, et le lecteur "
       "ZK-9500 est adapté au poste RH. La reconnaissance faciale est "
       "hors périmètre (plus complexe, plus sensible).")

    qa(doc,
       "Qu'est-ce que le ZK-9500 ?",
       "Un lecteur d'empreintes digitales de la marque ZKTeco, branché "
       "en USB sur le PC du responsable RH. Prix retenu dans le budget : "
       "80 USD. Il sert à l'enrôlement et au pointage.")

    qa(doc,
       "Qu'est-ce que le RFID ?",
       "Radio Frequency Identification : une carte (badge) communique "
       "avec un lecteur sans contact (ondes radio). On attribue une "
       "carte nominative à l'agent comme moyen de pointage de secours "
       "ou complémentaire à l'empreinte.")

    qa(doc,
       "Pourquoi combiner empreinte + RFID ?",
       "L'empreinte est plus forte contre la fraude (on ne prête pas "
       "facilement son doigt). La carte sert de secours (doigt blessé) "
       "ou de complément. Les deux alimentent le module Présences.")

    qa(doc,
       "Quels risques éthiques avec la biométrie ?",
       "Données sensibles. Il faut le consentement, ne pas stocker "
       "l'image brute de l'empreinte si possible (plutôt un modèle/"
       "template), journaliser les accès, et pouvoir révoquer une carte. "
       "Ce ne sont pas des conseils juridiques officiels, mais des "
       "mesures techniques de base du prototype.")

    qa(doc,
       "Pourquoi ne pas utiliser SAP, Workday ou Odoo directement ?",
       "Coût, paramétrage lourd, dépendance Internet, adaptation "
       "imparfaite au contexte CNSS, et surtout pas d'intégration "
       "native simple du ZK-9500. Développer SGRH Pro permet de "
       "maîtriser le code et le pointage biométrique.")

    qa(doc,
       "Qu'est-ce que l'architecture n-tiers / séparation des couches ?",
       "On sépare présentation (écrans), métier (règles) et données "
       "(base). Avantage : on peut changer l'interface plus tard "
       "(ex. mobile) sans tout refaire.")

    # ═══════════════════════════════════════════════════════════
    add_heading(doc, "5. Questions sur le Chapitre II (CNSS, besoins, modules)")

    qa(doc,
       "Qu'est-ce que la CNSS ?",
       "Caisse Nationale de Sécurité Sociale de la RDC : institution "
       "publique de sécurité sociale. Mon mémoire ne gère pas les "
       "assurés externes, seulement le personnel interne du siège.")

    qa(doc,
       "Comment gère-t-on le RH aujourd'hui à la CNSS (constat) ?",
       "Registres papier, fichiers Excel, pointage manuel à l'accueil, "
       "congés sur formulaires papier, consolidation manuelle des états "
       "pour la finance. Pas de source unique de vérité.")

    qa(doc,
       "Quels dysfonctionnements principaux (D1–D7) ?",
       "Doublons d'effectifs ; pointages peu fiables ; retards "
       "administratifs ; congés mal synchronisés ; évaluations non "
       "structurées ; absence de traçabilité ; reporting inexistant.")

    qa(doc,
       "Qui sont les acteurs du système ?",
       "Humains : Admin RH, Responsable de service, Agent. "
       "Techniques : Bridge biométrique, capteur ZK-9500, lecteur RFID. "
       "Tous interagissent avec le cœur SGRH Pro (API + base).")

    qa(doc,
       "Expliquez les 8 modules un par un (réponse courte).",
       "M1 Accès : connexion et droits. M2 Employés : dossiers. "
       "M3 Biométrie : enrôlement/pointage ZK+RFID. M4 Présences : "
       "heures, retards. M5 Congés : demandes et validation. "
       "M6 Rémunération : états pour la finance. M7 Évaluation : "
       "grilles de performance. M8 Rapports : KPI et alertes.")

    qa(doc,
       "Quelle est la dépendance entre biométrie et présences ?",
       "M3 (biométrie) alimente M4 (présences) : chaque pointage "
       "empreinte/RFID crée un enregistrement de présence horodaté.")

    qa(doc,
       "Comment les présences alimentent-elles la rémunération ?",
       "M4 calcule absences/retards ; M6 s'en sert pour produire "
       "l'état administratif mensuel exporté vers la finance.")

    qa(doc,
       "Qu'est-ce que MoSCoW ?",
       "Méthode de priorité des exigences : Must (indispensable), "
       "Should (important), Could (souhaitable), Won't (pas maintenant).")

    qa(doc,
       "Donnez un exemple d'exigence fonctionnelle (EF).",
       "EF-04 : Enrôler une empreinte via ZK-9500 (priorité Must). "
       "Ou EF-01 : Authentifier un utilisateur par matricule et mot de passe.")

    qa(doc,
       "Quels sont les critères d'acceptation du prototype ?",
       "Enrôler au moins un agent sur le ZK-9500 ; enregistrer un "
       "pointage réel ; produire un état administratif exporté ; "
       "faire un workflow de congé complet ; afficher des KPI ; "
       "connecter les 3 profils (Admin RH, Responsable, Agent).")

    qa(doc,
       "Décrivez le scénario de pointage.",
       "L'agent pose le doigt (ou passe la carte). Le premier scan du jour "
       "enregistre l'arrivée ; le second enregistre la sortie. Un troisième "
       "scan est refusé (journée déjà close). Le système identifie l'agent "
       "(matching 1:N ou RFID actif), horodate, calcule le retard si besoin.")

    qa(doc,
       "Décrivez le workflow de congé.",
       "Agent soumet → Responsable avise → Admin RH décide → "
       "solde mis à jour et agent informé.")

    # ═══════════════════════════════════════════════════════════
    add_heading(doc, "6. Questions techniques approfondies (mais réponses claires)")

    qa(doc,
       "Quelle est la stack technique ?",
       "Backend : PHP, Laravel 11, Eloquent, Sanctum, bcrypt. "
       "Frontend : HTML, CSS, JavaScript, Chart.js. "
       "Exports : DomPDF. Bridge : C# headless, SDK ZKTeco, installateur Windows. "
       "Base : SQLite (proto local) / MySQL (production).")

    qa(doc,
       "Pourquoi Laravel et pas Flask / Node.js ?",
       "Laravel (PHP) correspond à l'hébergement mutualisé retenu pour "
       "le prototype (PHP + MySQL). Il offre une architecture en couches "
       "claire, un ORM (Eloquent) et une authentification prête (Sanctum). "
       "L'important est la maîtrise et la séparation backend/frontend.")

    qa(doc,
       "Comment se passe l'enrôlement techniquement ?",
       "L'Admin RH crée le dossier (M2), lance l'enrôlement depuis "
       "l'interface web. Le backend appelle le Bridge C# sur le PC "
       "(port 5002). Le ZK-9500 capture l'empreinte ; le modèle est "
       "stocké ; une carte RFID peut être associée.")

    qa(doc,
       "Pourquoi le bridge écoute-t-il le port 5002 ?",
       "C'est le port local choisi pour le service Bridge. Le backend "
       "lui envoie des commandes (scan, match, status) via HTTP local. "
       "Ce n'est pas un port Internet public : c'est sur le poste RH.")

    qa(doc,
       "Comment installe-t-on le bridge sur un PC Windows ?",
       "On décompresse le kit et on lance INSTALLER.bat (droits admin). "
       "Le service se copie, démarre tout seul à l'ouverture de session "
       "et écoute http://127.0.0.1:5002. Il faut brancher le ZK-9500.")

    qa(doc,
       "Que stocke-t-on comme donnée biométrique ?",
       "Un modèle (template) d'empreinte pour la reconnaissance, "
       "pas forcément l'image complète. On trace aussi la source "
       "du pointage et on peut désactiver une carte RFID.")

    qa(doc,
       "Comment sécurise-t-on l'API ?",
       "Login → token Sanctum ; mots de passe bcrypt ; permissions RBAC côté "
       "serveur ; validation des entrées ; journal d'audit "
       "pour les actions sensibles.")

    qa(doc,
       "Qu'est-ce qu'un endpoint ? Exemple ?",
       "Une adresse d'API pour une action. Exemple : POST /api/auth/login "
       "pour se connecter ; POST /api/presence/punch pour pointer ; "
       "GET /api/presence/today pour le tableau du jour.")

    qa(doc,
       "Différence SQLite / MySQL ?",
       "SQLite = fichier unique, simple pour le prototype sur un PC. "
       "MySQL = serveur de base utilisé en production (hébergement "
       "mutualisé). On développe en SQLite, on déploie en MySQL.")

    qa(doc,
       "Qu'est-ce qu'un ORM (Eloquent) ?",
       "Un outil qui permet de manipuler la base avec des objets "
       "PHP plutôt qu'écrire tout le SQL à la main. Ça accélère "
       "le développement et réduit certaines erreurs. Laravel utilise Eloquent.")

    qa(doc,
       "Que signifie CRUD ?",
       "Create, Read, Update, Delete : créer, lire, modifier, supprimer. "
       "Exemple : gérer un dossier agent (CRUD employé).")

    qa(doc,
       "Qu'est-ce qu'un SDK ?",
       "Software Development Kit : boîte à outils fournie par le "
       "fabricant (ZKTeco) pour piloter le lecteur depuis un programme.")

    qa(doc,
       "Que se passe-t-il si le capteur est débranché ?",
       "Le bridge signale un statut indisponible. On ne peut plus "
       "enrôler/pointer par empreinte tant que le matériel n'est pas "
       "reconnecté. La carte RFID peut servir de secours selon le cas.")

    qa(doc,
       "Le système marche-t-il sans Internet ?",
       "Le prototype vise un fonctionnement local sur le poste RH "
       "(API + bridge + base locale). Une connexion Internet n'est "
       "pas obligatoire pour la démo de base. Un hébergement serveur "
       "interne/VPS est une option d'évolution.")

    qa(doc,
       "Comment l'espace agent est-il limité ?",
       "L'agent voit surtout ses propres données (présences, heures, retards, "
       "évaluations, congés) dans « Mon espace ». Il n'accède pas aux "
       "données des collègues ni à l'administration globale.")

    # ═══════════════════════════════════════════════════════════
    add_heading(doc, "7. Planification (PERT, Gantt, budget) — très demandé")

    qa(doc,
       "Qu'est-ce qu'un diagramme de Gantt ?",
       "Un calendrier en barres : chaque tâche est une barre horizontale "
       "montrant quand elle commence et combien de temps elle dure.")

    qa(doc,
       "Qu'est-ce qu'un graphe PERT / MPM ?",
       "Un réseau de tâches avec dépendances. Chaque case (nœud) montre "
       "les dates au plus tôt / au plus tard ; les flèches portent les "
       "durées. Ça permet de voir l'ordre des travaux.")

    qa(doc,
       "Qu'est-ce que le chemin critique ?",
       "La suite de tâches sans marge : si l'une retarde, tout le projet "
       "retarde. Chez nous : A→B→C→D→E→F→I→J = 63 jours ouvrés.")

    qa(doc,
       "Quelle est la durée totale du projet ?",
       "63 jours ouvrés, du 1er juillet 2026 au 28 septembre 2026 "
       "environ (calendrier prévisionnel).")

    qa(doc,
       "Citez les tâches A à J rapidement.",
       "A Analyse (14 j), B Spécification (6), C UML (9), D BDD (3), "
       "E Backend (13), F Frontend (9), G Bridge (6), H Intégration "
       "ZK/RFID (6), I Tests (6), J Déploiement (3).")

    qa(doc,
       "Quelles tâches ont une marge (ne sont pas critiques) ?",
       "G (bridge) marge 10 jours ; H (intégration) marge 3 jours. "
       "Elles peuvent glisser un peu sans retarder la fin du projet.")

    qa(doc,
       "La rédaction du mémoire et la soutenance sont-elles dans le PERT ?",
       "Non. Le planning technique ne contient que les tâches système "
       "(analyse, conception, développement, tests, déploiement).")

    qa(doc,
       "Quel est le budget estimé ?",
       "Environ 160 USD au total (ZK-9500 80 USD + RFID/lecteur/câbles/"
       "hébergement optionnel + contingence 10 %). Les logiciels "
       "(PHP, Laravel, Visual Studio Community) sont gratuits.")

    qa(doc,
       "Que signifient ES, EF, LS, LF, marge ?",
       "ES = début au plus tôt, EF = fin au plus tôt, LS = début au "
       "plus tard, LF = fin au plus tard. Marge = LS−ES (ou LF−EF). "
       "Marge 0 = tâche critique.")

    # ═══════════════════════════════════════════════════════════
    add_heading(doc, "8. Questions « pièges » et réponses prudentes")

    qa(doc,
       "Votre système empêche-t-il toute fraude de pointage ?",
       "Non, aucun système n'est parfait. La biométrie élève fortement "
       "la barrière (plus difficile de pointer pour un autre). Mais il "
       "faut aussi une organisation et un contrôle humain. Je ne promets "
       "pas l'élimination totale de la fraude.")

    qa(doc,
       "Est-ce déjà déployé dans toute la CNSS ?",
       "Non. C'est un prototype de démonstration au poste RH du siège. "
       "La généralisation (provinces, production) est une perspective.")

    qa(doc,
       "Avez-vous respecté toutes les lois sur les données biométriques ?",
       "Le prototype prévoit consentement, traçabilité et mesures "
       "techniques de base. Une conformité juridique complète relève "
       "d'une démarche institutionnelle au-delà du mémoire. Je reste "
       "prudente : ce n'est pas un avis juridique.")

    qa(doc,
       "Pourquoi Excel ne suffit-il pas ?",
       "Excel n'est pas multi-utilisateur sécurisé, pas de workflow, "
       "pas d'audit fiable, pas d'intégration biométrique native, "
       "risque de versions multiples et d'erreurs de ressaisie.")

    qa(doc,
       "Que ferez-vous au chapitre III / IV ?",
       "III : conception UML, modèle de données, architecture détaillée. "
       "IV : implémentation, tests, résultats, perspectives.")

    qa(doc,
       "Quelle est votre contribution personnelle ?",
       "Analyse de terrain CNSS, cahier des charges recentré, "
       "architecture logicielle, intégration biométrie/RFID, "
       "planification et prototype démontrable — pas un simple "
       "copier-coller d'un logiciel du marché.")

    qa(doc,
       "Si le jury dit « expliquez comme à un non-informaticien » ?",
       "SGRH Pro est un logiciel RH pour la CNSS. L'agent pointe avec "
       "son doigt ou sa carte. Le RH voit les présences, valide les "
       "congés, évalue le personnel et envoie un état propre à la "
       "finance pour le paiement. Tout est centralisé au lieu d'être "
       "éparpillé dans des cahiers et Excel.")

    # ═══════════════════════════════════════════════════════════
    add_heading(doc, "9. Mini-glossaire à réciter")

    items = [
        ("SIGRH", "logiciel de gestion RH"),
        ("API", "lien de communication entre programmes"),
        ("Frontend", "écrans visibles"),
        ("Backend", "moteur serveur / logique"),
        ("Base de données", "stockage organisé des données"),
        ("Sanctum", "ticket de session après login"),
        ("RBAC", "droits selon le rôle"),
        ("ZK-9500", "lecteur d'empreintes USB"),
        ("RFID", "carte/badge sans contact"),
        ("Bridge", "petit programme Windows qui parle au capteur"),
        ("PERT", "réseau des tâches du projet"),
        ("Gantt", "calendrier en barres"),
        ("Chemin critique", "tâches sans marge (63 jours)"),
        ("KPI", "indicateur de pilotage"),
        ("Prototype", "version de démonstration"),
    ]
    for term, defn in items:
        add_bullet(doc, f" {term} : {defn}.")

    # ═══════════════════════════════════════════════════════════
    add_heading(doc, "10. Conseils pour l'oral")

    add_numbered_item(doc, 1,
        " Répondez d'abord en 2–3 phrases simples, puis développez si on insiste.")
    add_numbered_item(doc, 2,
        " Si vous ne savez pas un détail de code, dites : « Dans le mémoire "
        "la conception prévoit X ; l'implémentation détaillée est au chapitre III/IV. »")
    add_numbered_item(doc, 3,
        " Ne promettez jamais que le logiciel « paie les salaires » : il produit des états.")
    add_numbered_item(doc, 4,
        " Mémorisez : 8 modules, 63 jours, chemin critique A…J, budget ~160 USD, ZK-9500 = 80 USD.")
    add_numbered_item(doc, 5,
        " Montrez que vous comprenez le pourquoi (problème CNSS) autant que le comment (technique).")

    add_body(doc,
        "Fin du questionnaire. Relisez ce document à voix haute plusieurs fois. "
        "Priorité : sections 1, 2, 5, 6 et 7.")

    out = OUTPUT
    try:
        doc.save(out)
    except PermissionError:
        out = OUTPUT_FALLBACK
        doc.save(out)
        print("Note : fichier ouvert — sauvegarde alternative")
    print(f"Questionnaire genere : {out}")


if __name__ == "__main__":
    build()

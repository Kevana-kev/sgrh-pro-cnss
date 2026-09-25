# -*- coding: utf-8 -*-
"""Génère le Chapitre III — Conception et architecture du système SGRH Pro."""
from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH

from memoire_format import (
    init_document, add_page_number, add_chapter_title, add_heading, add_subheading,
    add_body, add_mixed, add_bullet, add_numbered_item, add_table, add_figure,
    add_page_break, add_source,
)

OUTPUT = r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\CHAPITRE III - CONCEPTION ET ARCHITECTURE.docx"
OUTPUT_FALLBACK = r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\CHAPITRE III - CONCEPTION ET ARCHITECTURE - v2.docx"
IMG_DIR = Path(r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\images\chapitre3")
PAGE_START = 40


def _fig(name: str) -> str:
    return str(IMG_DIR / name)


def _ensure_figures():
    import generate_figures_ch3
    generate_figures_ch3.main()


def append_chapitre3(doc, page_start=40):
    _ensure_figures()
    add_page_number(doc, page_start)
    add_chapter_title(doc, "CHAPITRE III. CONCEPTION ET ARCHITECTURE DU SYSTÈME")

    # ───────────────── III.1 ─────────────────
    add_heading(doc, "III.1. Introduction")

    add_body(doc,
        "Le chapitre précédent a formalisé le diagnostic du système RH actuel "
        "de la CNSS, les besoins des acteurs et le cahier des charges des huit "
        "modules de SGRH Pro. Le présent chapitre traduit ces spécifications "
        "en conception logicielle : architecture globale, modélisation UML, "
        "schéma de données, organisation du backend Laravel, conception de "
        "l'interface web, sous-système biométrique et stratégie de déploiement."
    )

    add_body(doc,
        "Conformément aux exigences académiques du programme, la conception "
        "s'appuie sur UML (cas d'utilisation, classes, séquences, activités, "
        "déploiement) et sur une architecture en couches séparant présentation, "
        "métier et persistance. Les choix techniques retenus — Laravel 11, "
        "Sanctum, Eloquent, MySQL/SQLite, bridge C# Windows — découlent des "
        "contraintes d'hébergement mutualisé et de l'intégration du lecteur "
        "ZK-9500, déjà argumentées aux chapitres I et II."
    )

    add_body(doc,
        "Ce chapitre ne décrit pas encore le code ligne à ligne : il fixe le "
        "cadre que le chapitre IV implémentera et testera. Chaque section "
        "renvoie explicitement aux exigences fonctionnelles (EF) du cahier "
        "des charges lorsque cela est pertinent."
    )

    add_body(doc,
        "Les diagrammes UML et le modèle entité-relation présentés ci-après "
        "ont été établis par analyse directe du dépôt applicatif "
        "(RH_CNSS/sgrh-pro et RH_CNSS/fingerprint-service) : migration "
        "2026_08_09_000001_create_sgrh_core_tables.php, routes/api.php, "
        "PresenceApiController, BiometricBridgeService, HeadlessBridge.cs "
        "et le module public/js/sgrh-vision.js. Ils ne constituent donc "
        "pas des schémas génériques, mais la traduction graphique de "
        "l'architecture réellement implémentée."
    )

    # ───────────────── III.2 ─────────────────
    add_heading(doc, "III.2. Architecture globale du système")

    add_subheading(doc, "III.2.1. Vue d'ensemble des composants")

    add_body(doc,
        "SGRH Pro s'organise en deux espaces physiques complémentaires. "
        "D'une part, un serveur applicatif (hébergement PHP) expose l'API "
        "REST Laravel et stocke les données dans MySQL (ou SQLite en "
        "développement). D'autre part, le poste Windows du terminal de "
        "pointage exécute le bridge biométrique C# en mode headless, "
        "relie le lecteur ZK-9500 et, le cas échéant, le lecteur RFID, "
        "puis dialogue avec l'API via HTTP local sécurisé par clé API."
    )

    add_body(doc,
        "L'interface utilisateur est une application web monopage (SPA) "
        "servie par Laravel et consommée dans le navigateur. Elle couvre "
        "le pilot de bord RH, le terminal de pointage, l'espace personnel "
        "de l'agent (« Mon espace ») et les modules métier. L'authentification "
        "repose sur des tokens Bearer Laravel Sanctum."
    )

    add_figure(
        doc, _fig("fig_iii1_architecture_globale.png"),
        "Figure 19 : Architecture globale de SGRH Pro (applicatif + poste de pointage)",
        width_cm=15.8,
    )

    add_subheading(doc, "III.2.2. Architecture logique et physique")

    add_table(doc,
              ["Couche", "Composant", "Responsabilité"],
              [
                  ["Présentation", "SPA HTML/CSS/JS", "Écrans RH, pointage, espace agent"],
                  ["Métier", "API Laravel 11", "Règles RH, RBAC, présence, exports"],
                  ["Persistance", "MySQL / SQLite", "Dossiers, pointages, templates"],
                  ["Acquisition", "Bridge C# + ZK/RFID", "Scan, match 1:N, badges"],
              ],
              caption="Tableau 28 : Répartition logique des responsabilités",
              col_widths=[3.0, 4.5, 8.5])

    add_body(doc,
        "Physiquement, le bridge reste volontairement sur le poste Windows : "
        "le SDK ZKFinger est conçu pour cet environnement et le capteur USB "
        "ne peut pas être piloté depuis un hébergement distant. Cette "
        "séparation évite de coupler le serveur applicatif au système "
        "d'exploitation du terminal (EF-04, EF-06, contrainte C-01)."
    )

    add_subheading(doc, "III.2.3. Flux de données entre composants")

    add_numbered_item(doc, 1,
        " l'utilisateur s'authentifie auprès de l'API ; un token Sanctum "
        "est stocké côté navigateur ;")
    add_numbered_item(doc, 2,
        " les opérations métier (CRUD employés, congés, KPI) transitent "
        "par l'API authentifiée ;")
    add_numbered_item(doc, 3,
        " pour un pointage empreinte, l'API demande un scan au bridge "
        "(POST /scan), puis une identification 1:N (POST /match) ;")
    add_numbered_item(doc, 4,
        " le contrôleur de présence enregistre l'entrée ou la sortie "
        "dans la table attendances et met à jour le tableau du jour ;")
    add_numbered_item(doc, 5,
        " l'espace agent lit les mêmes données filtrées sur employee_id "
        "du compte connecté.")

    # ───────────────── III.3 ─────────────────
    add_heading(doc, "III.3. Modélisation UML")

    add_subheading(doc, "III.3.1. Diagramme de cas d'utilisation")

    add_body(doc,
        "Le diagramme de cas d'utilisation recense l'ensemble des interactions "
        "du prototype. Cinq acteurs sont distingués : l'administrateur RH, "
        "le manager, l'agent, le lecteur d'empreintes et le lecteur RFID. "
        "Les associations sont orientées de l'acteur vers le cas qu'il déclenche. "
        "Les relations «include» (flèche pointillée ouverte) indiquent qu'un cas "
        "en appelle obligatoirement un autre : les cas métier protégés incluent "
        "« S'authentifier » ; l'enrôlement inclut « Capturer une empreinte » ; "
        "l'attribution d'un badge inclut « Lire un badge RFID ». "
        "Les relations «extend» matérialisent des variantes optionnelles : "
        "la capture d'empreinte et la lecture RFID étendent le pointage selon "
        "le mode choisi ; le changement de mot de passe étend l'authentification "
        "lorsque le drapeau must_change_password est actif. "
        "Le pointage kiosque n'inclut pas l'authentification : il reste possible "
        "sans session utilisateur, via le terminal (POST /presence/punch-public)."
    )

    add_figure(
        doc, _fig("fig_iii2_cas_utilisation.png"),
        "Figure 20 : Diagramme de cas d'utilisation complet de SGRH Pro",
        width_cm=15.8,
    )

    add_table(doc,
              ["Acteur", "Cas d'utilisation", "Exigences"],
              [
                  ["Tous (humains)", "S'authentifier, se déconnecter, changer le mot de passe", "EF-01"],
                  ["Admin RH", "Employés, départements, comptes/rôles, enrôlement, RFID, validation, KPI, rémunération, paramétrage", "EF-01 à EF-13"],
                  ["Manager", "Avis / validation des congés, suivi d'équipe, évaluations", "EF-08, EF-13"],
                  ["Agent", "Pointage, demande de congé, consultation de Mon espace", "EF-06, EF-14"],
                  ["Lecteur biométrique", "Capturer et comparer une empreinte (enrôlement et pointage)", "EF-04, EF-06"],
                  ["Lecteur RFID", "Lire un badge lors du pointage ou de l'attribution", "EF-05, EF-06"],
              ],
              caption="Tableau 29 : Acteurs et cas d'utilisation de SGRH Pro",
              col_widths=[3.2, 8.3, 4.5])

    add_subheading(doc, "III.3.2. Diagramme de classes")

    add_body(doc,
        "Le modèle de classes retenu reprend les entités du cœur métier : "
        "Rôle, Utilisateur, Employé, Département, Présence, Congé, "
        "Rémunération et Évaluation. Les multiplicités UML suivent le schéma "
        "réel : un compte peut exister sans dossier agent (employee_id nullable), "
        "un agent peut n'avoir aucun compte applicatif, un département n'est "
        "pas obligatoire (department_id nullable), et un agent peut n'avoir "
        "encore aucune présence, aucun congé, aucune rémunération ni évaluation. "
        "La figure 21 en présente un extrait centré sur le dossier agent, "
        "le pointage et les workflows RH."
    )

    add_figure(
        doc, _fig("fig_iii3_diagramme_classes.png"),
        "Figure 21 : Extrait du diagramme de classes métier",
        width_cm=15.8,
    )

    add_subheading(doc, "III.3.3. Diagramme de séquence — pointage biométrique")

    add_body(doc,
        "Le scénario critique du mémoire est le pointage quotidien. La "
        "séquence suivante reproduit le flux réel implémenté dans "
        "sgrh-vision.js : la fonction punchFingerprint() appelle d'abord "
        "POST /api/biometric/scan (BiometricApiController → "
        "BiometricBridgeService → POST localhost:5002/scan), puis "
        "POST /api/presence/punch avec {method: fingerprint, template}. "
        "PresenceApiController::identifyByFingerprint() construit la "
        "galerie des agents enrôlés et invoque bridge.match() ; le score "
        "retourné est comparé au seuil system_parameters "
        "fingerprint_match_threshold (40 par défaut). Elle couvre EF-06 et EF-07."
    )

    add_figure(
        doc, _fig("fig_iii4_sequence_pointage.png"),
        "Figure 22 : Diagramme de séquence du pointage biométrique",
        width_cm=15.8,
    )

    add_body(doc,
        "La règle métier est codée dans registerPunch() : absence de "
        "check_out ouvert → INSERT attendances (action checkin, source "
        "fingerprint ou rfid) ; présence ouverte → UPDATE check_out et "
        "worked_hours (action checkout) ; journée déjà clôturée → HTTP 409 "
        "avec action blocked. Le retard late_minutes est calculé via "
        "computeLateMinutes() à partir de work_start_time (08:00) et "
        "late_threshold_minutes (15 min de tolérance) — EF-16."
    )

    add_subheading(doc, "III.3.4. Diagramme d'activités — workflow de congé")

    add_figure(
        doc, _fig("fig_iii5_activite_conge.png"),
        "Figure 23 : Diagramme d'activités du workflow de congé",
        width_cm=15.8,
    )

    add_body(doc,
        "Le circuit Agent → Manager → Admin RH matérialise la séparation "
        "des tâches observée à la CNSS et répond à EF-08. Le statut de la "
        "demande (En attente, Approuvé, Rejeté) et le commentaire de "
        "décision sont persistés pour traçabilité."
    )

    add_subheading(doc, "III.3.5. Diagramme d'activités — processus de pointage")

    add_figure(
        doc, _fig("fig_iii5b_activite_pointage.png"),
        "Figure 24 : Diagramme d'activités du processus de pointage",
        width_cm=15.8,
    )

    add_body(doc,
        "Le second diagramme d'activités décrit la règle quotidienne "
        "d'entrée et de sortie. Après capture de l'empreinte ou lecture "
        "du badge, le système identifie l'agent. S'il n'est pas reconnu, "
        "le pointage est refusé. S'il l'est, le système vérifie qu'aucune "
        "journée n'est déjà clôturée (refus HTTP 409), puis enregistre "
        "soit une entrée, soit une sortie avec calcul des heures — "
        "conformément à registerPunch() (EF-06, EF-07, EF-16)."
    )

    add_subheading(doc, "III.3.6. Diagramme de déploiement")

    add_figure(
        doc, _fig("fig_iii6_deploiement.png"),
        "Figure 25 : Diagramme de déploiement de SGRH Pro",
        width_cm=15.8,
    )

    add_body(doc,
        "Deux nœuds suffisent au prototype : le serveur applicatif "
        "(artefacts API Laravel et base MySQL) et le poste terminal "
        "(navigateur SPA, bridge C#, ZK-9500, lecteur RFID). L'installateur "
        "Windows one-touch configure le démarrage automatique du bridge "
        "et la clé API alignée sur la configuration Laravel."
    )

    # ───────────────── III.4 ─────────────────
    add_heading(doc, "III.4. Conception de la base de données")

    add_subheading(doc, "III.4.1. Modèle entité-relation")

    add_body(doc,
        "Le modèle logique est relationnel et rédigé en français. "
        "Les cardinalités sont notées à la Merise : (min, max) inscrit à côté "
        "d'une entité indique combien d'occurrences de CETTE entité correspondent "
        "à une occurrence de l'entité liée. "
        "Côté RÔLE : (1,1) — un utilisateur (comme un employé) a exactement un rôle ; "
        "côté UTILISATEUR et EMPLOYÉ : (0,n) — un rôle peut n'être attribué à personne. "
        "Côté UTILISATEUR et côté EMPLOYÉ : (0,1) — employee_id est nullable et un agent "
        "peut n'avoir aucun compte. "
        "Côté EMPLOYÉ face à DÉPARTEMENT : (0,n) — un département compte de 0 à n agents ; "
        "côté DÉPARTEMENT : (0,1) — department_id est nullable. "
        "Côté EMPLOYÉ face aux tables filles : (1,1) — une présence, un congé, "
        "une rémunération ou une évaluation appartient à un seul agent ; "
        "côté PRÉSENCE, CONGÉ, RÉMUNÉRATION et ÉVALUATION : (0,n) — un agent peut "
        "n'en avoir encore aucun. Les autres tables (permissions, journaux, "
        "jours fériés, dispositifs, contrats, formations, etc.) sont décrites "
        "au modèle physique."
    )

    add_figure(
        doc, _fig("fig_iii7_mer.png"),
        "Figure 26 : Modèle logique de données (extrait) de SGRH Pro",
        width_cm=15.8,
    )
    add_source(doc)

    add_subheading(doc, "III.4.2. Tables principales")

    add_table(doc,
              ["Table", "Rôle", "Champs clés"],
              [
                  ["roles", "Profils d'accès", "name"],
                  ["permissions", "Droits unitaires", "name"],
                  ["role_permission", "Association RBAC", "role_id, permission_id"],
                  ["departments", "Services / directions", "name, budget, manager_id"],
                  ["employees", "Dossiers agents", "matricule, fingerprint_template, rfid_card_id"],
                  ["users", "Comptes applicatifs", "username, password, role_id, employee_id"],
                  ["activity_logs", "Journal d'audit", "username, action"],
                  ["attendances", "Présences", "check_in, check_out, late_minutes, source"],
                  ["leaves", "Congés", "start_date, end_date, status"],
                  ["holidays", "Jours fériés", "name, date, is_recurring"],
                  ["biometric_devices", "Terminaux biométriques", "name, device_type, location"],
                  ["remuneration_elements", "États pour la finance", "period, total_indicative, status"],
                  ["performance_evaluations", "Évaluations", "score, period, evaluator_id"],
                  ["system_parameters", "Paramètres système", "key, value"],
                  ["contracts", "Contrats de travail", "contract_type, contractual_salary"],
                  ["messages", "Messagerie interne", "sender_user_id, recipient_user_id"],
                  ["trainings / training_enrollments", "Formations", "title, employee_id, status"],
                  ["skills / employee_skills", "Compétences", "name, level"],
                  ["medical_leaves", "Arrêts maladie", "diagnosis, daily_allowance"],
                  ["notifications", "Alertes applicatives", "title, is_read"],
                  ["job_offers / job_applications", "Recrutement", "title, applicant_name, status"],
                  ["payrolls", "Bulletins de paie", "base_salary, net_salary, paid_at"],
              ],
              caption="Tableau 30 : Catalogue complet des tables du schéma SGRH Pro",
              col_widths=[5.2, 4.8, 6.0])

    add_subheading(doc, "III.4.3. Modèle physique de données (MPD)")

    add_body(doc,
        "Le modèle physique reprend les types et contraintes des migrations "
        "Laravel (cœur 2026_08_09_000001 et modules 2026_08_09_100000). "
        "Toutes les tables du schéma sont recensées. "
        "PK désigne la clé primaire, FK une clé étrangère, UK une unicité. "
        "Les horodatages created_at / updated_at sont présents sur chaque table."
    )

    add_table(doc,
              ["Champ", "Type", "Contrainte"],
              [
                  ["id", "BIGINT", "PK, AUTO_INCREMENT"],
                  ["username", "VARCHAR(80)", "NOT NULL, UK"],
                  ["password", "VARCHAR(255)", "NOT NULL"],
                  ["must_change_password", "BOOLEAN", "DEFAULT TRUE"],
                  ["employee_id", "BIGINT", "FK → employees(id), NULL"],
                  ["role_id", "BIGINT", "FK → roles(id), NOT NULL"],
                  ["remember_token", "VARCHAR(100)", "NULL"],
              ],
              caption="Tableau 31 : Table users",
              col_widths=[5.0, 4.5, 6.5])

    add_table(doc,
              ["Champ", "Type", "Contrainte"],
              [
                  ["id", "BIGINT", "PK, AUTO_INCREMENT"],
                  ["first_name / last_name", "VARCHAR(100)", "NOT NULL"],
                  ["matricule", "VARCHAR(40)", "UK, NULL"],
                  ["photo_path", "VARCHAR(255)", "NULL"],
                  ["email", "VARCHAR(120)", "NOT NULL, UK"],
                  ["phone", "VARCHAR(30)", "NOT NULL"],
                  ["address", "VARCHAR(255)", "NOT NULL"],
                  ["hire_date", "DATE", "NOT NULL"],
                  ["status", "VARCHAR(30)", "DEFAULT 'Actif'"],
                  ["department_id", "BIGINT", "FK → departments(id), NULL"],
                  ["role_id", "BIGINT", "FK → roles(id), NOT NULL"],
                  ["fingerprint_template", "LONGTEXT", "NULL"],
                  ["rfid_card_id", "VARCHAR(64)", "UK, NULL"],
                  ["rfid_card_active", "BOOLEAN", "DEFAULT TRUE"],
              ],
              caption="Tableau 32 : Table employees",
              col_widths=[5.0, 4.5, 6.5])

    add_table(doc,
              ["Champ", "Type", "Contrainte"],
              [
                  ["id", "BIGINT", "PK, AUTO_INCREMENT"],
                  ["employee_id", "BIGINT", "FK → employees(id), CASCADE"],
                  ["check_in", "DATETIME", "NOT NULL"],
                  ["check_out", "DATETIME", "NULL"],
                  ["worked_hours", "DECIMAL(8,2)", "DEFAULT 0"],
                  ["late_minutes", "INT UNSIGNED", "DEFAULT 0"],
                  ["is_absent", "BOOLEAN", "DEFAULT FALSE"],
                  ["source", "VARCHAR(20)", "fingerprint | rfid | manual"],
              ],
              caption="Tableau 33 : Table attendances",
              col_widths=[5.0, 4.5, 6.5])

    add_table(doc,
              ["Champ", "Type", "Contrainte"],
              [
                  ["id", "BIGINT", "PK, AUTO_INCREMENT"],
                  ["employee_id", "BIGINT", "FK → employees(id), CASCADE"],
                  ["start_date / end_date", "DATE", "NOT NULL"],
                  ["reason", "VARCHAR(255)", "NOT NULL"],
                  ["status", "VARCHAR(40)", "En attente | Approuvé | Rejeté"],
                  ["decision_comment", "VARCHAR(500)", "NULL"],
              ],
              caption="Tableau 34 : Table leaves",
              col_widths=[5.0, 4.5, 6.5])

    add_table(doc,
              ["Table", "Champ", "Type / contrainte"],
              [
                  ["roles", "id / name", "PK ; VARCHAR(80) UK"],
                  ["permissions", "id / name", "PK ; VARCHAR(120) UK"],
                  ["role_permission", "role_id + permission_id", "PK composite, FK CASCADE"],
              ],
              caption="Tableau 35 : Tables roles, permissions et role_permission",
              col_widths=[4.5, 5.5, 6.0])

    add_table(doc,
              ["Champ", "Type", "Contrainte"],
              [
                  ["id", "BIGINT", "PK, AUTO_INCREMENT"],
                  ["name", "VARCHAR(120)", "NOT NULL, UK"],
                  ["budget", "DECIMAL(14,2)", "DEFAULT 0"],
                  ["manager_id", "BIGINT", "FK → employees(id), NULL"],
              ],
              caption="Tableau 36 : Table departments",
              col_widths=[5.0, 4.5, 6.5])

    add_table(doc,
              ["Table", "Champs principaux", "Contraintes"],
              [
                  ["activity_logs", "username, action", "journal d'audit horodaté"],
                  ["holidays", "name, date, is_recurring", "jours fériés du calendrier"],
                  ["biometric_devices", "name, device_type, location, is_active, last_seen", "parc de terminaux"],
                  ["system_parameters", "key UK, value, description", "paramétrage applicatif"],
              ],
              caption="Tableau 37 : Tables activity_logs, holidays, biometric_devices et system_parameters",
              col_widths=[4.2, 6.5, 5.3])

    add_table(doc,
              ["Champ", "Type", "Contrainte"],
              [
                  ["id", "BIGINT", "PK, AUTO_INCREMENT"],
                  ["employee_id", "BIGINT", "FK → employees(id), CASCADE"],
                  ["period", "VARCHAR(20)", "NOT NULL"],
                  ["base_salary / bonus", "DECIMAL(14,2)", "NOT NULL / DEFAULT 0"],
                  ["overtime_hours / overtime_amount", "DECIMAL", "DEFAULT 0"],
                  ["deductions", "DECIMAL(14,2)", "DEFAULT 0"],
                  ["total_indicative", "DECIMAL(14,2)", "NOT NULL"],
                  ["status", "VARCHAR(40)", "DEFAULT 'Brouillon'"],
                  ["notes", "TEXT", "NULL"],
              ],
              caption="Tableau 38 : Table remuneration_elements",
              col_widths=[5.4, 4.3, 6.3])

    add_table(doc,
              ["Champ", "Type", "Contrainte"],
              [
                  ["id", "BIGINT", "PK, AUTO_INCREMENT"],
                  ["employee_id", "BIGINT", "FK → employees(id), CASCADE"],
                  ["evaluator_id", "BIGINT", "FK → employees(id), NULL"],
                  ["period", "VARCHAR(40)", "NOT NULL"],
                  ["score", "TINYINT UNSIGNED", "DEFAULT 0"],
                  ["objectives / strengths / improvements / comments", "TEXT", "NULL"],
                  ["status", "VARCHAR(40)", "DEFAULT 'Brouillon'"],
              ],
              caption="Tableau 39 : Table performance_evaluations",
              col_widths=[6.2, 4.0, 5.8])

    add_table(doc,
              ["Table", "Champs principaux", "Rôle"],
              [
                  ["contracts", "employee_id, contract_type, start_date, end_date, contractual_salary", "Contrats"],
                  ["messages", "sender_user_id, recipient_user_id, subject, content, sent_at", "Messagerie"],
                  ["trainings", "title, trainer, start_date, end_date, max_participants, status", "Sessions"],
                  ["training_enrollments", "training_id, employee_id, status, score, enrolled_at", "Inscriptions"],
                  ["skills", "name UK, category", "Référentiel"],
                  ["employee_skills", "employee_id, skill_id, level, certified_at", "Compétences agent"],
                  ["medical_leaves", "employee_id, start_date, end_date, diagnosis, daily_allowance", "Arrêts maladie"],
                  ["notifications", "user_id, type, title, message, is_read", "Alertes"],
                  ["job_offers", "title, department_id, description, requirements, status", "Offres"],
                  ["job_applications", "job_offer_id, applicant_name, applicant_email, cv_path, status", "Candidatures"],
                  ["payrolls", "employee_id, base_salary, bonus, deductions, taxes, net_salary, paid_at", "Paie"],
              ],
              caption="Tableau 40 : Tables des modules complémentaires",
              col_widths=[4.0, 8.0, 4.0])

    add_subheading(doc, "III.4.4. Intégrité et données biométriques")

    add_bullet(doc, " clés étrangères avec suppression contrôlée (cascade sur les "
               "présences liées à un agent) ;")
    add_bullet(doc, " unicité de matricule, email et rfid_card_id ;")
    add_bullet(doc, " stockage du template d'empreinte (longText) et non de l'image "
               "brute — principe déjà posé au chapitre I ;")
    add_bullet(doc, " drapeau rfid_card_active pour révoquer une carte sans supprimer "
               "l'historique des pointages ;")
    add_bullet(doc, " source du pointage (fingerprint, rfid, manual) pour traçabilité.")

    add_body(doc,
        "Les migrations Laravel matérialisent ce schéma et permettent de "
        "reproduire la base en environnement de développement (SQLite) "
        "puis de basculer vers MySQL en production sans réécrire le modèle "
        "Eloquent."
    )

    # ───────────────── III.5 ─────────────────
    add_heading(doc, "III.5. Conception du backend (API REST)")

    add_subheading(doc, "III.5.1. Organisation en couches")

    add_figure(
        doc, _fig("fig_iii8_couches_backend.png"),
        "Figure 27 : Architecture en couches du backend Laravel",
        width_cm=15.8,
    )

    add_body(doc,
        "La présentation s'appuie sur l'application ; celle-ci s'appuie à "
        "la fois sur la persistance (modèles Eloquent) et sur l'acquisition "
        "biométrique (bridge C#), sans que la base de données dépende du "
        "capteur. Les routes déclarées dans api.php délèguent aux contrôleurs "
        "(PresenceApiController, BiometricApiController, SpaAuthController, "
        "etc.). Les services encapsulent les appels au bridge et la "
        "journalisation. Cette structuration facilite les tests et limite "
        "le couplage."
    )

    add_subheading(doc, "III.5.2. Endpoints structurants")

    add_table(doc,
              ["Groupe", "Exemples d'endpoints", "Auth"],
              [
                  ["Auth", "POST /auth/login, GET /auth/me", "Public / Sanctum"],
                  ["Présences", "GET /presence/today, POST /presence/punch, POST /presence/punch-public, GET /presence/me", "Sanctum / kiosque"],
                  ["Biométrie", "POST /biometric/scan, POST /biometric/enroll/{id}", "Sanctum"],
                  ["RH", "CRUD /employees, /leaves, /departments", "Sanctum + RBAC"],
                  ["Pilotage", "GET /reports/dashboard", "Sanctum"],
              ],
              caption="Tableau 41 : Principaux groupes d'endpoints de l'API",
              col_widths=[2.8, 9.2, 4.0])

    add_subheading(doc, "III.5.3. Sécurité applicative")

    add_bullet(doc, " Sanctum : token Bearer après login, révocation à la déconnexion ;")
    add_bullet(doc, " bcrypt pour le hash des mots de passe ;")
    add_bullet(doc, " RBAC : permissions françaises (Voir employés, Valider congés, etc.) "
               "vérifiées côté serveur ;")
    add_bullet(doc, " journal d'activité pour les opérations sensibles "
               "(enrôlement, pointage, reset mot de passe) ;")
    add_bullet(doc, " validation des entrées au niveau des contrôleurs ;")
    add_bullet(doc, " clé API du bridge distincte des tokens utilisateurs.")

    add_body(doc,
        "Ces mécanismes couvrent EF-01, EF-02 et EF-15, et prolongent les "
        "principes de sécurité exposés au chapitre I."
    )

    # ───────────────── III.6 ─────────────────
    add_heading(doc, "III.6. Conception du frontend (interface web)")

    add_subheading(doc, "III.6.1. Structure des écrans")

    add_body(doc,
        "L'interface est organisée autour d'une barre latérale de navigation "
        "et d'un contenu central. Les entrées prioritaires du menu sont : "
        "Pilot de bord, Pointage, Mon espace, Présences (registre), "
        "Enrôlement biométrique, puis les modules RH (employés, congés, "
        "évaluations, rapports). Sur tablette et mobile, un tiroir de menu "
        "remplace la barre fixe."
    )

    add_table(doc,
              ["Écran", "Public cible", "Fonctions"],
              [
                  ["Pilot de bord", "Admin RH / Manager", "KPI, présence du jour, graphiques filtrables"],
                  ["Pointage", "Accueil / RH", "Horloge, empreinte, RFID, feed live, tableau du jour"],
                  ["Mon espace", "Agent", "Statut du jour, heures, retards, congés, évaluations"],
                  ["Enrôlement", "Admin RH", "Scan template, attribution RFID, liste enrôlés"],
                  ["Congés / Employés", "RH / Manager", "CRUD et workflows"],
              ],
              caption="Tableau 42 : Cartographie des écrans prioritaires",
              col_widths=[3.2, 4.0, 8.8])

    add_subheading(doc, "III.6.2. Terminal de pointage et espace agent")

    add_body(doc,
        "Le terminal de pointage est conçu comme un poste opérationnel : "
        "horloge temps réel, actions Empreinte / RFID, résultat immédiat, "
        "flux live et tableau filtrable (présents, sortis, non arrivés, "
        "absents). Il matérialise M3/M4 au centre de l'expérience utilisateur."
    )

    add_body(doc,
        "Mon espace répond à EF-14 : l'agent voit uniquement ses données "
        "(statut du jour, série d'heures et de retards, évaluations, congés). "
        "Cette limitation est appliquée côté API via le rattachement "
        "user.employee_id, et non seulement par masquage d'écran."
    )

    add_subheading(doc, "III.6.3. Ergonomie et personnalisation du dashboard")

    add_body(doc,
        "Le tableau de bord expose de nombreux indicateurs. Pour éviter la "
        "surcharge visuelle, la conception prévoit un panneau « Personnaliser "
        "l'affichage » : l'utilisateur choisit les blocs et graphiques "
        "visibles ; le choix est mémorisé localement. Par défaut, seuls les "
        "essentiels (KPI, présence du jour, masse salariale, départements, "
        "présences/absences, activité) sont affichés."
    )

    # ───────────────── III.7 ─────────────────
    add_heading(doc, "III.7. Conception du sous-système biométrique")

    add_subheading(doc, "III.7.1. Architecture du Fingerprint Bridge")

    add_body(doc,
        "Le bridge est une application .NET Windows publiée en mode "
        "self-contained (win-x86) pour cohabiter avec le SDK ZKFinger. "
        "En production, il s'exécute en mode --headless : pas d'interface "
        "obligatoire, écoute HTTP sur le port 5002, journalisation dans "
        "le profil applicatif. Les endpoints structurants sont GET /status, "
        "POST /scan et POST /match."
    )

    add_subheading(doc, "III.7.2. Protocole bridge ↔ backend")

    add_numbered_item(doc, 1,
        " Laravel appelle le bridge avec l'en-tête X-API-KEY ;")
    add_numbered_item(doc, 2,
        " /scan renvoie un template Base64 issu du ZK-9500 ;")
    add_numbered_item(doc, 3,
        " /match compare ce template à la galerie des agents enrôlés "
        "(id, template_b64) et renvoie le meilleur score ;")
    add_numbered_item(doc, 4,
        " PresenceApiController n'enregistre le pointage que si le score "
        "dépasse le seuil paramétré (fingerprint_match_threshold).")

    add_body(doc,
        "Pour le RFID, l'identification est directe en base "
        "(rfid_card_id + rfid_card_active). La même règle entrée/sortie "
        "s'applique, indépendamment de la modalité (EF-05, EF-06)."
    )

    add_subheading(doc, "III.7.3. Installateur one-touch et sécurisation")

    add_body(doc,
        "Le kit d'installation Windows (INSTALLER.bat) copie le payload, "
        "intègre les DLL ZK disponibles, fixe la clé API machine, crée "
        "une tâche de démarrage à l'ouverture de session, ouvre le port "
        "5002 en pare-feu et lance immédiatement le service. La clé peut "
        "également être stockée via DPAPI LocalMachine côté bridge. "
        "Cette conception répond à la contrainte C-06 (prototype "
        "démontrable sur un poste unique) tout en préparant la "
        "duplication sur plusieurs terminaux."
    )

    # ───────────────── III.8 ─────────────────
    add_heading(doc, "III.8. Conception des modules métier RH")

    add_body(doc,
        "Les huit modules du cahier des charges sont conçus comme des "
        "périmètres fonctionnels partageant le même socle technique. "
        "Le tableau 43 en rappelle la conception cible."
    )

    add_table(doc,
              ["Module", "Conception clé", "Artefacts"],
              [
                  ["M1 Accès", "Login Sanctum, rôles, audit", "SpaAuth, Role, ActivityLog"],
                  ["M2 Employés", "Dossier unique, affectation", "Employee, Department"],
                  ["M3 Biométrie", "Enrôlement ZK/RFID", "BiometricApi, Bridge"],
                  ["M4 Présences", "Entrée/sortie, retard, feed", "PresenceApi, Attendance"],
                  ["M5 Congés", "Workflow Agent→Manager→RH", "LeaveApi"],
                  ["M6 Rémunération", "États indicatifs exportables", "RemunerationElement"],
                  ["M7 Évaluation", "Grille, score, historique", "PerformanceEvaluation"],
                  ["M8 Rapports", "KPI et graphiques", "ReportApi, dashboard"],
              ],
              caption="Tableau 43 : Conception synthétique des huit modules",
              col_widths=[3.0, 6.5, 6.5])

    add_body(doc,
        "M6 respecte la règle institutionnelle rappelée dès l'introduction : "
        "SGRH Pro produit des états administratifs ; la direction financière "
        "exécute les virements bancaires. Aucun module de virement n'est "
        "conçu dans le périmètre du mémoire."
    )

    add_body(doc,
        "Les domaines secondaires éventuellement présents dans le code "
        "(contrats, formation, recrutement) restent hors du cœur de "
        "conception du chapitre III, conformément au recentrage décidé "
        "au chapitre II."
    )

    # ───────────────── III.9 ─────────────────
    add_heading(doc, "III.9. Conception de la dimension intelligente")

    add_subheading(doc, "III.9.1. Indicateurs KPI")

    add_body(doc,
        "La dimension « intelligente » retenue est celle de l'aide à la "
        "décision opérationnelle, non celle du machine learning. Les KPI "
        "calculés automatiquement incluent notamment : effectif actif, "
        "taux d'absence, retards du jour, inscriptions/évaluations, "
        "congés en attente, taux de présence journalier."
    )

    add_subheading(doc, "III.9.2. Alertes et tableaux de bord")

    add_bullet(doc, " alertes de retard et d'absence après l'heure limite ;")
    add_bullet(doc, " congés en attente de validation ;")
    add_bullet(doc, " notifications métier consultables dans l'interface ;")
    add_bullet(doc, " dashboards différenciés : vue institutionnelle (RH), "
               "vue équipe (Manager), vue personnelle (Agent).")

    add_body(doc,
        "La personnalisation des graphiques du pilot de bord fait partie "
        "de la conception UX : elle réduit le bruit informationnel tout "
        "en conservant la richesse analytique pour la soutenance et "
        "l'exploitation quotidienne."
    )

    # ───────────────── III.10 ─────────────────
    add_heading(doc, "III.10. Stratégie d'hébergement et déploiement")

    add_subheading(doc, "III.10.1. Options retenues")

    add_body(doc,
        "Pour le prototype institutionnel, l'hébergement mutualisé PHP/MySQL "
        "est retenu comme cible de production légère : il correspond aux "
        "offres courantes (Hostinger et équivalents) et justifie Laravel. "
        "Le bridge, lui, ne peut pas y résider : il s'installe sur chaque "
        "PC de pointage Windows."
    )

    add_table(doc,
              ["Environnement", "Backend", "Base", "Bridge"],
              [
                  ["Développement", "php artisan serve", "SQLite", "localhost:5002"],
                  ["Démonstration poste RH", "Laravel local/serveur", "SQLite/MySQL", "Installateur one-touch"],
                  ["Production cible", "Hébergement PHP", "MySQL", "PC terminal(s) Windows"],
              ],
              caption="Tableau 44 : Environnements de déploiement",
              col_widths=[4.0, 4.5, 3.5, 4.0])

    add_subheading(doc, "III.10.2. Démonstration sur poste unique")

    add_body(doc,
        "Le scénario de soutenance et de validation (critères d'acceptation "
        "du chapitre II) suppose un poste unique : navigateur + API + bridge "
        "+ ZK-9500. Cette configuration couvre C-06 et permet d'enchaîner "
        "enrôlement, pointage réel, consultation KPI et espace agent sans "
        "infrastructure complexe."
    )

    # ───────────────── III.11 ─────────────────
    add_heading(doc, "III.11. Conclusion du chapitre")

    add_body(doc,
        "Ce chapitre a transformé le cahier des charges en architecture "
        "opérationnelle. L'organisation en couches Laravel, le schéma de "
        "données centré sur l'employé et les présences, les diagrammes UML et la "
        "conception du bridge biométrique constituent le référentiel de "
        "construction du prototype."
    )

    add_body(doc,
        "Le pointage — entrée le matin, sortie en fin de journée, "
        "identification empreinte ou RFID — y apparaît comme le fil "
        "conducteur technique et fonctionnel, en cohérence avec la "
        "problématique du mémoire et avec l'application réalisée. "
        "Le chapitre IV décrira l'implémentation effective, les tests "
        "et la validation de ces choix de conception."
    )

    return page_start


def build():
    doc = init_document()
    append_chapitre3(doc, PAGE_START)
    out = OUTPUT
    try:
        doc.save(out)
    except PermissionError:
        out = OUTPUT_FALLBACK
        doc.save(out)
        print("Note : fichier ouvert — sauvegarde alternative")
    words = sum(len(p.text.split()) for p in doc.paragraphs)
    print(f"Chapitre III genere : {out}")
    print(f"Mots approximatifs : {words}")


if __name__ == "__main__":
    build()

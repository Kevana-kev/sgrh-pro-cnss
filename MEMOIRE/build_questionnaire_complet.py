# -*- coding: utf-8 -*-
"""
Questionnaire Q/R COMPLET — préparation soutenance SGRH Pro / CNSS.
Couvre : intro, chapitres I à IV, conclusion, technique, oral, questions simples.
"""
from pathlib import Path

from memoire_format import (
    init_document, add_chapter_title, add_heading, add_subheading,
    add_body, add_mixed, add_bullet, add_numbered_item,
)

OUTPUT = Path(r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\QUESTIONNAIRE COMPLET - SOUTENANCE SGRH PRO.docx")
OUTPUT_FALLBACK = OUTPUT.with_name(OUTPUT.stem + " - v2.docx")


def qa(doc, q: str, a: str):
    add_mixed(doc, [("Q. ", True, False), (q, True, False)])
    add_body(doc, "R. " + a)


def section_pitch(doc):
    add_heading(doc, "1. Pitch de 30 secondes (à réciter debout)")

    qa(doc,
       "Présentez votre travail en 30 secondes.",
       "Je m'appelle BONGA KASUSA Rebecca. Mon mémoire porte sur la conception "
       "et l'implémentation de SGRH Pro, un système de gestion des ressources "
       "humaines pour le siège de la CNSS à Kinshasa. Le logiciel centralise "
       "les dossiers agents, le pointage par empreinte digitale ZK-9500 et "
       "carte RFID, les congés, les évaluations et les tableaux de bord. "
       "J'ai analysé le fonctionnement actuel, conçu l'architecture, développé "
       "un prototype fonctionnel et validé les scénarios principaux.")

    qa(doc,
       "En une phrase : quel problème résolvez-vous ?",
       "Remplacer le papier et Excel par un système unique, traçable et "
       "fiable pour suivre le personnel de la CNSS.")

    qa(doc,
       "En une phrase : quelle est votre solution ?",
       "SGRH Pro : une application web avec biométrie et RFID pour un "
       "pointage imputable et un pilotage RH en temps réel.")


def section_personnel(doc):
    add_heading(doc, "2. Vous, le stage et le contexte")

    qa(doc, "Qui êtes-vous ?", "BONGA KASUSA Rebecca, étudiante en informatique de gestion (B3), auteure du mémoire.")

    qa(doc, "Où avez-vous fait votre stage ?", "À la CNSS — Caisse Nationale de Sécurité Sociale, siège central à Kinshasa (Gombe).")

    qa(doc, "Quel était votre rôle pendant le stage ?", "Observer le service RH, identifier les dysfonctionnements, proposer et développer une solution informatique adaptée au terrain.")

    qa(doc, "Pourquoi la CNSS et pas une autre entreprise ?", "C'est le lieu du stage ; institution publique importante en RDC ; problèmes RH concrets et mesurables (pointage, congés, états).")

    qa(doc, "Votre directeur de mémoire vous a-t-il imposé le sujet ?", "Le sujet découle du constat terrain et du cadrage académique ; il a été validé et orienté par l'encadrement.")

    qa(doc, "Avez-vous travaillé seule ou en équipe ?", "Seule sur le mémoire et le développement principal ; échanges avec le service RH pour les besoins et la validation des écrans.")

    qa(doc, "Combien de temps a duré le projet ?", "Environ 63 jours ouvrés de travail technique (juillet–septembre 2026), plus la rédaction et la soutenance.")

    qa(doc, "Qu'avez-vous appris personnellement ?", "Analyser un besoin réel, modéliser (UML), développer full-stack, intégrer du matériel biométrique, et communiquer avec des non-informaticiens.")


def section_basique(doc):
    add_heading(doc, "3. Questions très simples (le jury teste votre clarté)")

    add_body(doc, "Ne sous-estimez pas ces questions : elles vérifient que vous maîtrisez le vocabulaire.")

    for q, a in [
        ("Qu'est-ce qu'un logiciel ?", "Un programme qui exécute des tâches pour l'utilisateur. Exemple : SGRH Pro, Word, Excel."),
        ("Qu'est-ce qu'un site web / application web ?", "Un logiciel accessible via un navigateur (Chrome, Edge) avec une adresse. Pas besoin d'installer une grosse application sur chaque PC."),
        ("Qu'est-ce qu'Internet ?", "Un réseau mondial qui relie des ordinateurs. Notre prototype peut tourner en local ; Internet n'est pas obligatoire pour la démo."),
        ("Qu'est-ce qu'un ordinateur serveur ?", "Une machine (ou un programme) qui fournit un service aux autres. Ici : l'API Laravel qui répond au navigateur."),
        ("Qu'est-ce qu'une base de données ?", "Un stockage organisé et durable des informations (agents, pointages, congés…)."),
        ("Qu'est-ce qu'un fichier Excel ?", "Un tableur pour calculer et lister. Utile mais limité pour un système multi-utilisateurs sécurisé."),
        ("Qu'est-ce qu'un mot de passe ?", "Un secret pour prouver son identité à la connexion."),
        ("Qu'est-ce qu'un identifiant / login ?", "Le nom d'utilisateur ou matricule qui dit « qui je suis » avant le mot de passe."),
        ("Qu'est-ce qu'un tableau de bord ?", "Un écran qui résume les chiffres importants (effectif, absences, congés…) pour décider vite."),
        ("Qu'est-ce qu'un export PDF ?", "Générer un document imprimable à partir des données du système."),
        ("Qu'est-ce qu'un capteur ?", "Un appareil physique qui lit une information (ici : empreinte ou carte RFID)."),
        ("Qu'est-ce qu'un USB ?", "Port pour brancher un périphérique (lecteur ZK-9500) sur le PC."),
        ("Qu'est-ce qu'une interface utilisateur ?", "Ce que l'utilisateur voit et clique : boutons, menus, formulaires."),
        ("Qu'est-ce qu'un bug ?", "Une erreur dans le programme. On corrige avec des tests et du débogage."),
        ("Qu'est-ce qu'une mise à jour logicielle ?", "Une nouvelle version qui corrige ou améliore le système."),
        ("Qu'est-ce que la maintenance ?", "Corriger, adapter et faire évoluer le logiciel après la livraison."),
        ("Qu'est-ce qu'un utilisateur final ?", "La personne qui utilise le système au quotidien (agent, responsable RH)."),
        ("Qu'est-ce qu'un administrateur ?", "Celui qui gère les comptes, les droits et la configuration (Admin RH)."),
        ("Qu'est-ce qu'une sauvegarde (backup) ?", "Copie des données pour les restaurer en cas de panne."),
        ("Qu'est-ce qu'un prototype ?", "Une première version démontrable, pas encore le déploiement national."),
    ]:
        qa(doc, q, a)


def section_intro(doc):
    add_heading(doc, "4. Introduction, problématique et méthodologie")

    qa(doc, "Quel est le titre exact du mémoire ?",
       "Conception et implémentation d'un système d'information intelligent de gestion des ressources humaines intégrant la biométrie (ZK-Teco 9500) et les cartes RFID pour le suivi et l'optimisation du personnel : cas de la CNSS.")

    qa(doc, "Qu'est-ce que SGRH Pro ?",
       "Système de Gestion des Ressources Humaines Professionnel : application web centralisant dossiers agents, pointage biométrique/RFID, présences, congés, rémunération (états), évaluations et rapports.")

    qa(doc, "Quelle est la problématique ?",
       "Comment concevoir et implémenter un SIGRH fiable pour la CNSS, basé sur un logiciel modulaire complété par empreinte et RFID, pour mieux suivre le personnel au siège central ?")

    qa(doc, "Quels sont les objectifs généraux et spécifiques ?",
       "Général : concevoir et implémenter SGRH Pro. Spécifiques : analyser l'existant, spécifier les besoins, modéliser, développer le prototype, intégrer ZK-9500/RFID, tester et documenter.")

    qa(doc, "Quelle est l'hypothèse de recherche ?",
       "Un SIGRH intégré améliore le suivi administratif : centralisation, automatisation des présences/congés, pointage imputable, KPI pour le pilotage.")

    qa(doc, "Que signifie « intelligent » dans le titre ?",
       "Pas d'IA lourde : tableaux de bord, KPI, alertes (retards, absences, congés en attente) pour aider à décider.")

    qa(doc, "Quel est le périmètre géographique ?",
       "Siège central CNSS Kinshasa. Pas les agences provinciales dans ce mémoire.")

    qa(doc, "Qu'est-ce qui est hors périmètre ?",
       "Gestion des assurés sociaux et cotisations ; virements bancaires ; calcul fiscal officiel ; app mobile native ; reconnaissance faciale ; déploiement multi-sites national.")

    qa(doc, "Quelles méthodes de recherche ?",
       "Observation participante, entretiens semi-directifs, analyse documentaire, approche structuro-fonctionnelle, développement itératif, UML, tests.")

    qa(doc, "Pourquoi ce sujet est-il pertinent pour la RDC ?",
       "Modernisation administrative, traçabilité dans le secteur public, réduction de la fraude au pointage, gain de temps pour la RH.")

    qa(doc, "Le système paie-t-il les salaires ?", "Non. Il produit des états administratifs pour la direction financière qui effectue les virements.")


def section_ch1(doc):
    add_heading(doc, "5. Chapitre I — Cadre théorique")

    qa(doc, "Qu'est-ce que la GRH ?", "Gestion des Ressources Humaines : pratiques pour recruter, administrer, développer et suivre le personnel.")

    qa(doc, "Qu'est-ce qu'un SIGRH / SIRH ?", "Système d'Information des Ressources Humaines : logiciel qui collecte, stocke, traite et restitue les données RH.")

    qa(doc, "Quelles sont les trois couches d'un SIGRH ?", "Acquisition (saisies, pointage) ; Traitement (règles, workflows) ; Restitution (rapports, KPI).")

    qa(doc, "Qu'est-ce que la biométrie ?", "Identification par caractéristique physique. Ici : empreinte digitale.")

    qa(doc, "Qu'est-ce que le ZK-9500 ?", "Lecteur d'empreintes ZKTeco en USB, utilisé pour enrôlement et pointage (~80 USD).")

    qa(doc, "Qu'est-ce que le RFID ?", "Identification par carte/badge sans contact (radio). Pointage complémentaire ou de secours.")

    qa(doc, "Pourquoi empreinte + RFID ?", "Empreinte = forte identification ; RFID = secours si doigt blessé ou lecteur indisponible.")

    qa(doc, "Quels risques avec la biométrie ?", "Données sensibles : consentement, stockage de templates (pas d'image brute), traçabilité, révocation carte.")

    qa(doc, "Pourquoi pas SAP / Odoo / Workday ?", "Coût, complexité, hébergement, et intégration native du ZK-9500 non garantie. SGRH Pro est adapté au contexte CNSS.")

    qa(doc, "Qu'est-ce que l'architecture n-tiers ?", "Séparation présentation / métier / données pour faciliter évolution et maintenance.")

    qa(doc, "Qu'est-ce qu'un KPI ?", "Indicateur clé : effectif, absentéisme, retards, score d'évaluation…")

    qa(doc, "Qu'est-ce qu'un workflow ?", "Circuit de validation par étapes (ex. congé : demande → responsable → RH).")


def section_ch2(doc):
    add_heading(doc, "6. Chapitre II — Analyse CNSS et besoins")

    qa(doc, "Qu'est-ce que la CNSS ?", "Caisse Nationale de Sécurité Sociale de la RDC. Le mémoire concerne le personnel interne du siège, pas les assurés.")

    qa(doc, "Comment fonctionne le RH aujourd'hui (constat) ?", "Registres papier, Excel, pointage manuel, congés sur formulaires, consolidation lente pour la finance.")

    qa(doc, "Citez les dysfonctionnements D1 à D7.", "Doublons ; pointage peu fiable ; retards admin ; congés mal synchronisés ; évaluations non structurées ; pas de traçabilité ; pas de reporting.")

    qa(doc, "Qui sont les acteurs ?", "Admin RH, Responsable, Agent ; Bridge biométrique, ZK-9500, lecteur RFID ; API + base de données.")

    qa(doc, "Combien de modules au cœur du système ?", "Huit modules cœur : Accès, Employés, Biométrie, Présences, Congés, Rémunération, Évaluation, Rapports.")

    qa(doc, "Pourquoi huit modules ?", "Périmètre réaliste pour un mémoire : l'essentiel RH + pointage. D'autres écrans (formation, recrutement) sont des extensions démo du prototype.")

    qa(doc, "Expliquez chaque module en une phrase.",
       "M1 connexion/droits ; M2 dossiers ; M3 enrôlement ZK/RFID ; M4 heures/retards ; M5 congés ; M6 états finance ; M7 évaluations ; M8 KPI.")

    qa(doc, "Qu'est-ce que MoSCoW ?", "Priorisation : Must (indispensable), Should, Could, Won't (hors scope maintenant).")

    qa(doc, "Donnez un exemple d'exigence fonctionnelle.", "EF-04 : enrôler une empreinte via ZK-9500. EF-01 : authentifier par identifiant et mot de passe.")

    qa(doc, "Décrivez le scénario de pointage.", "1er scan = arrivée ; 2e = sortie ; 3e refusé. Identification 1:N ou RFID. Horodatage et calcul retard.")

    qa(doc, "Décrivez le workflow de congé.", "Agent demande → Responsable avise → Admin RH décide → solde mis à jour.")

    qa(doc, "Qu'est-ce que le chemin critique PERT ?", "Chaîne de tâches sans marge : A→B→C→D→E→F→I→J = 63 jours ouvrés.")

    qa(doc, "Quel budget matériel ?", "Environ 160 USD (ZK-9500 ~80 USD, RFID, câbles, contingence). Logiciels open source gratuits.")


def section_ch3(doc):
    add_heading(doc, "7. Chapitre III — Conception et architecture")

    qa(doc, "Pourquoi modéliser avant de coder ?", "Pour clarifier les acteurs, les flux, les données et éviter de coder au hasard.")

    qa(doc, "Qu'est-ce qu'UML ?", "Langage de modélisation unifié : diagrammes de cas d'utilisation, classes, séquences, activités, déploiement.")

    qa(doc, "Quels diagrammes UML avez-vous produits ?",
       "Architecture globale, cas d'utilisation, classes, séquence pointage, activités congé/pointage, déploiement, MER (MLD), couches backend.")

    qa(doc, "Qu'est-ce qu'un cas d'utilisation ?", "Une fonction du système vue par un acteur (ex. « Pointer par empreinte »).")

    qa(doc, "Que signifient « include » et « extend » ?", "Include = sous-fonction obligatoire réutilisée ; extend = comportement optionnel selon condition.")

    qa(doc, "Qu'est-ce qu'un diagramme de séquence ?", "Ordre chronologique des messages entre acteurs et composants (ex. pointage : UI → API → Bridge → ZK).")

    qa(doc, "Qu'est-ce qu'un diagramme de classes ?", "Structure des entités (Employé, Présence, Congé…) et leurs relations.")

    qa(doc, "Qu'est-ce que le MLD / MER ?", "Modèle logique de données : tables, clés, cardinalités (1,n), (0,1)…")

    qa(doc, "Quelles tables principales ?", "users, employees, departments, attendances, leaves, payrolls, contracts, fingerprint templates, roles, permissions…")

    qa(doc, "Pourquoi séparer User et Employee ?", "User = compte de connexion ; Employee = dossier RH. Un compte peut être lié à un employé.")

    qa(doc, "Comment stockez-vous les empreintes en base ?", "Champ fingerprint_template : JSON de 3 templates (modèles), pas l'image brute.")

    qa(doc, "Quelle architecture logicielle ?", "Client web (SPA) ↔ API REST Laravel ↔ SQLite/MySQL ; Bridge C# local ↔ ZK-9500 USB.")

    qa(doc, "Pourquoi un bridge C# séparé ?", "Le SDK ZKTeco est Windows/.NET ; le navigateur ne peut pas accéder directement à l'USB.")

    qa(doc, "Quel port pour le bridge ?", "5002 en local (127.0.0.1). Communication HTTP entre Laravel et le bridge.")

    qa(doc, "Qu'est-ce que RBAC dans la conception ?", "Rôles (SuperAdmin, Admin RH, Manager, Employé, Comptable) avec permissions granulaires.")

    qa(doc, "Qu'est-ce qu'un middleware d'authentification ?", "Filtre qui vérifie le token avant d'autoriser l'accès à une route API.")


def section_ch4(doc):
    add_heading(doc, "8. Chapitre IV — Implémentation, tests et interfaces")

    qa(doc, "Quelle stack technique exacte ?",
       "Backend : PHP 8, Laravel 11, Eloquent, Sanctum, bcrypt. Frontend : HTML/CSS/JS, Chart.js. Bridge : C# .NET, SDK ZKTeco. BDD : SQLite (dev) / MySQL (prod). Export : DomPDF.")

    qa(doc, "Où est le code source ?", "Dépôt RH_CNSS/sgrh-pro (application Laravel) + service bridge biométrique.")

    qa(doc, "Comment lancer le prototype ?", "php artisan serve (port 8000) + bridge sur port 5002 + navigateur sur http://127.0.0.1:8000.")

    qa(doc, "Quels comptes de démonstration ?", "superadmin, adminrh, manager, agent — mots de passe documentés dans le mémoire / README.")

    qa(doc, "Quelles interfaces avez-vous réalisées ?",
       "Connexion, pilot de bord, pointage, Mon espace, enrôlement biométrique, congés, employés, rapports (+ modules démo : formation, recrutement…).")

    qa(doc, "Qu'est-ce que le pilot de bord ?", "Écran KPI : effectif, masse salariale, absences, performance, présence du jour en temps réel.")

    qa(doc, "Qu'est-ce que « Mon espace » ?", "Portail agent : statut du jour, heures, bulletin, contrat, formations, notifications, graphiques assiduité.")

    qa(doc, "Comment fonctionne l'enrôlement des 3 doigts ?",
       "L'admin sélectionne l'employé, scanne 3 doigts distincts. Chaque scan est vérifié anti-doublon (session + base). Enregistrement final seulement si 3 templates valides.")

    qa(doc, "Pourquoi 3 empreintes par personne ?", "Fiabilité (doigt blessé) et réduction des faux rejets ; standard courant en biométrie RH.")

    qa(doc, "Que se passe-t-il si on scanne deux fois le même doigt ?", "Refus : message d'erreur, pas d'enregistrement.")

    qa(doc, "Quelles actions sur les employés enrôlés ?", "Menu : désactiver/supprimer carte RFID, modifier carte, supprimer empreinte, relancer enrôlement.")

    qa(doc, "Comment fonctionne le pointage 1:N ?", "Le bridge compare l'empreinte scannée à la galerie de tous les templates enrôlés et retourne le meilleur score.")

    qa(doc, "Quel seuil de matching ?", "Paramètre système fingerprint_match_threshold (ex. 40) — configurable.")

    qa(doc, "Quels tests avez-vous effectués ?", "Tests manuels des parcours : login, enrôlement, pointage entrée/sortie, congé, exports, rôles. Tests unitaires sur services critiques si documentés.")

    qa(doc, "Le prototype est-il en production ?", "Non. Démonstration au siège ; généralisation = perspective.")

    qa(doc, "Quelles figures illustrent le chapitre IV ?", "Figures 28–35 : captures d'écran des interfaces réelles (login, dashboard, pointage, Mon espace, enrôlement, congés, employés, rapports).")


def section_tech(doc):
    add_heading(doc, "9. Questions techniques (détaillées mais compréhensibles)")

    for q, a in [
        ("Qu'est-ce qu'une API REST ?", "Interface web standard : URL + GET/POST/PUT/DELETE, réponses en JSON."),
        ("Exemple d'endpoint ?", "POST /api/auth/login ; GET /api/presence/today ; POST /api/biometric/enroll/{id}."),
        ("Qu'est-ce que JSON ?", "Format texte structuré pour échanger des données entre programmes."),
        ("Qu'est-ce que Laravel ?", "Framework PHP : routes, contrôleurs, modèles, migrations, sécurité."),
        ("Qu'est-ce qu'Eloquent ?", "ORM Laravel : manipuler la base avec des objets PHP."),
        ("Qu'est-ce que Sanctum ?", "Authentification par token Bearer après login."),
        ("Qu'est-ce que bcrypt ?", "Algorithme de hachage des mots de passe (irréversible)."),
        ("Différence SQLite / MySQL ?", "SQLite = fichier local simple ; MySQL = serveur pour production."),
        ("Qu'est-ce qu'une migration ?", "Fichier versionné qui crée/modifie les tables de la base."),
        ("Qu'est-ce qu'un contrôleur ?", "Classe qui reçoit la requête HTTP et appelle la logique métier."),
        ("Qu'est-ce qu'un service (couche métier) ?", "Classe qui centralise les règles (ex. FingerprintTemplateService)."),
        ("Qu'est-ce que le matching biométrique ?", "Comparer une empreinte inconnue à une base de templates enregistrés."),
        ("Qu'est-ce qu'un template d'empreinte ?", "Représentation mathématique du doigt, pas une photo."),
        ("Pourquoi ne pas stocker la photo du doigt ?", "Moins lourd, plus conforme aux bonnes pratiques de protection des données."),
        ("Qu'est-ce que CORS ?", "Règles de sécurité navigateur pour les appels entre origines (API)."),
        ("Qu'est-ce qu'un seed / seeder ?", "Script qui remplit la base avec des données de test (employés démo)."),
        ("Qu'est-ce que Chart.js ?", "Bibliothèque JavaScript pour les graphiques du dashboard."),
        ("Qu'est-ce qu'une SPA ?", "Single Page Application : une page web qui change de section sans recharger toute la page."),
        ("Qu'est-ce qu'un token JWT / Bearer ?", "Ticket numérique envoyé à chaque requête pour prouver la session."),
        ("Que fait le rate limiting ?", "Limite le nombre de requêtes pour éviter les abus (brute force)."),
    ]:
        qa(doc, q, a)


def section_securite(doc):
    add_heading(doc, "10. Sécurité, éthique et données personnelles")

    qa(doc, "Comment protégez-vous les mots de passe ?", "Hachage bcrypt, jamais en clair en base.")

    qa(doc, "Comment protégez-vous l'API ?", "Token Sanctum, RBAC, validation des entrées, HTTPS en production.")

    qa(doc, "Qui peut voir les données des autres agents ?", "Selon le rôle : un agent voit surtout son espace ; Admin RH voit tout.")

    qa(doc, "Conformité RGPD / loi congolaise ?", "Mesures techniques de base (consentement, minimisation, traçabilité). Conformité juridique complète = démarche institutionnelle au-delà du mémoire.")

    qa(doc, "Peut-on supprimer les données d'un employé ?", "Oui : droit à l'oubli prévu dans la conception (suppression dossier, empreintes, carte).")

    qa(doc, "Que loguez-vous dans le journal d'audit ?", "Actions sensibles : enrôlement, modification RFID, validation congé, connexion admin…")

    qa(doc, "Un collègue peut-il pointer pour un autre ?", "Difficile avec empreinte ; possible avec carte si prêtée — d'où la biométrie comme moyen principal.")


def section_limites(doc):
    add_heading(doc, "11. Limites, critiques et perspectives")

    qa(doc, "Quelles sont les limites du travail ?",
       "Un seul poste de pointage ; dépendance Windows/USB ; pas de virement bancaire ; provisions fiscales indicatives ; prototype pas certifié juridiquement ; pas multi-sites.")

    qa(doc, "Votre système élimine-t-il toute fraude ?", "Non. Il réduit fortement le risque mais n'annule pas la fraude organisationnelle.")

    qa(doc, "Et si le lecteur tombe en panne ?", "Pointage RFID en secours ; maintenance matérielle ; statut bridge affiché dans l'interface.")

    qa(doc, "Et sans électricité ?", "Le système ne fonctionne pas ; il faut un plan de continuité institutionnel.")

    qa(doc, "Perspectives d'évolution ?",
       "Multi-sites provinciaux ; hébergement central MySQL ; app mobile consultation ; agrégateur bancaire ; IA pour anomalies (hors scope actuel).")

    qa(doc, "Pourquoi ne pas utiliser uniquement Excel ?", "Pas multi-utilisateur sécurisé, pas de workflow, pas d'audit, pas de biométrie native, risque d'erreurs.")

    qa(doc, "Qu'apporteriez-vous en V2 ?", "Sync cloud, plusieurs lecteurs, SSO institutionnel, module paie avancé, API Powens si besoin bancaire RH.")


def section_oral(doc):
    add_heading(doc, "12. Questions de soutenance pratique")

    qa(doc, "Faites une démo en direct ?", "Oui si possible : login adminrh → dashboard → pointage → Mon espace agent. Prévoir plan B (captures figures 28–35).")

    qa(doc, "Que faire si la biométrie ne marche pas le jour J ?", "Montrer le mode mock du bridge + captures d'écran + expliquer l'architecture.")

    qa(doc, "Comment répondre si on ne connaît pas un détail de code ?", "« La règle métier est documentée au chapitre III ; l'implémentation est dans le service X du dépôt. »")

    qa(doc, "Comment répondre à une critique ?", "Reconnaître la limite, expliquer le choix, proposer une piste d'amélioration.")

    qa(doc, "Quelle est VOTRE contribution ?", "Analyse CNSS, cahier des charges, modélisation UML, développement intégral, intégration biométrie, prototype démontrable.")

    qa(doc, "Avez-vous copié un projet existant ?", "Non. Code développé pour ce mémoire ; Laravel est un framework open source, pas un copier-coller d'application.")

    qa(doc, "Pourquoi vous et pas un commercial ?", "Adaptation au contexte CNSS, maîtrise du code, coût maîtrisé, intégration ZK-9500 native.")

    qa(doc, "Le jury demande « en français simple » ?", "« Un logiciel RH pour la CNSS : on pointe avec le doigt ou la carte, la RH voit tout en un seul endroit au lieu de cahiers et Excel. »")


def section_cheatsheet(doc):
    add_heading(doc, "13. Aide-mémoire chiffres et mots-clés")

    items = [
        ("Titre", "SIGRH + biométrie ZK-9500 + RFID — cas CNSS"),
        ("Modules cœur", "8 (Accès → Rapports)"),
        ("Durée PERT", "63 jours ouvrés"),
        ("Chemin critique", "A→B→C→D→E→F→I→J"),
        ("Budget", "~160 USD"),
        ("ZK-9500", "~80 USD, USB"),
        ("Bridge", "C#, port 5002"),
        ("Backend", "Laravel 11, PHP"),
        ("Auth", "Sanctum + bcrypt"),
        ("Empreintes", "3 doigts / personne, anti-doublon"),
        ("Pointage", "1 entrée + 1 sortie / jour"),
        ("Figures interfaces", "28 à 35 (chapitre IV)"),
        ("Auteure", "BONGA KASUSA Rebecca"),
    ]
    for k, v in items:
        add_bullet(doc, f" {k} : {v}.")

    add_heading(doc, "14. Conseils finaux pour l'oral")
    add_numbered_item(doc, 1, " Commencez toujours par le problème CNSS, pas par la technologie.")
    add_numbered_item(doc, 2, " Réponse courte d'abord (10–20 s), détail ensuite si on relance.")
    add_numbered_item(doc, 3, " Ne dites jamais que le logiciel « paie » : il produit des états.")
    add_numbered_item(doc, 4, " Montrez les captures figures 28–35 si la démo live échoue.")
    add_numbered_item(doc, 5, " Assurez-vous que adminrh / agent fonctionnent avant la soutenance.")
    add_numbered_item(doc, 6, " Relisez ce questionnaire à voix haute 3 fois minimum.")


def section_conclusion(doc):
    add_heading(doc, "15. Conclusion, hypothèses et apports")

    qa(doc, "Vos hypothèses sont-elles validées ?",
       "Oui au niveau prototype : centralisation, automatisation présences/congés, pointage imputable, KPI — avec réserve : validation institutionnelle à grande échelle non faite.")

    qa(doc, "Quel est l'apport scientifique ?", "Modèle SIGRH adapté au contexte institutionnel congolais avec intégration biométrique ZK-9500 et RFID documentée de bout en bout.")

    qa(doc, "Quel est l'apport pratique pour la CNSS ?", "Prototype utilisable pour démontrer un circuit RH numérique : pointage, congés, états, pilotage.")

    qa(doc, "Que retenir en une phrase de la conclusion ?", "Il est possible, dans le cadre d'un mémoire, de livrer un SIGRH opérationnel répondant aux besoins du siège CNSS.")

    qa(doc, "Quelles recommandations pour la CNSS ?",
       "Pilote sur 3 mois au RH ; formation des utilisateurs ; politique de données biométriques ; budget matériel ; passage MySQL serveur interne.")


def section_figures(doc):
    add_heading(doc, "16. Questions sur les figures et captures")

    qa(doc, "Que montre la figure 28 (connexion) ?", "Écran split-screen institutionnel CNSS + formulaire sécurisé identifiant/mot de passe.")

    qa(doc, "Que montre la figure 29 (dashboard) ?", "8 KPI, présence du jour, graphiques — pilot de bord Admin RH.")

    qa(doc, "Que montre la figure 30 (pointage) ?", "Terminal biométrique : horloge, scan empreinte/RFID, flux temps réel, tableau du jour.")

    qa(doc, "Que montre la figure 31 (Mon espace) ?", "Portail agent : statut, bulletin, contrat, formations, assiduité.")

    qa(doc, "Que montre la figure 32 (enrôlement) ?", "Scan 3 doigts, assignation RFID, menu actions employés enrôlés.")

    qa(doc, "Que montre la figure 33 (congés) ?", "Statistiques congés, file d'attente validation, historique.")

    qa(doc, "Que montre la figure 34 (employés) ?", "Liste 25 agents, filtres, statuts Actif/Suspendu/Démissionné.")

    qa(doc, "Que montre la figure 35 (rapports) ?", "Masse salariale, salaire moyen, taux absence, répartition par département.")


def section_pièges(doc):
    add_heading(doc, "17. Questions pièges supplémentaires")

    qa(doc, "Pourquoi PHP et pas Python/Java ?", "PHP + Laravel = hébergement mutualisé courant, courbe d'apprentissage maîtrisée, écosystème riche pour le web.")

    qa(doc, "Votre base est-elle normalisée ?", "Oui : 3NF visée, clés étrangères, tables séparées par domaine (RH, présence, sécurité).")

    qa(doc, "Avez-vous fait de l'IA ?", "Non. « Intelligent » = aide à la décision par KPI et alertes, pas machine learning.")

    qa(doc, "Combien d'employés dans la démo ?", "25 employés fictifs congolais pour les captures et tests.")

    qa(doc, "Le RFID remplace-t-il l'empreinte ?", "Non. Complément/secours. L'empreinte reste le moyen principal d'identification forte.")

    qa(doc, "Un agent peut-il modifier son propre salaire ?", "Non. Rôle et permissions l'interdisent ; seuls les profils autorisés gèrent les états.")

    qa(doc, "Que se passe-t-il à minuit si quelqu'un n'a pas pointé la sortie ?", "Journée ouverte jusqu'à clôture manuelle ou règle métier ; à préciser en production.")

    qa(doc, "Pourquoi trois scans max par jour ?", "Règle métier : une arrivée et une sortie ; troisième scan = journée déjà close (refus).")

    qa(doc, "Avez-vous testé avec de vrais agents CNSS ?", "Tests avec comptes démo et scénarios validés avec le service RH ; déploiement massif = perspective.")

    qa(doc, "C'est quoi la différence entre rémunération et paie ?", "Rémunération dans SGRH Pro = états administratifs (présences, variables) ; paie = virement par la finance.")

    qa(doc, "Pourquoi Kinshasa seulement ?", "Périmètre réaliste pour un mémoire de B3 ; le siège central concentre la fonction RH étudiée.")

    qa(doc, "Si on vous demande une faille de sécurité ?", "Prototype local : renforcer HTTPS, durcir serveur, audit externe avant production nationale.")


def build():
    doc = init_document()
    add_chapter_title(
        doc,
        "QUESTIONNAIRE COMPLET DE PRÉPARATION À LA SOUTENANCE\n"
        "SGRH Pro — CNSS Kinshasa — BONGA KASUSA Rebecca",
    )
    add_body(doc,
        "Ce document recense les questions que le jury peut poser — des plus "
        "simples aux plus techniques — avec des réponses claires. Apprenez "
        "d'abord les réponses courtes ; utilisez les détails si on approfondit. "
        "Couvre l'introduction, les chapitres I à IV, la conclusion, la "
        "sécurité, les limites et l'oral.")

    section_pitch(doc)
    section_personnel(doc)
    section_basique(doc)
    section_intro(doc)
    section_ch1(doc)
    section_ch2(doc)
    section_ch3(doc)
    section_ch4(doc)
    section_tech(doc)
    section_securite(doc)
    section_limites(doc)
    section_oral(doc)
    section_conclusion(doc)
    section_figures(doc)
    section_pièges(doc)
    section_cheatsheet(doc)

    add_body(doc,
        "— Fin du questionnaire complet. Bonne préparation pour la soutenance. —")

    out = OUTPUT
    try:
        doc.save(out)
    except PermissionError:
        out = OUTPUT_FALLBACK
        doc.save(out)
        print("Note : fichier ouvert — sauvegarde alternative")
    print(f"Questionnaire complet genere : {out}")


if __name__ == "__main__":
    build()

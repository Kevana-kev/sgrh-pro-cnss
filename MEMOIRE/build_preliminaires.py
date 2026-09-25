# -*- coding: utf-8 -*-
"""Pages préliminaires du mémoire (modèle UWB / Clémence)."""
from memoire_format import (
    add_chapter_title, add_body, add_table, add_page_break,
    add_reserved_title_page, add_mixed, add_dotted_entry, start_body_section,
)

# Numérotation continue (modèle Clémence), ordre d'apparition dans le mémoire
FIGURES = [
    ("Figure 1 : Cycle de vie de l'agent couvert par un SIGRH intégré", "…"),
    ("Figure 2 : Évolution des générations de systèmes d'information RH", "…"),
    ("Figure 3 : Architecture fonctionnelle à trois couches d'un SIGRH", "…"),
    ("Figure 4 : Modèle de contrôle d'accès par rôles (RBAC) dans SGRH Pro", "…"),
    ("Figure 5 : Chaîne de transformation des données en aide à la décision RH", "…"),
    ("Figure 6 : Lecteur d'empreintes digitales ZK-9500 (poste RH)", "…"),
    ("Figure 7 : Carte RFID nominative et lecteur USB associé", "…"),
    ("Figure 8 : Processus d'enrôlement biométrique et de pointage dans SGRH Pro", "…"),
    ("Figure 9 : Architecture globale du système SGRH Pro", "…"),
    ("Figure 10 : Organigramme simplifié du siège central CNSS (focus DRH)", "…"),
    ("Figure 11 : Chaîne documentaire fragmentée du système actuel", "…"),
    ("Figure 12 : Comparaison entre pointage manuel et dispositif cible SGRH Pro", "…"),
    ("Figure 13 : Acteurs humains et composants techniques du système cible", "…"),
    ("Figure 14 : Workflow de validation d'une demande de congé", "…"),
    ("Figure 15 : Architecture modulaire des huit composants de SGRH Pro", "…"),
    ("Figure 16 : Graphe PERT / MPM du projet SGRH Pro", "…"),
    ("Figure 17 : Chemin critique du projet (63 jours ouvrés)", "…"),
    ("Figure 18 : Diagramme de Gantt du projet SGRH Pro", "…"),
    ("Figure 19 : Architecture globale de SGRH Pro (applicatif + poste de pointage)", "…"),
    ("Figure 20 : Diagramme de cas d'utilisation complet de SGRH Pro", "…"),
    ("Figure 21 : Extrait du diagramme de classes métier", "…"),
    ("Figure 22 : Diagramme de séquence du pointage biométrique", "…"),
    ("Figure 23 : Diagramme d'activités du workflow de congé", "…"),
    ("Figure 24 : Diagramme d'activités du processus de pointage", "…"),
    ("Figure 25 : Diagramme de déploiement de SGRH Pro", "…"),
    ("Figure 26 : Modèle logique de données (extrait) de SGRH Pro", "…"),
    ("Figure 27 : Architecture en couches du backend Laravel", "…"),
    ("Figure 28 : Interface d'authentification de SGRH Pro", "…"),
    ("Figure 29 : Tableau de bord principal (pilot de bord RH)", "…"),
    ("Figure 30 : Terminal de pointage (empreinte et RFID)", "…"),
    ("Figure 31 : Espace personnel de l'agent (Mon espace)", "…"),
    ("Figure 32 : Enrôlement biométrique et attribution RFID", "…"),
    ("Figure 33 : Gestion des demandes de congé", "…"),
    ("Figure 34 : Gestion des dossiers employés", "…"),
    ("Figure 35 : Rapports et indicateurs de pilotage", "…"),
]

TABLEAUX = [
    ("Tableau 1 : Facteurs de réussite d'un SIGRH en contexte africain", "…"),
    ("Tableau 2 : Principaux KPI RH implémentés dans SGRH Pro", "…"),
    ("Tableau 3 : Typologie des alertes automatiques dans SGRH Pro", "…"),
    ("Tableau 4 : Modules SGRH Pro et apports décisionnels", "…"),
    ("Tableau 5 : Comparatif des modalités d'identification", "…"),
    ("Tableau 6 : Comparatif des solutions SIGRH et positionnement de SGRH Pro", "…"),
    ("Tableau 7 : Grille multicritères de sélection (échelle qualitative)", "…"),
    ("Tableau 8 : Dysfonctionnements CNSS et réponses du système proposé", "…"),
    ("Tableau 9 : Diagrammes UML prévus au chapitre III", "…"),
    ("Tableau 10 : Principes d'architecture de SGRH Pro", "…"),
    ("Tableau 11 : Démarche de collecte et d'analyse des besoins", "…"),
    ("Tableau 12 : Outils actuels de gestion RH à la CNSS", "…"),
    ("Tableau 13 : Synthèse des dysfonctionnements du système actuel", "…"),
    ("Tableau 14 : Forces et faiblesses du système actuel", "…"),
    ("Tableau 15 : Indicateurs demandés par les acteurs", "…"),
    ("Tableau 16 : Matrice acteurs / besoins", "…"),
    ("Tableau 17 : Scénarios d'utilisation prioritaires", "…"),
    ("Tableau 18 : Spécification synthétique des huit modules", "…"),
    ("Tableau 19 : Interdépendances principales entre modules", "…"),
    ("Tableau 20 : Exigences non fonctionnelles (synthèse)", "…"),
    ("Tableau 21 : Orientations techniques (niveau cahier des charges)", "…"),
    ("Tableau 22 : Exigences fonctionnelles (extrait)", "…"),
    ("Tableau 23 : Recensement des tâches du projet SGRH Pro", "…"),
    ("Tableau 24 : Ordonnancement des tâches (méthode MPM)", "…"),
    ("Tableau 25 : Calcul MPM (dates au plus tôt et au plus tard)", "…"),
    ("Tableau 26 : Calendrier d'exécution prévisionnel", "…"),
    ("Tableau 27 : Estimation du coût du projet SGRH Pro", "…"),
    ("Tableau 28 : Répartition logique des responsabilités", "…"),
    ("Tableau 29 : Acteurs et cas d'utilisation de SGRH Pro", "…"),
    ("Tableau 30 : Catalogue complet des tables du schéma SGRH Pro", "…"),
    ("Tableau 31 : Table users", "…"),
    ("Tableau 32 : Table employees", "…"),
    ("Tableau 33 : Table attendances", "…"),
    ("Tableau 34 : Table leaves", "…"),
    ("Tableau 35 : Tables roles, permissions et role_permission", "…"),
    ("Tableau 36 : Table departments", "…"),
    ("Tableau 37 : Tables activity_logs, holidays, biometric_devices et system_parameters", "…"),
    ("Tableau 38 : Table remuneration_elements", "…"),
    ("Tableau 39 : Table performance_evaluations", "…"),
    ("Tableau 40 : Tables des modules complémentaires", "…"),
    ("Tableau 41 : Principaux groupes d'endpoints de l'API", "…"),
    ("Tableau 42 : Cartographie des écrans prioritaires", "…"),
    ("Tableau 43 : Conception synthétique des huit modules", "…"),
    ("Tableau 44 : Environnements de déploiement", "…"),
    ("Tableau 45 : Technologies et outils d'implémentation", "…"),
    ("Tableau 46 : Cartographie des écrans implémentés", "…"),
    ("Tableau 47 : Paramètres de la démonstration locale", "…"),
    ("Tableau 48 : Scénarios de tests fonctionnels", "…"),
    ("Tableau 49 : Contrôle d'accès selon le profil", "…"),
    ("Tableau 50 : Correspondance entre besoins identifiés et réponses", "…"),
]


def write_preliminaires(doc):
    add_reserved_title_page(doc, "EPIGRAPHE")
    add_reserved_title_page(doc, "DÉDICACE")
    add_reserved_title_page(doc, "REMERCIEMENTS")

    add_chapter_title(doc, "ABRÉVIATIONS ET SIGLES")
    add_table(doc,
              ["Sigle / Abréviation", "Signification"],
              [
                  [".NET", "Plateforme de développement Microsoft (service biométrique)"],
                  ["API", "Application Programming Interface"],
                  ["BD", "Base de données"],
                  ["C#", "Langage utilisé pour le service de lecture d'empreintes"],
                  ["CNSS", "Caisse Nationale de Sécurité Sociale"],
                  ["CPM", "Critical Path Method (méthode du chemin critique)"],
                  ["CRUD", "Create, Read, Update, Delete"],
                  ["DRH", "Direction des Ressources Humaines"],
                  ["Gantt", "Diagramme de planification temporelle des tâches"],
                  ["GRH", "Gestion des Ressources Humaines"],
                  ["HTTP", "HyperText Transfer Protocol"],
                  ["IHM", "Interface Homme-Machine"],
                  ["JSON", "JavaScript Object Notation"],
                  ["JWT", "JSON Web Token (jeton d'authentification)"],
                  ["KPI", "Key Performance Indicator (indicateur clé de performance)"],
                  ["Laravel", "Cadre applicatif PHP utilisé pour SGRH Pro"],
                  ["MER", "Modèle Entité-Relation"],
                  ["MLD", "Modèle Logique de Données"],
                  ["MPD", "Modèle Physique de Données"],
                  ["MPM", "Méthode des Potentiels Métra"],
                  ["MySQL", "Système de gestion de bases de données relationnelles"],
                  ["PERT", "Program Evaluation and Review Technique"],
                  ["PHP", "Langage de programmation côté serveur"],
                  ["RBAC", "Role-Based Access Control (contrôle d'accès par rôles)"],
                  ["RDC", "République Démocratique du Congo"],
                  ["REST", "Representational State Transfer"],
                  ["RFID", "Radio-Frequency Identification"],
                  ["RH", "Ressources humaines"],
                  ["SDK", "Software Development Kit"],
                  ["SGBD", "Système de Gestion de Base de Données"],
                  ["SGRH Pro", "Système de Gestion des Ressources Humaines Professionnel"],
                  ["SI", "Système d'Information"],
                  ["SIGRH / SIRH", "Système d'Information de Gestion des Ressources Humaines"],
                  ["SQL", "Structured Query Language"],
                  ["SQLite", "Moteur de base de données embarqué (démonstration locale)"],
                  ["TIC", "Technologies de l'Information et de la Communication"],
                  ["UML", "Unified Modeling Language"],
                  ["USB", "Universal Serial Bus"],
                  ["UWB", "Université William Booth"],
                  ["Windows", "Système d'exploitation du poste de démonstration"],
                  ["ZK-9500", "Lecteur d'empreintes digitales ZKTeco 9500"],
                  ["ZKFinger", "Kit de développement biométrique ZKTeco"],
              ],
              col_widths=[4.5, 11.5])
    add_page_break(doc)

    add_chapter_title(doc, "LISTE DES FIGURES")
    for title, page in FIGURES:
        add_dotted_entry(doc, title, page)
    add_page_break(doc)

    add_chapter_title(doc, "LISTE DES TABLEAUX")
    for title, page in TABLEAUX:
        add_dotted_entry(doc, title, page)
    add_page_break(doc)

    add_chapter_title(doc, "RÉSUMÉ")
    add_body(doc,
        "La modernisation de la gestion des ressources humaines constitue un enjeu "
        "majeur pour les institutions publiques congolaises. À la Caisse Nationale "
        "de Sécurité Sociale (CNSS), le suivi du personnel au siège central de "
        "Kinshasa repose encore, pour une part importante, sur des registres, "
        "des fichiers dispersés et un pointage peu fiable. Cette situation "
        "génère des lenteurs administratives, des écarts de présence difficiles "
        "à justifier et une faible capacité de pilotage."
    )
    add_body(doc,
        "Le présent mémoire porte sur la conception et l'implémentation de "
        "SGRH Pro, un système d'information intelligent de gestion des "
        "ressources humaines intégrant la biométrie (lecteur ZK-9500) et les "
        "cartes RFID. L'objectif est de centraliser les dossiers, fiabiliser "
        "le pointage entrée/sortie, structurer le circuit des congés, produire "
        "des états destinés à la direction financière et restituer des "
        "indicateurs de suivi aux responsables."
    )
    add_body(doc,
        "La démarche a consisté à analyser l'existant et les besoins, à "
        "formaliser un cahier des charges de huit modules, à concevoir "
        "l'architecture et les diagrammes UML, puis à réaliser et tester un "
        "prototype opérationnel. La dimension « intelligente » retenue "
        "correspond aux tableaux de bord, aux alertes et aux indicateurs, "
        "et non à un modèle d'apprentissage automatique."
    )
    add_body(doc,
        "Le prototype démontre la faisabilité d'un suivi quotidien par "
        "empreinte ou badge, d'un espace personnel pour l'agent et d'un "
        "pilotage RH sur un poste unique de démonstration. Les principales "
        "limites concernent le nombre de terminaux, la dépendance au poste "
        "Windows et le cadre juridique des données biométriques."
    )
    add_mixed(doc, [
        ("Mots-clés : ", True, False),
        ("SIGRH, gestion des ressources humaines, biométrie, empreinte digitale, "
         "RFID, pointage, CNSS, tableaux de bord, UML, République Démocratique du Congo.",
         False, False),
    ])
    add_page_break(doc)

    add_chapter_title(doc, "ABSTRACT")
    add_body(doc,
        "The modernization of human resource management is a major challenge "
        "for Congolese public institutions. At the National Social Security "
        "Fund (CNSS), staff follow-up at the Kinshasa headquarters still "
        "relies largely on paper registers, scattered spreadsheets and "
        "unreliable attendance recording. This situation leads to delays, "
        "unexplained presence gaps and weak decision-making capacity."
    )
    add_body(doc,
        "This thesis presents the design and implementation of SGRH Pro, "
        "an intelligent HR information system integrating fingerprint "
        "biometrics (ZK-9500 reader) and RFID cards. The system aims to "
        "centralize employee files, secure check-in and check-out, "
        "structure leave approval, produce administrative statements for "
        "the finance department and provide managers with key indicators."
    )
    add_body(doc,
        "The research followed a progressive approach: analysis of the "
        "existing situation and needs, specification of eight functional "
        "modules, UML-based design, then implementation and testing of "
        "an operational prototype. Intelligence is understood here as "
        "dashboards, alerts and KPIs, not as machine-learning models."
    )
    add_body(doc,
        "The prototype shows that daily fingerprint or badge attendance, "
        "a personal employee space and an HR dashboard can be demonstrated "
        "on a single workstation. Main limitations include the number of "
        "terminals, dependence on a Windows workstation and the legal "
        "framework for biometric data."
    )
    add_mixed(doc, [
        ("Keywords: ", True, False),
        ("HRIS, human resource management, biometrics, fingerprint, RFID, "
         "attendance, CNSS, dashboards, UML, Democratic Republic of the Congo.",
         False, False),
    ])
    add_page_break(doc)

    add_chapter_title(doc, "RÉSUMÉ EN LINGALA")
    add_body(doc,
        "Kobongisa ndenge basali ya Leta bazali kokamba basali na bango "
        "ezali likambo ya ntina na RDC. Na CNSS, na ndako-mokolo ya Kinshasa, "
        "bokambi ya basali ezali kaka mingi na mikanda, na ba fichiers "
        "o yo ezali kopalangana mpe na pointage o yo ezali te ya boyokani. "
        "Yango ezali komema retard, mpe makambo ya présence o yo ezali "
        "mpasi koyebisa na bosembo."
    )
    add_body(doc,
        "Mémoire oyo etali conception mpe implémentation ya SGRH Pro, "
        "système ya sango ya GRH o yo ezali na biométrie (lecteur ZK-9500) "
        "mpe ba cartes RFID. Mokano ezali ya kokanga ba dossiers na esika "
        "moko, kobongisa pointage ya kokota mpe kobima, kosala circuit "
        "ya ba congés, kobimisa ba états mpo na finance mpe kopesa ba "
        "indicateurs na ba responsables."
    )
    add_body(doc,
        "Mosala etambolaki na analyse ya système o yo ezali, na cahier "
        "des charges ya modules mwambe, na conception UML, na sima "
        "implémentation mpe ba tests ya prototype. « Intelligence » "
        "awawa ezali ba tableaux de bord, ba alertes mpe ba KPI."
    )
    add_mixed(doc, [
        ("Maloba ya ntina : ", True, False),
        ("SIGRH, GRH, biométrie, empreinte, RFID, pointage, CNSS, "
         "tableaux de bord, UML, RDC.", False, False),
    ])
    # Section suivante = corps (pagination arabe à partir de 1)
    start_body_section(doc)

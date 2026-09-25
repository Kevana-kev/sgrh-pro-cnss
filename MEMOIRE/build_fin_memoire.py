# -*- coding: utf-8 -*-
"""Conclusion générale, bibliographie et table des matières (modèle Clémence)."""
from memoire_format import (
    add_chapter_title, add_heading, add_body, add_bullet,
    add_page_break, add_biblio_entry, add_dotted_entry,
)


def write_conclusion_bibliographie(doc, page_start=78):
    add_chapter_title(doc, "CONCLUSION GÉNÉRALE")

    add_body(doc,
        "Au terme de ce travail, il convient de revenir sur la problématique "
        "posée en introduction, de rappeler le chemin parcouru et d'apprécier "
        "dans quelle mesure les hypothèses ont été confirmées par le prototype "
        "SGRH Pro, conçu pour le siège central de la Caisse Nationale de "
        "Sécurité Sociale."
    )

    add_heading(doc, "Synthèse des travaux réalisés")

    add_body(doc,
        "L'introduction a situé le sujet dans le contexte de la modernisation "
        "administrative congolaise et a formulé la question centrale : comment "
        "concevoir et implémenter un SIGRH capable d'assurer un suivi fiable "
        "du personnel, en s'appuyant sur une application de gestion et sur "
        "des dispositifs d'identification par empreinte et par carte RFID."
    )

    add_body(doc,
        "Le premier chapitre a établi le cadre théorique : notions de GRH et "
        "de SIGRH, dimension intelligente entendue comme aide à la décision, "
        "principes de la biométrie et des cartes RFID, limites des pratiques "
        "manuelles. Les choix de langages et d'outils y ont été volontairement "
        "écartés, afin de rester au niveau conceptuel."
    )

    add_body(doc,
        "Le deuxième chapitre a confronté ces notions à la réalité du siège "
        "central de la CNSS. L'observation, les entretiens et l'analyse "
        "documentaire ont permis de diagnostiquer la dispersion des dossiers, "
        "la faiblesse du pointage et l'absence de tableaux de bord. Huit "
        "modules ont été spécifiés, ainsi qu'une planification PERT/Gantt."
    )

    add_body(doc,
        "Le troisième chapitre a traduit le cahier des charges en conception : "
        "architecture, cas d'utilisation, classes, séquence de pointage, "
        "workflow de congé, déploiement, modèle logique et physique des "
        "données. Le quatrième chapitre a décrit l'implémentation réelle, "
        "les extraits de code du dépôt RH_CNSS, les tests et les captures "
        "d'écran des interfaces réalisées."
    )

    add_heading(doc, "Validation des hypothèses")

    add_body(doc,
        "L'hypothèse générale — un SIGRH intégré améliore le suivi "
        "administratif du personnel — est confirmée au niveau du prototype : "
        "les dossiers sont centralisés, le pointage est horodaté, les congés "
        "suivent un circuit explicite et les indicateurs sont calculés "
        "automatiquement."
    )

    add_bullet(doc, " la centralisation réduit les écarts entre registres et fichiers "
               "éparpillés (hypothèse 1) ;")
    add_bullet(doc, " l'automatisation des présences et des congés accélère la "
               "production des états (hypothèse 2) ;")
    add_bullet(doc, " l'empreinte et le RFID rendent le pointage imputable à "
               "un agent identifié (hypothèse 3) ;")
    add_bullet(doc, " les KPI et l'espace agent renforcent le pilotage et la "
               "transparence (hypothèse 4).")

    add_body(doc,
        "Ces confirmations restent celles d'un prototype de démonstration. "
        "Une validation institutionnelle à grande échelle, sur plusieurs "
        "semaines d'exploitation réelle, dépasse le cadre du mémoire."
    )

    add_heading(doc, "Apports et limites")

    add_body(doc,
        "Pour la CNSS, l'apport principal est de disposer d'un modèle "
        "opérationnel de suivi quotidien, reproductible sur le poste du "
        "responsable RH, sans prétendre remplacer la direction financière "
        "dans l'exécution des virements. Pour la formation, le travail "
        "articule analyse de terrain, modélisation UML et implémentation "
        "contrôlée."
    )

    add_body(doc,
        "Les limites concernent le nombre de terminaux, la dépendance au "
        "poste Windows, le périmètre fonctionnel recentré sur huit modules "
        "et le cadre juridique des données biométriques, seulement abordé "
        "sous l'angle des bonnes pratiques du prototype."
    )

    add_heading(doc, "Perspectives")

    add_body(doc,
        "Plusieurs évolutions peuvent être envisagées : déploiement sur "
        "plusieurs postes de pointage, hébergement institutionnel, "
        "application mobile de consultation, interconnexion contrôlée avec "
        "les états déjà produits pour la finance, et, à plus long terme, "
        "des analyses prédictives d'absentéisme. Ces pistes confirment que "
        "SGRH Pro constitue une base, et non un aboutissement définitif."
    )

    add_body(doc,
        "En définitive, le mémoire montre qu'un système d'information "
        "intelligent de gestion des ressources humaines, adossé à la "
        "biométrie et aux cartes RFID, peut contribuer concrètement à "
        "l'optimisation du suivi du personnel au siège central de la CNSS, "
        "à condition d'être conçu à partir des processus réels et validé "
        "par un prototype démontrable."
    )

    add_page_break(doc)
    add_chapter_title(doc, "BIBLIOGRAPHIE")

    add_heading(doc, "A. Ouvrages généraux sur les systèmes d'information et le génie logiciel")
    add_biblio_entry(doc, 1,
        "Booch, G., Rumbaugh, J., & Jacobson, I. (2005). The unified modeling "
        "language user guide (2nd ed.). Addison-Wesley Professional.")
    add_biblio_entry(doc, 2,
        "Laudon, K. C., & Laudon, J. P. (2020). Management information systems: "
        "Managing the digital firm (16th ed.). Pearson.")
    add_biblio_entry(doc, 3,
        "Sommerville, I. (2016). Software engineering (10th ed.). Pearson.")
    add_biblio_entry(doc, 4,
        "Fowler, M. (2022). Patterns of enterprise application architecture. "
        "Addison-Wesley.")
    add_biblio_entry(doc, 5,
        "Reix, R. (2019). Systèmes d'information et management des organisations. "
        "Vuibert.")

    add_heading(doc, "B. Gestion des ressources humaines et SIGRH")
    add_biblio_entry(doc, 6,
        "Dessler, G. (2020). Human resource management (16th ed.). Pearson.")
    add_biblio_entry(doc, 7,
        "Beaudoin, P., & Roy, M. (2019). Les systèmes d'information de gestion "
        "des ressources humaines. Presses de l'Université.")
    add_biblio_entry(doc, 8,
        "Ndiaye, A., & Diop, S. (2021). Systèmes d'information RH et réalités "
        "africaines. Revue africaine de gestion, 8(1).")
    add_biblio_entry(doc, 9,
        "Boateng, R., & Agyemang, F. (2021). Digitalisation of public organisations "
        "in Africa. African Journal of Information Systems, 13(2).")

    add_heading(doc, "C. Biométrie, identification et sécurité")
    add_biblio_entry(doc, 10,
        "Jain, A. K., Ross, A., & Nandakumar, K. (2021). Introduction to biometrics. "
        "Springer.")
    add_biblio_entry(doc, 11,
        "Stallings, W. (2020). Cryptography and network security (8th ed.). Pearson.")

    add_heading(doc, "D. Méthodologie de recherche et conduite de projet")
    add_biblio_entry(doc, 12,
        "Pinto, R., & Grawitz, M. (2020). Méthodes des sciences sociales. Dalloz.")
    add_biblio_entry(doc, 13,
        "Project Management Institute. (2021). A guide to the project management "
        "body of knowledge (PMBOK guide) (7th ed.). Project Management Institute.")
    add_biblio_entry(doc, 14,
        "Hillier, F. S., & Lieberman, G. J. (2019). Introduction to operations "
        "research (extraits PERT/CPM). McGraw-Hill.")
    add_biblio_entry(doc, 15,
        "Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science "
        "in information systems research. MIS Quarterly, 28(1), 75–105. "
        "https://doi.org/10.2307/25148625")

    add_heading(doc, "E. Gouvernance, organisations et transformation numérique")
    add_biblio_entry(doc, 16,
        "Mintzberg, H. (1982). Structure et dynamique des organisations. "
        "Éditions d'Organisation.")
    add_biblio_entry(doc, 17,
        "Vial, G. (2019). Understanding digital transformation: A review and a "
        "research agenda. The Journal of Strategic Information Systems, 28(2), "
        "118–144. https://doi.org/10.1016/j.jsis.2019.01.003")

    add_heading(doc, "F. Normes et modélisation UML")
    add_biblio_entry(doc, 18,
        "Object Management Group. (2017). OMG unified modeling language (OMG UML), "
        "version 2.5.1. https://www.omg.org/spec/UML/2.5.1/")

    add_heading(doc, "G. Documentation technique")
    add_biblio_entry(doc, 19,
        "Laravel. (2026). Laravel documentation. https://laravel.com/docs")
    add_biblio_entry(doc, 20,
        "ZKTeco. (2024). ZKFinger SDK / ZK-9500 user documentation.")
    add_biblio_entry(doc, 21,
        "Microsoft. (2024). .NET documentation. https://learn.microsoft.com/dotnet")

    add_heading(doc, "H. Sources institutionnelles")
    add_biblio_entry(doc, 22,
        "Caisse Nationale de Sécurité Sociale. (2026). Missions et organisation "
        "de la CNSS. Kinshasa, République Démocratique du Congo.")
    add_biblio_entry(doc, 23,
        "Université William Booth. (2026). Site officiel de l'Université William Booth. "
        "https://uwbcongo.org/")

    add_page_break(doc)
    add_chapter_title(doc, "TABLE DES MATIÈRES")
    # Entrées provisoires : les numéros sont recalculés par Word après génération
    _write_toc_skeleton(doc)


def _write_toc_skeleton(doc):
    """TdM à trois niveaux (grands titres + sections + sous-sections), modèle Clémence."""
    # niveau : 0 = chapitre, 1 = section, 2 = sous-section
    from docx.shared import Pt

    prelim = [
        ("EPIGRAPHE", "i"),
        ("DÉDICACE", "ii"),
        ("REMERCIEMENTS", "iii"),
        ("ABRÉVIATIONS ET SIGLES", "iv"),
        ("LISTE DES FIGURES", "v"),
        ("LISTE DES TABLEAUX", "vi"),
        ("RÉSUMÉ", "vii"),
        ("ABSTRACT", "viii"),
        ("RÉSUMÉ EN LINGALA", "ix"),
    ]
    for title, page in prelim:
        add_dotted_entry(doc, title, page, indent_cm=0, bold=True, roman=True)

    body = [
        (0, "INTRODUCTION GÉNÉRALE"),
        (1, "0.1. Contexte de l'étude"),
        (1, "0.2. Problématique et hypothèses"),
        (2, "0.2.1. Problématique de l'étude"),
        (2, "0.2.2. Questions de recherche"),
        (2, "0.2.3. Hypothèses de recherche"),
        (1, "0.3. Objectifs de la recherche"),
        (2, "0.3.1. Objectif général"),
        (2, "0.3.2. Objectifs spécifiques"),
        (2, "0.3.3. Résultats attendus"),
        (1, "0.4. Choix et intérêt de la recherche"),
        (1, "0.5. Revue de la littérature"),
        (1, "0.6. Méthodologie de la recherche"),
        (2, "0.6.1. Méthodes"),
        (2, "0.6.2. Techniques"),
        (2, "0.6.3. Phases du projet"),
        (1, "0.7. Délimitation du sujet"),
        (2, "0.7.1. Délimitation thématique"),
        (2, "0.7.2. Délimitation spatiale et institutionnelle"),
        (2, "0.7.3. Délimitation technique"),
        (2, "0.7.4. Délimitation temporelle"),
        (1, "0.8. Subdivision du travail"),
        (0, "CHAPITRE I. CADRE THÉORIQUE ET ÉTAT DE L'ART"),
        (1, "I.1. Introduction"),
        (1, "I.2. Généralités sur la gestion des ressources humaines (GRH)"),
        (2, "I.2.1. Définition et enjeux de la GRH"),
        (2, "I.2.2. Les fonctions et processus RH"),
        (2, "I.2.3. La GRH dans les institutions publiques africaines"),
        (2, "I.2.4. Évolution des systèmes d'information RH"),
        (2, "I.2.5. Processus RH retenus pour SGRH Pro"),
        (2, "I.2.7. Digitalisation de la GRH en Afrique subsaharienne"),
        (1, "I.3. Systèmes d'information des ressources humaines (SIGRH / SIRH)"),
        (2, "I.3.1. Définition et composantes"),
        (2, "I.3.1.1. Rémunération des agents publics et rôle du SIGRH"),
        (2, "I.3.2. Architecture fonctionnelle d'un SIGRH"),
        (2, "I.3.3. Avantages d'un SIGRH intégré"),
        (2, "I.3.4. Sécurité, authentification et gestion des accès"),
        (2, "I.3.5. Composantes d'un SIGRH moderne"),
        (1, "I.4. Dimension « intelligente » du système"),
        (2, "I.4.1. Tableaux de bord et indicateurs clés (KPI RH)"),
        (2, "I.4.2. Alertes automatiques"),
        (2, "I.4.3. Automatisation et intelligence décisionnelle : distinction"),
        (2, "I.4.4. Couverture fonctionnelle des huit modules"),
        (1, "I.5. Technologies d'identification et de contrôle d'accès"),
        (2, "I.5.1. La biométrie : principes et modalités"),
        (2, "I.5.2. Intégration logicielle du capteur ZK-9500"),
        (2, "I.5.3. Intégration logicielle des cartes RFID"),
        (2, "I.5.3 bis. Comparatif des modalités biométriques"),
        (2, "I.5.4. Combinaison empreinte digitale et RFID dans SGRH Pro"),
        (2, "I.5.5. Aspects éthiques et protection des données biométriques"),
        (2, "I.5.6. Processus théorique d'enrôlement et de pointage"),
        (1, "I.6. Revue des solutions existantes"),
        (2, "I.6.1. Solutions internationales et open source"),
        (2, "I.6.2. Contexte africain et congolais"),
        (2, "I.6.4. Analyse comparative"),
        (2, "I.6.5. Critères de sélection d'une solution SIGRH"),
        (1, "I.7. Limites des systèmes traditionnels de gestion RH"),
        (1, "I.8. Modélisation UML et architectures logicielles"),
        (2, "I.8.1. Le langage UML"),
        (2, "I.8.2. Architecture en couches et séparation backend / frontend"),
        (2, "I.8.3. Principes d'architecture retenus"),
        (1, "I.9. Conclusion du chapitre"),
        (0, "CHAPITRE II. ANALYSE DU SYSTÈME ACTUEL ET SPÉCIFICATION DES BESOINS"),
        (1, "II.1. Introduction"),
        (1, "II.2. Présentation institutionnelle de la CNSS (RDC)"),
        (2, "II.2.1. Historique et missions"),
        (2, "II.2.2. Organisation du siège central"),
        (2, "II.2.3. Effectif et enjeux de la DRH"),
        (1, "II.3. Analyse du système actuel de gestion RH"),
        (2, "II.3.1. Processus actuels de gestion du personnel"),
        (2, "II.3.2. Outils utilisés"),
        (2, "II.3.3. Gestion actuelle des présences et pointage"),
        (2, "II.3.4. Gestion des congés et transmission administrative"),
        (2, "II.3.5. Problèmes et dysfonctionnements identifiés"),
        (2, "II.3.6. Analyse des fraudes et irrégularités de pointage"),
        (2, "II.3.7. Impacts sur la productivité et la prise de décision"),
        (2, "II.3.8. Synthèse du diagnostic : forces et faiblesses"),
        (1, "II.4. Analyse des besoins des acteurs"),
        (2, "II.4.1. Besoins des administrateurs RH"),
        (2, "II.4.2. Besoins des responsables de service"),
        (2, "II.4.3. Besoins des agents (espace personnel)"),
        (2, "II.4.4. Besoins en identification fiable (biométrie et RFID)"),
        (2, "II.4.5. Besoins en reporting et tableaux de bord"),
        (2, "II.4.6. Matrice acteurs / besoins prioritaires"),
        (1, "II.5. Scénarios d'utilisation"),
        (2, "II.5.1. Enrôlement biométrique et pointage"),
        (2, "II.5.2. Congés, rémunération et évaluation"),
        (1, "II.6. Spécification fonctionnelle — les huit modules"),
        (2, "II.6.1. Interdépendances entre modules"),
        (1, "II.7. Spécification technique et contraintes"),
        (1, "II.8. Cahier des charges fonctionnel et technique"),
        (2, "II.8.1. Exigences fonctionnelles principales"),
        (2, "II.8.2. Contraintes techniques et institutionnelles"),
        (2, "II.8.3. Périmètre hors scope"),
        (2, "II.8.4. Critères d'acceptation du prototype"),
        (1, "II.9. Cadrage et planification du projet"),
        (2, "II.9.1. Tableau de recensement des tâches"),
        (2, "II.9.2. Tableau d'ordonnancement des tâches"),
        (2, "II.9.3. Graphe PERT / MPM"),
        (2, "II.9.4. Détermination du chemin critique"),
        (2, "II.9.5. Calendrier d'exécution des tâches"),
        (2, "II.9.6. Diagramme de Gantt"),
        (2, "II.9.7. Estimation du coût du projet"),
        (1, "II.10. Conclusion"),
        (0, "CHAPITRE III. CONCEPTION ET ARCHITECTURE DU SYSTÈME"),
        (1, "III.1. Introduction"),
        (1, "III.2. Architecture globale du système"),
        (2, "III.2.1. Vue d'ensemble des composants"),
        (2, "III.2.2. Architecture logique et physique"),
        (2, "III.2.3. Flux de données entre composants"),
        (1, "III.3. Modélisation UML"),
        (2, "III.3.1. Diagramme de cas d'utilisation"),
        (2, "III.3.2. Diagramme de classes"),
        (2, "III.3.3. Diagramme de séquence — pointage biométrique"),
        (2, "III.3.4. Diagramme d'activités — workflow de congé"),
        (2, "III.3.5. Diagramme d'activités — processus de pointage"),
        (2, "III.3.6. Diagramme de déploiement"),
        (1, "III.4. Conception de la base de données"),
        (2, "III.4.1. Modèle entité-relation"),
        (2, "III.4.2. Tables principales"),
        (2, "III.4.3. Modèle physique de données (MPD)"),
        (2, "III.4.4. Intégrité et données biométriques"),
        (1, "III.5. Conception du backend (API REST)"),
        (2, "III.5.1. Organisation en couches"),
        (2, "III.5.2. Endpoints structurants"),
        (2, "III.5.3. Sécurité applicative"),
        (1, "III.6. Conception du frontend (interface web)"),
        (2, "III.6.1. Structure des écrans"),
        (2, "III.6.2. Terminal de pointage et espace agent"),
        (2, "III.6.3. Ergonomie et personnalisation du dashboard"),
        (1, "III.7. Conception du sous-système biométrique"),
        (2, "III.7.1. Architecture du Fingerprint Bridge"),
        (2, "III.7.2. Protocole bridge ↔ backend"),
        (2, "III.7.3. Installateur one-touch et sécurisation"),
        (1, "III.8. Conception des modules métier RH"),
        (1, "III.9. Conception de la dimension intelligente"),
        (2, "III.9.1. Indicateurs KPI"),
        (2, "III.9.2. Alertes et tableaux de bord"),
        (1, "III.10. Stratégie d'hébergement et déploiement"),
        (2, "III.10.1. Options retenues"),
        (2, "III.10.2. Démonstration sur poste unique"),
        (1, "III.11. Conclusion du chapitre"),
        (0, "CHAPITRE IV. IMPLÉMENTATION, TESTS ET VALIDATION"),
        (1, "IV.1. Introduction du chapitre"),
        (1, "IV.2. Environnement de développement et outils"),
        (2, "IV.2.1. Matériel et logiciels"),
        (2, "IV.2.2. Organisation du dépôt"),
        (1, "IV.3. Implémentation de l'application de gestion"),
        (2, "IV.3.1. Authentification et contrôle d'accès"),
        (2, "IV.3.2. Règle métier du pointage"),
        (2, "IV.3.3. Identification par empreinte"),
        (2, "IV.3.4. Workflow de congé"),
        (1, "IV.4. Implémentation de l'interface web"),
        (2, "IV.4.1. Organisation des écrans"),
        (2, "IV.4.2. Flux de pointage côté interface"),
        (1, "IV.5. Implémentation du sous-système biométrique"),
        (2, "IV.5.1. Service local de lecture"),
        (2, "IV.5.2. Appel depuis l'application de gestion"),
        (2, "IV.5.3. Installateur Windows"),
        (1, "IV.6. Fonctionnalités intelligentes implémentées"),
        (1, "IV.7. Intégration et déploiement du prototype"),
        (1, "IV.8. Tests et validation"),
        (2, "IV.8.1. Scénarios fonctionnels"),
        (2, "IV.8.2. Tests de contrôle d'accès"),
        (2, "IV.8.3. Correspondance besoins / réponses"),
        (1, "IV.9. Résultats et présentation des interfaces"),
        (1, "IV.10. Limites du prototype et perspectives"),
        (1, "IV.11. Conclusion du chapitre"),
        (0, "CONCLUSION GÉNÉRALE"),
        (0, "BIBLIOGRAPHIE"),
        (0, "TABLE DES MATIÈRES"),
    ]
    indents = {0: 0, 1: 0.5, 2: 1.25}
    for level, title in body:
        add_dotted_entry(
            doc, title, "…",
            indent_cm=indents[level],
            bold=(level == 0),
            roman=False,
            size=Pt(11) if level == 2 else Pt(12),
        )


# Compatibilité avec l'ancien nom
write_conclusion_bibliographie_annexes = write_conclusion_bibliographie

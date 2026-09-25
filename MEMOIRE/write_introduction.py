# -*- coding: utf-8 -*-
"""Introduction générale du mémoire — version développée (≥ 8 pages)."""
from memoire_format import (
    add_page_number, add_chapter_title, add_heading, add_subheading,
    add_body, add_mixed, add_bullet, add_numbered_item,
)


def write_introduction(doc):
    add_page_number(doc, 1)
    add_chapter_title(doc, "INTRODUCTION GÉNÉRALE")

    # ── 0.1 Contexte ──
    add_heading(doc, "0.1. Contexte de l'étude")

    add_body(doc,
        "La gestion des ressources humaines occupe, dans toute organisation, une fonction "
        "qui conditionne l'ensemble de son fonctionnement. Recrutement, affectation, suivi "
        "des présences, gestion des congés, évaluation des performances et production de "
        "reporting : autant de tâches qui, lorsqu'elles sont mal coordonnées, finissent "
        "par peser sur la qualité du service rendu. Dans les institutions publiques, où "
        "la régularité et la continuité de service sont exigées, cette exigence prend une "
        "dimension encore plus nette."
    )

    add_body(doc,
        "En République Démocratique du Congo, la modernisation administrative progresse par "
        "étapes. Si certains services ont amorcé une informatisation partielle de leurs "
        "activités, le traitement des données du personnel demeure, dans plusieurs "
        "directions, tributaire de pratiques héritées du fonctionnement manuel : registres "
        "papier, fichiers Excel éparpillés, relevés de présence signés à la main, ou encore "
        "logiciels anciens dont la maintenance n'est plus assurée. Cette situation crée des "
        "lenteurs, des doublons d'information et, dans certains cas, des écarts difficiles "
        "à expliquer entre le personnel théoriquement présent et la réalité constatée sur "
        "le terrain."
    )

    add_body(doc,
        "La Caisse Nationale de Sécurité Sociale (CNSS), institution chargée notamment de la "
        "couverture sociale des travailleurs congolais, n'échappe pas à cette réalité. Au "
        "siège central de Kinshasa, où convergent les directions administratives et "
        "opérationnelles, la gestion du personnel mobilise un volume important d'agents "
        "répartis dans des services aux missions variées. Durant le stage effectué au sein "
        "de la Direction des ressources humaines, il a été observé que les activités RH — "
        "tenue des dossiers, suivi des absences, préparation des états administratifs, "
        "traitement des demandes de congé — reposent encore sur une combinaison d'outils "
        "peu intégrés. Les responsables consacrent une part significative de leur temps à "
        "recouper des informations qui devraient, en principe, être disponibles dans un "
        "système unique."
    )

    add_body(doc,
        "Il importe de préciser le cadre institutionnel propre à la CNSS. En tant "
        "qu'organisme public, l'institution rémunère ses agents par virement bancaire, "
        "sous la responsabilité de la direction administrative et financière. Le service "
        "des ressources humaines ne verse pas les salaires : il produit les données "
        "administratives fiables — états de présence, absences, éléments variables, "
        "mouvements de personnel — sur lesquelles s'appuie la finance pour le paiement. "
        "Le présent mémoire ne porte donc pas sur un logiciel de paie privé, mais sur "
        "un système d'information de gestion des ressources humaines (SIGRH) orienté "
        "administration du personnel, pilotage et traçabilité."
    )

    add_body(doc,
        "Le contrôle du temps de travail illustre particulièrement les faiblesses du "
        "dispositif actuel. Lorsque le pointage repose sur une signature ou une mention "
        "manuscrite, il devient difficile d'établir avec certitude les heures réellement "
        "prestées, de repérer les retards récurrents ou de produire, à la fin du mois, "
        "un état fiable des présences transmissible à la direction financière. Des "
        "irrégularités — pointages groupés, absences non signalées, heures mal "
        "documentées — ont été signalées comme source de tension entre les agents et "
        "l'administration. Les retards dans la consolidation des états administratifs, "
        "parfois liés à des données incomplètes ou contradictoires, viennent renforcer "
        "le sentiment que la gestion RH manque de rigueur et de transparence."
    )

    add_body(doc,
        "Dans le même temps, les technologies disponibles permettent de concevoir des "
        "systèmes d'information des ressources humaines capables de centraliser les "
        "données, d'automatiser les processus répétitifs et de produire des indicateurs "
        "utiles à la décision. L'identification biométrique par empreinte digitale, "
        "notamment à l'aide du lecteur ZK-9500, et l'usage de cartes RFID personnelles "
        "offrent des moyens concrets de fiabiliser le pointage. Couplés à une interface "
        "web accessible aux administrateurs comme aux employés, ces dispositifs alimentent "
        "le module présences d'un logiciel central plutôt que de constituer une solution "
        "isolée."
    )

    add_body(doc,
        "En République Démocratique du Congo, la digitalisation des "
        "administrations publiques s'inscrit dans une dynamique plus "
        "large de modernisation de l'État. Toutefois, les projets "
        "informatiques y restent souvent ponctuels — achat de matériel "
        "sans refonte des processus — ou dépendants de financements "
        "extérieurs limités dans le temps. Le présent mémoire propose "
        "une démarche inverse : partir des processus observés à la CNSS, "
        "formaliser les dysfonctionnements, spécifier les besoins, "
        "planifier le projet, puis concevoir et implémenter une solution "
        "logicielle contextualisée."
    )

    add_body(doc,
        "Un système d'information des ressources humaines (SIGRH) se définit "
        "comme l'ensemble coordonné de bases de données, de règles métier "
        "et d'interfaces permettant de collecter, traiter et restituer "
        "l'information relative au personnel. Contrairement à un simple "
        "fichier Excel ou à un module de pointage isolé, un SIGRH couvre "
        "l'ensemble du cycle administratif de l'agent — de l'intégration "
        "à l'archivage — et produit des indicateurs de pilotage pour "
        "les responsables. SGRH Pro se veut une réponse de ce type, "
        "adaptée au statut d'institution publique congolaise."
    )

    add_mixed(doc, [
        ("C'est dans cette perspective que s'inscrit le présent travail, consacré à la "
         "conception et à l'implémentation de ", False, False),
        ("SGRH Pro", True, False),
        (" — Système de Gestion des Ressources Humaines Professionnel — : une application "
         "web destinée au siège central de la CNSS, organisée en huit modules "
         "fonctionnels (accès, employés, biométrie, présences, congés, éléments "
         "de rémunération, évaluation et rapports) et complétée par un dispositif "
         "d'identification par empreinte digitale et par carte RFID.", False, False),
    ])

    # ── 0.2 Problématique ──
    add_heading(doc, "0.2. Problématique et hypothèses")
    add_subheading(doc, "0.2.1. Problématique de l'étude")

    add_body(doc,
        "Au-delà des constats généraux sur la gestion RH dans le secteur public congolais, "
        "la situation observée à la CNSS appelle une interrogation précise. Comment une "
        "institution de cette envergure peut-elle, avec les moyens dont elle dispose, "
        "reprendre le contrôle de l'information relative à son personnel et réduire les "
        "dysfonctionnements qui entravent son fonctionnement interne ?"
    )

    add_body(doc,
        "Sur le plan administratif, la dispersion des dossiers complique toute recherche "
        "d'antécédent professionnel, toute mise à jour contractuelle ou toute production "
        "d'attestation. Lorsqu'un agent change de service ou sollicite un congé, le "
        "responsable RH doit souvent consulter plusieurs sources avant de disposer d'une "
        "vue complète. Sur le plan opérationnel, l'absence de workflow informatisé pour "
        "les congés multiplie les allers-retours entre l'agent, son supérieur hiérarchique "
        "et le service RH. Sur le plan du contrôle des présences, le pointage manuel ne "
        "permet ni l'horodatage fiable ni la consolidation automatique des données."
    )

    add_body(doc,
        "Enfin, sur le plan décisionnel, les responsables disposent rarement d'un tableau "
        "de bord consolidé : effectifs par direction, taux d'absentéisme, retards et "
        "évaluations. L'adjectif « intelligent » retenu dans le titre désigne "
        "cette capacité à restituer automatiquement des KPI pertinents et à générer des "
        "alertes lorsque certains seuils sont dépassés — et non l'intégration d'une "
        "intelligence artificielle généraliste."
    )

    add_body(doc, "La problématique fondamentale est formulée ainsi :")

    add_mixed(doc, [
        ("Comment concevoir et implémenter un SIGRH — SGRH Pro — capable d'assurer un "
         "suivi fiable et intégré du personnel au siège central de la CNSS, en s'appuyant "
         "prioritairement sur une architecture logicielle modulaire et en complétant "
         "celle-ci par des modules d'acquisition biométrique (ZK-9500) et RFID ?",
         True, False),
    ])

    add_body(doc, "Cette interrogation met en évidence un double enjeu :")
    add_bullet(doc, " un enjeu organisationnel, lié à la centralisation et à la fiabilisation "
               "des processus RH ;")
    add_bullet(doc, " un enjeu technique, lié à la conception d'une architecture logicielle "
               "modulaire, hébergeable et adaptée aux contraintes du terrain congolais.")

    add_subheading(doc, "0.2.2. Questions de recherche")

    add_body(doc,
        "Pour structurer l'investigation, les questions de recherche suivantes "
        "ont été formulées :"
    )

    add_numbered_item(doc, 1,
        " Quels sont les dysfonctionnements du système actuel de gestion RH "
        "au siège central de la CNSS ?")
    add_numbered_item(doc, 2,
        " Quelles exigences fonctionnelles et techniques doit satisfaire un "
        "SIGRH adapté au contexte institutionnel congolais ?")
    add_numbered_item(doc, 3,
        " Comment planifier et ordonnancer le développement du prototype "
        "(PERT, Gantt, chemin critique, budget) ?")
    add_numbered_item(doc, 4,
        " Quelle architecture de système d'information (modélisation UML, "
        "application web, dispositif biométrique) permet d'intégrer les "
        "huit modules retenus ?")
    add_numbered_item(doc, 5,
        " Le prototype SGRH Pro répond-il aux critères de validation définis "
        "avec l'encadreur et le responsable RH ?")

    add_subheading(doc, "0.2.3. Hypothèses de recherche")

    add_body(doc,
        "Au regard des insuffisances constatées durant le stage, cette étude repose sur "
        "l'hypothèse générale suivante : la conception et la mise en œuvre d'un SIGRH "
        "intégré — centralisation des données, automatisation des workflows, restitution "
        "de KPI et alertes — amélioreront le suivi administratif du personnel à la CNSS."
    )

    add_body(doc, "Cette hypothèse se décline ainsi :")

    add_bullet(doc,
        " la centralisation des dossiers agents réduira les incohérences "
        "entre registres papier et Excel ;",
        "Premièrement,")
    add_bullet(doc,
        " l'automatisation des présences et congés accélérera les états "
        "transmis à la finance ;",
        "Deuxièmement,")
    add_bullet(doc,
        " la biométrie et le RFID fiabiliseront le pointage ;",
        "Troisièmement,")
    add_bullet(doc,
        " l'évaluation structurée et les KPI amélioreront le pilotage RH.",
        "Enfin,")

    # ── 0.3 Objectifs ──
    add_heading(doc, "0.3. Objectifs de la recherche")
    add_subheading(doc, "0.3.1. Objectif général")

    add_body(doc,
        "Concevoir et implémenter SGRH Pro, un SIGRH modulaire et intelligent (KPI, "
        "alertes), complété par des modules d'acquisition biométrique et RFID, pour "
        "améliorer le suivi administratif du personnel au siège central de la CNSS."
    )

    add_subheading(doc, "0.3.2. Objectifs spécifiques")

    add_body(doc,
        "Pour atteindre l'objectif général, les objectifs spécifiques suivants sont "
        "définis :"
    )

    objectives = [
        "Analyser le fonctionnement actuel du service RH de la CNSS ;",
        "Élaborer un cahier des charges des huit modules (présences, biométrie, "
        "rémunération, évaluation, etc.) ;",
        "Planifier le projet (PERT, Gantt, chemin critique, coûts) ;",
        "Modéliser le système (UML) et réaliser un prototype opérationnel "
        "intégrant le lecteur ZK-9500 ;",
        "Valider le prototype (pointage réel, états finance, évaluation, KPI).",
    ]
    for i, obj in enumerate(objectives, 1):
        add_numbered_item(doc, i, " " + obj)

    add_subheading(doc, "0.3.3. Résultats attendus")

    add_body(doc,
        "Les livrables attendus sont : cahier des charges et planification "
        "(chapitre II) ; diagrammes UML (chapitre III) ; prototype SGRH Pro "
        "(API, interface, bridge, huit modules) et protocole de tests "
        "(chapitre IV). Le prototype doit permettre l'enrôlement biométrique, "
        "le pointage réel, l'export d'un état pour la finance et une évaluation "
        "structurée."
    )

    # ── 0.4 Choix et intérêt ──
    add_heading(doc, "0.4. Choix et intérêt de la recherche")

    add_body(doc,
        "Le sujet naît du stage à la CNSS : dossiers dispersés, pointage peu "
        "fiable, états de présence construits manuellement. Sur le plan "
        "académique, il mobilise SIGRH, UML et intégration biométrique ; "
        "sur le plan institutionnel, il propose une solution applicable au "
        "siège central ; sur le plan opérationnel, il recentre le prototype "
        "sur les présences, la biométrie, l'évaluation et les éléments de "
        "rémunération."
    )

    # ── 0.5 Revue littérature ──
    add_heading(doc, "0.5. Revue de la littérature")

    add_body(doc,
        "Dessler (2020) définit la GRH comme l'ensemble des pratiques visant à attirer, "
        "développer, motiver et retenir le personnel. Beaudoin et Roy (2019) montrent "
        "qu'un SIGRH intégré réduit les délais de traitement et fournit des indicateurs "
        "aux décideurs. En contexte africain, Ndiaye et Diop (2021) soulignent l'écart "
        "entre modèles importés et réalités locales. Jain et al. (2021) rappellent que "
        "l'empreinte digitale reste la modalité biométrique la plus répandue en "
        "milieu professionnel."
    )

    add_body(doc,
        "Sur le plan méthodologique, Sommerville (2016) rappelle que la qualité des "
        "exigences conditionne la réussite d'un projet logiciel. Le PMBOK (2021) et "
        "Hillier (2019) insistent sur l'ordonnancement des tâches et le chemin critique, "
        "formalisés au chapitre II (PERT, Gantt). La littérature confirme ainsi la "
        "pertinence d'un SIGRH intégré et laisse un espace pour une étude de cas "
        "congolaise recentrée sur les présences, la biométrie, l'évaluation et "
        "les éléments de rémunération."
    )

    # ── 0.6 Méthodologie ──
    add_heading(doc, "0.6. Méthodologie de la recherche")

    add_body(doc,
        "Pour mener à bien cette étude, une démarche structurée en phases successives "
        "a été adoptée : analyse du contexte, spécification des besoins, planification "
        "du projet, modélisation UML, développement itératif et validation par tests."
    )

    add_subheading(doc, "0.6.1. Méthodes")

    add_body(doc,
        "La méthode analytique a consisté à examiner le fonctionnement actuel du service "
        "RH : circuits de validation des congés, consolidation des états administratifs, "
        "tenue des registres de présence et suivi des évaluations. Cette analyse, nourrie "
        "par l'observation en stage et l'étude documentaire, a permis d'identifier les "
        "points de blocage et de traduire les besoins en exigences fonctionnelles."
    )

    add_body(doc,
        "La méthode structuro-fonctionnelle a décomposé le futur système en huit "
        "modules cohérents et défini les flux d'information entre eux — par exemple "
        "le lien entre pointages biométriques, calcul des présences, évaluation "
        "et export des états de rémunération pour la direction financière."
    )

    add_body(doc,
        "Le développement itératif suit une logique proche du Processus Unifié : "
        "inception (cahier des charges), élaboration (modélisation UML), construction "
        "(prototype) et transition (tests, soutenance). "
        "La planification du projet mobilise en parallèle les techniques "
        "PERT/MPM et le diagramme de Gantt, formalisés au chapitre II."
    )

    add_subheading(doc, "0.6.2. Techniques")

    add_bullet(doc, " consultation d'ouvrages, d'articles et de documentation technique ;",
               "Technique documentaire :")
    add_bullet(doc, " observation des pratiques RH à la CNSS durant le stage ;",
               "Technique d'observation :")
    add_bullet(doc, " entretiens semi-directifs avec responsables RH et agents ;",
               "Technique d'entretien :")
    add_bullet(doc, " formalisation UML et planification PERT/Gantt ;",
               "Technique de modélisation :")
    add_bullet(doc, " réalisation d'un prototype web et d'un dispositif de lecture "
               "d'empreintes sur poste Windows ;",
               "Technique de prototypage :")
    add_bullet(doc, " tests fonctionnels et comparaison avec l'existant.",
               "Technique d'expérimentation :")

    add_subheading(doc, "0.6.3. Phases du projet")

    add_body(doc,
        "Le déroulement du mémoire correspond à six phases séquentielles "
        "et parfois parallèles : (1) analyse du système actuel et collecte "
        "des besoins durant le stage ; (2) rédaction du cahier des charges "
        "et planification PERT/Gantt ; (3) conception UML et architecture ; "
        "(4) développement du prototype (application web et lecteur biométrique) ; "
        "(5) intégration, tests et déploiement du prototype ; (6) rédaction "
        "des chapitres de conception et d'implémentation, préparation de "
        "la soutenance. Cette structuration garantit la traçabilité entre "
        "besoins exprimés, planification, conception et livrable final."
    )

    # ── 0.7 Délimitation ──
    add_heading(doc, "0.7. Délimitation du sujet")

    add_subheading(doc, "0.7.1. Délimitation thématique")

    add_body(doc,
        "Le travail porte exclusivement sur la gestion interne des ressources humaines "
        "de la CNSS : dossiers agents, présences, congés, éléments de rémunération, "
        "évaluation et reporting. Les missions "
        "externes — gestion des assurés, cotisations, prestations — sont hors périmètre. "
        "Sont également exclus du prototype : gestion des contrats, recrutement, "
        "formation et congés médicaux."
    )

    add_subheading(doc, "0.7.2. Délimitation spatiale et institutionnelle")

    add_body(doc,
        "L'étude se réfère au siège central de la CNSS à Kinshasa, commune "
        "de la Gombe, où sont regroupées la direction générale, la direction "
        "des ressources humaines et les directions métier. Le prototype est "
        "destiné au poste du responsable RH à des fins de démonstration et "
        "de soutenance. Une généralisation vers les agences provinciales "
        "n'est pas couverte, bien que l'application soit conçue pour "
        "permettre un hébergement centralisé ultérieur."
    )

    add_subheading(doc, "0.7.3. Délimitation technique")

    add_body(doc,
        "Le système couvre la conception logicielle, l'intégration du lecteur "
        "ZK-9500 et l'usage de cartes RFID. Il n'inclut ni gestion des virements "
        "bancaires, ni calcul fiscal (IRG), ni déploiement multi-sites en "
        "production. Seules les mesures techniques élémentaires de protection "
        "des données biométriques (stockage des templates, révocation des "
        "cartes, journal d'audit) sont implémentées dans le prototype."
    )

    add_subheading(doc, "0.7.4. Délimitation temporelle")

    add_body(doc,
        "La recherche s'inscrit dans la période académique 2026-2027. Elle "
        "vise un prototype fonctionnel et testé, non un déploiement "
        "institutionnel complet ni une certification juridique du dispositif "
        "biométrique. Le calendrier d'exécution du projet — soixante-trois jours "
        "ouvrés sur le chemin critique — est détaillé au chapitre II."
    )

    # ── 0.8 Subdivision ──
    add_heading(doc, "0.8. Subdivision du travail")

    add_body(doc,
        "Hormis l'introduction générale et la conclusion générale, le présent mémoire "
        "est structuré en quatre chapitres :"
    )

    chapters = [
        ("Le premier chapitre", " expose le cadre théorique et l'état de l'art : GRH, "
         "SIGRH, biométrie, RFID, solutions existantes, limites des pratiques manuelles "
         "et fondements UML."),
        ("Le deuxième chapitre", " analyse le système actuel de la CNSS, les besoins "
         "des acteurs, le cahier des charges des huit modules, ainsi que la "
         "planification du projet (PERT, Gantt, chemin critique, coûts)."),
        ("Le troisième chapitre", " présente la conception et l'architecture de SGRH Pro : "
         "diagrammes UML, modèle de données, API backend, interface frontend et "
         "sous-système biométrique."),
        ("Le quatrième chapitre", " décrit l'implémentation, les tests, les résultats "
         "obtenus et les perspectives d'évolution."),
    ]
    for prefix, rest in chapters:
        add_mixed(doc, [(prefix, True, False), (rest, False, False)])

    add_body(doc,
        "Cette progression — de la théorie à la validation expérimentale — vise à "
        "garantir la traçabilité entre le constat de terrain, les choix de conception "
        "et le prototype livré. Elle reprend l'organisation classique des mémoires "
        "de la Faculté : fondements conceptuels, analyse de l'existant, conception, "
        "puis implémentation et tests."
    )

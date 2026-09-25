# -*- coding: utf-8 -*-
"""DEPRECATED — Ne pas utiliser. Source active : write_introduction.py (via build_memoire_partie1.py)."""
from docx import Document
from docx.shared import Pt, Cm, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

OUTPUT = r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\INTRODUCTION GENERALE.docx"

FONT = "Times New Roman"
BODY_SIZE = Pt(12)
TITLE_SIZE = Pt(14)
HEADING_SIZE = Pt(12)
LINE_SPACING = 1.15
SPACE = Pt(6)


def set_run_font(run, bold=False, italic=False, size=BODY_SIZE):
    run.font.name = FONT
    run.font.size = size
    run.font.bold = bold
    run.font.italic = italic
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        from docx.oxml import OxmlElement
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), FONT)
    rFonts.set(qn("w:hAnsi"), FONT)
    rFonts.set(qn("w:cs"), FONT)


def add_page_number(paragraph, num):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run(f"- {num} -")
    set_run_font(run)
    paragraph.paragraph_format.space_after = Pt(12)


def add_title(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = SPACE
    p.paragraph_format.space_after = SPACE
    p.paragraph_format.line_spacing = LINE_SPACING
    run = p.add_run(text)
    set_run_font(run, bold=True, size=TITLE_SIZE)


def add_heading(doc, text, level=2):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = SPACE
    p.paragraph_format.space_after = SPACE
    p.paragraph_format.line_spacing = LINE_SPACING
    run = p.add_run(text)
    set_run_font(run, bold=True, size=HEADING_SIZE)
    return p


def add_body(doc, text, bold=False, italic=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = SPACE
    p.paragraph_format.space_after = SPACE
    p.paragraph_format.line_spacing = LINE_SPACING
    run = p.add_run(text)
    set_run_font(run, bold=bold, italic=italic)
    return p


def add_mixed(doc, parts):
    """parts: list of (text, bold, italic)"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = SPACE
    p.paragraph_format.space_after = SPACE
    p.paragraph_format.line_spacing = LINE_SPACING
    for text, bold, italic in parts:
        run = p.add_run(text)
        set_run_font(run, bold=bold, italic=italic)
    return p


def add_bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style="List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = LINE_SPACING
    if bold_prefix:
        r1 = p.add_run(bold_prefix)
        set_run_font(r1, bold=True)
        r2 = p.add_run(text)
        set_run_font(r2)
    else:
        run = p.add_run(text)
        set_run_font(run)


def build():
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Cm(2.54)
    sec.bottom_margin = Cm(2.54)
    sec.left_margin = Cm(2.54)
    sec.right_margin = Cm(2.54)

    add_page_number(doc.add_paragraph(), 1)
    add_title(doc, "INTRODUCTION GÉNÉRALE")

    # ── 0.1 Contexte ──
    add_heading(doc, "0.1. Contexte de l'étude")

    add_body(doc,
        "La gestion des ressources humaines occupe, dans toute organisation, une fonction "
        "d'appoint qui conditionne pourtant l'ensemble de son fonctionnement. Recrutement, "
        "affectation, suivi des présences, traitement de la paie, gestion des congés, évaluation "
        "des performances : autant de tâches qui, lorsqu'elles sont mal coordonnées, finissent "
        "par peser sur la qualité du service rendu. Dans les institutions publiques, où la "
        "régularité et la continuité de service sont exigées, cette exigence prend une dimension "
        "encore plus nette."
    )

    add_body(doc,
        "En République Démocratique du Congo, la modernisation administrative progresse par "
        "étapes. Si certains services ont amorcé une informatisation partielle de leurs activités, "
        "le traitement des données du personnel demeure, dans plusieurs directions, tributaire "
        "de pratiques héritées du fonctionnement manuel : registres papier, fichiers Excel "
        "éparpillés, relevés de présence signés à la main, ou encore logiciels anciens dont la "
        "maintenance n'est plus assurée. Cette situation crée des lenteurs, des doublons "
        "d'information et, dans certains cas, des écarts difficiles à expliquer entre le "
        "personnel théoriquement présent et la réalité constatée sur le terrain."
    )

    add_body(doc,
        "La Caisse Nationale de Sécurité Sociale (CNSS), institution chargée notamment de la "
        "couverture sociale des travailleurs congolais, n'échappe pas à cette réalité. Au siège "
        "central de Kinshasa, où convergent les directions administratives et opérationnelles, "
        "la gestion du personnel mobilise un volume important d'agents répartis dans des "
        "services aux missions variées. Durant le stage effectué au sein de cette institution, "
        "il a été observé que les activités RH — tenue des dossiers, suivi des absences, "
        "préparation des éléments de paie, traitement des demandes de congé — reposent encore "
        "sur une combinaison d'outils peu intégrés. Les responsables consacrent une part "
        "significative de leur temps à recouper des informations qui devraient, en principe, "
        "être disponibles dans un système unique."
    )

    add_body(doc,
        "Le contrôle du temps de travail illustre particulièrement cette faiblesse. Lorsque le "
        "pointage repose sur une signature ou une mention manuscrite, il devient difficile "
        "d'établir avec certitude les heures réellement prestées, de repérer les retards "
        "récurrents ou de produire, à la fin du mois, un état fiable des présences. Des "
        "irrégularités — pointages groupés, absences non signalées, heures supplémentaires mal "
        "documentées — ont été signalées comme source de tension entre les agents et "
        "l'administration. Les retards dans le traitement de la paie, parfois liés à des "
        "données incomplètes ou contradictoires, viennent renforcer le sentiment que la "
        "gestion RH manque de rigueur et de transparence."
    )

    add_body(doc,
        "Dans le même temps, les technologies disponibles sur le marché permettent aujourd'hui "
        "de concevoir des systèmes d'information des ressources humaines (SIGRH) capables de "
        "centraliser les données, d'automatiser les processus répétitifs et de produire des "
        "indicateurs utiles à la décision. L'identification biométrique par empreinte digitale, "
        "notamment à l'aide de lecteurs tels que le ZK-Teco 9500, et l'usage de cartes RFID "
        "personnelles offrent des moyens concrets de fiabiliser le pointage sans alourdir le "
        "travail quotidien des agents. Couplés à une interface web accessible aux "
        "administrateurs comme aux employés, ces dispositifs peuvent transformer une "
        "administration du personnel essentiellement réactive en un pilotage plus maîtrisé."
    )

    add_body(doc,
        "C'est dans cette perspective que s'inscrit le présent travail, intitulé "
        "« Conception et implémentation d'un système d'information intelligent de gestion des "
        "ressources humaines intégrant la biométrie (ZK-Teco 9500) et les cartes RFID pour le "
        "suivi et l'optimisation du personnel : cas de la CNSS ». Il vise à proposer une "
        "solution informatique — dénommée SGRH Pro — couvrant l'ensemble des tâches "
        "habituellement confiées au service des ressources humaines, depuis la gestion des "
        "dossiers jusqu'à la production de tableaux de bord, en passant par le pointage "
        "biométrique, la paie et l'espace personnel de chaque agent."
    )

    # ── 0.2 Problématique ──
    add_heading(doc, "0.2. Problématique et hypothèses")
    add_heading(doc, "0.2.1. Problématique de l'étude")

    add_body(doc,
        "Au-delà des constats généraux sur la gestion RH dans le secteur public congolais, "
        "la situation observée à la CNSS appelle une interrogation précise. Comment une "
        "institution de cette envergure peut-elle, avec les moyens dont elle dispose, "
        "reprendre le contrôle de l'information relative à son personnel et réduire les "
        "dysfonctionnements qui entravent son fonctionnement interne ?"
    )

    add_body(doc,
        "Sur le plan administratif, la dispersion des dossiers — parfois partiellement "
        "numérisés, parfois encore physiques — complique toute recherche d'antécédent "
        "professionnel, toute mise à jour contractuelle ou toute préparation d'attestation. "
        "Lorsqu'un agent change de service ou sollicite un congé, le responsable RH doit "
        "souvent consulter plusieurs sources avant de disposer d'une vue complète. Ce "
        "morcellement consomme du temps et expose à des erreurs de saisie."
    )

    add_body(doc,
        "Sur le plan opérationnel, l'absence de chaîne de validation informatisée pour les "
        "congés et permissions oblige à multiplier les allers-retours entre l'agent, son "
        "supérieur hiérarchique et le service RH. Les soldes de congés ne sont pas toujours "
        "consultables en temps réel ; les agents ignorent parfois combien de jours il leur "
        "reste, et les managers peinent à anticiper les absences simultanées dans une même "
        "équipe."
    )

    add_body(doc,
        "Sur le plan du contrôle des présences, le recours au pointage manuel ne permet ni "
        "d'horodater avec précision les entrées et sorties, ni de croiser automatiquement "
        "ces données avec les plannings ou les autorisations d'absence. Les tentatives de "
        "fraude — signature par un collègue, mention a posteriori — restent difficiles à "
        "prouver faute de trace numérique inviolable. C'est précisément ce vide que la "
        "biométrie et les cartes RFID sont susceptibles de combler, à condition d'être "
        "intégrées dans un système cohérent plutôt que déployées isolément."
    )

    add_body(doc,
        "Enfin, sur le plan décisionnel, les responsables disposent rarement d'un tableau "
        "de bord consolidé : taux d'absentéisme par direction, masse salariale mensuelle, "
        "contrats arrivant à échéance, agents les plus ponctuels ou les plus absents. Sans "
        "ces indicateurs, la gestion RH reste descriptive plutôt qu'analytique ; elle "
        "enregistre des faits sans toujours en tirer des orientations. L'adjectif "
        "« intelligent » retenu dans le titre du mémoire désigne ici cette capacité à "
        "restituer automatiquement des KPI pertinents et à générer des alertes lorsque "
        "certains seuils sont dépassés — retards répétés, budget département dépassé, "
        "contrat expirant — et non l'intégration d'une intelligence artificielle généraliste."
    )

    add_body(doc, "La problématique fondamentale qui se dégage est donc la suivante :")

    add_mixed(doc, [
        ("Comment concevoir et implémenter un système d'information des ressources humaines "
         "intégrant la biométrie (ZK-Teco 9500) et les cartes RFID, capable d'assurer un "
         "suivi fiable du personnel et d'appuyer l'optimisation de la gestion RH au sein du "
         "siège central de la CNSS en République Démocratique du Congo ?", True, False),
    ])

    add_body(doc, "Cette interrogation met en évidence un double enjeu :")
    add_bullet(doc, "un enjeu organisationnel, lié à la centralisation et à la fiabilisation "
                 "des processus RH ;")
    add_bullet(doc, "un enjeu technique, lié à la conception d'une architecture logicielle "
                 "modulaire, hébergeable et adaptée aux contraintes du terrain congolais.")

    # ── 0.2.2 Hypothèses ──
    add_heading(doc, "0.2.2. Hypothèses de recherche")

    add_body(doc,
        "Au regard des insuffisances constatées durant le stage — gestion fragmentée, "
        "pointage peu fiable, retards de paie, absence d'outils d'analyse —, cette étude "
        "repose sur l'hypothèse générale suivante :"
    )

    add_body(doc,
        "La conception et la mise en œuvre d'un SIGRH intégrant centralisation des données, "
        "automatisation des tâches récurrentes, identification biométrique et restitution "
        "d'indicateurs de pilotage permettraient d'améliorer sensiblement le suivi et "
        "l'optimisation du personnel au siège central de la CNSS.",
        italic=False
    )

    add_body(doc, "Cette hypothèse générale se décline en hypothèses spécifiques :")

    add_bullet(doc,
        " la centralisation des dossiers agents, des contrats et des historiques de paie "
        "dans une base unique rendrait la gestion administrative plus cohérente et réduirait "
        "les recherches croisées entre fichiers Excel et registres papier ;",
        "Premièrement,")
    add_bullet(doc,
        " l'automatisation des workflows — demandes de congé, calcul des heures travaillées, "
        "génération des bulletins — limiterait les erreurs de ressaisie et accélérerait le "
        "traitement mensuel de la paie ;",
        "Deuxièmement,")
    add_bullet(doc,
        " le pointage par empreinte digitale via le lecteur ZK-Teco 9500, complété par "
        "l'attribution de cartes RFID nominatives, restreindrait les pratiques frauduleuses "
        "observées avec le pointage manuel ;",
        "Troisièmement,")
    add_bullet(doc,
        " la mise à disposition d'un espace agent en ligne (consultation des bulletins, "
        "soldes de congés, historique de pointage) renforcerait la transparence et "
        "allégerait la charge des services RH en réduisant les demandes de renseignement ;",
        "Quatrièmement,")
    add_bullet(doc,
        " les tableaux de bord et alertes automatiques permettraient aux responsables "
        "d'identifier plus tôt les anomalies (absences non justifiées, dépassements "
        "budgétaires, contrats expirants) et d'ajuster leurs décisions en conséquence ;",
        "Cinquièmement,")
    add_bullet(doc,
        " un prototype fonctionnel déployé sur le poste du responsable RH, même dans un "
        "périmètre réduit, suffirait à démontrer la faisabilité technique et l'apport "
        "concret d'une solution hébergeable ultérieurement en production.",
        "Enfin,")

    add_body(doc,
        "Ainsi formulées, ces hypothèses orientent la démarche vers la conception UML, "
        "le développement du backend et du frontend, l'intégration du bridge biométrique "
        "et la validation expérimentale du système SGRH Pro."
    )

    # ── 0.3 Objectifs ──
    add_heading(doc, "0.3. Objectifs de la recherche")
    add_heading(doc, "0.3.1. Objectif général")

    add_body(doc,
        "L'objectif général de cette recherche est de concevoir et d'implémenter un système "
        "d'information intelligent de gestion des ressources humaines — SGRH Pro — "
        "intégrant la biométrie (ZK-Teco 9500) et les cartes RFID, afin d'améliorer le "
        "suivi, la gestion et l'optimisation du personnel au siège central de la CNSS en "
        "République Démocratique du Congo."
    )

    add_heading(doc, "0.3.2. Objectifs spécifiques")
    add_body(doc,
        "Pour atteindre l'objectif général susmentionné, les objectifs spécifiques suivants "
        "sont définis :"
    )

    objectives = [
        "Analyser le fonctionnement actuel du service RH de la CNSS et identifier les "
        "lacunes des outils et pratiques en usage ;",
        "Élaborer un cahier des charges couvrant les quatorze modules fonctionnels du "
        "système (gestion des utilisateurs, dossiers agents, biométrie, présences, congés, "
        "paie, contrats, formation, évaluation, congés médicaux, notifications, recrutement, "
        "reporting et paramétrage) ;",
        "Modéliser l'architecture du système à l'aide d'UML (cas d'utilisation, classes, "
        "séquences, activités, déploiement) en séparant clairement le backend et le frontend ;",
        "Développer une API REST sécurisée et une interface web responsive destinées aux "
        "administrateurs RH, aux managers et aux agents ;",
        "Intégrer le lecteur d'empreintes ZK-Teco 9500 et le mécanisme d'attribution des "
        "cartes RFID au travers d'un bridge logiciel communicant avec le backend ;",
        "Mettre en place les mécanismes de calcul de paie (salaire brut/net, cotisations "
        "CNSS, retenues IRG) et de génération des bulletins au format PDF ;",
        "Implémenter les tableaux de bord, les KPI et le système d'alertes constituant la "
        "dimension « intelligente » du SIGRH ;",
        "Réaliser un prototype opérationnel sur poste de travail, procéder aux tests "
        "fonctionnels et mesurer les apports par rapport à la gestion manuelle existante.",
    ]
    for obj in objectives:
        add_bullet(doc, " " + obj)

    # ── 0.4 Choix et intérêt ──
    add_heading(doc, "0.4. Choix et intérêt de la recherche")
    add_heading(doc, "0.4.1. Choix du sujet")

    add_body(doc,
        "Le choix de ce sujet ne relève pas d'une simple application d'un cours de "
        "génie logiciel à un cas fictif. Il est directement nourri par l'expérience de "
        "stage à la CNSS, où les limites des pratiques actuelles se manifestent "
        "concrètement : files d'attente d'agents cherchant une information sur leur "
        "paie, responsables RH comparant manuellement deux fichiers Excel pour établir "
        "un état de présence, directions recevant tardivement les effectifs réels de "
        "leur service."
    )

    add_body(doc,
        "Par ailleurs, la littérature en management des ressources humaines rappelle "
        "depuis plusieurs décennies que la fonction RH doit évoluer d'un rôle "
        "administratif vers un rôle de conseil stratégique (Ulrich, 1997). Or, cette "
        "évolution suppose disposer d'informations fiables et actualisées — condition "
        "rarement remplie lorsque les données sont éparpillées. Proposer un SIGRH "
        "adapté au contexte congolais, plutôt que d'importer une solution conçue pour "
        "un autre environnement juridique et organisationnel, constitue une réponse "
        "pérenne à un besoin réel."
    )

    add_body(doc,
        "L'intégration de la biométrie et du RFID répond, elle, à une préoccupation "
        "exprimée sur le terrain : celle de l'authenticité du pointage. Le lecteur "
        "ZK-Teco 9500, largement utilisé dans les systèmes de contrôle d'accès, "
        "permet d'enregistrer des templates d'empreintes et de les associer à un "
        "matricule ; les cartes RFID, quant à elles, matérialisent l'identité "
        "numérique de l'agent au sein du système. Leur combinaison dans SGRH Pro "
        "n'est pas un effet de mode technologique, mais une réponse argumentée à un "
        "problème observé."
    )

    add_heading(doc, "0.4.2. Intérêt du sujet")
    add_body(doc, "L'intérêt de cette recherche se décline sur plusieurs plans :")

    add_bullet(doc,
        " elle mobilise les concepts de systèmes d'information, de modélisation UML, "
        "d'architecture web et d'intégration de périphériques dans une problématique "
        "interdisciplinaire mêlant informatique et gestion ;",
        "Sur le plan académique,")
    add_bullet(doc,
        " elle propose une solution directement applicable au siège central de la CNSS, "
        "avec la possibilité d'une extension ultérieure vers d'autres sites ;",
        "Sur le plan institutionnel,")
    add_bullet(doc,
        " elle réduit les tâches répétitives du personnel RH, fiabilise la paie et "
        "clarifie les droits des agents (congés, bulletins, pointages) ;",
        "Sur le plan opérationnel,")
    add_bullet(doc,
        " elle démontre qu'un prototype SIGRH complet — incluant biométrie réelle — "
        "peut être réalisé avec des technologies accessibles (PHP/Laravel, HTML/CSS/JS, "
        "SDK ZKTeco) et hébergé sur une infrastructure locale ou cloud ;",
        "Sur le plan technique,")
    add_bullet(doc,
        " elle ouvre une voie à la formalisation des pratiques RH dans d'autres "
        "organismes publics congolais confrontés à des difficultés similaires.",
        "Sur le plan de la transférabilité,")

    # ── 0.5 Revue littérature ──
    add_heading(doc, "0.5. Revue de la littérature")

    add_body(doc,
        "La gestion des ressources humaines a fait l'objet d'une abondante littérature. "
        "Dessler (2020) définit la GRH comme l'ensemble des pratiques visant à attirer, "
        "développer, motiver et retenir le personnel au service des objectifs de "
        "l'organisation. Cette vision intégrée implique que les données relatives aux "
        "agents — identité, contrat, rémunération, présence, formation — soient traitées "
        "de manière cohérente, ce qui justifie le recours aux systèmes d'information."
    )

    add_body(doc,
        "Les SIGRH, ou SIRH, occupent une place croissante dans cette dynamique. "
        "Beaudoin et Roy (2019) montrent qu'un système intégré permet de réduire les "
        "délais de traitement, d'améliorer la conformité réglementaire et de fournir "
        "aux décideurs des indicateurs synthétiques. En contexte africain, plusieurs "
        "travaux — notamment ceux de Ndiaye et Diop (2021) sur l'informatisation des "
        "administrations publiques — soulignent toutefois l'écart entre les modèles "
        "théoriques importés et les réalités infrastructurelles locales, d'où l'intérêt "
        "de solutions conçues en tenant compte des contraintes de connectivité, de "
        "compétences et de budget."
    )

    add_body(doc,
        "Concernant le contrôle des présences, Jain et al. (2016), dans leur synthèse "
        "sur l'identification biométrique, rappellent que l'empreinte digitale reste "
        "l'une des modalités les plus répandues en milieu professionnel du fait de son "
        "rapport coût/fiabilité. Les systèmes combinant biométrie et badge RFID, "
        "documentés par Roberts (2018), offrent une redondance utile : l'empreinte "
        "authentifie le pointage, tandis que la carte constitue un support d'identification "
        "visualisable et révocable en cas de perte."
    )

    add_body(doc,
        "Sur le plan architectural, Fowler (2022) et Larman (2019) recommandent, pour "
        "les applications métier de taille moyenne, une séparation entre couche de "
        "présentation, logique métier et persistance — principe appliqué ici par la "
        "distinction frontend/backend. La modélisation UML, normalisée par l'OMG, "
        "fournit un langage partagé pour documenter les cas d'utilisation et les "
        "interactions entre acteurs, indispensable dans un mémoire de conception."
    )

    add_body(doc,
        "Enfin, la dimension « intelligente » du système envisagé s'inscrit dans la "
        "tradition de l'aide à la décision (Turban, Sharda et Delen, 2019) plutôt que "
        "dans celle du machine learning : il s'agit de restituer automatiquement des "
        "agrégats pertinents — masse salariale, taux d'absentéisme, retards par "
        "direction — et de signaler les écarts par rapport à des seuils paramétrables. "
        "Cette approche correspond aux attentes exprimées par les responsables rencontrés "
        "durant le stage, plus sensibles à l'opérationnalité qu'à la sophistication "
        "algorithmique."
    )

    add_body(doc,
        "La littérature confirme donc la pertinence d'un SIGRH intégré, l'apport de la "
        "biométrie pour le pointage, et la nécessité d'une conception adaptée au "
        "contexte. Elle laisse toutefois un espace pour une étude de cas congolaise "
        "articulant ces éléments dans une solution complète couvrant l'ensemble des "
        "tâches RH — espace qui constitue précisément l'objet de ce mémoire."
    )

    # ── 0.6 Méthodologie ──
    add_heading(doc, "0.6. Méthodologie de la recherche")

    add_body(doc,
        "Pour mener à bien cette étude portant sur la conception et l'implémentation "
        "de SGRH Pro au profit de la CNSS, une démarche structurée en phases successives "
        "a été adoptée. Elle combine analyse du contexte, spécification des besoins, "
        "modélisation, développement itératif et validation par tests."
    )

    add_heading(doc, "0.6.1. Méthodes")

    add_heading(doc, "0.6.1.1. Méthode analytique")
    add_body(doc,
        "La méthode analytique a consisté à examiner le fonctionnement actuel du service "
        "RH au siège central : circuits de validation des congés, préparation de la paie, "
        "tenue des registres de présence, archivage des contrats. Cette analyse, nourrie "
        "par l'observation en stage et l'étude documentaire interne, a permis d'identifier "
        "les points de blocage et de traduire les besoins exprimés par les acteurs en "
        "exigences fonctionnelles."
    )

    add_heading(doc, "0.6.1.2. Méthode structuro-fonctionnelle")
    add_body(doc,
        "La méthode structuro-fonctionnelle a été mobilisée pour décomposer le futur "
        "système en modules cohérents (les quatorze modules retenus) et pour définir les "
        "flux d'information entre eux : par exemple, le lien entre les pointages "
        "biométriques, le calcul des heures travaillées et la paie mensuelle."
    )

    add_heading(doc, "0.6.1.3. Méthode de conception orientée objet (UML)")
    add_body(doc,
        "Conformément aux exigences académiques du programme, la conception s'appuie sur "
        "UML. Les diagrammes de cas d'utilisation modélisent les interactions Admin RH, "
        "Manager, Agent et Système biométrique ; les diagrammes de classes structurent "
        "les entités métier ; les diagrammes de séquence décrivent les scénarios critiques "
        "(enrôlement d'une empreinte, validation d'un congé, génération d'un bulletin) ; "
        "le diagramme de déploiement situe les composants (serveur, poste RH, bridge "
        "biométrique, lecteur ZK-Teco 9500)."
    )

    add_heading(doc, "0.6.1.4. Démarche de développement itératif")
    add_body(doc,
        "Le développement a suivi une logique itérative proche du Processus Unifié (UP) : "
        "phase d'inception (cahier des charges), phase d'élaboration (UML, architecture), "
        "phase de construction (implémentation backend, frontend, bridge) et phase de "
        "transition (tests, corrections, préparation de la soutenance). Chaque module a "
        "été intégré progressivement avant la recette globale."
    )

    add_heading(doc, "0.6.2. Techniques")

    add_bullet(doc,
        " consultation d'ouvrages, d'articles et de documentation technique (SDK ZKTeco, "
        "normes UML, référentiels GRH) ;",
        "Technique documentaire :")
    add_bullet(doc,
        " observation des pratiques RH à la CNSS durant le stage et recueil informel "
        "des attentes des utilisateurs ;",
        "Technique d'observation :")
    add_bullet(doc,
        " formalisation des besoins et de l'architecture via StarUML ou équivalent ;",
        "Technique de modélisation UML :")
    add_bullet(doc,
        " implémentation de l'API Laravel, de l'interface web et du bridge C# avec le "
        "lecteur ZK-Teco 9500 ;",
        "Technique de prototypage :")
    add_bullet(doc,
        " tests unitaires, tests d'intégration et scénarios de validation (pointage réel, "
        "calcul paie, parcours agent) ;",
        "Technique d'expérimentation :")
    add_bullet(doc,
        " comparaison qualitative entre la gestion manuelle observée et le prototype "
        "SGRH Pro (temps de traitement, fiabilité du pointage, accessibilité des données).",
        "Technique comparative :")

    # ── 0.7 Délimitation ──
    add_heading(doc, "0.7. Délimitation du sujet")

    add_heading(doc, "0.7.1. Délimitation thématique")
    add_body(doc,
        "Le travail porte exclusivement sur la gestion interne des ressources humaines "
        "de la CNSS : dossiers agents, présences, congés, paie, contrats, formation, "
        "évaluation, recrutement et reporting. Les missions externes de l'institution "
        "— gestion des assurés, collecte des cotisations, paiement des prestations — "
        "sont hors périmètre."
    )

    add_heading(doc, "0.7.2. Délimitation spatiale et institutionnelle")
    add_body(doc,
        "L'étude se réfère au siège central de la CNSS à Kinshasa. Le prototype est "
        "destiné à être installé, dans un premier temps, sur le poste de travail du "
        "responsable RH à des fins de démonstration et de soutenance. Une généralisation "
        "multi-sites n'est pas couverte, bien que l'architecture soit conçue pour "
        "permettre un hébergement centralisé ultérieur."
    )

    add_heading(doc, "0.7.3. Délimitation technique")
    add_body(doc,
        "Le système couvre la conception logicielle, l'intégration du lecteur ZK-Teco 9500 "
        "et l'usage de cartes RFID. La fabrication des composants matériels ou l'étude "
        "approfondie du droit congolais de la protection des données biométriques ne "
        "sont pas traités ; seules les mesures techniques élémentaires (stockage des "
        "templates, révocation des cartes, journal d'audit) sont implémentées dans le "
        "prototype."
    )

    add_heading(doc, "0.7.4. Délimitation temporelle")
    add_body(doc,
        "La recherche s'inscrit dans la période de réalisation du mémoire (2026-2027). "
        "Elle vise un prototype fonctionnel et testé, non un déploiement institutionnel "
        "complet ni une certification juridique du dispositif biométrique."
    )

    # ── 0.8 Subdivision ──
    add_heading(doc, "0.8. Subdivision du travail")

    add_body(doc,
        "Hormis l'introduction générale et la conclusion générale, le présent mémoire "
        "est structuré en quatre chapitres :"
    )

    chapters = [
        ("Le premier chapitre", " expose le cadre théorique et l'état de l'art : "
         "généralités sur la GRH, les SIGRH, la biométrie et le RFID, les solutions "
         "existantes, les limites des pratiques manuelles et les fondements UML."),
        ("Le deuxième chapitre", " analyse le système actuel de la CNSS, les besoins "
         "des acteurs et le cahier des charges des quatorze modules fonctionnels."),
        ("Le troisième chapitre", " présente la conception et l'architecture de SGRH Pro : "
         "diagrammes UML, modèle de données, API backend, interface frontend, sous-système "
         "biométrique et stratégie d'hébergement."),
        ("Le quatrième chapitre", " décrit l'implémentation, les tests (dont le pointage "
         "biométrique réel), les résultats obtenus, la comparaison avec l'existant et les "
         "perspectives d'évolution."),
    ]
    for prefix, rest in chapters:
        add_mixed(doc, [(prefix, True, False), (rest, False, False)])

    add_body(doc,
        "Cette progression — de la théorie à la validation expérimentale — vise à "
        "démontrer de manière argumentée qu'un SIGRH intelligent, intégrant biométrie "
        "et RFID, constitue une réponse adaptée aux besoins de gestion du personnel "
        "au sein du siège central de la CNSS."
    )

    doc.save(OUTPUT)
    print(f"Introduction générée : {OUTPUT}")


if __name__ == "__main__":
    build()

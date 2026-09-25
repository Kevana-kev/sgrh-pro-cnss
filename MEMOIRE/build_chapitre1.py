# -*- coding: utf-8 -*-
"""Génère le Chapitre I — Cadre théorique et état de l'art."""
from pathlib import Path

from memoire_format import (
    init_document, add_page_number, add_chapter_title, add_heading, add_subheading,
    add_body, add_mixed, add_bullet, add_numbered_item, add_objectives_list, add_table,
    add_figure,
)

OUTPUT = r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\CHAPITRE I - CADRE THEORIQUE ET ETAT DE L ART.docx"
OUTPUT_FALLBACK = r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\CHAPITRE I - CADRE THEORIQUE ET ETAT DE L ART - v2.docx"
IMG_DIR = Path(r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\images\chapitre1")
PAGE_START = 13


def _fig(name: str) -> str:
    p = IMG_DIR / name
    if name == "fig_i6_zkteco9500.png" and not p.exists():
        alt = IMG_DIR / "figi6_zkteco9500.png"
        if alt.exists():
            return str(alt)
    return str(p)


def _ensure_figures():
    import generate_figures_ch1
    generate_figures_ch1.main()


def append_chapitre1(doc, page_start=13):
    _ensure_figures()
    add_page_number(doc, page_start)
    add_chapter_title(doc, "CHAPITRE I. CADRE THÉORIQUE ET ÉTAT DE L'ART")

    # ───────────────── I.1 ─────────────────
    add_heading(doc, "I.1. Introduction")

    add_body(doc,
        "La conception d'un système d'information de gestion des ressources humaines — "
        "tel que celui envisagé pour la Caisse Nationale de Sécurité Sociale (CNSS) en "
        "République Démocratique du Congo — ne saurait se réduire à l'écriture de code "
        "ou au déploiement de périphériques biométriques. Elle suppose au préalable une "
        "compréhension rigoureuse des concepts que mobilise le projet : gestion du "
        "personnel, architecture des SIGRH, identification numérique, indicateurs de "
        "pilotage et modélisation logicielle."
    )

    add_body(doc,
        "Comme le rappellent Pinto et Grawitz (2020), toute recherche appliquée doit "
        "s'appuyer sur un cadre théorique explicite, faute de quoi les choix techniques "
        "apparaîtraient arbitraires et les résultats difficilement défendables devant "
        "un jury. Dans le cas présent, l'enjeu est double : il s'agit à la fois de "
        "situer le travail dans la continuité des travaux sur la GRH et les systèmes "
        "d'information, et de montrer en quoi l'association d'un SIGRH modulaire, d'un "
        "lecteur d'empreintes ZK-9500 et de cartes RFID répond à un besoin identifié "
        "lors du stage au siège central de Kinshasa."
    )

    add_body(doc, "Ce chapitre vise ainsi à :")

    add_objectives_list(doc, [
        [("Définir les notions fondamentales de ", False, False),
         ("gestion des ressources humaines (GRH)", True, False),
         (" et de ", False, False),
         ("système d'information des ressources humaines (SIGRH)", True, False),
         (".", False, False)],
        [("Présenter la ", False, False),
         ("dimension « intelligente »", True, False),
         (" retenue dans le projet SGRH Pro, fondée sur les tableaux de bord, les KPI "
          "et les alertes automatiques.", False, False)],
        [("Exposer les principes de la ", False, False),
         ("biométrie", True, False),
         (" et des ", False, False),
         ("cartes RFID", True, False),
         (", ainsi que les caractéristiques du lecteur ZK-9500.", False, False)],
        [("Analyser les ", False, False),
         ("solutions SIGRH existantes", True, False),
         (" et les limites des pratiques manuelles encore observées dans les "
          "administrations congolaises.", False, False)],
        [("Présenter les ", False, False),
         ("fondements UML", True, False),
         (" et l'", False, False),
         ("architecture logicielle", True, False),
         (" backend/frontend retenue pour l'implémentation.", False, False)],
    ])

    add_body(doc,
        "L'approche adoptée combine une revue de la littérature académique et professionnelle, "
        "l'analyse de solutions logicielles disponibles sur le marché et la réflexion sur "
        "les contraintes propres au contexte institutionnel congolais. Ce socle théorique "
        "alimentera directement le chapitre II (analyse du système actuel et cahier des "
        "charges) et guidera les choix de conception développés au chapitre III."
    )

    add_body(doc,
        "La structure retenue pour ce chapitre s'inspire des mémoires de référence "
        "en ingénierie informatique : une progression du général au particulier, "
        "alternant définitions, schémas, tableaux comparatifs et retours sur l'état "
        "de l'art. Chaque notion théorique est reliée, lorsque c'est pertinent, "
        "au projet SGRH Pro et au contexte CNSS, afin que le lecteur puisse "
        "suivre le fil conducteur entre cadre conceptuel et solution proposée."
    )

    # ───────────────── I.2 GRH ─────────────────
    add_heading(doc, "I.2. Généralités sur la gestion des ressources humaines (GRH)")

    add_subheading(doc, "I.2.1. Définition et enjeux de la GRH")

    add_mixed(doc, [
        ("La ", False, False),
        ("gestion des ressources humaines (GRH)", True, False),
        (", selon Dessler (2020), désigne l'ensemble des pratiques organisées visant à "
         "attirer, recruter, former, rémunérer, évaluer et retenir le personnel au "
         "service des objectifs d'une organisation. Elle ne se limite donc pas au "
         "traitement administratif du personnel : elle englobe la ", False, False),
        ("gestion du capital humain", True, False),
        (", c'est-à-dire la manière dont une institution valorise les compétences, "
         "anticipe les besoins en effectifs et crée les conditions d'un travail productif.",
         False, False),
    ])

    add_body(doc,
        "Historiquement, la fonction personnel est née de la nécessité de tenir des "
        "registres d'employés et de respecter les obligations légales en matière de "
        "contrats et de cotisations sociales. Au fil des décennies, elle s'est "
        "complexifiée : la montée en puissance des syndicats, la diversification des "
        "statuts (CDI, CDD, stage, intérim), la réglementation du temps de travail et "
        "l'exigence croissante de transparence ont élargi le périmètre des services RH."
    )

    add_body(doc,
        "Aujourd'hui, la GRH se présente comme un levier stratégique. Ulrich (1997) "
        "proposait déjà de distinguer quatre rôles du professionnel RH : partenaire "
        "stratégique, agent de changement, expert administratif et défenseur des "
        "employés. Dans une institution publique comme la CNSS, le rôle administratif "
        "reste prépondérant — tenue des dossiers, congés, présences —, mais la pression "
        "exercée par les directions sur la fiabilité des effectifs et des coûts salariaux "
        "pousse progressivement vers un pilotage plus analytique."
    )

    add_body(doc,
        "On distingue classiquement deux approches de la GRH (Torrington, Hall "
        "et Taylor, 2020) : une approche "
        "hard, centrée sur les chiffres, les procédures et la conformité réglementaire ; "
        "et une approche soft, attentive aux relations humaines, à la motivation "
        "et à la culture organisationnelle. Un SIGRH comme SGRH Pro relève "
        "principalement de la première — automatisation, calculs, reporting — "
        "mais il peut aussi servir la seconde en libérant du temps aux responsables "
        "RH pour l'accompagnement individuel des agents, plutôt que pour la "
        "recherche de documents égarés."
    )

    add_subheading(doc, "I.2.2. Les fonctions et processus RH")

    add_body(doc,
        "La littérature identifie généralement six grandes fonctions RH, auxquelles "
        "correspondent des processus métier que le système SGRH Pro se propose "
        "d'informatiser :"
    )

    add_numbered_item(doc, 1, " recrutement et intégration des nouveaux agents ;",
                      "Planification des effectifs et ")
    add_numbered_item(doc, 2, " administration du personnel (dossiers, contrats, "
                      "mutations, documents) ;")
    add_numbered_item(doc, 3, " gestion des temps et des activités (présences, "
                      "absences, heures supplémentaires) ;")
    add_numbered_item(doc, 4, " suivi administratif et avantages (éléments variables, "
                      "transmission à la finance) ;")
    add_numbered_item(doc, 5, " développement des compétences (formations, évaluations, "
                      "plans de carrière) ;")
    add_numbered_item(doc, 6, " relations sociales et conformité réglementaire.")

    add_figure(
        doc, _fig("fig_i7_cycle_grh.png"),
        "Figure 1 : Cycle de vie de l'agent couvert par un SIGRH intégré",
        width_cm=15.8,
    )

    add_body(doc,
        "Chacune de ces fonctions produit et consomme des données. Lorsque celles-ci "
        "circulent entre registres papier, fichiers Excel et logiciels non connectés, "
        "des incohérences apparaissent rapidement : un agent présent sur le registre "
        "de pointage mais absent du fichier administratif ; un congé approuvé verbalement "
        "mais non déduit du solde ; un contrat CDD arrivant à échéance sans alerte "
        "préalable. Ces dysfonctionnements, observés durant le stage à la CNSS, "
        "illustrent l'intérêt d'un traitement intégré."
    )

    add_subheading(doc, "I.2.3. La GRH dans les institutions publiques africaines")

    add_body(doc,
        "En Afrique subsaharienne, la fonction RH des administrations publiques "
        "présente des caractéristiques communes : effectifs nombreux, carrières longues, "
        "réglementation héritée de l'administration coloniale puis réformée par "
        "voie législative locale, et informatisation inégale selon les ministères "
        "et les établissements publics."
    )

    add_body(doc,
        "Ndiaye et Diop (2021), dans leur analyse des systèmes d'information "
        "administratifs en Afrique de l'Ouest et centrale, soulignent que la "
        "modernisation RH progresse lentement lorsque les investissements portent "
        "sur le matériel sans accompagnement des processus. L'achat d'ordinateurs "
        "n'efface pas les registres si les agents continuent de recopier les mêmes "
        "informations dans des tableurs parallèles. La réussite d'un projet comme "
        "SGRH Pro dépend autant de la qualité logicielle que de l'adéquation aux "
        "habitudes de travail réelles."
    )

    add_body(doc,
        "En République Démocratique du Congo, la CNSS occupe une place particulière : "
        "institution de prévoyance sociale chargée des cotisations et prestations, "
        "elle emploie elle-même un personnel administratif, technique et de terrain "
        "dont la gestion relève des mêmes impératifs que dans tout grand organisme "
        "public — centralisation, traçabilité, équité dans le traitement des agents."
    )

    add_subheading(doc, "I.2.4. Évolution des systèmes d'information RH")

    add_body(doc,
        "L'historique des systèmes d'information appliqués à la GRH peut être "
        "schématisé en quatre générations (Tannenbaum, 2018). La première "
        "correspond à l'informatisation des seules opérations de paie sur "
        "mainframe, dans les années 1960-1970. La deuxième voit l'extension "
        "aux dossiers administratifs et à la gestion des absences, avec des "
        "logiciels monolithiques sur micro-ordinateurs. La troisième génération, "
        "à partir des années 2000, introduit les portails web et l'accès "
        "self-service pour les employés. La quatrième — parfois qualifiée "
        "d'expérience employé (Employee Experience) — intègre mobilité, "
        "analytics avancés, voire intelligence artificielle."
    )

    add_body(doc,
        "Le projet SGRH Pro se situe principalement entre la troisième et "
        "la quatrième génération : portail agent, reporting avancé, alertes "
        "automatiques, mais sans recours au machine learning. L'apport "
        "distinctif du projet réside dans l'intégration native de la "
        "biométrie ZK-9500, peu présente dans les SIGRH généralistes "
        "du marché congolais."
    )

    add_figure(
        doc, _fig("fig_i8_generations_sigrh.png"),
        "Figure 2 : Évolution des générations de systèmes d'information RH",
        width_cm=15.8,
    )

    add_subheading(doc, "I.2.5. Processus RH retenus pour SGRH Pro")

    add_body(doc,
        "SGRH Pro couvre prioritairement le pointage biométrique, les "
        "congés, les éléments administratifs de rémunération, l'évaluation "
        "et le reporting. Les processus secondaires (recrutement, contrats, "
        "formation) sont hors périmètre du prototype."
    )

    add_subheading(doc, "I.2.7. Digitalisation de la GRH en Afrique subsaharienne")

    add_body(doc,
        "La transformation numérique des fonctions RH progresse de manière "
        "inégale sur le continent africain. Plusieurs facteurs expliquent "
        "cette hétérogénéité : niveau d'investissement public, disponibilité "
        "de l'infrastructure réseau, compétences informatiques internes "
        "et résistance au changement des agents habitués aux procédures "
        "papier. Ndiaye et Diop (2021) observent que les projets les plus "
        "durables combinent trois leviers : un logiciel adapté au contexte "
        "local, une formation ciblée des utilisateurs et un accompagnement "
        "politique de la direction générale."
    )

    add_body(doc,
        "En République Démocratique du Congo, la digitalisation des "
        "administrations publiques s'inscrit dans une dynamique plus "
        "large de modernisation de l'État. Toutefois, les projets "
        "informatiques y restent souvent ponctuels — achat de matériel "
        "sans refonte des processus — ou dépendants de financements "
        "extérieurs limités dans le temps. Le développement de SGRH Pro "
        "s'inscrit dans une logique inverse : partir des processus "
        "observés à la CNSS, modéliser leurs dysfonctionnements, "
        "puis proposer une solution logicielle contextualisée, "
        "hébergeable localement et évolutive."
    )

    add_table(doc,
              ["Facteur de réussite", "Risque si absent", "Mesure prévue dans SGRH Pro"],
              [
                  ["Adéquation aux processus locaux", "Rejet utilisateur", "Spécifications issues du stage CNSS"],
                  ["Formation des agents RH", "Sous-utilisation", "Interface en français, parcours guidés"],
                  ["Source unique de données", "Doublons persistants", "Base centralisée, API unique"],
                  ["Soutien de la direction", "Abandon du projet", "KPI pour pilotage décisionnel"],
                  ["Sécurité des données", "Fuites, défiance", "RBAC, audit log, consentement biométrique"],
              ],
              "Tableau 1 : Facteurs de réussite d'un SIGRH en contexte africain")

    # ───────────────── I.3 SIGRH ─────────────────
    add_heading(doc, "I.3. Systèmes d'information des ressources humaines (SIGRH / SIRH)")

    add_subheading(doc, "I.3.1. Définition et composantes")

    add_mixed(doc, [
        ("Un ", False, False),
        ("système d'information (SI)", True, False),
        (", au sens de Reix (2019), est un ensemble organisé de ressources "
         "(humaines, matérielles, logicielles, données) permettant d'acquérir, "
         "de traiter, de conserver et de diffuser l'information au sein d'une "
         "organisation. Un ", False, False),
        ("système d'information des ressources humaines (SIGRH)", True, False),
        (", aussi désigné SIRH en francophonie, en constitue une spécialisation "
         "centrée sur le capital humain.", False, False),
    ])

    add_mixed(doc, [
        ("Un ", False, False),
        ("système d'information des ressources humaines (SIGRH)", True, False),
        (" est donc un ensemble coordonné de bases de données, de règles métier "
         "et d'interfaces permettant de ", False, False),
        ("collecter, stocker, traiter et restituer", True, False),
        (" l'information relative au personnel (Beaudoin et Roy, 2019).",
         False, False),
    ])

    add_body(doc,
        "Contrairement à un simple fichier administratif ou à une application de pointage "
        "isolée, un SIGRH couvre l'ensemble du cycle de vie de l'agent : de "
        "l'embauche à la sortie, en passant par les évolutions de poste, les "
        "formations suivies et les évaluations reçues. Sa valeur réside dans la "
        "liaison entre modules : les heures enregistrées par le pointage biométrique "
        "alimentent le calcul des heures supplémentaires ; celles-ci influencent "
        "le relevé administratif ; les données sont consultables par l'agent dans son "
        "espace personnel."
    )

    add_body(doc, "Les composantes fonctionnelles retenues pour SGRH Pro comprennent :")

    add_bullet(doc, " un référentiel agents (identité, matricule, photo, coordonnées) ;")
    add_bullet(doc, " un module temps et activités (pointages biométriques, absences) ;")
    add_bullet(doc, " un module éléments de rémunération et états pour la finance ;")
    add_bullet(doc, " un module congés et permissions avec workflow de validation ;")
    add_bullet(doc, " un module évaluation et performance ;")
    add_bullet(doc, " un portail self-service pour les agents ;")
    add_bullet(doc, " un module reporting et tableaux de bord ;")
    add_bullet(doc, " un socle de sécurité (authentification, rôles, journal d'audit).")

    add_body(doc,
        "Le projet SGRH Pro retenu pour la CNSS reprend cette décomposition sous "
        "forme de huit modules fonctionnels, détaillés au chapitre II, recentrés "
        "sur les présences, la biométrie, l'évaluation et les éléments de rémunération."
    )

    add_subheading(doc, "I.3.1.1. Rémunération des agents publics et rôle du SIGRH")

    add_body(doc,
        "À la CNSS, comme dans la plupart des institutions publiques congolaises, "
        "la rémunération des agents est versée par voie bancaire sous la responsabilité "
        "de la direction administrative et financière. Le service des ressources humaines "
        "n'effectue pas le paiement des salaires : il produit et transmet les "
        "informations administratives fiables — états de présence, absences, éléments "
        "variables, mouvements de personnel — sur lesquelles s'appuie la finance "
        "pour le virement bancaire."
    )

    add_body(doc,
        "Le logiciel SGRH Pro est conçu en cohérence avec cette organisation : "
        "son module de suivi administratif des éléments de rémunération consolide "
        "les données enregistrées par les autres modules (présences, congés, évaluations) "
        "et génère des états exportables pour la direction financière. Il ne se "
        "substitue pas au système bancaire ni au circuit comptable de l'État, "
        "mais il supprime les ressaisies manuelles qui alimentent aujourd'hui "
        "les retards et les incohérences observés au siège central."
    )

    add_subheading(doc, "I.3.2. Architecture fonctionnelle d'un SIGRH")

    add_body(doc,
        "Du point de vue fonctionnel, un SIGRH s'organise autour de trois couches "
        "logiques (Laudon et Laudon, 2022) :"
    )

    add_numbered_item(doc, 1,
        " la couche de saisie et d'acquisition, où les données sont produites "
        "(formulaires web, import de fichiers, terminaux de pointage, capteurs) ;")
    add_numbered_item(doc, 2,
        " la couche de traitement, où s'appliquent les règles métier (workflows, "
        "validation hiérarchique, détection de retards) ;")
    add_numbered_item(doc, 3,
        " la couche de restitution, où les informations sont présentées aux utilisateurs "
        "(écrans de gestion, états administratifs exportés, graphiques, exports).")

    add_body(doc,
        "Dans SGRH Pro, la couche d'acquisition inclut le lecteur d'empreintes "
        "ZK-9500 et le lecteur de cartes RFID ; la couche de traitement applique "
        "les règles de présence, de congé et d'évaluation ; la couche de "
        "restitution correspond à l'interface web, différenciée selon le profil "
        "(administrateur RH, manager, agent)."
    )

    add_figure(
        doc, _fig("fig_i1_architecture_sigrh.png"),
        "Figure 3 : Architecture fonctionnelle à trois couches d'un SIGRH",
        width_cm=15.8,
    )

    add_subheading(doc, "I.3.3. Avantages d'un SIGRH intégré")

    add_body(doc,
        "Le passage d'une gestion dispersée à un SIGRH intégré procure des bénéfices "
        "documentés dans de nombreuses études de cas. Pour une institution publique, "
        "on peut citer :"
    )

    add_bullet(doc,
        " la réduction des délais de traitement (congés, états administratifs, édition d'attestations) ;",
        "Gain de productivité :")
    add_bullet(doc,
        " la fiabilité accrue des données grâce à une source unique de vérité ;",
        "Qualité de l'information :")
    add_bullet(doc,
        " la traçabilité des opérations sensibles (modification de dossier, "
        "réinitialisation de mot de passe, désactivation d'une carte RFID) ;",
        "Contrôle et audit :")
    add_bullet(doc,
        " la possibilité de produire des statistiques consolidées pour les directions ;",
        "Pilotage :")
    add_bullet(doc,
        " l'autonomie des agents via un portail (consultation des présences, demande de congé).",
        "Transparence :")

    add_body(doc,
        "Ces avantages ne sont pas automatiques : ils supposent une modélisation "
        "correcte des processus, une formation minimale des utilisateurs et une "
        "maintenance régulière du système. Le chapitre IV reviendra sur la mesure "
        "concrète de ces gains dans le prototype déployé."
    )

    add_subheading(doc, "I.3.4. Sécurité, authentification et gestion des accès")

    add_body(doc,
        "Un SIGRH traite des données sensibles : coordonnées, présences, éventuellement "
        "données biométriques. Sa sécurité repose sur plusieurs mécanismes complémentaires "
        "retenus dans SGRH Pro (Stallings, 2020) :"
    )

    add_bullet(doc, " authentification par identifiant et mot de passe (stocké sous forme chiffrée) ;")
    add_bullet(doc, " sessions limitées dans le temps, révoquées à la déconnexion ;")
    add_bullet(doc, " contrôle d'accès basé sur les rôles : SuperAdmin, Admin RH, Manager, Employé ;")
    add_bullet(doc, " journal d'activité (audit log) des opérations sensibles ;")
    add_bullet(doc, " changement obligatoire du mot de passe par défaut à la première connexion.")

    add_body(doc,
        "Cette architecture garantit qu'un agent ne peut consulter que son propre "
        "espace, qu'un manager valide les congés de son équipe et qu'un administrateur "
        "RH dispose des droits étendus sans que les permissions ne se mélangent. "
        "Le principe du moindre privilège — chaque utilisateur reçoit uniquement "
        "les droits nécessaires à sa fonction — guide la configuration des rôles."
    )

    add_figure(
        doc, _fig("fig_i4_rbac.png"),
        "Figure 4 : Modèle de contrôle d'accès par rôles (RBAC) dans SGRH Pro",
        width_cm=15.8,
    )

    add_subheading(doc, "I.3.5. Composantes d'un SIGRH moderne")

    add_body(doc,
        "Un SIGRH moderne repose, de manière générale, sur trois composantes "
        "coordonnées : une application de gestion consultable par les "
        "responsables et les agents, une base de données relationnelle "
        "centralisant les dossiers, et, le cas échéant, des périphériques "
        "d'identification (lecteur d'empreintes, cartes RFID). Les fonctions "
        "principales couvrent l'authentification, le dossier employé, le "
        "pointage, les congés, l'enrôlement biométrique et les indicateurs "
        "de pilotage. Cette organisation, exposée ici sur le plan conceptuel, "
        "sera traduite en architecture détaillée au chapitre III."
    )

    # ───────────────── I.4 Intelligent ─────────────────
    add_heading(doc, "I.4. Dimension « intelligente » du système")

    add_body(doc,
        "Le qualificatif « intelligent » appliqué au système SGRH Pro mérite d'être "
        "précisé, car il prête à confusion avec l'intelligence artificielle au sens "
        "strict (apprentissage automatique, réseaux de neurones). Dans le cadre de "
        "ce mémoire, il renvoie à une "
        "intelligence décisionnelle opérationnelle : le système agrège des données "
        "brutes, calcule des indicateurs et signale proactivement les situations "
        "requérant l'attention d'un responsable."
    )

    add_subheading(doc, "I.4.1. Tableaux de bord et indicateurs clés (KPI RH)")

    add_body(doc,
        "Un tableau de bord RH est une interface synthétique présentant, sous forme "
        "de chiffres clés et de graphiques, l'état du capital humain à un instant "
        "donné (Parmentier et Thébault, 2018). Les KPI (Key Performance Indicators) "
        "les plus couramment suivis dans un SIGRH sont :"
    )

    kpis = [
        ("Effectif total et répartition par département", "Mesure la structure des ressources"),
        ("Taux d'absentéisme", "Absences / jours ouvrables × 100"),
        ("Taux de retard", "Agents en retard / agents pointés"),
        ("Taux de présence mensuel", "Présents / effectif attendu"),
        ("Congés en attente de validation", "Nombre de demandes non traitées"),
        ("Score moyen d'évaluation", "Pilotage des performances"),
        ("Taux de couverture biométrique", "Agents enrôlés / effectif actif"),
    ]
    add_table(doc,
              ["Indicateur", "Formulation / intérêt"],
              kpis,
              "Tableau 2 : Principaux KPI RH implémentés dans SGRH Pro")

    add_body(doc,
        "Dans le prototype, ces indicateurs sont calculés dynamiquement à partir "
        "de la base de données et affichés sur le dashboard principal, avec des "
        "graphiques par département et une évolution temporelle des congés. Cette "
        "restitution visuelle répond à une demande exprimée par les responsables "
        "rencontrés durant le stage : disposer d'un coup d'œil sur la situation "
        "RH sans lancer manuellement des recoupements Excel."
    )

    add_subheading(doc, "I.4.2. Alertes automatiques")

    add_body(doc,
        "Au-delà de la visualisation, la dimension intelligente du système repose "
        "sur un mécanisme d'alertes paramétrables. Une alerte est déclenchée "
        "lorsqu'une condition métier est satisfaite. Le tableau I.5 bis "
        "précise les principales alertes prévues, leur gravité et le "
        "destinataire concerné."
    )

    add_table(doc,
              ["Type d'alerte", "Condition", "Destinataire", "Gravité"],
              [
                  ["Retard répété", "> 3 retards / semaine", "Manager, RH", "Moyenne"],
                  ["Absence non justifiée", "Absence sans motif validé", "RH", "Élevée"],
                  ["Congé en attente", "> 3 jours sans traitement", "RH, Manager", "Moyenne"],
                  ["Évaluation en retard", "Période clôturée sans grille", "RH", "Moyenne"],
                  ["Carte RFID inactive", "Pointage avec carte désactivée", "RH", "Élevée"],
              ],
              "Tableau 3 : Typologie des alertes automatiques dans SGRH Pro")

    add_body(doc,
        "Ces alertes complémentaires s'ajoutent aux conditions suivantes :"
    )

    add_bullet(doc, " seuil de retard dépassé (ex. plus de 15 minutes) ;")
    add_bullet(doc, " absence non justifiée consécutive ;")
    add_bullet(doc, " solde de congé insuffisant pour une demande ;")
    add_bullet(doc, " carte RFID désactivée utilisée pour un pointage.")

    add_body(doc,
        "Ces alertes sont consultables par les profils autorisés. Elles "
        "ne remplacent pas la décision humaine, mais réduisent le risque "
        "qu'une anomalie passe inaperçue."
    )

    add_subheading(doc, "I.4.3. Automatisation et intelligence décisionnelle : distinction")

    add_body(doc,
        "Il importe de distinguer clairement l'automatisation de l'intelligence "
        "décisionnelle (Turban, Sharda et Delen, 2019). L'automatisation exécute "
        "une règle fixe : consolider les présences du mois, "
        "déduire un jour de congé approuvé, horodater un pointage biométrique. "
        "L'intelligence décisionnelle, telle que retenue ici, aide à interpréter "
        "des agrégats de données et à prioriser les actions — par exemple "
        "signaler que le département X concentre 40 % des retards du mois."
    )

    add_body(doc,
        "Le projet n'intègre pas, à ce stade, de modèles prédictifs (forecasting "
        "d'absentéisme, scoring de performance par ML). Une telle extension "
        "constituerait une perspective ouverte au chapitre IV, mais dépasserait "
        "le périmètre du prototype de démonstration."
    )

    add_figure(
        doc, _fig("fig_i9_si_donnees_flux.png"),
        "Figure 5 : Chaîne de transformation des données en aide à la décision RH",
        width_cm=15.8,
    )

    add_subheading(doc, "I.4.4. Couverture fonctionnelle des huit modules")

    add_body(doc,
        "La dimension intelligente du système irrigue les modules retenus. "
        "Le tableau I.3 en présente une synthèse."
    )

    add_table(doc,
              ["Module", "Apport « intelligent » principal"],
              [
                  ["Utilisateurs & accès", "Audit des connexions et des changements de rôle"],
                  ["Dossiers employés", "Recherche unifiée, statuts consolidés"],
                  ["Biométrie & RFID", "Taux d'enrôlement, traçabilité du pointage"],
                  ["Présences & absences", "Calcul auto retards, heures travaillées"],
                  ["Congés", "Workflow de validation, soldes en temps réel"],
                  ["Éléments rémunération", "États consolidés, export finance"],
                  ["Évaluation", "Historique des notations par agent"],
                  ["Reporting", "KPI globaux, alertes, exports PDF/CSV"],
              ],
              "Tableau 4 : Modules SGRH Pro et apports décisionnels")

    # ───────────────── I.5 Biométrie ─────────────────
    add_heading(doc, "I.5. Technologies d'identification et de contrôle d'accès")

    add_subheading(doc, "I.5.1. La biométrie : principes et modalités")

    add_mixed(doc, [
        ("La ", False, False),
        ("biométrie", True, False),
        (" désigne l'ensemble des techniques permettant d'identifier ou de "
         "authentifier un individu à partir de caractéristiques physiques ou "
         "comportementales mesurables (Jain, Flynn et Ross, 2021). Les modalités "
         "les plus répandues en milieu professionnel sont :", False, False),
    ])

    add_bullet(doc, " l'empreinte digitale ;")
    add_bullet(doc, " la reconnaissance faciale ;")
    add_bullet(doc, " la géométrie de la main ;")
    add_bullet(doc, " la reconnaissance de l'iris.")

    add_body(doc,
        "L'empreinte digitale reste la modalité la plus adoptée dans les systèmes "
        "de pointage RH du fait de son coût modéré, de sa maturité technologique "
        "et de son taux d'erreur acceptable (FAR/FRR) pour des effectifs de "
        "quelques centaines à quelques milliers d'agents. Le principe est le "
        "suivant : lors de l'enrôlement, le capteur extrait un "
        "template numérique de l'empreinte — une représentation mathématique, "
        "non une image photographique stockée telle quelle — qui est enregistrée "
        "dans la base du système. Lors du pointage, une nouvelle capture est "
        "comparée aux templates enregistrés ; en cas de correspondance au-delà "
        "d'un seuil de confiance, l'identité est validée."
    )

    add_subheading(doc, "I.5.2. Intégration logicielle du capteur ZK-9500")

    add_body(doc,
        "Le lecteur ZK-9500 est un capteur d'empreintes digitales USB conçu "
        "pour l'enrôlement et la vérification d'identité en environnement "
        "de bureau. Il s'intègre au poste du responsable RH et alimente "
        "le module biométrique de SGRH Pro via le bridge logiciel."
    )

    add_figure(
        doc, _fig("fig_i6_zkteco9500.png"),
        "Figure 6 : Lecteur d'empreintes digitales ZK-9500 (poste RH)",
        width_cm=15.8,
    )

    add_body(doc,
        "Dans SGRH Pro, le capteur ZK-9500 n'est pas un objet autonome : c'est "
        "un composant d'acquisition raccordé au logiciel par un service "
        "intermédiaire installé sur le poste Windows du responsable RH. "
        "Le module biométrique de l'application reçoit les modèles d'empreintes, "
        "les associe au matricule de l'agent et alimente le suivi des présences. "
        "Cette séparation évite de lier le serveur applicatif au système "
        "d'exploitation du poste de pointage."
    )

    add_body(doc,
        "Ce découplage illustre une règle de conception retenue tout au long "
        "du projet : le logiciel porte la logique métier ; le matériel fournit "
        "des événements horodatés (pointage, enrôlement) que le système "
        "enregistre, contrôle et restitue. Les fonctions logicielles associées "
        "sont : enrôlement via l'interface web, vérification d'identité lors "
        "du pointage, traçabilité de la source (empreinte ou RFID) et "
        "sécurisation des échanges entre le lecteur et l'application."
    )

    add_subheading(doc, "I.5.3. Intégration logicielle des cartes RFID")

    add_mixed(doc, [
        ("La technologie ", False, False),
        ("RFID", True, False),
        (" (", False, False),
        ("Radio-Frequency Identification", False, True),
        (") repose sur l'échange d'informations par ondes radio entre une ",
         False, False),
        ("étiquette", True, False),
        (" (puce + antenne) et un ", False, False),
        ("lecteur", True, False),
        (". Dans un contexte RH, la carte RFID nominative sert de support "
         "d'identification matériel : chaque agent reçoit une carte associée "
         "à son matricule dans le système.", False, False),
    ])

    add_body(doc,
        "Contrairement à une idée reçue, la carte RFID ne remplace pas ici "
        "l'empreinte pour le pointage : dans SGRH Pro, c'est l'empreinte "
        "digitale qui authentifie le passage effectif à l'entrée ou à la sortie. "
        "La carte joue un rôle complémentaire — identification visuelle, accès "
        "aux locaux, support de secours en cas d'impossibilité temporaire de "
        "scanner une empreinte (doigt blessé) — et surtout matérialise le lien "
        "numérique entre l'agent et son dossier."
    )

    add_body(doc,
        "Le module biométrique de SGRH Pro enregistre l'identifiant RFID dans "
        "le dossier Employee, active ou désactive la carte via l'API et consigne "
        "la source « rfid » lors d'un pointage. La révocabilité de la carte "
        "complète la logique logicielle de sécurité : une carte perdue est "
        "désactivée sans modifier le dossier agent ni le template d'empreinte."
    )

    add_figure(
        doc, _fig("fig_i5_rfid_principe.png"),
        "Figure 7 : Carte RFID nominative et lecteur USB associé",
        width_cm=15.8,
    )

    add_subheading(doc, "I.5.3 bis. Comparatif des modalités biométriques")

    add_body(doc,
        "Le choix de l'empreinte digitale pour SGRH Pro s'appuie sur une "
        "analyse comparative des modalités disponibles. Le tableau I.6 bis "
        "résume les critères retenus."
    )

    add_table(doc,
              ["Modalité", "Coût", "Précision", "Acceptabilité", "Retenu"],
              [
                  ["Empreinte digitale", "Modéré", "Élevée", "Bonne", "Oui (ZK-9500)"],
                  ["Reconnaissance faciale", "Élevé", "Variable", "Controversée", "Non"],
                  ["Géométrie de la main", "Élevé", "Élevée", "Moyenne", "Non"],
                  ["Iris", "Très élevé", "Très élevée", "Faible", "Non"],
                  ["Badge RFID seul", "Faible", "Faible (pas biométrique)", "Bonne", "Complément"],
              ],
              "Tableau 5 : Comparatif des modalités d'identification")

    add_subheading(doc, "I.5.4. Combinaison empreinte digitale et RFID dans SGRH Pro")

    add_body(doc,
        "Roberts (2018) recommande, pour les organisations de taille moyenne, "
        "une approche hybride combinant biométrie et badge RFID : la biométrie "
        "garantit que la personne présente est bien celle qui pointe ; le badge "
        "facilite l'identification visuelle par le gardien ou le responsable RH "
        "et accélère certaines opérations administratives (attribution de "
        "matériel, accès parking)."
    )

    add_body(doc,
        "Au sein de la CNSS, cette combinaison répond à une problématique "
        "concrète observée en stage : des pointages manuscrits parfois signés "
        "par un collègue. L'empreinte rend ce contournement nettement plus "
        "difficile ; la carte RFID, quant à elle, permet au service RH "
        "d'identifier rapidement un agent dans les locaux et de vérifier "
        "que son profil système est actif."
    )

    add_subheading(doc, "I.5.5. Aspects éthiques et protection des données biométriques")

    add_body(doc,
        "Le traitement de données biométriques soulève des questions éthiques "
        "et juridiques. En Europe, le RGPD classe les données biométriques "
        "parmi les catégories sensibles ; en République Démocratique du Congo, "
        "le cadre légal spécifique reste en cours de consolidation, mais le "
        "principe de consentement éclairé et de finalité limitée s'impose "
        "déjà comme bonne pratique."
    )

    add_body(doc,
        "Dans le prototype SGRH Pro, plusieurs mesures techniques limitent "
        "les risques : stockage des templates chiffrés et non des images "
        "brutes ; accès réservé aux profils Admin RH pour l'enrôlement ; "
        "journal d'audit des opérations biométriques ; possibilité de "
        "désactiver une carte sans supprimer le dossier agent. Le déploiement "
        "institutionnel à grande échelle nécessiterait, au-delà de ce mémoire, "
        "une validation juridique formelle et une politique interne de "
        "protection des données."
    )

    add_subheading(doc, "I.5.6. Processus théorique d'enrôlement et de pointage")

    add_body(doc,
        "Le schéma logique du processus biométrique dans SGRH Pro, tel qu'il "
        "sera modélisé au chapitre III, comporte les étapes suivantes :"
    )

    add_numbered_item(doc, 1,
        " création du dossier agent dans le SIGRH (identité, matricule, service) ;")
    add_numbered_item(doc, 2,
        " lancement de l'enrôlement depuis l'interface Admin RH ;")
    add_numbered_item(doc, 3,
        " demande de lecture adressée au service biométrique du poste RH ;")
    add_numbered_item(doc, 4,
        " capture de l'empreinte par le ZK-9500 ;")
    add_numbered_item(doc, 5,
        " enregistrement du modèle d'empreinte dans le dossier de l'agent ;")
    add_numbered_item(doc, 6,
        " attribution optionnelle d'une carte RFID liée au matricule ;")
    add_numbered_item(doc, 7,
        " pointage quotidien : premier scan du jour = entrée, second scan = sortie "
        "(empreinte identifiée en 1:N ou carte RFID), puis clôture de la journée.")

    add_body(doc,
        "Ce processus garantit une chaîne de confiance : seul un agent préalablement "
        "enregistré dans le système peut être enrôlé ; seul un template enregistré "
        "peut produire un pointage valide. Les tentatives de scan sans correspondance "
        "sont rejetées et peuvent, dans une version ultérieure, déclencher une "
        "alerte de sécurité."
    )

    add_figure(
        doc, _fig("fig_i3_flux_biometrique.png"),
        "Figure 8 : Processus d'enrôlement biométrique et de pointage dans SGRH Pro",
        width_cm=15.8,
    )

    add_body(doc,
        "La figure I.8 synthétise le processus opérationnel retenu à la CNSS : "
        "l'enrôlement biométrique n'intervient qu'après la création du dossier "
        "administratif, sous le contrôle d'un agent RH habilité. Le bridge local "
        "assure l'interface avec le SDK du ZK-9500 sans exposer le poste de capture "
        "sur le réseau institutionnel. La carte RFID complète l'identification pour "
        "les agents dont l'empreinte est difficilement lisible ou en cas de "
        "défaillance ponctuelle du capteur. Chaque pointage horodaté alimente "
        "directement le module présences du logiciel, évitant toute ressaisie "
        "en fin de mois."
    )

    # ───────────────── I.6 Solutions ─────────────────
    add_heading(doc, "I.6. Revue des solutions existantes")

    add_subheading(doc, "I.6.1. Solutions internationales et open source")

    add_body(doc,
        "Le marché des SIGRH propose des suites cloud matures "
        "(SAP SuccessFactors, Oracle HCM, Workday, Microsoft Dynamics 365 HR) "
        "ainsi que des alternatives open source (Odoo RH, OrangeHRM, Dolibarr). "
        "Ces outils constituent des références de l'état de l'art, mais leur "
        "adoption directe à la CNSS se heurte au coût des licences, à la "
        "complexité du paramétrage, à la dépendance réseau et à l'adaptation "
        "incomplète au contexte administratif congolais."
    )

    add_body(doc,
        "Odoo RH, souvent cité comme alternative accessible, couvre congés "
        "et évaluation, mais n'offre ni localisation CNSS/IRG prête à l'emploi "
        "ni connecteur natif pour le ZK-9500. Une personnalisation poussée "
        "revient alors à un effort comparable au développement de SGRH Pro, "
        "avec moins de maîtrise sur le pointage biométrique et les états "
        "administratifs destinés à la finance."
    )

    add_subheading(doc, "I.6.2. Contexte africain et congolais")

    add_body(doc,
        "En Afrique, plusieurs pays ont lancé des initiatives de digitalisation "
        "RH dans la fonction publique (Ghana, Rwanda, Sénégal), avec des "
        "résultats contrastés selon le degré d'accompagnement au changement. "
        "En RDC, l'informatisation des grandes institutions (banques, "
        "télécoms, établissements publics) progresse par vagues successives, "
        "souvent initiées par des projets ponctuels plutôt que par une "
        "stratégie nationale unifiée."
    )

    add_body(doc,
        "La CNSS, dans cette configuration, représente un cas d'étude pertinent : "
        "organisation de taille significative, missions sensibles, personnel "
        "administratif structuré en directions et services, et besoin avéré "
        "de modernisation interne constaté durant le stage. L'absence, à ce "
        "jour, d'un SIGRH intégré avec biométrie au siège central justifie "
        "le développement d'une solution contextualisée plutôt que l'import "
        "direct d'un produit conçu pour un autre environnement."
    )

    add_body(doc,
        "Il convient également de mentionner les initiatives régionales de "
        "digitalisation des ressources humaines dans la fonction publique : "
        "certains pays d'Afrique de l'Est ont expérimenté des registres "
        "biométriques de fonctionnaires couplés à des systèmes de paie "
        "centralisés. Ces expériences montrent que la réussite dépend moins "
        "du choix de la marque du lecteur d'empreintes que de la qualité "
        "de l'intégration logicielle et de l'adhésion des utilisateurs finaux. "
        "C'est précisément sur cette intégration — application web, "
        "dashboard web — que porte le cœur technique du présent mémoire."
    )

    add_subheading(doc, "I.6.4. Analyse comparative")

    add_table(doc,
              ["Solution", "Type", "Biométrie native", "Adaptabilité RDC", "Coût"],
              [
                  ["SAP SuccessFactors", "Cloud propriétaire", "Via partenaires", "Faible", "Élevé"],
                  ["Oracle HCM", "Cloud propriétaire", "Via intégration", "Faible", "Élevé"],
                  ["Odoo RH", "Open core", "Modules tiers", "Moyenne", "Modéré"],
                  ["OrangeHRM", "Open source", "Plugins", "Moyenne", "Faible"],
                  ["SGRH Pro (projet)", "Sur mesure", "ZK-9500 + RFID", "Élevée", "Maîtrisé"],
              ],
              "Tableau 6 : Comparatif des solutions SIGRH et positionnement de SGRH Pro")

    add_body(doc,
        "Le tableau I.2 met en évidence que les suites internationales, bien que "
        "matures, ne répondent pas optimalement aux contraintes de coût, "
        "d'adaptation légale et d'intégration biométrique locale. SGRH Pro se "
        "positionne comme une alternative sur mesure, développée en connaissance "
        "du contexte CNSS et hébergeable sur infrastructure locale ou VPS accessible "
        "depuis Kinshasa."
    )

    add_subheading(doc, "I.6.5. Critères de sélection d'une solution SIGRH")

    add_body(doc,
        "La décision de développer une solution sur mesure plutôt que d'acquérir "
        "un progiciel s'appuie sur une grille multicritères. Les pondérations "
        "reflètent les priorités identifiées avec la DRH lors du stage."
    )

    add_table(doc,
              ["Critère", "Poids", "Suite internationale", "Open source", "SGRH Pro"],
              [
                  ["Coût total de possession", "25 %", "Faible", "Moyen", "Élevé"],
                  ["Adaptation contexte RDC", "20 %", "Faible", "Moyen", "Élevé"],
                  ["Intégration biométrique", "20 %", "Faible", "Faible", "Élevé"],
                  ["Maîtrise du code source", "15 %", "Nulle", "Élevée", "Élevée"],
                  ["Formation utilisateurs", "10 %", "Moyenne", "Moyenne", "Élevée"],
                  ["Évolutivité fonctionnelle", "10 %", "Élevée", "Moyenne", "Élevée"],
              ],
              "Tableau 7 : Grille multicritères de sélection (échelle qualitative)")

    # ───────────────── I.7 Limites ─────────────────
    add_heading(doc, "I.7. Limites des systèmes traditionnels de gestion RH")

    add_body(doc,
        "Avant l'introduction d'un SIGRH, la CNSS s'appuie encore largement "
        "sur un mode semi-manuel : dossiers papier, fichiers Excel non "
        "synchronisés, pointage par signature. Cette architecture d'information "
        "génère dispersion des données, absence de traçabilité, pointage "
        "contestable, lenteur décisionnelle et files d'attente au guichet RH "
        "(Mayo, 2019). Le tableau I.5 résume ces dysfonctionnements et les "
        "réponses apportées par SGRH Pro."
    )

    add_table(doc,
              ["Dysfonctionnement observé", "Conséquence", "Réponse SGRH Pro"],
              [
                  ["Registres papier + Excel", "Doublons, versions divergentes", "Base unique centralisée"],
                  ["Pointage manuel", "Fraudes, horaires imprécis", "Biométrie ZK-9500"],
                  ["Congés sur papier", "Retards, soldes erronés", "Workflow en ligne + soldes auto"],
                  ["Transmission manuelle", "Erreurs, retards administratifs", "Export automatisé PDF/CSV"],
                  ["Absence de KPI / évaluation", "Décisions tardives", "Dashboard + module évaluation"],
                  ["Pas d'espace agent", "Files au guichet RH", "Portail self-service"],
                  ["Pas d'audit", "Responsabilités floues", "Journal d'activité"],
              ],
              "Tableau 8 : Dysfonctionnements CNSS et réponses du système proposé")

    # ───────────────── I.8 UML ─────────────────
    add_heading(doc, "I.8. Modélisation UML et architectures logicielles")

    add_subheading(doc, "I.8.1. Le langage UML")

    add_mixed(doc, [
        ("L'", False, False),
        ("Unified Modeling Language (UML)", True, False),
        (" est un langage de modélisation graphique normalisé par l'OMG (Object "
         "Management Group), devenu la référence pour la conception orientée objet "
         "de systèmes logiciels (Larman, 2019 ; Booch, Rumbaugh et Jacobson, 2005). "
         "Il ne s'agit pas d'une méthode de développement en soi, mais d'un "
         "vocabulaire visuel partagé entre analystes, développeurs et encadrants.",
         False, False),
    ])

    add_body(doc,
        "Dans le cadre de ce mémoire, les diagrammes UML suivants seront produits "
        "au chapitre III :"
    )

    add_numbered_item(doc, 1,
        " diagramme de cas d'utilisation — interactions Admin RH, Manager, "
        "Agent, Système biométrique ;")
    add_numbered_item(doc, 2,
        " diagramme de classes — entités Employee, User, Attendance, RemunerationElement, "
        "Leave, Evaluation, BiometricDevice ;")
    add_numbered_item(doc, 3,
        " diagrammes de séquence — scénarios d'enrôlement, pointage, validation "
        "de congé, consolidation administrative ;")
    add_numbered_item(doc, 4,
        " diagramme d'activités — workflow de demande de congé ;")
    add_numbered_item(doc, 5,
        " diagramme de déploiement — serveur backend, poste RH, bridge "
        "biométrique, lecteur ZK-9500.")

    add_body(doc,
        "Ces modèles servent à valider la cohérence fonctionnelle avant l'écriture "
        "du code et à documenter le système pour la validation du prototype."
    )

    add_table(doc,
              ["Diagramme UML", "Objectif", "Usage dans SGRH Pro"],
              [
                  ["Cas d'utilisation", "Fonctionnalités vues par les acteurs",
                   "Admin RH, Manager, Agent, Bridge"],
                  ["Classes", "Structure statique des entités",
                   "Employee, User, Attendance, Leave, Evaluation"],
                  ["Séquence", "Ordre chronologique des interactions",
                   "Enrôlement, pointage, validation congé"],
                  ["Activités", "Workflow et branchements",
                   "Circuit de demande de congé"],
                  ["Déploiement", "Topologie matérielle et logicielle",
                   "Serveur, poste RH, ZK-9500, bridge C#"],
              ],
              "Tableau 9 : Diagrammes UML prévus au chapitre III")

    add_body(doc,
        "Le diagramme de cas d'utilisation (Use Case Diagram) représente les "
        "acteurs externes — Admin RH, Manager, Agent, Bridge biométrique — "
        "et les fonctionnalités qu'ils déclenchent. Il répond à la question : "
        "« Que fait le système du point de vue de l'utilisateur ? » Le diagramme "
        "de classes modélise la structure statique : entités, attributs, "
        "associations et cardinalités. Le diagramme de séquence illustre, pour "
        "un scénario donné, l'ordre chronologique des messages échangés entre "
        "objets — par exemple l'enchaînement Agent → interface → application "
        "→ lecteur ZK-9500 → base de données lors d'un enrôlement."
    )

    add_subheading(doc, "I.8.2. Architecture en couches et séparation backend / frontend")

    add_body(doc,
        "L'architecture retenue pour SGRH Pro suit le modèle en trois couches "
        "classique des applications web modernes (Fowler, 2022) :"
    )

    add_numbered_item(doc, 1,
        " couche de présentation — écrans consultés par le navigateur "
        "(connexion, tableaux de bord, formulaires) ;")
    add_numbered_item(doc, 2,
        " couche métier — règles de gestion (présences, congés, droits d'accès) ;")
    add_numbered_item(doc, 3,
        " couche de persistance — base de données relationnelle conservant "
        "dossiers, pointages et historiques.")

    add_body(doc,
        "La séparation backend/frontend présente plusieurs avantages pour le "
        "projet : développement parallèle des deux parties ; possibilité "
        "de remplacer l'interface web par une application mobile ultérieure "
        "sans modifier l'API ; déploiement du serveur sur un VPS accessible "
        "depuis le réseau du siège CNSS tandis que le bridge biométrique "
        "reste sur le poste Windows connecté au ZK-9500."
    )

    add_figure(
        doc, _fig("fig_i2_architecture_sgrh_pro.png"),
        "Figure 9 : Architecture globale du système SGRH Pro",
        width_cm=15.8,
    )

    add_subheading(doc, "I.8.3. Principes d'architecture retenus")

    add_table(doc,
              ["Principe", "Justification"],
              [
                  ["Séparation des couches", "Présentation, métier et données restent distincts"],
                  ["Application web", "Accès depuis un navigateur, sans installation lourde"],
                  ["Base relationnelle", "Intégrité des dossiers et historique des présences"],
                  ["Lecteur local Windows", "Le ZK-9500 reste branché sur le poste de pointage"],
                  ["Droits par rôle", "Chaque profil ne voit que ce qui le concerne"],
              ],
              "Tableau 10 : Principes d'architecture de SGRH Pro")

    add_body(doc,
        "Les technologies concrètes (langage, cadre applicatif, moteur de "
        "base de données, service biométrique) sont détaillées aux chapitres "
        "III et IV, lorsqu'il s'agit de concevoir et d'implémenter le "
        "prototype. Le présent chapitre se limite aux principes, afin de "
        "ne pas confondre le cadre théorique avec les choix d'implémentation."
    )

    # ───────────────── I.9 Conclusion ─────────────────
    add_heading(doc, "I.9. Conclusion du chapitre")

    add_body(doc,
        "Ce premier chapitre a posé les fondements théoriques sur lesquels "
        "s'appuie l'ensemble du mémoire. Il a permis de définir la GRH et "
        "le SIGRH, de clarifier la dimension « intelligente » retenue pour "
        "SGRH Pro (KPI, alertes, aide à la décision), d'examiner les technologies "
        "d'identification biométrique et RFID avec le lecteur ZK-9500, "
        "de comparer les solutions existantes et de montrer les limites des "
        "pratiques manuelles encore en usage à la CNSS."
    )

    add_body(doc,
        "Sur le plan méthodologique, ce chapitre a mobilisé neuf figures "
        "et plusieurs tableaux pour structurer la revue de littérature et "
        "l'état de l'art — schémas d'architecture, comparatifs de solutions, "
        "matrices de processus et grilles de sélection. Cette richesse "
        "documentaire vise à démontrer que le projet SGRH Pro ne procède "
        "pas d'un choix technique arbitraire, mais d'une analyse "
        "argumentée des alternatives disponibles et des contraintes "
        "institutionnelles congolaises."
    )

    add_body(doc,
        "La modélisation UML et l'architecture backend/frontend ont été présentées "
        "comme le cadre méthodologique de la conception. Le chapitre suivant "
        "appliquera ces repères au terrain : il analysera le système actuel "
        "de gestion RH au siège central de la CNSS, formalisera les besoins "
        "des acteurs et définira le cahier des charges des huit modules "
        "fonctionnels du système SGRH Pro."
    )

    return page_start


def build():
    doc = init_document()
    append_chapitre1(doc, PAGE_START)
    out = OUTPUT
    try:
        doc.save(out)
    except PermissionError:
        out = OUTPUT_FALLBACK
        doc.save(out)
        print("Note : fichier original ouvert dans Word — sauvegardé sous v2")
    words = sum(len(p.text.split()) for p in doc.paragraphs)
    print(f"Chapitre I généré : {out}")
    print(f"Mots approximatifs : {words}")


if __name__ == "__main__":
    build()

# -*- coding: utf-8 -*-
"""Génère le Chapitre II — Analyse du système actuel et spécification des besoins."""
from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH

from memoire_format import (
    init_document, add_page_number, add_chapter_title, add_heading, add_subheading,
    add_body, add_mixed, add_bullet, add_numbered_item, add_objectives_list, add_table,
    add_figure,
)

OUTPUT = r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\CHAPITRE II - ANALYSE ET SPECIFICATION DES BESOINS.docx"
OUTPUT_FALLBACK = OUTPUT.replace(".docx", " - v2.docx")
IMG_DIR = Path(r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\images\chapitre2")
PLANNING_DIR = Path(r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\images\planification")
PAGE_START = 38


def _fig(name: str) -> str:
    return str(IMG_DIR / name)


def _fig_planning(name: str) -> str:
    return str(PLANNING_DIR / name)


def _ensure_figures():
    import generate_figures_ch2
    import generate_figures_planning
    generate_figures_ch2.main()
    generate_figures_planning.main()


def append_chapitre2(doc, page_start=38):
    _ensure_figures()
    add_page_number(doc, page_start)
    add_chapter_title(doc, "CHAPITRE II. ANALYSE DU SYSTÈME ACTUEL ET SPÉCIFICATION DES BESOINS")

    # ───────────────── II.1 ─────────────────
    add_heading(doc, "II.1. Introduction")

    add_body(doc,
        "Le chapitre précédent a posé le cadre théorique : définitions de la GRH, "
        "architecture d'un SIGRH, principes biométriques et limites des pratiques "
        "manuelles. Il reste désormais à descendre sur le terrain — celui du siège "
        "central de la Caisse Nationale de Sécurité Sociale (CNSS) en République "
        "Démocratique du Congo — pour comprendre comment la gestion du personnel "
        "s'organise réellement, où se situent les dysfonctionnements et quelles "
        "exigences doit satisfaire le système SGRH Pro."
    )

    add_body(doc,
        "Ce chapitre répond à la deuxième question de recherche formulée dans "
        "l'introduction : quels sont les besoins fonctionnels et techniques d'un "
        "SIGRH intégrant biométrie et RFID au sein de la CNSS ? Pour y répondre, "
        "nous procédons en quatre temps complémentaires : présentation institutionnelle, "
        "diagnostic du système actuel, analyse des besoins par acteur, puis "
        "formalisation des spécifications et du cahier des charges."
    )

    add_body(doc, "La démarche d'analyse repose sur trois techniques de collecte :")

    add_bullet(doc, " l'observation participante au sein du service des ressources humaines "
               "du siège central, durant la période de stage ;")
    add_bullet(doc, " des entretiens semi-directifs menés auprès du responsable RH, "
               "de deux gestionnaires du personnel et de trois agents de différents "
               "services ;")
    add_bullet(doc, " l'analyse documentaire de registres de pointage, de fichiers "
               "Excel de suivi du personnel et de procédures internes mises à disposition "
               "par l'institution.")

    add_body(doc,
        "Les données sensibles (noms complets, données personnelles sensibles) ont été "
        "anonymisées dans le présent exposé. Les constats et chiffres agrégés "
        "proviennent néanmoins de la réalité observée sur le terrain et fondent "
        "directement les choix de conception développés aux chapitres III et IV."
    )

    add_body(doc,
        "Ce chapitre s'organise en dix sections. Les sections II.2 et II.3 "
        "dressent le portrait institutionnel et le diagnostic du « système "
        "existant », au sens de la méthode d'analyse structurée des systèmes "
        "d'information (ASSI). Les sections II.4 et II.5 traduisent les "
        "dysfonctionnements en besoins et en scénarios opérationnels. Les "
        "sections II.6 à II.8 constituent le livrable principal : spécification "
        "fonctionnelle, contraintes techniques et cahier des charges formalisé. "
        "La section II.9 planifie le projet ; la section II.10 en conclut."
    )

    add_table(doc,
              ["Phase", "Technique", "Durée estimée", "Livrable"],
              [
                  ["Exploration", "Observation participante DRH", "4 semaines",
                   "Notes de terrain, inventaire outils"],
                  ["Investigation", "Entretiens semi-directifs (6 personnes)", "2 semaines",
                   "Grilles d'entretien, verbatim synthétisés"],
                  ["Analyse", "Analyse documentaire", "1 semaine",
                   "Cartographie processus, tableau dysfonctionnements"],
                  ["Spécification", "Atelier de validation avec responsable RH", "3 jours",
                   "Cahier des charges validé"],
              ],
              caption="Tableau 11 : Démarche de collecte et d'analyse des besoins",
              col_widths=[2.6, 5.2, 2.8, 5.4])

    # ───────────────── II.2 CNSS ─────────────────
    add_heading(doc, "II.2. Présentation institutionnelle de la CNSS (RDC)")

    add_subheading(doc, "II.2.1. Historique et missions")

    add_mixed(doc, [
        ("La ", False, False),
        ("Caisse Nationale de Sécurité Sociale (CNSS)", True, False),
        (" de la République Démocratique du Congo est l'institution publique "
         "chargée de l'organisation et de la gestion du régime général de sécurité "
         "sociale. Créée par la loi n° 67-009 du 28 janvier 1967, elle assure la "
         "couverture des risques professionnels, maladie, maternité, invalidité, "
         "vieillesse et décès pour les travailleurs du secteur formel.", False, False),
    ])

    add_body(doc,
        "Au-delà de sa mission sociale, la CNSS emploie un personnel nombreux "
        "(agents administratifs, comptables, informaticiens, juristes). La gestion "
        "interne de ce capital humain — affectation, rémunération, discipline, "
        "évaluation — relève de la DRH et constitue le périmètre exclusif du "
        "présent mémoire, distinct de la gestion des cotisations et prestations."
    )

    add_subheading(doc, "II.2.2. Organisation du siège central")

    add_body(doc,
        "Le siège central de la CNSS est établi à Kinshasa, dans la commune de "
        "la Gombe. Il concentre les directions transversales et les directions "
        "métier qui pilotent l'activité au plan national. L'organigramme simplifié "
        "retenu pour l'analyse met en évidence la place de la DRH au sein de "
        "l'appareil administratif central."
    )

    add_body(doc,
        "La structure retenue distingue la Direction générale, les directions "
        "transversales (dont la DRH), les bureaux fonctionnels RH "
        "(gestion du personnel, administration et transmission, discipline) "
        "et le personnel opérationnel. Cette organisation oriente la "
        "modélisation des rôles dans SGRH Pro."
    )

    add_figure(
        doc, _fig("fig_ii1_organigramme_cnss.png"),
        "Figure 10 : Organigramme simplifié du siège central CNSS (focus DRH)",
        width_cm=15.8,
    )

    add_body(doc,
        "La DRH concentre les dossiers agents, les présences et la transmission "
        "des états à la direction financière. Elle emploie une quinzaine de "
        "personnes au siège, auxquelles s'ajoutent les responsables de service."
    )

    add_subheading(doc, "II.2.3. Effectif et enjeux de la DRH")

    add_body(doc,
        "Le siège central emploie environ 350 agents (permanents ≈ 75 %, "
        "CDD ≈ 15 %, stagiaires ≈ 10 %). La DRH traite au quotidien "
        "attestations, absences, mutations et états pour la finance ; "
        "sans outil intégré, chaque requête mobilise des recherches "
        "dans des classeurs et Excel, allongeant les délais. En tant "
        "qu'institution publique soumise à audits et contrôles, la CNSS "
        "a besoin de données RH fiables : SGRH Pro vise précisément "
        "ce levier de modernisation."
    )

    # ───────────────── II.3 Système actuel ─────────────────
    add_heading(doc, "II.3. Analyse du système actuel de gestion RH")

    add_subheading(doc, "II.3.1. Processus actuels de gestion du personnel")

    add_body(doc,
        "La gestion du personnel au siège central repose sur une combinaison "
        "de procédures écrites — héritées de circulaires administratives — et "
        "de pratiques informelles adaptées aux contraintes quotidiennes. Le "
        "cycle de vie d'un agent, de son recrutement à son archivage, traverse "
        "plusieurs supports non connectés entre eux."
    )

    add_body(doc,
        "La chaîne actuelle peut se résumer ainsi : registre papier de pointage → "
        "fichier Excel des effectifs → consolidation manuelle des éléments "
        "administratifs → impression d'attestations ou d'états → archivage "
        "physique. Entre chaque étape, aucune liaison automatique n'existe : "
        "les données sont ressaisies, ce qui multiplie les erreurs et empêche "
        "toute source unique de vérité — constat documenté dans la littérature "
        "sur l'informatisation des administrations publiques africaines "
        "(Ndiaye et Diop, 2021 ; Beaudoin et Roy, 2019)."
    )

    add_figure(
        doc, _fig("fig_ii2_processus_actuel.png"),
        "Figure 11 : Chaîne documentaire fragmentée du système actuel",
        width_cm=15.8,
    )

    add_body(doc,
        "Lors de l'arrivée d'un nouvel agent, un dossier papier est constitué "
        "(acte de nomination ou contrat, pièces d'état civil, formulaire de "
        "renseignements). Ce dossier est classé dans un armoire du bureau gestion "
        "du personnel. Une ligne est ajoutée manuellement dans un fichier Excel "
        "« effectifs » partagé sur un ordinateur du service. Le matricule est "
        "attribué selon une nomenclature interne, mais aucun contrôle automatique "
        "n'empêche les doublons."
    )

    add_body(doc,
        "Les mouvements (mutation interne, promotion, suspension) font l'objet "
        "d'une note de service papier, parfois retranscrite tardivement dans "
        "Excel. Le bureau chargé de la transmission administrative dispose "
        "de son propre fichier pour les éléments variables ; la cohérence "
        "avec le fichier effectifs est vérifiée manuellement avant envoi "
        "à la direction financière — une source récurrente d'erreurs signalée "
        "lors des entretiens."
    )

    add_subheading(doc, "II.3.2. Outils utilisés")

    add_body(doc,
        "L'inventaire des outils a été réalisé lors des deux premières "
        "semaines de stage, en parcourant les postes de travail des "
        "quatre bureaux de la DRH et en interrogeant les utilisateurs "
        "sur leurs pratiques réelles — parfois différentes des procédures "
        "officielles. Il en ressort une palette limitée et vieillissante."
    )

    add_table(doc,
              ["Outil", "Usage principal", "Limites identifiées"],
              [
                  ["Registres papier", "Pointage, demandes de congé, correspondance",
                   "Risque de perte, falsification, consultation difficile"],
                  ["Microsoft Excel", "Effectifs, éléments administratifs de rémunération, soldes congés",
                   "Pas de contrôle d'accès fin, versions multiples, pas d'audit"],
                  ["Ancien logiciel interne", "Consultation partielle des agents",
                   "Obsolète, non maintenu, sans module éléments de rémunération ni pointage"],
                  ["Traitement de texte / imprimante", "Attestations, notes de service",
                   "Production lente, mise en page manuelle"],
                  ["Classeurs physiques", "Archivage dossiers, contrats",
                   "Encombrement, recherche chronophage"],
              ],
              caption="Tableau 12 : Outils actuels de gestion RH à la CNSS",
              col_widths=[3.2, 4.8, 8.0])

    add_body(doc,
        "L'entretien mené avec le responsable RH a confirmé que le fichier Excel "
        "principal n'a pas de verrouillage par cellule : plusieurs agents du "
        "service peuvent le modifier simultanément, sans historique des changements. "
        "L'ancien logiciel — dont le nom n'est plus affiché dans les menus — "
        "permet encore une consultation limitée des fiches, mais il n'est plus "
        "alimenté depuis plusieurs années."
    )

    add_body(doc,
        "Un gestionnaire du personnel a indiqué lors de l'entretien qu'il "
        "maintient « une version personnelle » du fichier effectifs sur "
        "clé USB, par crainte de corruption du fichier réseau partagé. "
        "Cette pratique — compréhensible au regard des coupures électriques "
        "fréquentes — multiplie les versions divergentes et rend illusoire "
        "toute tentative de consolidation en l'état."
    )

    add_subheading(doc, "II.3.3. Gestion actuelle des présences et pointage")

    add_body(doc,
        "Le pointage repose sur un registre papier tenu à l'accueil du bâtiment "
        "administratif. Chaque matin, l'agent signe à la main son heure d'arrivée ; "
        "le départ en fin de journée est parfois oublié. En fin de mois, un agent "
        "du bureau gestion du personnel relève manuellement les signatures, calcule "
        "les retards à l'œil nu et consolide les données dans Excel."
    )

    add_body(doc,
        "Le dispositif cible repose sur SGRH Pro : l'agent pointe via le module "
        "logiciel de présences (alimenté par empreinte digitale ou carte RFID) ; "
        "les horaires sont enregistrés automatiquement en base ; les retards et "
        "absences sont calculés par les services métier du backend ; le "
        "responsable RH consulte un tableau de bord web actualisé. Le matériel "
        "biométrique n'est qu'une porte d'entrée des données : la valeur ajoutée "
        "réside dans le traitement, la consolidation et la restitution assurés "
        "par le logiciel."
    )

    add_figure(
        doc, _fig("fig_ii3_pointage_comparatif.png"),
        "Figure 12 : Comparaison entre pointage manuel et dispositif cible SGRH Pro",
        width_cm=15.8,
    )

    add_body(doc,
        "Les entretiens avec des agents opérationnels ont révélé plusieurs "
        "pratiques contournant le dispositif : signature par un collègue en "
        "cas de retard, inscription d'une heure arrondie, absence de relevé "
        "des sorties. Le responsable RH estime que le taux de fiabilité du "
        "registre « n'excède pas 60 à 70 % » — chiffre avoué lors de l'entretien "
        "mais non vérifiable statistiquement faute d'outil de mesure."
    )

    add_subheading(doc, "II.3.4. Gestion des congés et transmission administrative")

    add_body(doc,
        "Les demandes de congé se font sur un formulaire papier adressé au "
        "supérieur hiérarchique, puis au bureau RH. L'approbation est apposée "
        "par signature manuscrite. Le solde de congés est tenu dans une colonne "
        "Excel mise à jour après chaque demande — parfois avec retard. Aucun "
        "calendrier partagé n'existe : deux agents du même service peuvent "
        "obtenir un congé simultané faute de visibilité commune."
    )

    add_body(doc,
        "En institution publique, la rémunération des agents est versée par "
        "virement bancaire sous la responsabilité de la direction administrative "
        "et financière. Le rôle du service RH consiste à produire des états "
        "administratifs fiables — présences, absences, éléments variables, "
        "mouvements de personnel — et non à effectuer le paiement lui-même. "
        "Or, la consolidation de ces états repose encore sur des ressaisies "
        "Excel et des impressions Word. Le délai moyen observé entre la "
        "clôture du mois et la transmission à la finance est de huit à "
        "douze jours ouvrables, délai jugé excessif par les responsables "
        "interrogés."
    )

    add_body(doc,
        "SGRH Pro doit automatiser cette chaîne côté logiciel : les modules "
        "présences et congés alimentent le module éléments de rémunération, "
        "qui exporte un état consolidé (PDF/CSV) transmis à la direction "
        "financière pour le virement bancaire. Le logiciel ne calcule pas "
        "le salaire net ni ne gère les comptes bancaires ; il garantit "
        "l'intégrité et la traçabilité des données administratives."
    )

    add_subheading(doc, "II.3.5. Problèmes et dysfonctionnements identifiés")

    add_table(doc,
              ["N°", "Dysfonctionnement", "Cause principale", "Impact"],
              [
                  ["D1", "Doublons et incohérences dans les effectifs",
                   "Double saisie papier / Excel", "Erreurs administratives, sur-effectif fictif"],
                  ["D2", "Pointages peu fiables", "Registre papier contournable",
                   "Présence fictive, calcul retards impossible"],
                  ["D3", "Retards administratifs", "Saisies manuelles, ressaisies",
                   "Insatisfaction agents, tension sociale"],
                  ["D4", "Congés mal synchronisés", "Absence de workflow numérique",
                   "Chevauchements, soldes erronés"],
                  ["D5", "Évaluations non structurées", "Grilles papier, pas d'historique",
                   "Pilotage des performances difficile"],
                  ["D6", "Absence de traçabilité", "Pas de journal d'audit",
                   "Modifications de dossier non historisées"],
                  ["D7", "Reporting inexistant", "Données dispersées",
                   "Décisions RH sans indicateurs fiables"],
              ],
              caption="Tableau 13 : Synthèse des dysfonctionnements du système actuel",
              col_widths=[1.2, 4.2, 4.6, 6.0],
              col_align=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.JUSTIFY,
                         WD_ALIGN_PARAGRAPH.JUSTIFY, WD_ALIGN_PARAGRAPH.JUSTIFY])

    add_subheading(doc, "II.3.6. Analyse des fraudes et irrégularités de pointage")

    add_body(doc,
        "Les fraudes au pointage observées ou rapportées lors des entretiens "
        "relèvent moins de la malveillance organisée que de la permissivité "
        "structurelle du système. Trois formes principales ont été recensées :"
    )

    add_numbered_item(doc, 1, " la signature par procuration (un collègue signe pour un absent) ;")
    add_numbered_item(doc, 2, " l'inscription d'horaires arrondis ou anticipés ;")
    add_numbered_item(doc, 3, " l'absence de pointage de sortie, rendant impossible "
                      "le calcul des heures effectivement travaillées.")

    add_body(doc,
        "Ces pratiques persistent parce que le registre ne vérifie pas l'identité "
        "du signataire et qu'aucune corrélation n'est établie entre présence "
        "physique et éléments administratifs de rémunération en temps réel. L'introduction d'un "
        "capteur biométrique ZK-9500 vise précisément à lier l'identité "
        "biologique de l'agent à l'enregistrement horaire, en complément "
        "d'une carte RFID pour les opérations d'identification rapide."
    )

    add_subheading(doc, "II.3.7. Impacts sur la productivité et la prise de décision")

    add_body(doc,
        "Les dysfonctionnements recensés produisent des effets en cascade. "
        "Le temps consacré par la DRH à la ressaisie et à la vérification "
        "des données — estimé à environ 30 % de la charge hebdomadaire du "
        "bureau gestion du personnel lors de l'observation — est du temps soustrait à l'accompagnement "
        "des managers et à l'évaluation des performances. Les agents, de leur "
        "côté, perdent confiance dans l'équité du système lorsqu'ils constatent "
        "des lenteurs de traitement administratif ou des soldes de congés erronés."
    )

    add_body(doc,
        "Au niveau décisionnel, l'absence de tableau de bord empêche la "
        "direction de disposer d'indicateurs actualisés : effectif par service, "
        "taux d'absentéisme, effectif opérationnel mensuel, résultats "
        "d'évaluation. Les rapports demandés par la direction générale sont "
        "préparés manuellement, parfois sur plusieurs jours, à partir de "
        "fichiers hétérogènes."
    )

    add_subheading(doc, "II.3.8. Synthèse du diagnostic : forces et faiblesses")

    add_table(doc,
              ["Forces actuelles", "Faiblesses structurelles"],
              [
                  ["Connaissance métier RH des équipes", "Données dispersées sur supports hétérogènes"],
                  ["Procédures écrites de référence", "Absence d'intégration entre processus"],
                  ["Matricule agent reconnu institutionnellement", "Pointage non fiable et contournable"],
                  ["Volonté de direction de moderniser", "Logiciel legacy non maintenu"],
                  ["Personnel RH disponible pour conduite du changement",
                   "Pas de KPI pour piloter l'activité RH"],
              ],
              caption="Tableau 14 : Forces et faiblesses du système actuel",
              col_widths=[7.5, 8.5])

    add_body(doc,
        "Malgré les dysfonctionnements, le système actuel présente des "
        "atouts qu'il convient de préserver dans la solution cible. Les "
        "procédures papier, bien que lourdes, garantissent une culture "
        "de la trace écrite que le numérique devra reproduire via le "
        "journal d'audit. Les agents RH connaissent parfaitement les "
        "règles administratives internes — savoir-faire qui alimentera "
        "le paramétrage des modules logiciels de SGRH Pro."
    )

    # ───────────────── II.4 Besoins acteurs ─────────────────
    add_heading(doc, "II.4. Analyse des besoins des acteurs")

    add_body(doc,
        "L'analyse des besoins distingue quatre profils d'utilisateurs identifiés "
        "lors des entretiens et de l'observation. Chaque profil exprime des "
        "attentes différentes, mais convergent vers un système unique, intégré "
        "et traçable."
    )

    add_body(doc,
        "Du point de vue logiciel, quatre acteurs interagissent avec SGRH Pro : "
        "l'administrateur RH (gestion complète via l'interface web et l'API), "
        "le responsable de service (validation des congés, suivi d'équipe), "
        "l'agent (espace personnel), et les services techniques périphériques "
        "(bridge biométrique, capteur ZK-9500, lecteur RFID) qui alimentent "
        "le backend en événements horodatés. Le schéma de déploiement détaillé "
        "figure au chapitre III ; le présent chapitre formalise leurs besoins "
        "fonctionnels respectifs."
    )

    add_figure(
        doc, _fig("fig_ii6_acteurs_systeme.png"),
        "Figure 13 : Acteurs humains et composants techniques du système cible",
        width_cm=15.8,
    )

    add_subheading(doc, "II.4.1. Besoins des administrateurs RH")

    add_body(doc,
        "Les administrateurs RH demandent une source unique de vérité regroupant "
        "dossiers, présences, évaluations et éléments administratifs. Le responsable "
        "du bureau gestion du personnel a exprimé le souhait de « produire les états "
        "de présence en deux jours au lieu de dix » grâce à une consolidation "
        "automatique par le logiciel. Le gestionnaire du personnel souhaite "
        "disposer d'une recherche instantanée par matricule ou nom, plutôt que "
        "de parcourir des classeurs. Leurs besoins prioritaires sont :"
    )

    add_bullet(doc, " créer et maintenir les dossiers agents avec matricule unique ;")
    add_bullet(doc, " produire automatiquement les états administratifs transmis "
               "à la direction financière (présences, variables) ;")
    add_bullet(doc, " superviser les pointages enregistrés par le logiciel et corriger les anomalies ;")
    add_bullet(doc, " valider les demandes de congé et suivre les soldes ;")
    add_bullet(doc, " disposer d'un tableau de bord (effectifs, absentéisme, congés en attente) ;")
    add_bullet(doc, " tracer toute modification sensible (dossier, rôle, suppression) "
               "dans un journal d'audit.")

    add_subheading(doc, "II.4.2. Besoins des responsables de service")

    add_body(doc,
        "Les responsables de service — chefs de bureau ou de direction — "
        "interviennent dans la validation des congés et le suivi de leur "
        "équipe. Lors des entretiens, un chef de bureau a indiqué ne "
        "« découvrir les absences qu'au moment de la signature du registre "
        "mensuel », faute de visibilité en temps réel. Ils ne doivent pas "
        "accéder aux données globales de rémunération, mais nécessitent :"
    )

    add_bullet(doc, " visualiser les présences et absences de leur équipe ;")
    add_bullet(doc, " recevoir des alertes en cas de retard répété ou d'absence "
               "non justifiée ;")
    add_bullet(doc, " approuver ou refuser les demandes de congé avec commentaire ;")
    add_bullet(doc, " consulter les évaluations de leurs subordonnés.")

    add_subheading(doc, "II.4.3. Besoins des agents (espace personnel)")

    add_body(doc,
        "Les agents — personnel administratif et technique — aspirent à plus "
        "de transparence et d'autonomie. L'espace personnel doit leur permettre :"
    )

    add_bullet(doc, " consulter leurs relevés de présence, heures travaillées et retards ;")
    add_bullet(doc, " suivre leur assiduité du mois et leurs scores d'évaluation ;")
    add_bullet(doc, " soumettre une demande de congé et suivre son statut ;")
    add_bullet(doc, " visualiser leur solde de congés et l'historique des pointages ;")
    add_bullet(doc, " accéder à un tableau de bord personnel (graphiques d'heures et de retards).")

    add_body(doc,
        "Lors des entretiens, les agents ont insisté sur la consultation des "
        "documents administratifs en ligne : actuellement, ils doivent se déplacer physiquement "
        "au bureau RH, créant files d'attente et interruptions de travail."
    )

    add_subheading(doc, "II.4.4. Besoins en identification fiable (biométrie et RFID)")

    add_bullet(doc, " enregistrer l'empreinte digitale via le capteur ZK-9500 lors "
               "de l'intégration ;")
    add_bullet(doc, " attribuer une carte RFID liée au matricule ;")
    add_bullet(doc, " pointer à l'entrée et à la sortie par empreinte ou carte ;")
    add_bullet(doc, " horodater automatiquement chaque événement avec source tracée ;")
    add_bullet(doc, " désactiver une carte en cas de perte sans supprimer le dossier.")

    add_subheading(doc, "II.4.5. Besoins en reporting et tableaux de bord")

    add_table(doc,
              ["Indicateur", "Fréquence", "Destinataire"],
              [
                  ["Effectif total et par département", "Temps réel", "DRH, Direction"],
                  ["Taux de présence / absentéisme", "Hebdomadaire", "DRH, Responsables"],
                  ["Effectif opérationnel mensuel", "Mensuelle", "DRH, Direction financière"],
                  ["Congés en attente de validation", "Temps réel", "DRH, Responsables"],
                  ["Score moyen d'évaluation", "Trimestrielle", "DRH"],
                  ["Retards répétés (> 3/semaine)", "Quotidienne", "Responsables"],
              ],
              caption="Tableau 15 : Indicateurs demandés par les acteurs",
              col_widths=[4.8, 2.8, 8.4],
              col_align=[WD_ALIGN_PARAGRAPH.JUSTIFY, WD_ALIGN_PARAGRAPH.CENTER,
                         WD_ALIGN_PARAGRAPH.JUSTIFY])

    add_subheading(doc, "II.4.6. Matrice acteurs / besoins prioritaires")

    add_table(doc,
              ["Besoin", "Admin RH", "Responsable", "Agent"],
              [
                  ["Gestion dossiers agents", "●", "—", "—"],
                  ["Validation congés", "●", "●", "Demande"],
                  ["Pointage biométrique", "●", "Consultation", "●"],
                  ["Consultation relevés administratifs", "●", "—", "●"],
                  ["Tableau de bord KPI", "●", "Partiel", "—"],
                  ["Alertes absences / retards", "●", "●", "—"],
                  ["Journal d'audit", "●", "—", "—"],
                  ["Évaluations", "●", "●", "Consultation"],
              ],
              caption="Tableau 16 : Matrice acteurs / besoins (● = accès requis)",
              col_widths=[5.8, 3.4, 3.4, 3.4],
              col_align=[WD_ALIGN_PARAGRAPH.JUSTIFY, WD_ALIGN_PARAGRAPH.CENTER,
                         WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER])

    add_body(doc,
        "Cette matrice confirme que le modèle RBAC retenu — quatre rôles "
        "principaux avec permissions granulaires — répond aux attentes "
        "de séparation des tâches : un agent ne consulte que ses propres "
        "données ; un responsable accède à son équipe sans voir les données "
        "globales de rémunération ; l'administrateur RH conserve la vue "
        "institutionnelle complète."
    )

    # ───────────────── II.5 Scénarios ─────────────────
    add_heading(doc, "II.5. Scénarios d'utilisation")

    add_body(doc,
        "Les scénarios suivants traduisent les besoins en parcours concrets "
        "et serviront de base aux diagrammes UML (chapitre III) et aux tests "
        "(chapitre IV)."
    )

    add_subheading(doc, "II.5.1. Enrôlement biométrique et pointage")

    add_body(doc,
        "L'administrateur RH crée le dossier agent, lance l'enrôlement via "
        "le lecteur ZK-9500, puis associe une carte RFID. Le service de "
        "lecture est installé sur le poste Windows du terminal : il démarre "
        "avec la session et permet la capture d'empreinte ainsi que "
        "la reconnaissance parmi les agents enrôlés."
    )

    add_body(doc,
        "En exploitation, le pointage obéit à une règle unique, lisible pour "
        "l'accueil comme pour le jury : le premier scan du jour (empreinte "
        "ou RFID) enregistre l'arrivée ; le second enregistre la sortie et "
        "calcule les heures travaillées. Un troisième scan est rejeté : la "
        "journée est déjà clôturée. L'identification par empreinte compare "
        "le template capturé à la galerie des agents enrôlés (matching 1:N "
        "côté SDK ZK) ; la carte RFID n'est acceptée que si elle est active "
        "et rattachée à un matricule. Chaque événement est horodaté, sourcé "
        "(fingerprint / rfid) et visible en temps réel sur le terminal de "
        "présence et dans l'espace personnel de l'agent."
    )

    add_subheading(doc, "II.5.2. Congés, rémunération et évaluation")

    add_body(doc,
        "L'agent soumet une demande de congé ; le responsable donne son avis "
        "et l'Admin RH décide. En fin de mois, SGRH Pro consolide présences "
        "et éléments variables, puis exporte un état PDF/CSV pour la finance. "
        "Le responsable saisit une grille d'évaluation ; l'Admin RH consulte "
        "les KPI (effectif, absentéisme, évaluations) sur le tableau de bord."
    )

    add_figure(
        doc, _fig("fig_ii4_workflow_conge.png"),
        "Figure 14 : Workflow de validation d'une demande de congé",
        width_cm=15.8,
    )

    add_table(doc,
              ["Scénario", "Acteur", "Résultat attendu"],
              [
                  ["Enrôlement biométrique", "Admin RH", "Empreinte + RFID actifs"],
                  ["Pointage quotidien", "Agent", "Présence horodatée"],
                  ["Demande de congé", "Agent → RH", "Décision et solde mis à jour"],
                  ["État de rémunération", "Admin RH", "Export PDF/CSV pour la finance"],
                  ["Évaluation", "Responsable", "Grille enregistrée"],
                  ["Consultation KPI", "Admin RH", "Indicateurs et alertes"],
              ],
              caption="Tableau 17 : Scénarios d'utilisation prioritaires",
              col_widths=[4.5, 3.5, 8.0])

    # ───────────────── II.6 Modules ─────────────────
    add_heading(doc, "II.6. Spécification fonctionnelle — les huit modules")

    add_body(doc,
        "Sur la base du diagnostic, SGRH Pro est décomposé en huit modules "
        "recentrés sur les présences, la biométrie, l'évaluation et les "
        "éléments de rémunération. Les domaines secondaires (contrats, "
        "recrutement, formation, congés médicaux) sont exclus du périmètre. "
        "La figure II.6 et le tableau II.6 bis en donnent la synthèse."
    )

    add_figure(
        doc, _fig("fig_ii5_modules_sgrh_pro.png"),
        "Figure 15 : Architecture modulaire des huit composants de SGRH Pro",
        width_cm=15.8,
    )

    add_table(doc,
              ["Module", "Objectif", "Fonctions clés"],
              [
                  ["M1 Accès", "Authentification et droits", "Rôles, journal d'audit"],
                  ["M2 Employés", "Dossier RH centralisé", "Matricule, affectation, statut"],
                  ["M3 Biométrie", "Enrôlement ZK/RFID", "ZK-9500, cartes RFID"],
                  ["M4 Présences", "Pointage du jour", "Entrée/sortie, retards"],
                  ["M5 Congés", "Workflow de validation", "Demande, avis, décision RH"],
                  ["M6 Rémunération", "États pour la finance", "Variables, absences, export PDF/CSV"],
                  ["M7 Évaluation", "Performance du personnel", "Grille, scores, historique"],
                  ["M8 Rapports", "Pilotage RH", "KPI, graphiques personnalisables"],
              ],
              caption="Tableau 18 : Spécification synthétique des huit modules",
              col_widths=[3.2, 4.8, 8.0])

    add_body(doc,
        "Les huit modules partagent le même socle applicatif et la même "
        "base de données. M4 constitue le cœur opérationnel : le terminal de "
        "pointage alimente le registre des présences et l'espace agent. "
        "M6 respecte la règle institutionnelle : le logiciel "
        "produit des états, la finance exécute les virements bancaires. "
        "Ces modules répondent aux dysfonctionnements D1–D7 du tableau II.3."
    )

    add_subheading(doc, "II.6.1. Interdépendances entre modules")

    add_body(doc,
        "M1 est prérequis à tous ; M2 alimente M3–M8 ; M3 alimente M4 ; "
        "M4 alimente M6 et M8 ; M5 et M7 alimentent M8."
    )

    add_table(doc,
              ["Module", "Dépend de", "Alimente"],
              [
                  ["M3 Biométrie", "M1, M2", "M4 Présences"],
                  ["M4 Présences", "M2, M3", "M6 Rémunération, M8 Rapports"],
                  ["M5 Congés", "M1, M2", "M8 Rapports"],
                  ["M6 Rémunération", "M2, M4", "M8 Rapports, finance"],
                  ["M7 Évaluation", "M2", "M8 Rapports"],
                  ["M8 Rapports", "Tous", "Direction, DRH"],
              ],
              caption="Tableau 19 : Interdépendances principales entre modules",
              col_widths=[3.0, 4.5, 8.5])

    # ───────────────── II.7 Spécification technique ─────────────────
    add_heading(doc, "II.7. Spécification technique et contraintes")

    add_body(doc,
        "Les exigences techniques du chapitre II restent volontairement "
        "orientées besoins plutôt que produits. Le système doit être une "
        "application web consultable depuis le poste du responsable RH, "
        "s'appuyer sur une base de données relationnelle, garantir des "
        "accès différenciés selon les profils et relier le lecteur ZK-9500 "
        "ainsi que les cartes RFID au suivi des présences. L'espace agent "
        "restitue présences, heures, retards, évaluations et congés. "
        "Le tableau de bord RH doit permettre de choisir les indicateurs "
        "affichés. Les choix de réalisation (langages, hébergement, "
        "installateur du lecteur) sont détaillés aux chapitres III et IV."
    )

    add_table(doc,
              ["Catégorie", "Exigence", "Critère"],
              [
                  ["Performance", "Réponse de l'application < 2 s", "Consultation locale fluide"],
                  ["Sécurité", "Authentification + rôles + journal", "Aucun accès métier ouvert"],
                  ["Fiabilité", "Intégrité des pointages", "Source (empreinte/RFID) tracée"],
                  ["Utilisabilité", "Prise en main < 2 h", "Test utilisateur RH"],
              ],
              caption="Tableau 20 : Exigences non fonctionnelles (synthèse)",
              col_widths=[2.8, 5.5, 7.7])

    add_table(doc,
              ["Composant", "Orientation"],
              [
                  ["Application", "Interface web + traitements métier centralisés"],
                  ["Données", "Base relationnelle (prototype local / production hébergée)"],
                  ["Sécurité", "Comptes, rôles, journal d'activité"],
                  ["Biométrie", "Lecteur ZK-9500 et cartes RFID sur poste Windows"],
                  ["Restitution", "Tableaux de bord, espace agent, exports pour la finance"],
              ],
              caption="Tableau 21 : Orientations techniques (niveau cahier des charges)",
              col_widths=[4.0, 12.0])

    # ───────────────── II.8 Cahier des charges ─────────────────
    add_heading(doc, "II.8. Cahier des charges fonctionnel et technique")

    add_body(doc,
        "Le cahier des charges formalise les exigences du système SGRH Pro "
        "destiné à la CNSS. Il distingue exigences fonctionnelles (EF), "
        "exigences non fonctionnelles (ENF) et contraintes (C). Les "
        "priorités suivent la notation MoSCoW : M (Must), S (Should), "
        "C (Could)."
    )

    add_body(doc,
        "Le nom SGRH Pro — Système de Gestion des Ressources Humaines "
        "Professionnel — a été retenu pour désigner le prototype, afin "
        "de le distinguer à la fois de l'ancien logiciel interne et des "
        "solutions commerciales génériques étudiées au chapitre I. "
        "Il traduit l'ambition d'un outil métier complet, et non d'un simple "
        "module de pointage isolé."
    )

    add_subheading(doc, "II.8.1. Exigences fonctionnelles principales")

    add_table(doc,
              ["Réf.", "Exigence", "Priorité"],
              [
                  ["EF-01", "Authentifier un utilisateur par matricule et mot de passe", "M"],
                  ["EF-02", "Gérer les rôles et permissions (RBAC)", "M"],
                  ["EF-03", "CRUD complet des dossiers agents", "M"],
                  ["EF-04", "Enrôler une empreinte digitale via ZK-9500", "M"],
                  ["EF-05", "Attribuer et désactiver une carte RFID", "M"],
                  ["EF-06", "Enregistrer pointage entrée/sortie biométrique ou RFID", "M"],
                  ["EF-07", "Calculer heures travaillées et retards", "M"],
                  ["EF-08", "Soumettre et valider une demande de congé (workflow)", "M"],
                  ["EF-09", "Consolider les états administratifs mensuels (présences, variables)", "M"],
                  ["EF-10", "Générer un relevé administratif PDF", "M"],
                  ["EF-11", "Afficher tableau de bord KPI RH", "M"],
                  ["EF-12", "Émettre alertes (absences, congés en attente)", "S"],
                  ["EF-13", "Gérer les évaluations de performance", "M"],
                  ["EF-14", "Espace agent : consulter présences, congés, documents administratifs", "M"],
                  ["EF-15", "Journal d'audit exportable CSV/PDF", "S"],
                  ["EF-16", "Paramétrer horaires et seuils de retard", "S"],
              ],
              caption="Tableau 22 : Exigences fonctionnelles (extrait)",
              col_widths=[1.6, 11.8, 2.6],
              col_align=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.JUSTIFY,
                         WD_ALIGN_PARAGRAPH.CENTER])

    add_subheading(doc, "II.8.2. Contraintes techniques et institutionnelles")

    add_numbered_item(doc, 1, " C-01 : compatibilité Windows pour le Bridge biométrique (SDK ZKTeco) ;")
    add_numbered_item(doc, 2, " C-02 : pas de stockage des identifiants bancaires des agents ;")
    add_numbered_item(doc, 3, " C-03 : consentement éclairé pour la collecte d'empreintes digitales ;")
    add_numbered_item(doc, 4, " C-04 : hébergement des données sur le territoire ou serveur "
                      "institutionnel (pas de cloud public non maîtrisé) ;")
    add_numbered_item(doc, 5, " C-05 : interface en langue française ;")
    add_numbered_item(doc, 6, " C-06 : prototype démontrable sur un poste unique du responsable RH.")

    add_subheading(doc, "II.8.3. Périmètre hors scope")

    add_body(doc,
        "Les éléments suivants sont explicitement exclus du périmètre du "
        "présent mémoire, sans préjuger d'une extension ultérieure :"
    )

    add_bullet(doc, " gestion des assurés sociaux et des cotisations employeurs ;")
    add_bullet(doc, " virements bancaires automatiques et déclarations électroniques "
               "aux administrations fiscales ;")
    add_bullet(doc, " gestion des contrats, du recrutement, de la formation et "
               "des congés médicaux (hors périmètre recentré) ;")
    add_bullet(doc, " application mobile native (Android/iOS) ;")
    add_bullet(doc, " reconnaissance faciale ou autre modalité biométrique que "
               "l'empreinte digitale ;")
    add_bullet(doc, " déploiement multi-sites (agences provinciales).")

    add_body(doc,
        "Ce cahier des charges constitue le référentiel contractuel entre "
        "l'analyse et la conception : toute fonctionnalité implémentée aux "
        "chapitres III et IV doit pouvoir être rattachée à une exigence EF "
        "ou à un scénario d'utilisation décrit dans le présent chapitre."
    )

    add_subheading(doc, "II.8.4. Critères d'acceptation du prototype")

    add_body(doc,
        "Pour valider le prototype en fin de projet, les critères "
        "d'acceptation suivants ont été définis avec l'encadreur et le "
        "responsable RH :"
    )

    add_numbered_item(doc, 1, " enrôlement réel d'au moins un agent sur le ZK-9500 ;")
    add_numbered_item(doc, 2, " pointage entrée/sortie enregistré en base avec source biométrique ;")
    add_numbered_item(doc, 3, " production d'au moins un état administratif consolidé (présences + export) ;")
    add_numbered_item(doc, 4, " workflow complet d'une demande de congé (soumission → validation) ;")
    add_numbered_item(doc, 5, " affichage du tableau de bord KPI avec données réelles ou de démonstration ;")
    add_numbered_item(doc, 6, " connexion et navigation fonctionnelles pour les trois profils "
                      "(Admin RH, Responsable, Agent).")

    add_body(doc,
        "Ces critères seront vérifiés au chapitre IV à l'aide d'un protocole "
        "de tests fonctionnels reprenant les scénarios II.5 et les exigences "
        "EF du présent cahier des charges."
    )

    # ───────────────── II.9 Cadrage du projet ─────────────────
    add_heading(doc, "II.9. Cadrage et planification du projet")

    add_body(doc,
        "Au-delà des spécifications fonctionnelles, la réussite du projet SGRH Pro "
        "suppose une planification rigoureuse des activités, des délais et des "
        "ressources. Comme le recommandent les méthodes de gestion de projet "
        "(PMBOK, 2021 ; Hillier, 2019), le cadrage permet de visualiser les "
        "dépendances entre tâches, d'identifier le chemin critique et d'estimer "
        "le budget nécessaire au prototype. Cette section formalise la planification "
        "retenue pour la conception, le développement et la validation de SGRH Pro."
    )

    add_body(doc,
        "La démarche mobilise les outils classiques de l'analyse réseau : "
        "recensement et ordonnancement des tâches, graphe PERT/MPM, détermination "
        "du chemin critique, calendrier d'exécution, diagramme de Gantt et "
        "estimation budgétaire bottom-up. Les durées sont exprimées en jours "
        "ouvrés, sur une période totale de soixante-trois jours ouvrés correspondant au "
        "calendrier académique du mémoire (juillet – septembre 2026)."
    )

    add_subheading(doc, "II.9.1. Tableau de recensement des tâches")

    add_body(doc,
        "Le tableau II.10 recense les dix activités techniques du projet SGRH Pro "
        "identifiées lors de l'élaboration du cahier des charges, classées par "
        "ordre alphabétique de leur code (A à J). Seules les tâches "
        "liées à la conception, au développement, aux tests et au déploiement "
        "du système y figurent. Chaque tâche est décrite par son code, son intitulé, "
        "sa durée estimée et le livrable attendu."
    )

    add_table(doc,
              ["Code", "Tâche", "Durée (j)", "Livrable principal"],
              [
                  ["A", "Analyse du système actuel (stage CNSS)", "14",
                   "Diagnostic, tableau dysfonctionnements"],
                  ["B", "Spécification des besoins et cahier des charges", "6",
                   "Exigences EF, huit modules"],
                  ["C", "Conception UML et architecture logicielle", "9",
                   "Diagrammes cas d'usage, classes, déploiement"],
                  ["D", "Modélisation de la base de données", "3",
                   "MER, schéma relationnel"],
                  ["E", "Développement backend Laravel (API REST)", "13",
                   "Contrôleurs, services, routes Sanctum"],
                  ["F", "Développement frontend dashboard", "9",
                   "Interface Admin RH, Responsable, Agent"],
                  ["G", "Développement bridge biométrique C#", "6",
                   "Service headless, installateur one-touch Windows"],
                  ["H", "Intégration biométrie et RFID", "6",
                   "Enrôlement et pointage opérationnels"],
                  ["I", "Tests fonctionnels et corrections", "6",
                   "Protocole de tests, rapports"],
                  ["J", "Déploiement prototype poste RH", "3",
                   "Prototype installé et configuré"],
              ],
              caption="Tableau 23 : Recensement des tâches du projet SGRH Pro",
              col_widths=[1.2, 6.8, 2.0, 6.0],
              col_align=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.JUSTIFY,
                         WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.JUSTIFY])

    add_subheading(doc, "II.9.2. Tableau d'ordonnancement des tâches")

    add_body(doc,
        "L'ordonnancement précise, pour chaque tâche, ses prédécesseurs immédiats "
        "— tâches devant être achevées avant son démarrage. Cette matrice constitue "
        "la base du graphe PERT et du calcul du chemin critique."
    )

    add_table(doc,
              ["Tâche", "Prédécesseurs", "Successeurs", "Durée (j)"],
              [
                  ["A", "—", "B", "14"],
                  ["B", "A", "C", "6"],
                  ["C", "B", "D", "9"],
                  ["D", "C", "E, G", "3"],
                  ["E", "D", "F, H", "13"],
                  ["F", "E", "I", "9"],
                  ["G", "D", "H", "6"],
                  ["H", "E, G", "I", "6"],
                  ["I", "F, H", "J", "6"],
                  ["J", "I", "—", "3"],
              ],
              caption="Tableau 24 : Ordonnancement des tâches (méthode MPM)",
              col_widths=[1.4, 4.5, 4.5, 5.6],
              col_align=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER,
                         WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER])

    add_subheading(doc, "II.9.3. Graphe PERT / MPM")

    add_body(doc,
        "Le graphe PERT (Program Evaluation and Review Technique), associé à la "
        "méthode des potentiels (MPM), visualise l'enchaînement des activités et "
        "leurs dépendances. Chaque nœud comporte les dates au plus tôt (en haut à "
        "gauche) et au plus tôt de fin (en haut à droite), conformément au modèle "
        "enseigné en gestion de projet. Les flèches portent la durée de chaque "
        "tâche. La figure II.7 présente le réseau retenu pour SGRH Pro."
    )

    add_figure(
        doc, _fig_planning("fig_pert_sgrh_pro.png"),
        "Figure 16 : Graphe PERT / MPM du projet SGRH Pro",
        width_cm=15.8,
    )

    add_subheading(doc, "II.9.4. Détermination du chemin critique")

    add_body(doc,
        "La méthode du chemin critique (Critical Path Method, CPM) identifie "
        "la suite de tâches sans marge de retard — toute glissade sur l'une "
        "d'entre elles retarde la fin du projet. Les calculs au plus tôt (ES/EF) "
        "et au plus tard (LS/LF) conduisent à identifier le chemin critique "
        "suivant :"
    )

    add_body(doc,
        "A (14 j) → B (6 j) → C (9 j) → D (3 j) → E (13 j) → F (9 j) → "
        "I (6 j) → J (3 j), soit une durée totale de soixante-trois (63) jours ouvrés. "
        "Le tableau II.12 détaille les dates au plus tôt et au plus tard de chaque tâche."
    )

    add_body(doc,
        "Le calcul au plus tôt (avant) et au plus tard (arrière) détermine les "
        "marges : une marge nulle place la tâche sur le chemin critique."
    )

    add_table(doc,
              ["Tâche", "Durée", "ES", "EF", "LS", "LF", "Marge"],
              [
                  ["A", "14", "0", "14", "0", "14", "0"],
                  ["B", "6", "14", "20", "14", "20", "0"],
                  ["C", "9", "20", "29", "20", "29", "0"],
                  ["D", "3", "29", "32", "29", "32", "0"],
                  ["E", "13", "32", "45", "32", "45", "0"],
                  ["F", "9", "45", "54", "45", "54", "0"],
                  ["G", "6", "32", "38", "42", "48", "10"],
                  ["H", "6", "45", "51", "48", "54", "3"],
                  ["I", "6", "54", "60", "54", "60", "0"],
                  ["J", "3", "60", "63", "60", "63", "0"],
              ],
              caption="Tableau 25 : Calcul MPM (dates au plus tôt et au plus tard, en jours ouvrés)",
              col_widths=[1.2, 1.5, 1.5, 1.5, 1.5, 1.5, 1.8],
              col_align=[WD_ALIGN_PARAGRAPH.CENTER] * 7)

    add_body(doc,
        "Les tâches G (bridge biométrique) et H (intégration ZK-9500/RFID) "
        "disposent d'une marge totale de respectivement dix et trois jours : elles "
        "peuvent être menées en parallèle du développement backend et frontend "
        "sans retarder la livraison du prototype."
    )

    add_figure(
        doc, _fig_planning("fig_chemin_critique_sgrh_pro.png"),
        "Figure 17 : Chemin critique du projet (63 jours ouvrés)",
        width_cm=15.8,
    )

    add_subheading(doc, "II.9.5. Calendrier d'exécution des tâches")

    add_body(doc,
        "Le calendrier d'exécution traduit l'ordonnancement en dates de début "
        "et de fin pour chaque activité. Le tableau II.13 présente le "
        "planning prévisionnel retenu, en supposant un démarrage au "
        "premier juillet 2026 (jour ouvré 1). Les numéros de semaine "
        "sont indicatifs : ils facilitent le suivi pédagogique durant "
        "l'année académique 2026-2027, du démarrage technique du projet jusqu'à "
        "la livraison du prototype déployé au poste RH."
    )

    add_body(doc,
        "Les tâches G et H progressent en parallèle du backend/frontend ; "
        "les tests (I) démarrent après convergence des deux volets."
    )

    add_table(doc,
              ["Tâche", "Début (j)", "Fin (j)", "Semaine approx."],
              [
                  ["A — Analyse système actuel", "1", "14", "S1 – S3"],
                  ["B — Spécification besoins", "15", "20", "S3 – S4"],
                  ["C — Conception UML", "21", "29", "S4 – S5"],
                  ["D — Modèle BDD", "30", "32", "S5"],
                  ["E — Backend Laravel", "33", "45", "S5 – S7"],
                  ["F — Frontend web", "46", "54", "S7 – S8"],
                  ["G — Bridge biométrique", "33", "38", "S5 – S6"],
                  ["H — Intégration ZK/RFID", "46", "51", "S7 – S8"],
                  ["I — Tests et validation", "55", "60", "S9"],
                  ["J — Déploiement prototype", "61", "63", "S9 – S10"],
              ],
              caption="Tableau 26 : Calendrier d'exécution prévisionnel (jours ouvrés)",
              col_widths=[5.5, 2.2, 2.2, 6.1],
              col_align=[WD_ALIGN_PARAGRAPH.JUSTIFY, WD_ALIGN_PARAGRAPH.CENTER,
                         WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER])

    add_subheading(doc, "II.9.6. Diagramme de Gantt")

    add_body(doc,
        "Le diagramme de Gantt offre une représentation visuelle du calendrier : "
        "chaque barre horizontale correspond à une tâche, sa position et sa "
        "longueur indiquent respectivement la date de début et la durée. "
        "Les tâches du chemin critique apparaissent en bleu soutenu ; les tâches "
        "parallèles avec marge, en bleu clair. Les lignes sont classées par ordre "
        "alphabétique des codes (A à J). La figure II.9 couvre l'ensemble des "
        "soixante-trois jours ouvrés du projet, du 1er juillet 2026 à la fin du déploiement "
        "du prototype."
    )

    add_figure(
        doc, _fig_planning("fig_gantt_sgrh_pro.png"),
        "Figure 18 : Diagramme de Gantt du projet SGRH Pro",
        width_cm=15.8,
    )

    add_body(doc,
        "Le diagramme met en évidence deux volets parallèles après la conception : "
        "le développement du bridge biométrique (G) peut démarrer dès la "
        "modélisation de la base de données, tandis que le backend (E) et le "
        "frontend (F) enchaînent sur le chemin critique avant l'intégration (H) "
        "et les tests (I)."
    )

    add_subheading(doc, "II.9.7. Estimation du coût du projet")

    add_body(doc,
        "L'estimation budgétaire suit une approche bottom-up : agrégation "
        "des coûts par poste de dépense, complétée d'une marge de contingence "
        "de dix pour cent pour couvrir les imprévus (variation des prix, "
        "délais d'importation du matériel). Les montants sont exprimés en "
        "dollars américains (USD), devise couramment utilisée pour l'achat "
        "de matériel informatique à Kinshasa, avec équivalent indicatif "
        "en franc congolais (CDF)."
    )

    add_table(doc,
              ["Poste de dépense", "Quantité", "Coût unitaire (USD)", "Total (USD)"],
              [
                  ["Lecteur empreintes ZK-9500", "1", "80", "80"],
                  ["Cartes RFID nominatives (lot 50)", "1 lot", "25", "25"],
                  ["Lecteur USB RFID", "1", "15", "15"],
                  ["Câbles USB et accessoires", "1", "10", "10"],
                  ["Hébergement VPS (3 mois, optionnel)", "3", "5", "15"],
                  ["Logiciels (PHP, Laravel, VS Community)", "—", "0", "0"],
                  ["Poste de développement (existant)", "1", "0", "0"],
                  ["Sous-total", "—", "—", "145"],
                  ["Contingence (10 %)", "—", "—", "15"],
                  ["TOTAL ESTIMÉ", "—", "—", "160"],
              ],
              caption="Tableau 27 : Estimation du coût du projet SGRH Pro",
              col_widths=[5.5, 2.0, 3.5, 5.0],
              col_align=[WD_ALIGN_PARAGRAPH.JUSTIFY, WD_ALIGN_PARAGRAPH.CENTER,
                         WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER])

    add_body(doc,
        "Le coût total estimé s'élève à environ 160 USD (équivalent indicatif "
        "410 000 à 480 000 CDF selon le taux de change). Le poste principal "
        "est le lecteur biométrique ZK-9500 (80 USD), indispensable à la démonstration "
        "du pointage réel. Les logiciels retenus (PHP, Laravel, SQLite/MySQL, "
        "Visual Studio Community) sont gratuits, ce qui maîtrise le budget "
        "dans le cadre d'un mémoire universitaire."
    )

    add_body(doc,
        "Il convient de préciser que ce budget couvre le prototype de "
        "démonstration et non un déploiement institutionnel à grande échelle, "
        "qui impliquerait des coûts supplémentaires (serveur dédié, "
        "formation des utilisateurs, maintenance, conformité juridique "
        "biométrique). Ces éléments sont identifiés comme perspectives "
        "au chapitre IV."
    )

    # ───────────────── II.10 Conclusion ─────────────────
    add_heading(doc, "II.10. Conclusion")

    add_body(doc,
        "L'analyse du système actuel de gestion RH au siège central de la CNSS "
        "révèle un écart significatif entre les obligations d'une institution "
        "publique de cette envergure et les outils réellement employés : "
        "registres papier, fichiers Excel non sécurisés, pointage contournable "
        "et absence de reporting consolidé. Ces dysfonctionnements — documentés "
        "par observation et entretiens — justifient le projet SGRH Pro."
    )

    add_body(doc,
        "Le passage du diagnostic à la spécification répond au principe "
        "méthodologique de l'analyse orientée objet : partir des faits "
        "observés, identifier les acteurs et leurs interactions, puis "
        "formaliser les exigences avant toute ligne de code. Cette "
        "discipline garantit que le prototype développé aux chapitres "
        "suivants n'est pas une démonstration technique déconnectée, "
        "mais une réponse argumentée aux problèmes réels de la DRH."
    )

    add_body(doc,
        "L'analyse des besoins a permis d'identifier quatre profils d'acteurs "
        "aux attentes convergentes mais différenciées, et de formaliser cinq "
        "scénarios d'utilisation prioritaires. La spécification en huit "
        "modules — recentrés sur les présences, la biométrie, l'évaluation "
        "et les éléments de rémunération — couvre le cycle RH opérationnel "
        "prioritaire au siège central. La planification du projet — dix tâches "
        "techniques (A à J), chemin critique de soixante-trois jours ouvrés, budget estimé "
        "à 160 USD — matérialise la faisabilité temporelle et financière "
        "du prototype. Le chapitre suivant traduira ces spécifications en architecture "
        "logicielle, modèles UML et schéma de base de données du système "
        "SGRH Pro."
    )

    return page_start


def build():
    doc = init_document()
    append_chapitre2(doc, PAGE_START)
    out = OUTPUT
    try:
        doc.save(out)
    except PermissionError:
        out = OUTPUT_FALLBACK
        doc.save(out)
        print("Note : fichier ouvert — sauvegarde alternative")
    words = sum(len(p.text.split()) for p in doc.paragraphs)
    print(f"Chapitre II genere : {out}")
    print(f"Mots approximatifs : {words}")


if __name__ == "__main__":
    build()

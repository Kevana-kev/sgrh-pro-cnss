# -*- coding: utf-8 -*-
"""Corrections de fond : orientation logiciel, institution publique, pas de gestion de salaire."""
from pathlib import Path

ROOT = Path(r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE")

REPLACEMENTS = [
    ("ZK-Teco 9500", "ZK-9500"),
    ("ZK-Teco", "ZK-9500"),
    ("retards de paie", "lenteurs de traitement administratif"),
    ("masse salariale", "effectif opérationnel"),
    ("Masse salariale", "Effectif opérationnel"),
    ("bulletins de paie", "documents administratifs"),
    ("bulletin de paie", "relevé administratif"),
    ("Bulletin PDF", "État administratif exporté"),
    ("bulletins PDF", "états administratifs exportés"),
    ("calcul de paie", "consolidation administrative"),
    ("Calcul de paie", "Consolidation administrative"),
    ("Module 6 — Gestion de la paie", "Module 6 — Suivi administratif des éléments de rémunération"),
    ("II.6.6. Module 6 — Gestion de la paie", "II.6.6. Module 6 — Suivi administratif des éléments de rémunération"),
    ("Gestion de la paie", "Suivi administratif des éléments de rémunération"),
    ("Module paie", "Module éléments de rémunération"),
    ("module paie", "module éléments de rémunération"),
    ("historiques de paie", "historiques administratifs"),
    ("éléments de paie", "éléments administratifs de rémunération"),
    ("fichier de paie", "fichier administratif"),
    ("préparation de la paie", "préparation des états administratifs"),
    ("préparation des éléments de paie", "préparation des états transmis à la finance"),
    ("bureau paie et avantages (calcul des salaires, primes, retenues)",
     "bureau administration du personnel et transmission (états de présence, éléments variables pour la finance)"),
    ("Le bureau paie dispose de son propre fichier pour les éléments "
     "rémunératoires ; la cohérence entre les deux fichiers est vérifiée "
     "manuellement au moment du calcul mensuel",
     "Le bureau chargé de la transmission administrative dispose de son propre fichier "
     "pour les éléments variables ; la cohérence avec le fichier effectifs est vérifiée "
     "manuellement avant envoi à la direction financière"),
    ("II.3.4. Gestion des congés, paie et contrats",
     "II.3.4. Gestion des congés, transmission administrative et contrats"),
    ("Microsoft Excel\", \"Effectifs, éléments de paie, soldes congés",
     "Microsoft Excel\", \"Effectifs, éléments administratifs, soldes congés"),
    ("Traitement de texte / imprimante\", \"Bulletins, attestations, notes",
     "Traitement de texte / imprimante\", \"Attestations, notes de service"),
    ("[\"D3\", \"Retards de paie\", \"Calcul manuel, ressaisies",
     "[\"D3\", \"Retards administratifs\", \"Saisies manuelles, ressaisies"),
    ("Erreurs de paie", "Erreurs administratives"),
    ("modification de salaire", "modification de dossier"),
    ("Modification de salaire", "Modification de dossier"),
    ("salaires individuels", "données personnelles sensibles"),
    ("Les administrateurs RH (bureaux gestion du personnel et paie) demandent "
     "une source unique de vérité regroupant dossiers, contrats, présences et "
     "éléments de rémunération. Le responsable du bureau paie a exprimé "
     "le souhait de « clôturer la paie en trois jours au lieu de dix » "
     "grâce à un calcul automatique intégrant les absences.",
     "Les administrateurs RH demandent une source unique de vérité regroupant "
     "dossiers, contrats, présences et éléments administratifs. Le responsable "
     "du bureau gestion du personnel a exprimé le souhait de « produire les états "
     "de présence en deux jours au lieu de dix » grâce à une consolidation "
     "automatique des données enregistrées par le logiciel."),
    (" calculer et valider la paie mensuelle avec génération automatique "
     "des bulletins PDF ;",
     " produire automatiquement les états de présence et les éléments variables "
     "transmis à la direction financière ;"),
    (" consulter leurs bulletins de paie et leur historique de rémunération ;",
     " consulter leurs relevés de présence, leurs congés et leurs documents administratifs ;"),
    ("bulletins en ligne", "documents administratifs en ligne"),
    ("II.5.4. Calcul et génération du bulletin de paie",
     "II.5.4. Production des états administratifs pour la direction financière"),
    ("En fin de mois, l'administrateur RH lance le calcul de paie pour "
     "la période concernée. Le système agrège le salaire de base, les primes, "
     "les heures supplémentaires issues du module présences, applique les "
     "retenues CNSS et IRG, déduit les absences injustifiées et produit "
     "le salaire net. Un bulletin PDF est généré et rendu consultable "
     "dans l'espace agent.",
     "En fin de mois, l'administrateur RH consolide dans SGRH Pro les présences, "
     "absences et éléments variables enregistrés par le logiciel. Le système "
     "génère un état administratif transmis à la direction financière, "
     "institution chargée du virement bancaire des agents — mode de "
     "rémunération en vigueur à la CNSS, institution publique. L'agent "
     "consulte en ligne ses relevés de présence et l'historique de ses "
     "demandes administratives."),
    ("Automatiser le calcul de la rémunération et la production des bulletins.",
     "Consolider les éléments administratifs de rémunération et produire les états pour la finance."),
    ("Paramétrage salaire de base, primes, heures sup.",
     "Enregistrement des éléments variables (primes, indemnités, retenues administratives)"),
    ("Calcul retenues CNSS (part salariale) et IRG",
     "Export des états mensuels pour la direction financière"),
    ("Génération bulletin PDF (ReportLab)",
     "Export PDF/CSV des états administratifs (ReportLab)"),
    ("Historique des fiches de paie",
     "Historique des états administratifs transmis"),
    ("[\"EF-09\", \"Calculer la paie mensuelle (CNSS, IRG, net)\", \"M\"]",
     "[\"EF-09\", \"Consolider les états administratifs mensuels (présences, variables)\", \"M\"]"),
    ("[\"EF-10\", \"Générer un bulletin de paie PDF\", \"M\"]",
     "[\"EF-10\", \"Exporter les états administratifs PDF/CSV pour la finance\", \"M\"]"),
    ("[\"EF-14\", \"Espace agent : consulter paie, congés, pointages\", \"M\"]",
     "[\"EF-14\", \"Espace agent : consulter présences, congés, documents administratifs\", \"M\"]"),
    (" calcul et génération PDF d'au moins une fiche de paie ;",
     " production d'au moins un état administratif consolidé (présences + export) ;"),
    ("[\"Gestion dossiers et paie\", \"●\", \"—\", \"—\"]",
     "[\"Gestion dossiers agents\", \"●\", \"—\", \"—\"]"),
    ("[\"Consultation bulletin paie\", \"●\", \"—\", \"●\"]",
     "[\"Consultation relevés administratifs\", \"●\", \"—\", \"●\"]"),
    ("[\"Calcul de paie\", \"Admin RH\", \"Présences du mois clôturées",
     "[\"États administratifs\", \"Admin RH\", \"Présences du mois clôturées"),
    ("Bulletin PDF disponible, retenues calculées",
     "État exporté disponible pour la finance"),
    ("M6 Paie", "M6 Éléments rémunération"),
    ("M6 Paie,", "M6 Éléments rémun.,"),
    ("Module 4 alimente le module 6 (paie) pour les retenues d'absence ;",
     "Module 4 alimente le module 6 pour les absences impactant les états administratifs ;"),
    ("démonstration biométrique et paie", "démonstration logicielle complète"),
    ("Intégration avec le module paie pour retenues",
     "Alimentation du module éléments de rémunération"),
    ("règles métier congolaises (cotisations CNSS, barème IRG) — "
     "savoir-faire qui alimentera le paramétrage du module paie.",
     "règles administratives internes — savoir-faire qui alimentera "
     "le paramétrage des modules logiciels de SGRH Pro."),
    ("Le calcul de paie intervient une fois par mois.",
     "La consolidation administrative intervient une fois par mois."),
]

CH1_EXTRA = [
    ("add_subheading(doc, \"I.3.1.1. Le module paie et le contexte réglementaire congolais\")",
     "add_subheading(doc, \"I.3.1.1. Rémunération des agents publics et rôle du SIGRH\")"),
]

def patch_file(path: Path):
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if path.name == "build_chapitre1.py":
        for old, new in CH1_EXTRA:
            text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"  patched {path.name}")
    else:
        print(f"  unchanged {path.name}")


def main():
    for name in ("build_chapitre1.py", "build_chapitre2.py"):
        patch_file(ROOT / name)
    print("Done.")


if __name__ == "__main__":
    main()

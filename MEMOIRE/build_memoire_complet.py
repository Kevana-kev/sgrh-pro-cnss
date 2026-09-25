# -*- coding: utf-8 -*-
"""
Mémoire complet SGRH Pro — Introduction + chapitres I à IV + conclusion.
Plan calqué sur le mémoire UWB (Clémence NSIALA NDONA), contenu CNSS / SGRH Pro.
"""
from pathlib import Path

from memoire_format import init_document, add_page_break, apply_document_page_numbering
from build_preliminaires import write_preliminaires
from write_introduction import write_introduction
from build_chapitre1 import append_chapitre1
from build_chapitre2 import append_chapitre2
from build_chapitre3 import append_chapitre3
from build_chapitre4 import append_chapitre4
from build_fin_memoire import write_conclusion_bibliographie

OUTPUT = r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\MEMOIRE COMPLET - SGRH PRO - BONGA KASUSA REBECCA.docx"
OUTPUT_FALLBACK = OUTPUT.replace(".docx", " - v2.docx")
OUTPUT_FALLBACK2 = OUTPUT.replace(".docx", " - v3.docx")


def build():
    doc = init_document()
    write_preliminaires(doc)
    write_introduction(doc)
    add_page_break(doc)
    append_chapitre1(doc, page_start=12)
    add_page_break(doc)
    append_chapitre2(doc, page_start=28)
    add_page_break(doc)
    append_chapitre3(doc, page_start=45)
    add_page_break(doc)
    append_chapitre4(doc, page_start=62)
    add_page_break(doc)
    write_conclusion_bibliographie(doc, page_start=78)
    apply_document_page_numbering(doc)

    out = OUTPUT
    try:
        doc.save(out)
    except PermissionError:
        for fallback in (OUTPUT_FALLBACK, OUTPUT_FALLBACK2):
            try:
                out = fallback
                doc.save(out)
                print("Note : fichier ouvert — sauvegarde alternative")
                break
            except PermissionError:
                continue
        else:
            raise

    words = sum(len(p.text.split()) for p in doc.paragraphs)
    paras = len(doc.paragraphs)
    tables = len(doc.tables)
    print(f"Memoire complet genere : {out}")
    print(f"Mots : {words}")
    print(f"Paragraphes : {paras}")
    print(f"Tableaux : {tables}")
    # Estimation pages : interligne 1.5, ~280 mots/page + figures/tableaux
    est_text = max(1, words // 280)
    est_extra = 18 + (tables // 3)  # prelim + figures + placeholders
    print(f"Estimation pages (texte) : ~{est_text}")
    print(f"Estimation pages (avec figures/tableaux/prelim) : ~{est_text + est_extra}")

    try:
        from paginate_memoire import paginate
        paginate(Path(out))
    except Exception as exc:
        print(f"Pagination Python non appliquee : {exc}")
        ps1 = Path(__file__).with_name("paginate_memoire.ps1")
        if ps1.exists():
            import subprocess
            print("Pagination Word via PowerShell...")
            subprocess.run(
                [
                    "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                    "-File", str(ps1), "-Path", out,
                ],
                check=False,
            )
        else:
            print("Relancer : paginate_memoire.ps1")


if __name__ == "__main__":
    build()

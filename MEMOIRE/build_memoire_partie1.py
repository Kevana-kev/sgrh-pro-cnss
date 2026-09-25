# -*- coding: utf-8 -*-
"""
Génère le document unique : Introduction générale + Chapitre I + Chapitre II.
Orientation : logiciel SIGRH (SGRH Pro), institution publique, paiement bancaire.
"""
from memoire_format import init_document, add_page_break
from write_introduction import write_introduction
from build_chapitre1 import append_chapitre1
from build_chapitre2 import append_chapitre2

OUTPUT = r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\MEMOIRE - INTRODUCTION ET CHAPITRES I ET II.docx"
OUTPUT_FALLBACK = OUTPUT.replace(".docx", " - v2.docx")
OUTPUT_FALLBACK2 = OUTPUT.replace(".docx", " - v3.docx")


def build():
    doc = init_document()
    write_introduction(doc)
    add_page_break(doc)
    append_chapitre1(doc, page_start=9)
    add_page_break(doc)
    append_chapitre2(doc, page_start=24)

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

    # Statistiques
    words = sum(len(p.text.split()) for p in doc.paragraphs)
    intro_words = 0
    in_intro = True
    for p in doc.paragraphs:
        t = p.text.strip()
        if t.startswith("CHAPITRE I."):
            in_intro = False
        if in_intro:
            intro_words += len(t.split())
    print(f"Memoire genere : {out}")
    print(f"Mots total : {words}")
    print(f"Mots introduction : {intro_words}")


if __name__ == "__main__":
    build()

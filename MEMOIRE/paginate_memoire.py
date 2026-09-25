# -*- coding: utf-8 -*-
"""
Recalcule les numéros de page (listes + table des matières) via Microsoft Word.
À lancer après build_memoire_complet.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DEFAULT = Path(r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\MEMOIRE COMPLET - SGRH PRO - BONGA KASUSA REBECCA.docx")

KEY_RE = re.compile(
    r"^(Figure|Tableau)\s+([IVX]+\.\d+(?:\s+(?:bis|ter|quater|quinquies))?)",
    re.IGNORECASE,
)


def to_roman(n: int) -> str:
    mapping = [
        (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i"),
    ]
    out = []
    for val, sym in mapping:
        while n >= val:
            out.append(sym)
            n -= val
    return "".join(out) or "i"


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").replace("\r", "").replace("\x07", "")).strip()


def paginate(path: Path) -> None:
    import win32com.client

    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(path.resolve()))
    try:
        doc.Repaginate()
        try:
            doc.Fields.Update()
        except Exception:
            pass

        fig_pages: dict[str, str] = {}
        tab_pages: dict[str, str] = {}
        heading_pages: dict[str, tuple[int, int]] = {}

        in_fig_list = False
        in_tab_list = False
        in_toc = False

        for para in doc.Paragraphs:
            raw = para.Range.Text or ""
            text = _norm(raw)
            if not text:
                continue
            style = ""
            try:
                style = str(para.Style.NameLocal)
            except Exception:
                pass

            page = int(para.Range.Information(3))  # wdActiveEndPageNumber
            section = int(para.Range.Information(2))  # wdActiveEndSectionNumber

            if text == "LISTE DES FIGURES":
                in_fig_list, in_tab_list, in_toc = True, False, False
                heading_pages[text] = (section, page)
                continue
            if text == "LISTE DES TABLEAUX":
                in_fig_list, in_tab_list, in_toc = False, True, False
                heading_pages[text] = (section, page)
                continue
            if text in ("TABLE DES MATIÈRES", "TABLE DES MATIERES"):
                in_fig_list, in_tab_list, in_toc = False, False, True
                heading_pages[text] = (section, page)
                continue
            if style.startswith("Heading 1") and text not in (
                "LISTE DES FIGURES", "LISTE DES TABLEAUX", "TABLE DES MATIÈRES",
            ):
                in_fig_list = in_tab_list = False
                if text != "TABLE DES MATIÈRES":
                    in_toc = False
                heading_pages[text] = (section, page)
                continue
            if style.startswith("Heading") and not in_toc:
                heading_pages[text] = (section, page)

            if in_fig_list or in_tab_list or in_toc:
                continue

            # Légendes du corps (pas les listes)
            m = KEY_RE.match(text)
            if m and ("—" in text or " - " in text or ":" in text):
                kind, num = m.group(1), m.group(2)
                key = f"{kind} {num}".replace("  ", " ")
                shown = str(page)
                if kind.lower().startswith("figure"):
                    fig_pages[key] = shown
                else:
                    tab_pages[key] = shown

        def fmt_page(section_no: int, page_no: int) -> tuple[str, bool]:
            if section_no <= 1:
                return to_roman(page_no), True
            return str(page_no), False

        def replace_dotted(paragraph, new_page: str, roman: bool) -> None:
            rng = paragraph.Range
            t = rng.Text.rstrip("\r")
            if "\t" in t:
                left = t.rsplit("\t", 1)[0]
            else:
                left = re.sub(r"(\s+\.+|\s+- \d+ -|\s+[ivx]+)\s*$", "", t, flags=re.I)
            suffix = new_page if roman else f"- {new_page} -"
            rng.Text = f"{left}\t{suffix}\r"

        in_fig_list = in_tab_list = in_toc = False
        for para in doc.Paragraphs:
            text = _norm(para.Range.Text)
            if not text:
                continue
            if text == "LISTE DES FIGURES":
                in_fig_list, in_tab_list, in_toc = True, False, False
                continue
            if text == "LISTE DES TABLEAUX":
                in_fig_list, in_tab_list, in_toc = False, True, False
                continue
            if text in ("TABLE DES MATIÈRES", "TABLE DES MATIERES"):
                in_fig_list, in_tab_list, in_toc = False, False, True
                continue
            try:
                st = str(para.Style.NameLocal)
            except Exception:
                st = ""
            if st.startswith("Heading 1") and text not in (
                "LISTE DES FIGURES", "LISTE DES TABLEAUX", "TABLE DES MATIÈRES",
            ):
                if in_toc and text not in ("TABLE DES MATIÈRES", "TABLE DES MATIERES"):
                    in_toc = False
                in_fig_list = in_tab_list = False
                continue

            if in_fig_list or in_tab_list:
                m = KEY_RE.match(text)
                if not m:
                    continue
                key = f"{m.group(1)} {m.group(2)}"
                pool = fig_pages if in_fig_list else tab_pages
                if key in pool:
                    replace_dotted(para, pool[key], roman=False)
                continue

            if in_toc:
                # titre = partie avant tabulation
                title = text.split("\t")[0].strip()
                title = re.sub(r"\s+\.+$", "", title).strip()
                if title in heading_pages:
                    sec, pg = heading_pages[title]
                    shown, roman = fmt_page(sec, pg)
                    replace_dotted(para, shown, roman=roman)

        doc.Repaginate()
        doc.Save()
        print(f"Pagination mise a jour : {path}")
        print(f"  Figures localisees : {len(fig_pages)}")
        print(f"  Tableaux localises : {len(tab_pages)}")
        print(f"  Rubriques TDM      : {len(heading_pages)}")
    finally:
        doc.Close(True)
        word.Quit()


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    paginate(target)

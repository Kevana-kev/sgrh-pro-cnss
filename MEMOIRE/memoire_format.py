# -*- coding: utf-8 -*-
"""Utilitaires de mise en page communs aux chapitres du mémoire."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.section import WD_SECTION_START
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FONT = "Times New Roman"
BODY_SIZE = Pt(12)
TITLE_SIZE = Pt(14)
HEADING_SIZE = Pt(12)
SUBHEADING_SIZE = Pt(12)
LINE_SPACING = 1.5
SPACE = Pt(6)
TABLE_WIDTH_CM = 16.0


def set_run_font(run, bold=False, italic=False, size=BODY_SIZE):
    run.font.name = FONT
    run.font.size = size
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), FONT)
    rFonts.set(qn("w:hAnsi"), FONT)
    rFonts.set(qn("w:cs"), FONT)
    color = rPr.find(qn("w:color"))
    if color is None:
        color = OxmlElement("w:color")
        rPr.append(color)
    for attr in list(color.attrib):
        if "theme" in attr.lower():
            del color.attrib[attr]
    color.set(qn("w:val"), "000000")


def init_document():
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Cm(2.54)
    sec.bottom_margin = Cm(2.54)
    sec.left_margin = Cm(2.54)
    sec.right_margin = Cm(2.54)
    sec.header_distance = Cm(1.25)
    _configure_heading_styles(doc)
    return doc


def _force_style_black(style):
    """Supprime la couleur thème (bleu Word) des titres."""
    try:
        style.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    except Exception:
        pass
    rPr = style.element.find(qn("w:rPr"))
    if rPr is None:
        rPr = OxmlElement("w:rPr")
        style.element.append(rPr)
    color = rPr.find(qn("w:color"))
    if color is None:
        color = OxmlElement("w:color")
        rPr.append(color)
    for attr in list(color.attrib):
        if "theme" in attr.lower():
            del color.attrib[attr]
    color.set(qn("w:val"), "000000")


def _configure_heading_styles(doc):
    for name, size, bold, center in (
        ("Heading 1", Pt(14), True, True),
        ("Heading 2", Pt(12), True, False),
        ("Heading 3", Pt(12), True, False),
    ):
        try:
            style = doc.styles[name]
        except KeyError:
            continue
        style.font.name = FONT
        style.font.size = size
        style.font.bold = bold
        style.font.italic = False
        _force_style_black(style)
        if style.paragraph_format is not None:
            style.paragraph_format.line_spacing = LINE_SPACING
            style.paragraph_format.space_before = Pt(6)
            style.paragraph_format.space_after = SPACE
    for extra in ("Title", "Subtitle", "Hyperlink"):
        try:
            _force_style_black(doc.styles[extra])
        except KeyError:
            pass


def _add_page_field(paragraph, wrap_dashes=True):
    """Insère un champ PAGE Word (numérotation réelle sur chaque page)."""
    if wrap_dashes:
        paragraph.add_run("- ")

    def _fld(el_name, **attrs):
        el = OxmlElement(el_name)
        for k, v in attrs.items():
            el.set(qn(k), v)
        return el

    r1 = paragraph.add_run()
    r1._r.append(_fld("w:fldChar", **{"w:fldCharType": "begin"}))
    r2 = paragraph.add_run()
    instr = _fld("w:instrText", **{"xml:space": "preserve"})
    instr.text = " PAGE "
    r2._r.append(instr)
    r3 = paragraph.add_run()
    r3._r.append(_fld("w:fldChar", **{"w:fldCharType": "end"}))
    for run in (r1, r2, r3):
        set_run_font(run)

    if wrap_dashes:
        paragraph.add_run(" -")
    for run in paragraph.runs:
        set_run_font(run)


def _set_pg_num_type(section, fmt="decimal", start=1):
    sect_pr = section._sectPr
    node = sect_pr.find(qn("w:pgNumType"))
    if node is None:
        node = OxmlElement("w:pgNumType")
        sect_pr.append(node)
    node.set(qn("w:fmt"), fmt)
    node.set(qn("w:start"), str(start))


def _header_page_number(section, wrap_dashes=True):
    header = section.header
    header.is_linked_to_previous = False
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.clear()
    _add_page_field(p, wrap_dashes=wrap_dashes)


def start_body_section(doc):
    """Section suivante : pagination arabe recommençant à 1 (après les pages romaines)."""
    return doc.add_section(WD_SECTION_START.NEW_PAGE)


def apply_document_page_numbering(doc):
    """
    Pages préliminaires : i, ii, iii… (en-tête).
    Corps : - 1 -, - 2 -, … sur toutes les pages.
    """
    if len(doc.sections) == 1:
        _set_pg_num_type(doc.sections[0], "decimal", 1)
        _header_page_number(doc.sections[0], wrap_dashes=True)
        return

    prelim = doc.sections[0]
    _set_pg_num_type(prelim, "lowerRoman", 1)
    _header_page_number(prelim, wrap_dashes=False)

    for section in doc.sections[1:]:
        section.different_first_page_header_footer = False
        _set_pg_num_type(section, "decimal", 1)
        _header_page_number(section, wrap_dashes=True)

    prelim.different_first_page_header_footer = False


def add_dotted_entry(doc, title, page="…", indent_cm=0, bold=False, roman=False, size=None):
    """Entrée style Clémence : titre .................... - 12 -"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.left_indent = Cm(indent_cm)
    p.paragraph_format.tab_stops.add_tab_stop(
        Cm(16.0), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS
    )
    font_size = size if size is not None else Pt(12)
    run = p.add_run(title)
    set_run_font(run, bold=bold, size=font_size)
    suffix = str(page) if roman else f"- {page} -"
    run2 = p.add_run("\t" + suffix)
    set_run_font(run2, size=font_size)
    return p


def add_biblio_entry(doc, number, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = LINE_SPACING
    p.paragraph_format.left_indent = Cm(1.0)
    p.paragraph_format.first_line_indent = Cm(-0.75)
    r0 = p.add_run(f"{number}. ")
    set_run_font(r0, bold=True)
    r1 = p.add_run(text)
    set_run_font(r1)
    return p


def add_page_number(doc, num):
    """Ancienne pagination manuelle : désactivée (en-tête Word sur chaque page)."""
    return None


def add_page_number_para(paragraph, num):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run(f"- {num} -")
    set_run_font(run)
    paragraph.paragraph_format.space_after = Pt(6)


def add_chapter_title(doc, text):
    p = doc.add_paragraph(text, style="Heading 1")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = SPACE
    p.paragraph_format.space_after = SPACE
    p.paragraph_format.line_spacing = LINE_SPACING
    for run in p.runs:
        set_run_font(run, bold=True, size=TITLE_SIZE)
    return p


def add_heading(doc, text, italic=False):
    p = doc.add_paragraph(text, style="Heading 2")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = SPACE
    p.paragraph_format.line_spacing = LINE_SPACING
    for run in p.runs:
        set_run_font(run, bold=True, italic=italic, size=HEADING_SIZE)
    return p


def add_subheading(doc, text, italic=False):
    p = doc.add_paragraph(text, style="Heading 3")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = SPACE
    p.paragraph_format.line_spacing = LINE_SPACING
    for run in p.runs:
        set_run_font(run, bold=True, italic=italic, size=SUBHEADING_SIZE)
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


def add_numbered_item(doc, number, text, bold_label=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = LINE_SPACING
    p.paragraph_format.left_indent = Cm(0.75)
    r0 = p.add_run(f"{number}. ")
    set_run_font(r0, bold=True)
    if bold_label:
        r1 = p.add_run(bold_label)
        set_run_font(r1, bold=True)
        r2 = p.add_run(text)
        set_run_font(r2)
    else:
        r1 = p.add_run(text)
        set_run_font(r1)


def add_objectives_list(doc, items):
    for item in items:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = LINE_SPACING
        p.paragraph_format.left_indent = Cm(1)
        parts = item if isinstance(item, list) else [(item, False, False)]
        for text, bold, italic in parts:
            run = p.add_run(text)
            set_run_font(run, bold=bold, italic=italic)


def _set_cell_shading(cell, fill="E8E8E8"):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = tcPr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tcPr.append(shd)
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)


def _set_cell_margins(cell, top=40, bottom=40, left=80, right=80):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    mar = tcPr.find(qn("w:tcMar"))
    if mar is None:
        mar = OxmlElement("w:tcMar")
        tcPr.append(mar)
    for side, val in (("top", top), ("bottom", bottom), ("start", left), ("end", right)):
        node = mar.find(qn(f"w:{side}"))
        if node is None:
            node = OxmlElement(f"w:{side}")
            mar.append(node)
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")


def _set_table_fixed_layout(table, width_cm=TABLE_WIDTH_CM):
    tbl = table._tbl
    tblPr = tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement("w:tblPr")
        tbl.insert(0, tblPr)
    layout = tblPr.find(qn("w:tblLayout"))
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        tblPr.append(layout)
    layout.set(qn("w:type"), "fixed")

    total_twips = int(width_cm * 567)
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.append(tblW)
    tblW.set(qn("w:w"), str(total_twips))
    tblW.set(qn("w:type"), "dxa")
    return total_twips


def _set_column_widths(table, widths_cm, total_cm=TABLE_WIDTH_CM):
    total_twips = _set_table_fixed_layout(table, total_cm)
    if not widths_cm:
        n = len(table.columns)
        widths_cm = [total_cm / n] * n
    ratio = sum(widths_cm)
    tbl = table._tbl
    grid = tbl.find(qn("w:tblGrid"))
    if grid is None:
        grid = OxmlElement("w:tblGrid")
        tbl.insert(1, grid)
    else:
        for gc in list(grid):
            grid.remove(gc)
    for i, w in enumerate(widths_cm):
        twips = int(total_twips * (w / ratio))
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(twips))
        grid.append(gc)
        if i < len(table.columns):
            for row in table.rows:
                row.cells[i].width = Cm(w)


def _default_col_widths(n_cols):
    """Largeurs proportionnelles selon le nombre de colonnes."""
    presets = {
        2: [5.5, 10.5],
        3: [3.5, 6.5, 6.0],
        4: [2.5, 4.5, 4.5, 4.5],
        5: [2.0, 3.5, 3.5, 3.5, 3.5],
        6: [2.0, 2.8, 2.8, 2.8, 2.8, 2.8],
    }
    if n_cols in presets:
        return presets[n_cols]
    return [TABLE_WIDTH_CM / n_cols] * n_cols


def _default_col_align(n_cols):
    """Alignement : 1re colonne centrée si repère, dernière colonne centrée si courte."""
    align = [WD_ALIGN_PARAGRAPH.JUSTIFY] * n_cols
    if n_cols >= 2:
        align[0] = WD_ALIGN_PARAGRAPH.CENTER
    return align


def _write_cell(cell, text, bold=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=Pt(10)):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run(text)
    set_run_font(r, bold=bold, size=size)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    _set_cell_margins(cell)


def add_table(doc, headers, rows, caption=None, col_widths=None, col_align=None):
    if caption:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_before = Pt(6)
        cp.paragraph_format.space_after = Pt(2)
        cr = cp.add_run(caption)
        set_run_font(cr, bold=True, italic=True, size=Pt(11))

    n_cols = len(headers)
    table = doc.add_table(rows=1 + len(rows), cols=n_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"

    widths = col_widths or _default_col_widths(n_cols)
    aligns = col_align or _default_col_align(n_cols)
    _set_column_widths(table, widths)

    for i, h in enumerate(headers):
        _write_cell(table.rows[0].cells[i], h, bold=True,
                    align=WD_ALIGN_PARAGRAPH.CENTER, size=Pt(10))
        _set_cell_shading(table.rows[0].cells[i])

    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            al = aligns[ci] if ci < len(aligns) else WD_ALIGN_PARAGRAPH.JUSTIFY
            _write_cell(table.rows[ri + 1].cells[ci], val, align=al, size=Pt(10))

    doc.add_paragraph()
    return table


def add_page_break(doc):
    """Saut de page."""
    from docx.enum.text import WD_BREAK
    p = doc.add_paragraph()
    p.add_run().add_break(WD_BREAK.PAGE)


def add_reserved_title_page(doc, title, roman_num=None):
    """Page préliminaire réservée : titre seul (numéro en en-tête)."""
    p = doc.add_paragraph(title, style="Heading 1")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(180)
    p.paragraph_format.space_after = Pt(12)
    for run in p.runs:
        set_run_font(run, bold=True, size=TITLE_SIZE)
    hint = doc.add_paragraph()
    hint.alignment = WD_ALIGN_PARAGRAPH.CENTER
    hint.paragraph_format.space_before = Pt(24)
    hr = hint.add_run("[Texte à compléter par l'auteur]")
    set_run_font(hr, italic=True, size=Pt(11))
    add_page_break(doc)


def add_source(doc, text="Source : conception de l'auteur, 2026."):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(10)
    run = p.add_run(text)
    set_run_font(run, italic=True, size=Pt(9))


def add_code_block(doc, code, caption=None, source_file=None):
    """Encadré d'extrait de code (Courier New, 8,5 pt)."""
    if caption:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_before = Pt(8)
        cp.paragraph_format.space_after = Pt(2)
        cr = cp.add_run(caption)
        set_run_font(cr, bold=True, italic=True, size=Pt(11))
    if source_file:
        sp = doc.add_paragraph()
        sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sr = sp.add_run(f"Fichier source : {source_file}")
        set_run_font(sr, italic=True, size=Pt(9))

    table = doc.add_table(rows=1, cols=1)
    table.style = "Table Grid"
    cell = table.rows[0].cells[0]
    _set_cell_shading(cell, "F4F4F4")
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(code.strip("\n"))
    run.font.name = "Courier New"
    run.font.size = Pt(8)
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), "Courier New")
    rFonts.set(qn("w:hAnsi"), "Courier New")
    _set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
    doc.add_paragraph()


def add_screenshot_placeholder(doc, caption, hint, image_path=None, width_cm=15.8):
    """Réserve l'emplacement d'une capture d'écran de l'application."""
    import os
    if image_path and os.path.exists(image_path):
        add_figure(doc, image_path, caption, source="Source : capture d'écran de SGRH Pro, 2026.",
                   width_cm=width_cm)
        return
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    cell = table.rows[0].cells[0]
    _set_cell_shading(cell, "FAFAFA")
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(36)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("ESPACE RÉSERVÉ — CAPTURE D'ÉCRAN")
    set_run_font(r, bold=True, size=Pt(11))
    p2 = cell.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_after = Pt(36)
    r2 = p2.add_run(hint)
    set_run_font(r2, italic=True, size=Pt(10))
    _set_cell_margins(cell, top=80, bottom=80, left=80, right=80)

    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(4)
    cr = cap.add_run(caption)
    set_run_font(cr, bold=True, italic=True, size=Pt(11))
    add_source(doc, "Source : capture d'écran de SGRH Pro à insérer par l'auteur.")


def add_figure(doc, image_path, caption, source=None, width_cm=15.8):
    """Insère une figure centrée avec légende et source optionnelle."""
    import os

    if not os.path.exists(image_path):
        add_body(doc, f"[Figure non disponible : {caption}]", italic=True)
        return

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run()
    run.add_picture(image_path, width=Cm(width_cm))

    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(2)
    cap.paragraph_format.space_after = Pt(2)
    cr = cap.add_run(caption)
    set_run_font(cr, bold=True, italic=True, size=Pt(11))

    if source:
        sp = doc.add_paragraph()
        sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sp.paragraph_format.space_after = Pt(8)
        sr = sp.add_run(source)
        set_run_font(sr, italic=True, size=Pt(9))

    doc.add_paragraph()

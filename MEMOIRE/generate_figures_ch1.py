# -*- coding: utf-8 -*-
"""Figures Chapitre I — style académique sobre, flèches précises, haute lisibilité."""
from __future__ import annotations

import shutil
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image

OUT = Path(r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\images\chapitre1")
OUT.mkdir(parents=True, exist_ok=True)

DPI = 400
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 13,
    "axes.unicode_minus": False,
    "figure.facecolor": "white",
})

BOX_FC = "#FFFFFF"
BOX_EC = "#000000"
ARROW_C = "#000000"
LW = 1.8
ARROW_LW = 2.2
ARROW_HEAD = 0.12
ARROW_SCALE = 14


def _arrow_head(ax, x_tip, y_tip, dx, dy):
    length = (dx ** 2 + dy ** 2) ** 0.5
    if length < 1e-6:
        return
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    base_x = x_tip - ux * ARROW_HEAD
    base_y = y_tip - uy * ARROW_HEAD
    half = ARROW_HEAD * 0.42
    ax.fill(
        [x_tip, base_x + px * half, base_x - px * half],
        [y_tip, base_y + py * half, base_y - py * half],
        color=ARROW_C, zorder=6, clip_on=False,
    )


def _draw_segment(ax, x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color=ARROW_C, linewidth=ARROW_LW,
            solid_capstyle="butt", zorder=5, clip_on=False)


def _save(fig, name: str):
    path = OUT / name
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.4,
                facecolor="white", edgecolor="none")
    plt.close(fig)
    print(f"  -> {path.name}")


class B:
    """Rectangle avec ancres pour flèches précises."""
    __slots__ = ("x", "y", "w", "h")

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2

    @property
    def top(self):
        return self.y + self.h

    @property
    def bottom(self):
        return self.y

    @property
    def right(self):
        return self.x + self.w

    @property
    def left(self):
        return self.x


def _draw_rect(ax, box: B, text, fs=10, bold_title=None, lw=LW):
    ax.add_patch(Rectangle(
        (box.x, box.y), box.w, box.h,
        linewidth=lw, edgecolor=BOX_EC, facecolor=BOX_FC, zorder=2,
    ))
    if bold_title:
        ax.text(box.cx, box.y + box.h * 0.68, bold_title, ha="center", va="center",
                fontsize=fs, fontweight="bold", zorder=3)
        ax.text(box.cx, box.y + box.h * 0.30, text, ha="center", va="center",
                fontsize=fs - 0.5, zorder=3)
    else:
        ax.text(box.cx, box.cy, text, ha="center", va="center", fontsize=fs, zorder=3)


def _arrow_v(ax, x, y_from, y_to):
    """Flèche verticale précise avec pointe à l'arrivée."""
    if abs(y_to - y_from) < 0.05:
        return
    direction = 1 if y_to > y_from else -1
    tip_y = y_to
    base_y = tip_y - direction * ARROW_HEAD
    y_tail = y_from + direction * 0.04
    if direction > 0:
        seg_y1, seg_y2 = y_tail, base_y
    else:
        seg_y1, seg_y2 = base_y, y_tail
    _draw_segment(ax, x, seg_y1, x, seg_y2)
    _arrow_head(ax, x, tip_y, 0, direction)


def _arrow_h(ax, x_from, x_to, y):
    """Flèche horizontale précise avec pointe à l'arrivée."""
    if abs(x_to - x_from) < 0.05:
        return
    direction = 1 if x_to > x_from else -1
    tip_x = x_to
    base_x = tip_x - direction * ARROW_HEAD
    x_tail = x_from + direction * 0.04
    if direction > 0:
        seg_x1, seg_x2 = x_tail, base_x
    else:
        seg_x1, seg_x2 = base_x, x_tail
    _draw_segment(ax, seg_x1, y, seg_x2, y)
    _arrow_head(ax, tip_x, y, direction, 0)


def _arrow_down(ax, src: B, dst: B):
    _arrow_v(ax, src.cx, src.bottom, dst.top)


def _arrow_up(ax, lower: B, upper: B):
    """Flèche vers le haut, dans l'espace entre deux blocs."""
    _arrow_v(ax, lower.cx, lower.top, upper.bottom)


def _arrow_right(ax, src: B, dst: B):
    _arrow_h(ax, src.right, dst.left, src.cy)


def fig_i1_architecture_sigrh():
    fig, ax = plt.subplots(figsize=(8.5, 6.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 9)
    ax.axis("off")

    bw, bh, bx = 6.8, 1.35, 1.6
    gap = 0.85
    y1 = 1.2
    y2 = y1 + bh + gap
    y3 = y2 + bh + gap

    b1 = B(bx, y1, bw, bh)
    b2 = B(bx, y2, bw, bh)
    b3 = B(bx, y3, bw, bh)

    _draw_rect(ax, b3, "Tableau de bord, rapports et exports", bold_title="Couche de restitution")
    _draw_rect(ax, b2, "Règles métier, workflows,\ncircuits de validation, indicateurs",
               bold_title="Couche de traitement")
    _draw_rect(ax, b1, "Formulaires web, pointage biométrique,\nimport RFID",
               bold_title="Couche d'acquisition")

    _arrow_up(ax, b1, b2)
    _arrow_up(ax, b2, b3)
    _save(fig, "fig_i1_architecture_sigrh.png")


def fig_i2_architecture_sgrh_pro():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # Bande applicative
    r1 = B(0.4, 7.8, 2.4, 1.15)
    r2 = B(3.2, 7.8, 2.6, 1.15)
    r3 = B(6.2, 7.8, 2.8, 1.15)
    r4 = B(9.4, 7.8, 2.8, 1.15)

    _draw_rect(ax, r1, "Admin RH\nResponsable\nAgent", fs=9)
    _draw_rect(ax, r2, "Interface web\n(tableau de bord)", fs=9)
    _draw_rect(ax, r3, "Serveur API\nLaravel", fs=9)
    _draw_rect(ax, r4, "Base de\ndonnées", fs=9)

    _arrow_right(ax, r1, r2)
    _arrow_right(ax, r2, r3)
    _arrow_right(ax, r3, r4)

    ax.plot([0.2, 14.5], [6.9, 6.9], color="#666666", linewidth=1.0, linestyle="--")

    # Bande poste RH
    p1 = B(0.4, 4.5, 2.4, 1.15)
    p2 = B(3.2, 4.5, 2.8, 1.15)
    p3 = B(6.4, 4.5, 2.4, 1.15)
    p4 = B(9.2, 4.5, 3.0, 1.15)

    _draw_rect(ax, p1, "Poste du\nresponsable RH", fs=9)
    _draw_rect(ax, p2, "Service local\n(Bridge C#)", fs=9)
    _draw_rect(ax, p3, "Capteur\nZK-9500", fs=9)
    _draw_rect(ax, p4, "Carte RFID\net lecteur USB", fs=9)

    _arrow_right(ax, p1, p2)
    _arrow_right(ax, p2, p3)
    _arrow_right(ax, p3, p4)

    # Liaison API Laravel ↔ Bridge (verticale, entre les deux blocs centraux)
    _arrow_v(ax, r3.cx, r3.bottom, p2.top)

    _save(fig, "fig_i2_architecture_sgrh_pro.png")


def fig_i3_flux_biometrique():
    fig, ax = plt.subplots(figsize=(7.5, 10.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis("off")

    steps = [
        "Création du dossier agent",
        "Lancement de l'enrôlement (service RH)",
        "Transmission vers le service local (Bridge)",
        "Capture de l'empreinte (ZK-9500)",
        "Enregistrement du modèle en base",
        "Attribution de la carte RFID",
        "Pointage quotidien (présences)",
    ]

    bw, bh = 5.8, 0.95
    bx = (10 - bw) / 2
    gap = 0.5
    y = 10.8

    boxes = []
    for i, label in enumerate(steps):
        b = B(bx, y - bh, bw, bh)
        _draw_rect(ax, b, f"{i + 1}. {label}", fs=9)
        boxes.append(b)
        y -= bh + gap

    for i in range(len(boxes) - 1):
        _arrow_down(ax, boxes[i], boxes[i + 1])

    _save(fig, "fig_i3_flux_biometrique.png")


def fig_i4_rbac():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7)
    ax.axis("off")

    roles = [
        ("Admin. système", "Paramétrage\ncomplet"),
        ("Admin RH", "Personnel, présences,\nadministration"),
        ("Responsable", "Congés,\nprésences"),
        ("Employé", "Consultation\npersonnelle"),
    ]
    rw, rh = 2.3, 1.6
    y_role = 4.0
    x0 = 0.4
    role_boxes = []

    for i, (title, desc) in enumerate(roles):
        b = B(x0 + i * 2.55, y_role, rw, rh)
        _draw_rect(ax, b, desc, fs=9, bold_title=title)
        role_boxes.append(b)

    auth = B(1.5, 1.2, 7.8, 1.1)
    _draw_rect(ax, auth,
               "Authentification et droits d'accès\n(journal des opérations sensibles)",
               fs=10)

    for b in role_boxes:
        _arrow_v(ax, b.cx, b.bottom, auth.top)

    _save(fig, "fig_i4_rbac.png")


def fig_i5_rfid_photos():
    card_path = OUT / "carte rfid.jpg"
    reader_path = OUT / "lecteur rfid.jpg"
    out_path = OUT / "fig_i5_rfid_principe.png"
    if not card_path.exists() or not reader_path.exists():
        print("  -> fig_i5 : photos RFID absentes")
        return

    card = Image.open(card_path).convert("RGB")
    reader = Image.open(reader_path).convert("RGB")
    h = 420

    def rh(img):
        r = h / img.height
        return img.resize((int(img.width * r), h), Image.LANCZOS)

    card, reader = rh(card), rh(reader)
    pad = 60
    canvas = Image.new(
        "RGB",
        (pad + card.width + pad + reader.width + pad, h + 2 * pad),
        "white",
    )
    canvas.paste(card, (pad, pad))
    canvas.paste(reader, (pad + card.width + pad, pad))
    canvas.save(out_path, quality=95)
    print(f"  -> {out_path.name}")


def fig_i6_use_photo():
    src = OUT / "figi6_zkteco9500.png"
    dst = OUT / "fig_i6_zkteco9500.png"
    if src.exists():
        shutil.copy2(src, dst)
        print(f"  -> {dst.name}")
    elif not dst.exists():
        print("  -> fig_i6 : photo ZK-9500 absente")


def fig_i7_cycle_grh():
    fig, ax = plt.subplots(figsize=(12, 4.8))
    ax.set_xlim(0, 14.5)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    phases = [
        "Recrutement", "Intégration", "Administration",
        "Temps et\nprésence", "Formation", "Évaluation", "Archivage",
    ]
    bw, bh, gap = 1.45, 1.0, 0.32
    total_w = len(phases) * bw + (len(phases) - 1) * gap
    x = (14.5 - total_w) / 2
    y = 1.8
    prev = None

    for phase in phases:
        b = B(x, y, bw, bh)
        _draw_rect(ax, b, phase, fs=9)
        if prev is not None:
            _arrow_right(ax, prev, b)
        prev = b
        x += bw + gap

    _save(fig, "fig_i7_cycle_grh.png")


def fig_i8_generations_sigrh():
    fig, ax = plt.subplots(figsize=(12, 4.8))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 5.5)
    ax.axis("off")

    gens = [
        ("1re génération\n(1960-1970)", "Paie\n(mainframe)"),
        ("2e génération\n(1980-1990)", "Administration\n(monolithique)"),
        ("3e génération\n(2000-2010)", "Portail web\n(self-service)"),
        ("4e génération\n(2015+)", "Analytics\net expérience\nemployé"),
    ]
    bw, bh, gap = 3.1, 1.45, 0.5
    x = 0.5
    y = 2.0
    prev = None

    for period, content in gens:
        b = B(x, y, bw, bh)
        _draw_rect(ax, b, content, fs=9, bold_title=period)
        if prev is not None:
            _arrow_right(ax, prev, b)
        prev = b
        x += bw + gap

    _save(fig, "fig_i8_generations_sigrh.png")


def fig_i9_si_donnees_flux():
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 4.8)
    ax.axis("off")

    blocks = [
        ("Données brutes", "Pointages, saisies,\nformulaires"),
        ("Traitement", "Règles métier,\nagrégations"),
        ("Information", "KPI, états,\nalertes"),
        ("Décision", "Validation,\npilotage RH"),
    ]
    bw, bh, gap = 2.6, 1.25, 0.5
    x = 0.4
    y = 1.5
    prev = None

    for title, detail in blocks:
        b = B(x, y, bw, bh)
        _draw_rect(ax, b, detail, fs=9, bold_title=title)
        if prev is not None:
            _arrow_right(ax, prev, b)
        prev = b
        x += bw + gap

    _save(fig, "fig_i9_si_donnees_flux.png")


def main():
    print("Regeneration figures Chapitre I...")
    fig_i1_architecture_sigrh()
    fig_i2_architecture_sgrh_pro()
    fig_i3_flux_biometrique()
    fig_i4_rbac()
    fig_i5_rfid_photos()
    fig_i6_use_photo()
    fig_i7_cycle_grh()
    fig_i8_generations_sigrh()
    fig_i9_si_donnees_flux()
    print("Termine.")


if __name__ == "__main__":
    main()

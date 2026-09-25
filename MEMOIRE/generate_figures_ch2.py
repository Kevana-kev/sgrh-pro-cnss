# -*- coding: utf-8 -*-
"""Figures Chapitre II — style académique, flèches précises, haute lisibilité."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = Path(r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\images\chapitre2")
OUT.mkdir(parents=True, exist_ok=True)

DPI = 400
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 13,
    "axes.unicode_minus": False,
    "figure.facecolor": "white",
})

BOX_EC = "#000000"
ARROW_C = "#000000"
MUTED = "#444444"
LW = 1.8
ARROW_LW = 2.2
ARROW_HEAD = 0.12
ARROW_SCALE = 14
ZONE_EC = "#666666"


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


def _draw(ax, box: B, text, fs=10, bold_title=None):
    ax.add_patch(Rectangle(
        (box.x, box.y), box.w, box.h,
        linewidth=LW, edgecolor=BOX_EC, facecolor="white", zorder=2,
    ))
    if bold_title:
        ax.text(box.cx, box.y + box.h * 0.68, bold_title, ha="center", va="center",
                fontsize=fs, fontweight="bold", zorder=3)
        ax.text(box.cx, box.y + box.h * 0.28, text, ha="center", va="center",
                fontsize=fs - 0.5, zorder=3)
    else:
        ax.text(box.cx, box.cy, text, ha="center", va="center", fontsize=fs, zorder=3)


def _arrow_v(ax, x, y_from, y_to):
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


def _arrow_right(ax, src: B, dst: B):
    _arrow_h(ax, src.right, dst.left, src.cy)


def _arrow_connect_lr(ax, src: B, dst: B):
    """Connexion horizontale avec coude si les centres ne sont pas alignés."""
    if abs(src.cy - dst.cy) < 0.2:
        _arrow_h(ax, src.right, dst.left, src.cy)
        return
    mid_x = (src.right + dst.left) / 2
    _draw_segment(ax, src.right + 0.04, src.cy, mid_x, src.cy)
    _draw_segment(ax, mid_x, src.cy, mid_x, dst.cy)
    _arrow_h(ax, mid_x, dst.left, dst.cy)


def fig_ii1_organigramme():
    """Organigramme CNSS — arborescence claire, bureaux sous DRH uniquement."""
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 12)
    ax.axis("off")

    # Niveau 1 — Direction générale
    dg = B(5.0, 10.2, 4.0, 0.95)
    _draw(ax, dg, "", bold_title="Direction générale")

    # Niveau 2 — Directions
    dir_w, dir_h = 2.9, 1.15
    dir_y = 8.0
    dirs_data = [
        (0.5, "Direction\nadministrative\net financière"),
        (3.7, "Direction des\nressources\nhumaines"),
        (6.9, "Direction\ntechnique\net informatique"),
        (10.1, "Directions\nmétier"),
    ]
    dir_boxes = []
    for x, label in dirs_data:
        b = B(x, dir_y, dir_w, dir_h)
        _draw(ax, b, label, fs=9)
        dir_boxes.append(b)
        _arrow_down(ax, dg, b)

    drh = dir_boxes[1]

    # Barre horizontale sous DRH
    bus_y = 7.0
    bur_left = 1.0
    bur_right = 11.8
    ax.plot([bur_left, bur_right], [bus_y, bus_y], color=ARROW_C, linewidth=LW, zorder=1)
    _arrow_v(ax, drh.cx, drh.bottom, bus_y)

    # Niveau 3 — Bureaux DRH
    bur_w, bur_h = 2.6, 1.0
    bur_y = 5.5
    bureaux = [
        (1.0, "Bureau gestion\ndu personnel"),
        (3.9, "Bureau administration\net transmission"),
        (6.8, "Bureau formation\net compétences"),
        (9.7, "Bureau discipline\net contentieux"),
    ]
    for x, label in bureaux:
        b = B(x, bur_y, bur_w, bur_h)
        _draw(ax, b, label, fs=8.5)
        _arrow_v(ax, b.cx, bus_y, b.top)

    # Niveau 4 — Personnel
    pers = B(2.5, 3.5, 9.0, 1.0)
    _draw(ax, pers,
          "Agents du siège central (administratif, technique, encadrement)",
          fs=9, bold_title="Personnel encadré par la DRH")
    # Liaison bureaux → personnel (centrée sur le bloc personnel)
    _arrow_v(ax, pers.cx, bur_y, pers.top)

    _save(fig, "fig_ii1_organigramme_cnss.png")


def fig_ii2_processus_actuel():
    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    steps = [
        "Registre\npapier", "Fichier\nExcel", "Consolidation\nadministrative",
        "État administratif\nimprimé", "Archivage\nphysique",
    ]
    bw, bh, gap = 2.3, 1.25, 0.45
    x0 = 0.4
    y = 2.4

    for i, label in enumerate(steps):
        b = B(x0 + i * (bw + gap), y, bw, bh)
        _draw(ax, b, label, fs=9.5)
        if i < len(steps) - 1:
            x_mid = b.right + gap / 2
            ax.plot([b.right + 0.08, b.right + gap - 0.08],
                    [b.cy, b.cy], color=MUTED, linewidth=1.0, linestyle=":", zorder=1)
            ax.text(x_mid, b.cy, "×", ha="center", va="center",
                    fontsize=14, color=MUTED, fontweight="bold", zorder=4)

    ax.text(7.5, 4.5, "Absence de liaison automatique entre les supports",
            ha="center", fontsize=11, fontweight="bold")
    ax.text(7.5, 0.6,
            "Conséquence : saisies multiples, risque d'erreurs, pas de source unique de vérité",
            ha="center", fontsize=10, style="italic")

    _save(fig, "fig_ii2_processus_actuel.png")


def fig_ii3_pointage_comparatif():
    fig, ax = plt.subplots(figsize=(11.5, 6.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis("off")

    ax.add_patch(Rectangle((0.3, 0.6), 5.4, 6.8, linewidth=1.2,
                           edgecolor="#888888", facecolor="none", linestyle="--"))
    ax.add_patch(Rectangle((6.3, 0.6), 5.4, 6.8, linewidth=1.2,
                           edgecolor="#888888", facecolor="none", linestyle="--"))

    ax.text(3.0, 7.2, "Situation actuelle", ha="center", fontsize=12, fontweight="bold")
    ax.text(9.0, 7.2, "Situation cible", ha="center", fontsize=12, fontweight="bold")

    left = [
        "Registre signé\nà l'accueil", "Relevé manuel\nen fin de mois",
        "Consolidation\nExcel", "Validation\nverbale RH",
    ]
    right = [
        "Pointage ZK-9500\n(empreinte digitale)", "Enregistrement\nautomatique (API)",
        "Calcul retards\net heures", "Tableau de bord\nRH actualisé",
    ]

    bw, bh, gap = 4.3, 0.95, 0.5
    y = 6.0
    prev_l = prev_r = None
    for i in range(4):
        bl = B(0.85, y - bh, bw, bh)
        br = B(6.85, y - bh, bw, bh)
        _draw(ax, bl, left[i], fs=9)
        _draw(ax, br, right[i], fs=9)
        if prev_l is not None:
            _arrow_v(ax, prev_l.cx, prev_l.bottom, bl.top)
            _arrow_v(ax, prev_r.cx, prev_r.bottom, br.top)
        prev_l, prev_r = bl, br
        y -= bh + gap

    _save(fig, "fig_ii3_pointage_comparatif.png")


def fig_ii4_workflow_conge():
    fig, ax = plt.subplots(figsize=(12, 3.8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4.5)
    ax.axis("off")

    roles = ["Agent", "Responsable\nde service", "Admin RH", "Notification"]
    sub = ["(demande en ligne)", "(avis)", "(décision)", "(agent + archives)"]

    bw, bh, gap = 2.6, 1.15, 0.55
    n = len(roles)
    total_w = n * bw + (n - 1) * gap
    x = (14 - total_w) / 2
    y = 1.4
    prev = None

    for title, detail in zip(roles, sub):
        b = B(x, y, bw, bh)
        _draw(ax, b, detail, fs=8.5, bold_title=title)
        if prev is not None:
            _arrow_right(ax, prev, b)
        prev = b
        x += bw + gap

    _save(fig, "fig_ii4_workflow_conge.png")


def fig_ii5_modules():
    """Architecture modulaire — huit modules recentrés + socle commun."""
    fig, ax = plt.subplots(figsize=(12.5, 8.5))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9.5)
    ax.axis("off")

    bw, bh, gap = 2.35, 0.95, 0.28
    bw_z2, gap_z2 = 2.15, 0.22
    zone_pad_x, zone_pad_y = 0.22, 0.32
    bus_y = 1.85

    zones = [
        (
            "Zone 1 — Identification et contrôle d'accès",
            [[("M1", "Utilisateurs\net accès"), ("M2", "Employés"), ("M3", "Biométrie\nRFID")]],
        ),
        (
            "Zone 2 — Présences, rémunération, évaluation et pilotage",
            [[
                ("M4", "Présences"), ("M5", "Congés"), ("M6", "Éléments\nrémunération"),
                ("M7", "Évaluation"), ("M8", "Tableaux\nde bord"),
            ]],
        ),
    ]

    module_boxes = []
    y_cursor = 8.6

    for title, rows in zones:
        row_dims = []
        for row in rows:
            rw, rg = (bw_z2, gap_z2) if len(row) > 3 else (bw, gap)
            row_dims.append((rw, rg))
        row_widths = [len(r) * rw + (len(r) - 1) * rg for r, (rw, rg) in zip(rows, row_dims)]
        zone_w = max(row_widths) + 2 * zone_pad_x
        zone_h = len(rows) * bh + (len(rows) - 1) * 0.22 + 2 * zone_pad_y + 0.35
        x_zone = (14 - zone_w) / 2
        y_zone = y_cursor - zone_h

        ax.add_patch(Rectangle(
            (x_zone, y_zone), zone_w, zone_h,
            linewidth=1.1, edgecolor=ZONE_EC, facecolor="none",
            linestyle="--", zorder=1,
        ))
        ax.text(x_zone + 0.15, y_zone + zone_h - 0.15, title,
                ha="left", va="top", fontsize=9, fontweight="bold", color=ZONE_EC)

        y_row = y_zone + zone_h - zone_pad_y - 0.35 - bh
        for row, (rw, rg) in zip(rows, row_dims):
            grid_w = len(row) * rw + (len(row) - 1) * rg
            x0 = (14 - grid_w) / 2
            for i, (code, label) in enumerate(row):
                b = B(x0 + i * (rw + rg), y_row, rw, bh)
                _draw(ax, b, label, fs=8, bold_title=code)
                module_boxes.append(b)
            y_row -= bh + 0.22

        y_cursor = y_zone - 0.45

    socle = B(1.0, 0.4, 12.0, 1.1)
    _draw(ax, socle,
          "Base de données centralisée — API REST — interface web",
          fs=10, bold_title="Socle technique commun")

    ax.plot([0.7, 13.3], [bus_y, bus_y], color=ARROW_C, linewidth=ARROW_LW, zorder=6)
    for b in module_boxes:
        _arrow_v(ax, b.cx, b.bottom, bus_y)
    _arrow_v(ax, 7.0, bus_y, socle.top)

    _save(fig, "fig_ii5_modules_sgrh_pro.png")


def fig_ii6_acteurs():
    """Acteurs humains et composants techniques — flèches horizontales nettes."""
    fig, ax = plt.subplots(figsize=(11.5, 6.0))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.2)
    ax.axis("off")

    core = B(4.7, 1.85, 3.9, 3.5)
    _draw(ax, core, "SGRH Pro\n(API + base de données)", fs=11)

    bw, bh = 2.35, 0.95
    lx = 0.5
    left_items = [
        (5.25, "Admin RH"),
        (3.55, "Responsable\nde service"),
        (1.85, "Agent"),
    ]
    for y, label in left_items:
        b = B(lx, y - bh / 2, bw, bh)
        _draw(ax, b, label, fs=10)
        _arrow_h(ax, b.right, core.left, b.cy)

    rx = 9.15
    right_items = [
        (5.25, "Bridge\nbiométrique"),
        (3.55, "Capteur\nZK-9500"),
        (1.85, "Lecteur\nRFID"),
    ]
    for y, label in right_items:
        b = B(rx, y - bh / 2, bw, bh)
        _draw(ax, b, label, fs=10)
        # Périphériques → backend (événements horodatés)
        _arrow_h(ax, b.left, core.right, b.cy)

    _save(fig, "fig_ii6_acteurs_systeme.png")


def main():
    print("Regeneration figures Chapitre II...")
    fig_ii1_organigramme()
    fig_ii2_processus_actuel()
    fig_ii3_pointage_comparatif()
    fig_ii4_workflow_conge()
    fig_ii5_modules()
    fig_ii6_acteurs()
    print("Termine.")


if __name__ == "__main__":
    main()

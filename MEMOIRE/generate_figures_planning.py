# -*- coding: utf-8 -*-
"""
Figures planification — modèle MPM identique aux exemples de mémoire (SI / CHB).
Nœuds : deux cases de dates en haut + libellé en bas. Durée sur la flèche.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = Path(r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\images\planification")
OUT.mkdir(parents=True, exist_ok=True)

DPI = 400
LW = 1.6
ARROW_LW = 2.2
ARROW_SCALE = 20
ARROW_HEAD = 0.14
LABEL_OFFSET = 0.14
EC = "#000000"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 12,
    "axes.unicode_minus": False,
    "figure.facecolor": "white",
})

TASKS = {
    "A": {"label": "Analyse système actuel", "dur": 14, "pred": []},
    "B": {"label": "Spécification besoins", "dur": 6, "pred": ["A"]},
    "C": {"label": "Conception UML", "dur": 9, "pred": ["B"]},
    "D": {"label": "Modèle BDD", "dur": 3, "pred": ["C"]},
    "E": {"label": "Backend Laravel", "dur": 13, "pred": ["D"]},
    "F": {"label": "Frontend web", "dur": 9, "pred": ["E"]},
    "G": {"label": "Bridge biométrique", "dur": 6, "pred": ["D"]},
    "H": {"label": "Intégration ZK/RFID", "dur": 6, "pred": ["E", "G"]},
    "I": {"label": "Tests validation", "dur": 6, "pred": ["F", "H"]},
    "J": {"label": "Déploiement prototype", "dur": 3, "pred": ["I"]},
}

CRITICAL = ["A", "B", "C", "D", "E", "F", "I", "J"]
GANTT_COLOR = "#6FA8DC"
GANTT_CRITICAL = "#2E5C8A"
GANTT_FLOAT = "#A8C8E8"
PROJECT_START = datetime(2026, 7, 1)


def _compute_mpm():
    es, ef = {}, {}
    for code in sorted(TASKS):
        t = TASKS[code]
        es[code] = max((ef[p] for p in t["pred"]), default=0)
        ef[code] = es[code] + t["dur"]
    end = max(ef.values())
    lf, ls = {}, {}
    for code in reversed(list(TASKS)):
        succ = [c for c, d in TASKS.items() if code in d["pred"]]
        lf[code] = min((ls[s] for s in succ), default=end)
        ls[code] = lf[code] - TASKS[code]["dur"]
    return es, ef, ls, lf, end


ES, EF, LS, LF, PROJECT_END = _compute_mpm()
TOTAL_DAYS = PROJECT_END


def _save(fig, name: str):
    path = OUT / name
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.25,
                facecolor="white", edgecolor="none")
    plt.close(fig)
    print(f"  -> {path.name}")


class Box:
    """Boîte MPM avec ancres."""

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
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.w


def _draw_node(ax, box: Box, d_left: int, d_right: int, label: str):
    """Nœud style exemple SI : 2 cases dates + libellé."""
    x, y, w, h = box.x, box.y, box.w, box.h
    split = y + h * 0.48

    ax.add_patch(Rectangle((x, y), w, h, linewidth=LW, edgecolor=EC,
                           facecolor="white", zorder=2))
    ax.plot([x, x + w], [split, split], color=EC, linewidth=LW, zorder=3)
    ax.plot([x + w / 2, x + w / 2], [split, y + h], color=EC, linewidth=LW, zorder=3)

    ax.text(x + w * 0.25, y + h * 0.74, str(d_left), ha="center", va="center",
            fontsize=9.5, fontweight="bold", zorder=4)
    ax.text(x + w * 0.75, y + h * 0.74, str(d_right), ha="center", va="center",
            fontsize=9.5, fontweight="bold", zorder=4)
    ax.text(box.cx, y + h * 0.22, label, ha="center", va="center",
            fontsize=10, fontweight="bold", zorder=4)


def _arrow_head(ax, x_tip, y_tip, dx, dy):
    """Pointe de flèche triangulaire nette."""
    length = (dx ** 2 + dy ** 2) ** 0.5
    if length < 1e-6:
        return
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    base_x = x_tip - ux * ARROW_HEAD
    base_y = y_tip - uy * ARROW_HEAD
    half = ARROW_HEAD * 0.42
    tri_x = [x_tip, base_x + px * half, base_x - px * half]
    tri_y = [y_tip, base_y + py * half, base_y - py * half]
    ax.fill(tri_x, tri_y, color=EC, zorder=6, clip_on=False)


def _draw_segment(ax, x1, y1, x2, y2, with_head: bool = False):
    """Trait droit entre deux points ; pointe optionnelle à l'arrivée."""
    ax.plot([x1, x2], [y1, y2], color=EC, linewidth=ARROW_LW,
            solid_capstyle="butt", zorder=5, clip_on=False)
    if with_head:
        _arrow_head(ax, x2, y2, x2 - x1, y2 - y1)


def _label_on_link(ax, x, y, label: str, horizontal: bool = True):
    """Durée au-dessus / à côté de la liaison, sans masquer la flèche."""
    if not label:
        return
    if horizontal:
        ax.text(x, y + LABEL_OFFSET, label, ha="center", va="bottom",
                fontsize=9.5, fontweight="bold", zorder=7, clip_on=False)
    else:
        ax.text(x + LABEL_OFFSET, y, label, ha="left", va="center",
                fontsize=9.5, fontweight="bold", zorder=7, clip_on=False)


def _arrow_h(ax, x1, x2, y, label: str = ""):
    """Flèche horizontale précise bord à bord."""
    if abs(x2 - x1) < 0.05:
        return
    x_start = min(x1, x2)
    x_end = max(x1, x2)
    direction = 1 if x2 >= x1 else -1
    tip_x = x_end if direction > 0 else x_start
    tail_x = x_start if direction > 0 else x_end
    base_x = tip_x - direction * ARROW_HEAD
    _draw_segment(ax, tail_x, y, base_x, y, with_head=False)
    _arrow_head(ax, tip_x, y, direction, 0)
    _label_on_link(ax, (tail_x + tip_x) / 2, y, label, horizontal=True)


def _arrow_v(ax, x, y1, y2, label: str = ""):
    """Flèche verticale précise bord à bord."""
    if abs(y2 - y1) < 0.05:
        return
    y_lo, y_hi = min(y1, y2), max(y1, y2)
    direction = 1 if y2 >= y1 else -1
    tip_y = y_hi if direction > 0 else y_lo
    tail_y = y_lo if direction > 0 else y_hi
    base_y = tip_y - direction * ARROW_HEAD
    _draw_segment(ax, x, tail_y, x, base_y, with_head=False)
    _arrow_head(ax, x, tip_y, 0, direction)
    _label_on_link(ax, x, (tail_y + tip_y) / 2, label, horizontal=False)


def _arrow_polyline(ax, points: list[tuple[float, float]], label: str = "",
                    label_xy: tuple[float, float] | None = None):
    """Polyligne à angles droits avec pointe à l'arrivée."""
    if len(points) < 2:
        return
    for i in range(len(points) - 2):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        _draw_segment(ax, x1, y1, x2, y2, with_head=False)
    x1, y1 = points[-2]
    x2, y2 = points[-1]
    dx, dy = x2 - x1, y2 - y1
    length = (dx ** 2 + dy ** 2) ** 0.5
    if length < 1e-6:
        return
    ux, uy = dx / length, dy / length
    base_x = x2 - ux * ARROW_HEAD
    base_y = y2 - uy * ARROW_HEAD
    _draw_segment(ax, x1, y1, base_x, base_y, with_head=False)
    _arrow_head(ax, x2, y2, dx, dy)
    if label:
        lx, ly = label_xy if label_xy else ((x1 + x2) / 2, (y1 + y2) / 2)
        ax.text(lx, ly + LABEL_OFFSET, label, ha="center", va="bottom",
                fontsize=9.5, fontweight="bold", zorder=7, clip_on=False)


def _arrow_ortho(ax, x1, y1, x2, y2, label: str = "", vertical_first: bool = True):
    """Liaison orthogonale nette (coude à angle droit + pointe)."""
    if abs(y1 - y2) < 0.05:
        _arrow_h(ax, x1, x2, y1, label)
        return
    if abs(x1 - x2) < 0.05:
        _arrow_v(ax, x1, y1, y2, label)
        return

    if vertical_first:
        _draw_segment(ax, x1, y1, x1, y2, with_head=False)
        x_dir = 1 if x2 > x1 else -1
        tip_x = x2
        base_x = tip_x - x_dir * ARROW_HEAD
        if x_dir > 0:
            seg_x1, seg_x2 = x1, base_x
        else:
            seg_x1, seg_x2 = base_x, x1
        _draw_segment(ax, seg_x1, y2, seg_x2, y2, with_head=False)
        _arrow_head(ax, tip_x, y2, x_dir, 0)
        if label:
            ax.text((x1 + x2) / 2, y2 + LABEL_OFFSET, label,
                    ha="center", va="bottom", fontsize=9.5, fontweight="bold",
                    zorder=7, clip_on=False)
    else:
        _draw_segment(ax, x1, y1, x2, y1, with_head=False)
        y_dir = 1 if y2 > y1 else -1
        tip_y = y2
        base_y = tip_y - y_dir * ARROW_HEAD
        if y_dir > 0:
            seg_y1, seg_y2 = y1, base_y
        else:
            seg_y1, seg_y2 = base_y, y1
        _draw_segment(ax, x2, seg_y1, x2, seg_y2, with_head=False)
        _arrow_head(ax, x2, tip_y, 0, y_dir)
        if label:
            ax.text(x2 + LABEL_OFFSET, (y1 + y2) / 2, label,
                    ha="left", va="center", fontsize=9.5, fontweight="bold",
                    zorder=7, clip_on=False)


def _place_row(ax, codes, times, x0, y, nw, nh, gap):
    """Place une rangée de nœuds de gauche à droite."""
    nodes = {}
    x = x0
    for code in codes:
        b = Box(x, y, nw, nh)
        d1, d2 = times[code]
        _draw_node(ax, b, d1, d2, code)
        nodes[code] = b
        x += nw + gap
    return nodes


def fig_pert():
    """Graphe PERT — disposition latérale (gauche → droite), modèle exemple SI."""
    fig, ax = plt.subplots(figsize=(16, 5.2))
    ax.set_xlim(0, 21)
    ax.set_ylim(0, 7)
    ax.axis("off")

    nw, nh = 1.25, 1.0
    gap = 0.48
    y_main = 4.6
    y_low = 2.3

    times_main = {"DEBUT": (0, 0), "FIN": (PROJECT_END, PROJECT_END)}
    for code in ["A", "B", "C", "D", "E", "F", "I", "J"]:
        times_main[code] = (ES[code], LS[code])
    order = ["DEBUT", "A", "B", "C", "D", "E", "F", "I", "J", "FIN"]
    nodes = _place_row(ax, order, times_main, 0.35, y_main, nw, nh, gap)

    nodes["G"] = Box(nodes["D"].x, y_low, nw, nh)
    _draw_node(ax, nodes["G"], ES["G"], LS["G"], "G")
    nodes["H"] = Box(nodes["E"].x, y_low, nw, nh)
    _draw_node(ax, nodes["H"], ES["H"], LS["H"], "H")

    cy = y_main + nh / 2

    # Chaîne principale — durée sur chaque liaison
    chain = ["DEBUT", "A", "B", "C", "D", "E", "F", "I", "J", "FIN"]
    for i in range(len(chain) - 1):
        a, b = chain[i], chain[i + 1]
        dur = "0" if a == "DEBUT" else str(TASKS[a]["dur"])
        _arrow_h(ax, nodes[a].right, nodes[b].left, cy, dur)

    # Branches parallèles G / H
    _arrow_v(ax, nodes["D"].cx, nodes["D"].bottom, nodes["G"].top, "")
    _arrow_v(ax, nodes["E"].cx, nodes["E"].bottom, nodes["H"].top, "")
    _arrow_h(ax, nodes["G"].right, nodes["H"].left, y_low + nh / 2,
             str(TASKS["G"]["dur"]))
    y_lane = y_low + nh + (y_main - (y_low + nh)) * 0.42
    _arrow_polyline(
        ax,
        [
            (nodes["H"].cx, nodes["H"].top),
            (nodes["H"].cx, y_lane),
            (nodes["I"].cx, y_lane),
            (nodes["I"].cx, nodes["I"].bottom),
        ],
        str(TASKS["H"]["dur"]),
        label_xy=((nodes["H"].cx + nodes["I"].cx) / 2, y_lane),
    )

    _save(fig, "fig_pert_sgrh_pro.png")


def fig_chemin_critique():
    """Chaîne linéaire horizontale — modèle exemple SI (gauche → droite)."""
    fig, ax = plt.subplots(figsize=(16, 4.2))
    ax.set_xlim(0, 21)
    ax.set_ylim(0, 4.5)
    ax.axis("off")

    nw, nh = 1.25, 1.0
    gap = 0.48
    y = 1.6

    chain = [("DEBUT", 0)]
    for code in ["A", "B", "C", "D", "E", "F", "I", "J"]:
        chain.append((code, ES[code]))
    chain.append(("FIN", PROJECT_END))

    boxes = []
    x = 0.35
    for label, t in chain:
        b = Box(x, y, nw, nh)
        _draw_node(ax, b, t, t, label)
        boxes.append(b)
        x += nw + gap

    cy = y + nh / 2
    for i in range(len(boxes) - 1):
        dur = "0" if chain[i][0] == "DEBUT" else str(TASKS[chain[i][0]]["dur"])
        _arrow_h(ax, boxes[i].right, boxes[i + 1].left, cy, dur)

    _save(fig, "fig_chemin_critique_sgrh_pro.png")


def _add_business_days(start: datetime, days: int) -> datetime:
    d, added = start, 0
    while added < days:
        d += timedelta(days=1)
        if d.weekday() < 5:
            added += 1
    return d


def fig_gantt():
    """Gantt — barres par tâche, chemin critique en bleu foncé."""
    fig, ax = plt.subplots(figsize=(14.5, 8.4))

    rows = []
    for code in sorted(TASKS):
        t = TASKS[code]
        start = _add_business_days(PROJECT_START, ES[code])
        end = _add_business_days(PROJECT_START, EF[code])
        margin = LS[code] - ES[code]
        rows.append((code, t["label"], start, end, margin))

    n = len(rows)
    end_project = _add_business_days(PROJECT_START, TOTAL_DAYS)
    ax.set_xlim(PROJECT_START - timedelta(days=3),
                end_project + timedelta(days=6))
    ax.set_ylim(-0.7, n + 0.4)
    ax.invert_yaxis()

    for i, (code, label, start, end, margin) in enumerate(rows):
        s, e = mdates.date2num(start), mdates.date2num(end)
        color = GANTT_CRITICAL if margin == 0 else GANTT_FLOAT
        ax.barh(i, e - s, left=s, height=0.55, color=color,
                edgecolor="#1a1a1a", linewidth=1.0)
        dur = TASKS[code]["dur"]
        ax.text(s - 1.0, i, code, ha="right", va="center",
                fontsize=10, fontweight="bold")
        mid = s + (e - s) / 2
        ax.text(mid, i, f"{dur} j", ha="center", va="center",
                fontsize=8, color="white", fontweight="bold")
        ax.text(e + 1.2, i, label, ha="left", va="center", fontsize=8.5)

    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0, interval=1))
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=0, interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.grid(axis="x", linestyle="--", alpha=0.4, linewidth=0.7)
    ax.set_xlabel("Calendrier (jours ouvrés, juil. 2026 – sept. 2026)", fontsize=10)
    ax.set_ylabel("Tâches du projet", fontsize=10)
    ax.set_yticks([])
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)

    ax.set_title(
        f"Diagramme de Gantt — Projet SGRH Pro ({TOTAL_DAYS} jours ouvrés)\n"
        f"{PROJECT_START.strftime('%d/%m/%Y')}  →  {end_project.strftime('%d/%m/%Y')}",
        fontsize=10, fontweight="bold", pad=10,
    )
    _save(fig, "fig_gantt_sgrh_pro.png")


def main():
    print("Regeneration figures planification (modele exemple SI)...")
    fig_pert()
    fig_chemin_critique()
    fig_gantt()
    print("Termine.")


if __name__ == "__main__":
    main()

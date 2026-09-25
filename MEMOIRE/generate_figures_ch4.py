# -*- coding: utf-8 -*-
"""
Figures Chapitre IV — emplacements réservés aux captures d'écran.
Fond blanc, cadre noir, bordure intérieure en pointillés.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = Path(r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\images\chapitre4")
OUT.mkdir(parents=True, exist_ok=True)

DPI = 400
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 12,
    "axes.unicode_minus": False,
    "figure.facecolor": "white",
})

BOX_EC = "#000000"
LW = 1.6


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


def _save(fig, name: str):
    path = OUT / name
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.25,
                facecolor="white", edgecolor="none")
    plt.close(fig)
    print(f"  -> {path.name}")


def _placeholder(filename: str, screen_name: str):
    fig, ax = plt.subplots(figsize=(13.5, 8.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.4)
    ax.axis("off")

    outer = B(0.35, 0.35, 9.30, 5.70)
    ax.add_patch(Rectangle(
        (outer.x, outer.y), outer.w, outer.h,
        linewidth=LW, edgecolor=BOX_EC, facecolor="white", zorder=2,
    ))
    inset = 0.28
    ax.add_patch(Rectangle(
        (outer.x + inset, outer.y + inset),
        outer.w - 2 * inset, outer.h - 2 * inset,
        linewidth=1.2, edgecolor=BOX_EC, facecolor="white",
        linestyle="--", zorder=3,
    ))
    ax.text(outer.cx, outer.cy + 0.35, "ESPACE RÉSERVÉ",
            ha="center", va="center", fontsize=18, fontweight="bold", zorder=4)
    ax.text(outer.cx, outer.cy - 0.35, screen_name,
            ha="center", va="center", fontsize=13, style="italic", zorder=4)
    _save(fig, filename)


def main():
    print("Generation des figures Chapitre IV...")
    screens = [
        ("fig_iv1_login.png", "Écran de connexion"),
        ("fig_iv2_dashboard.png", "Tableau de bord"),
        ("fig_iv3_pointage.png", "Terminal de pointage"),
        ("fig_iv4_mon_espace.png", "Mon espace"),
        ("fig_iv5_enrolement.png", "Enrôlement biométrique"),
        ("fig_iv6_conges.png", "Gestion des congés"),
        ("fig_iv7_employes.png", "Gestion des employés"),
        ("fig_iv8_rapports.png", "Rapports et indicateurs"),
    ]
    for filename, label in screens:
        path = OUT / filename
        if path.exists():
            print(f"  -> {filename} (fichier existant, conserve)")
            continue
        _placeholder(filename, label)
    print("Termine.")


if __name__ == "__main__":
    main()

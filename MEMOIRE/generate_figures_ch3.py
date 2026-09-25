# -*- coding: utf-8 -*-
"""
Figures Chapitre III — diagrammes UML académiques, noir et blanc.

Style mémoire UWB (conception de l'auteur) : Times/serif, fond blanc,
boîtes noires, libellés français, notation UML classique.
Aucun nom de fichier, port, framework ou contrôleur sur les figures.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Rectangle

OUT = Path(r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\images\chapitre3")
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
ARROW_C = "#000000"
LW = 1.6
ARROW_LW = 1.8
ARROW_HEAD = 0.11


def _arrow_head(ax, x_tip, y_tip, dx, dy, filled=True):
    length = (dx ** 2 + dy ** 2) ** 0.5
    if length < 1e-6:
        return
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    base_x = x_tip - ux * ARROW_HEAD
    base_y = y_tip - uy * ARROW_HEAD
    half = ARROW_HEAD * 0.42
    xs = [x_tip, base_x + px * half, base_x - px * half]
    ys = [y_tip, base_y + py * half, base_y - py * half]
    if filled:
        ax.fill(xs, ys, color=ARROW_C, zorder=6, clip_on=False)
    else:
        ax.plot([xs[1], xs[0], xs[2]], [ys[1], ys[0], ys[2]],
                color=ARROW_C, linewidth=ARROW_LW, zorder=6, clip_on=False)


def _line(ax, x1, y1, x2, y2, dashed=False, lw=None):
    ax.plot(
        [x1, x2], [y1, y2],
        color=ARROW_C, linewidth=lw or ARROW_LW,
        linestyle="--" if dashed else "-",
        solid_capstyle="butt", zorder=5, clip_on=False,
    )


def _arrow(ax, x1, y1, x2, y2, dashed=False, open_head=False, lw=None):
    dx, dy = x2 - x1, y2 - y1
    length = (dx ** 2 + dy ** 2) ** 0.5
    if length < 1e-6:
        return
    ux, uy = dx / length, dy / length
    _line(ax, x1, y1, x2 - ux * ARROW_HEAD, y2 - uy * ARROW_HEAD,
          dashed=dashed, lw=lw)
    _arrow_head(ax, x2, y2, dx, dy, filled=not open_head)


def _elbow(ax, points, dashed=False, open_head=True, lw=None):
    """Polyligne avec flèche à l'arrivée (include / extend / flux d'activité)."""
    if len(points) < 2:
        return
    for i in range(len(points) - 2):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        _line(ax, x1, y1, x2, y2, dashed=dashed, lw=lw)
    x1, y1 = points[-2]
    x2, y2 = points[-1]
    _arrow(ax, x1, y1, x2, y2, dashed=dashed, open_head=open_head, lw=lw)


def _stereo(ax, x, y, text, fs=8.0):
    ax.text(
        x, y, text, ha="center", va="center", fontsize=fs, style="italic",
        zorder=8,
        bbox=dict(boxstyle="square,pad=0.12", facecolor="white",
                  edgecolor="none", alpha=0.96),
    )


def _save(fig, name: str):
    path = OUT / name
    fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.45,
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


def _source(ax, x, y):
    ax.text(x, y, "Source : conception de l'auteur.",
            ha="center", va="center", fontsize=10, style="italic")


def _draw(ax, box: B, text, fs=11, bold_title=None):
    ax.add_patch(Rectangle(
        (box.x, box.y), box.w, box.h,
        linewidth=LW, edgecolor=BOX_EC, facecolor="white", zorder=2,
    ))
    if bold_title:
        ax.text(box.cx, box.y + box.h * 0.68, bold_title, ha="center", va="center",
                fontsize=fs, fontweight="bold", zorder=3)
        ax.text(box.cx, box.y + box.h * 0.28, text, ha="center", va="center",
                fontsize=fs - 0.5, zorder=3, linespacing=1.25)
    else:
        ax.text(box.cx, box.cy, text, ha="center", va="center",
                fontsize=fs, zorder=3, linespacing=1.25)


def _arrow_right(ax, a: B, b: B, label=None, fs=8):
    y = (a.cy + b.cy) / 2
    _arrow(ax, a.right, y, b.left, y)
    if label:
        ax.text((a.right + b.left) / 2, y + 0.16, label, ha="center", fontsize=fs)


def _arrow_down(ax, a: B, b: B, label=None, fs=8):
    _arrow(ax, a.cx, a.bottom, b.cx, b.top)
    if label:
        ax.text(a.cx + 0.14, (a.bottom + b.top) / 2, label, ha="left", va="center", fontsize=fs)


# ── primitives UML ──────────────────────────────────────────────────────

def _stick_actor(ax, x, y, label, fs=11):
    """Acteur UML classique (bonhomme bâton). (x, y) = centre de la tête."""
    r = 0.20
    ax.add_patch(Circle((x, y), r, fill=False, lw=1.5, edgecolor="black", zorder=3))
    body_top = y - r
    hips = y - 0.78
    ax.plot([x, x], [body_top, hips], color="black", lw=1.5, zorder=3)
    ax.plot([x - 0.34, x + 0.34], [y - 0.40, y - 0.40], color="black", lw=1.5, zorder=3)
    ax.plot([x, x - 0.24], [hips, hips - 0.40], color="black", lw=1.5, zorder=3)
    ax.plot([x, x + 0.24], [hips, hips - 0.40], color="black", lw=1.5, zorder=3)
    ax.text(x, hips - 0.58, label, ha="center", va="top", fontsize=fs,
            fontweight="bold", linespacing=1.15, zorder=3)


def _usecase(ax, cx, cy, w, h, text, fs=11):
    ax.add_patch(Ellipse((cx, cy), w, h, fill=False, lw=1.4, edgecolor="black", zorder=2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, zorder=3)


def _class_box(ax, x, top, w, name, attrs, methods, fs=9.2, line_h=0.32):
    """Boîte de classe UML à trois compartiments. Retourne B (origine bas-gauche)."""
    header_h = 0.42
    pad = 0.10
    attr_h = pad + max(len(attrs), 1) * line_h + pad
    meth_h = pad + max(len(methods), 1) * line_h + pad
    h = header_h + attr_h + meth_h
    y = top - h
    ax.add_patch(Rectangle((x, y), w, h, lw=LW, edgecolor="black",
                           facecolor="white", zorder=2))
    y_head = y + h - header_h
    ax.plot([x, x + w], [y_head, y_head], color="black", lw=1.15, zorder=3)
    y_attr = y + meth_h
    ax.plot([x, x + w], [y_attr, y_attr], color="black", lw=1.15, zorder=3)
    ax.text(x + w / 2, y + h - header_h / 2, name, ha="center", va="center",
            fontsize=fs + 1.2, fontweight="bold", zorder=3)
    ax.text(x + 0.12, y_head - pad, "\n".join(attrs), ha="left", va="top",
            fontsize=fs, linespacing=1.28, zorder=3, family="serif")
    ax.text(x + 0.12, y_attr - pad, "\n".join(methods), ha="left", va="top",
            fontsize=fs, linespacing=1.28, zorder=3, family="serif")
    return B(x, y, w, h)


def _entity(ax, x, top, w, name, attrs, fs=9.4, line_h=0.34):
    """Entité MLD : nom + attributs (PK / FK)."""
    header_h = 0.40
    pad = 0.10
    h = header_h + pad + len(attrs) * line_h + pad
    y = top - h
    ax.add_patch(Rectangle((x, y), w, h, lw=LW, edgecolor="black",
                           facecolor="white", zorder=2))
    y_head = y + h - header_h
    ax.plot([x, x + w], [y_head, y_head], color="black", lw=1.15, zorder=3)
    ax.text(x + w / 2, y + h - header_h / 2, name, ha="center", va="center",
            fontsize=fs + 1.1, fontweight="bold", zorder=3)
    ax.text(x + 0.12, y_head - pad, "\n".join(attrs), ha="left", va="top",
            fontsize=fs, linespacing=1.28, zorder=3, family="serif")
    return B(x, y, w, h)


def _node(ax, box: B, stereo, title, depth=0.20):
    """Nœud de déploiement UML (prisme 2,5 D)."""
    x, y, w, h = box.x, box.y, box.w, box.h
    d = depth
    ax.add_patch(Rectangle((x, y), w, h, lw=LW, edgecolor="black",
                           facecolor="white", zorder=2))
    ax.fill([x, x + d, x + w + d, x + w],
            [y + h, y + h + d, y + h + d, y + h],
            facecolor="white", edgecolor="black", lw=LW, zorder=2)
    ax.fill([x + w, x + w + d, x + w + d, x + w],
            [y, y + d, y + h + d, y + h],
            facecolor="white", edgecolor="black", lw=LW, zorder=2)
    ax.text(box.cx, box.top - 0.22, stereo, ha="center", va="center",
            fontsize=8, style="italic", zorder=3)
    ax.text(box.cx, box.top - 0.50, title, ha="center", va="center",
            fontsize=9.5, fontweight="bold", zorder=3)


def _artifact(ax, box: B, text, fs=8):
    ax.add_patch(Rectangle(
        (box.x, box.y), box.w, box.h,
        linewidth=1.3, edgecolor="black", facecolor="white", zorder=3,
    ))
    ax.text(box.cx, box.cy, text, ha="center", va="center",
            fontsize=fs, zorder=4, linespacing=1.2)


def _rounded(ax, box: B, text, fs=9):
    ax.add_patch(FancyBboxPatch(
        (box.x, box.y), box.w, box.h,
        boxstyle="round,pad=0.02,rounding_size=0.16",
        linewidth=LW, edgecolor="black", facecolor="white", zorder=2,
    ))
    ax.text(box.cx, box.cy, text, ha="center", va="center",
            fontsize=fs, zorder=3, linespacing=1.2)


def _diamond(ax, cx, cy, text, rx=0.95, ry=0.58, fs=8):
    ax.fill([cx, cx + rx, cx, cx - rx],
            [cy + ry, cy, cy - ry, cy],
            facecolor="white", edgecolor="black", lw=LW, zorder=2)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, zorder=3)


def _start(ax, cx, cy, r=0.16):
    ax.add_patch(Circle((cx, cy), r, facecolor="black", edgecolor="black", zorder=3))


def _end(ax, cx, cy, r=0.14):
    ax.add_patch(Circle((cx, cy), r + 0.08, fill=False, lw=1.6,
                        edgecolor="black", zorder=3))
    ax.add_patch(Circle((cx, cy), r, facecolor="black", edgecolor="black", zorder=3))


def _activation(ax, x, y_top, y_bot, w=0.14):
    ax.add_patch(Rectangle(
        (x - w / 2, y_bot), w, y_top - y_bot,
        linewidth=1.0, edgecolor="black", facecolor="white", zorder=4,
    ))


# ── Figure III.1 — Architecture fonctionnelle globale ───────────────────

def fig_iii1_architecture():
    fig, ax = plt.subplots(figsize=(14.8, 9.2))
    ax.set_xlim(0, 13.2)
    ax.set_ylim(0, 8.4)
    ax.axis("off")

    web = B(0.5, 5.7, 3.4, 1.7)
    app = B(4.9, 5.7, 3.4, 1.7)
    db = B(9.3, 5.7, 3.4, 1.7)
    _draw(ax, web, "Tableaux de bord,\nformulaires, pointage",
          bold_title="Interface web")
    _draw(ax, app, "Règles métier,\nidentification, workflows",
          bold_title="Application de gestion")
    _draw(ax, db, "Dossiers, présences,\ncongés, barèmes",
          bold_title="Base de données")
    _arrow_right(ax, web, app)
    ax.text(4.2, 7.55, "requêtes", fontsize=9, style="italic", ha="center")
    _arrow_right(ax, app, db)
    ax.text(8.6, 7.55, "persistance", fontsize=9, style="italic", ha="center")

    bio = B(4.9, 2.85, 3.4, 1.55)
    _draw(ax, bio, "Capture et comparaison\nd'empreintes",
          bold_title="Service biométrique")
    _arrow(ax, app.cx - 0.14, app.bottom, bio.cx - 0.14, bio.top)
    _arrow(ax, bio.cx + 0.14, bio.top, app.cx + 0.14, app.bottom)

    zk = B(1.3, 0.75, 3.0, 1.35)
    rfid = B(8.9, 0.75, 3.0, 1.35)
    _draw(ax, zk, "Lecteur d'empreintes\ndigitales", bold_title="ZK-9500")
    _draw(ax, rfid, "Badge de proximité", bold_title="RFID")
    _arrow(ax, zk.right, zk.top, bio.left + 0.15, bio.cy - 0.20)
    ax.text(3.35, 2.15, "capture", fontsize=9, style="italic")
    _arrow(ax, rfid.left, rfid.top, bio.right - 0.15, bio.cy - 0.20)
    ax.text(9.55, 2.15, "lecture", fontsize=9, style="italic")
    ax.text(6.6, 4.55, "identification", fontsize=9, style="italic", ha="center")

    _source(ax, 6.6, 0.28)
    _save(fig, "fig_iii1_architecture_globale.png")


# ── Figure III.2 — Diagramme de cas d'utilisation complet ───────────────

def fig_iii2_usecase():
    """Cas d'utilisation UML : associations fléchées, «include» et «extend»."""
    fig, ax = plt.subplots(figsize=(18.8, 17.2))
    ax.set_xlim(0, 20.0)
    ax.set_ylim(0, 17.4)
    ax.axis("off")

    ax.add_patch(Rectangle((3.55, 2.20), 12.90, 14.15, fill=False,
                           linewidth=1.7, edgecolor="black", zorder=1))
    ax.text(10.0, 16.00, "SGRH Pro — système de gestion des ressources humaines",
            ha="center", va="center", fontsize=12, fontweight="bold")

    _stick_actor(ax, 1.40, 13.85, "Admin RH", fs=11)
    _stick_actor(ax, 1.40, 8.55, "Manager", fs=11)
    _stick_actor(ax, 1.40, 3.55, "Agent", fs=11)
    _stick_actor(ax, 18.55, 12.15, "Lecteur\nbiométrique", fs=10.5)
    _stick_actor(ax, 18.55, 4.75, "Lecteur\nRFID", fs=10.5)

    ow, oh = 4.85, 0.98
    ovals = {
        "auth": (6.55, 14.55, "S'authentifier"),
        "logout": (6.55, 13.15, "Se déconnecter"),
        "mdp": (6.55, 11.75, "Changer le mot de passe"),
        "employes": (6.55, 10.35, "Gérer les employés"),
        "depts": (6.55, 8.95, "Gérer les départements"),
        "comptes": (6.55, 7.55, "Gérer comptes et rôles"),
        "enroler": (6.55, 6.15, "Enrôler une empreinte"),
        "badge": (6.55, 4.75, "Attribuer un badge RFID"),
        "params": (6.55, 3.35, "Paramétrer le système"),
        "pointer": (13.45, 14.55, "Pointer entrée / sortie"),
        "demander": (13.45, 13.15, "Demander un congé"),
        "valider": (13.45, 11.75, "Valider un congé"),
        "espace": (13.45, 10.35, "Consulter Mon espace"),
        "kpi": (13.45, 8.95, "Consulter KPI et rapports"),
        "evaluer": (13.45, 7.55, "Évaluer un agent"),
        "remu": (13.45, 6.15, "Produire un état de rémunération"),
        "capturer": (13.45, 4.75, "Capturer une empreinte"),
        "lire": (13.45, 3.35, "Lire un badge RFID"),
    }
    for _key, (cx, cy, label) in ovals.items():
        _usecase(ax, cx, cy, ow, oh, label, fs=10.5)

    hw, hh = ow / 2, oh / 2

    def edge(key, side):
        cx, cy, _ = ovals[key]
        if side == "left":
            return cx - hw, cy
        if side == "right":
            return cx + hw, cy
        if side == "top":
            return cx, cy + hh
        return cx, cy - hh

    def assoc(x1, y1, key, side="left"):
        x2, y2 = edge(key, side)
        _arrow(ax, x1, y1, x2, y2, lw=1.05)

    # Associations acteur → cas (flèche pleine)
    for key in ("auth", "logout", "mdp", "employes", "depts", "comptes",
                "enroler", "badge", "params"):
        assoc(1.82, 13.45, key, "left")
    for key in ("valider", "kpi", "remu"):
        assoc(1.82, 13.45, key, "left")
    for key in ("auth", "logout", "mdp", "valider", "kpi", "evaluer"):
        assoc(1.82, 8.15, key, "left")
    for key in ("auth", "logout", "mdp", "pointer", "demander", "espace"):
        assoc(1.82, 3.15, key, "left")
    for key in ("enroler", "pointer", "capturer"):
        assoc(18.15, 11.75, key, "right")
    for key in ("badge", "pointer", "lire"):
        assoc(18.15, 4.35, key, "right")

    # Gouttière centrale : «include» vers S'authentifier (sauf pointage kiosque)
    x_inc_auth = 9.90
    auth_r = edge("auth", "right")
    include_auth = (
        "logout", "employes", "depts", "comptes", "enroler", "badge", "params",
        "demander", "valider", "espace", "kpi", "evaluer", "remu",
    )
    for key in include_auth:
        x_src, y_src = edge(key, "right" if ovals[key][0] < 10 else "left")
        # Légère décalage vertical si le cas est à gauche (évite de coller deux includes)
        if key == "enroler":
            y_src += 0.16
        elif key == "badge":
            y_src += 0.16
        _elbow(ax, [(x_src, y_src), (x_inc_auth, y_src),
                    (x_inc_auth, auth_r[1]), auth_r],
               dashed=True, open_head=True, lw=1.05)
    _stereo(ax, x_inc_auth, 12.45, "«include»")

    # «include» Enrôler → Capturer une empreinte
    er = edge("enroler", "right")
    cl = edge("capturer", "left")
    _elbow(ax, [(er[0], er[1] - 0.16), (10.30, er[1] - 0.16),
                (10.30, cl[1]), cl],
           dashed=True, open_head=True, lw=1.05)
    _stereo(ax, 10.30, 5.55, "«include»")

    # «include» Attribuer un badge → Lire un badge RFID
    br = edge("badge", "right")
    ll = edge("lire", "left")
    _elbow(ax, [(br[0], br[1] - 0.16), (9.45, br[1] - 0.16),
                (9.45, ll[1]), ll],
           dashed=True, open_head=True, lw=1.05)
    _stereo(ax, 9.45, 4.05, "«include»")

    # «extend» Capturer / Lire → Pointer (modalités d'identification)
    cr = edge("capturer", "right")
    lr = edge("lire", "right")
    pr = edge("pointer", "right")
    _elbow(ax, [cr, (16.08, cr[1]), (16.08, pr[1]), pr],
           dashed=True, open_head=True, lw=1.05)
    _elbow(ax, [lr, (16.32, lr[1]), (16.32, pr[1] - 0.18), (pr[0], pr[1] - 0.18)],
           dashed=True, open_head=True, lw=1.05)
    _stereo(ax, 16.08, 9.65, "«extend»\n{mode empreinte}")
    _stereo(ax, 16.32, 6.35, "«extend»\n{mode RFID}")

    # «extend» Changer le mot de passe → S'authentifier
    mr = edge("mdp", "right")
    _elbow(ax, [(mr[0], mr[1]), (9.18, mr[1]), (9.18, auth_r[1]), auth_r],
           dashed=True, open_head=True, lw=1.05)
    _stereo(ax, 9.18, 12.48, "«extend»\n{mdp à renouveler}")

    # Légende
    _arrow(ax, 3.70, 1.45, 5.35, 1.45, lw=1.15)
    ax.text(5.50, 1.45, "association (acteur → cas)", ha="left", va="center",
            fontsize=9.5)
    _arrow(ax, 10.35, 1.45, 12.00, 1.45, dashed=True, open_head=True, lw=1.15)
    ax.text(12.15, 1.45, "«include» / «extend» (flèche ouverte)",
            ha="left", va="center", fontsize=9.5)
    ax.text(10.0, 0.85,
            "Le pointage kiosque n'inclut pas « S'authentifier » (terminal public).",
            ha="center", va="center", fontsize=9.5, style="italic")
    _source(ax, 10.0, 0.32)
    _save(fig, "fig_iii2_cas_utilisation.png")


# ── Figure III.3 — Diagramme de classes ─────────────────────────────────

def fig_iii3_classes():
    fig, ax = plt.subplots(figsize=(17.0, 13.0))
    ax.set_xlim(0, 16.0)
    ax.set_ylim(0, 12.2)
    ax.axis("off")

    top = 11.55
    role = _class_box(ax, 0.25, top, 3.15, "Rôle",
                      ["− identifiant", "− nom"],
                      ["+ attribuer()"])
    user = _class_box(ax, 4.15, top, 3.35, "Utilisateur",
                      ["− identifiant", "− nom_utilisateur",
                       "− mot_de_passe", "− employee_id", "− role_id"],
                      ["+ authentifier()", "+ changerMotDePasse()"])
    emp = _class_box(ax, 8.25, top, 3.50, "Employé",
                     ["− identifiant", "− prénom", "− nom",
                      "− matricule", "− email",
                      "− empreinte", "− rfid",
                      "− department_id", "− role_id"],
                     ["+ enrôlerEmpreinte()", "+ attribuerBadge()"])
    dept = _class_box(ax, 12.50, top, 3.20, "Département",
                      ["− identifiant", "− nom", "− budget",
                       "− manager_id"],
                      ["+ listerEmployes()"])

    top2 = 4.85
    pres = _class_box(ax, 0.25, top2, 3.55, "Présence",
                      ["− identifiant", "− employee_id",
                       "− heure_entrée", "− heure_sortie",
                       "− heures_travaillées", "− minutes_retard",
                       "− source"],
                      ["+ enregistrerEntrée()", "+ enregistrerSortie()"])
    conge = _class_box(ax, 4.15, top2, 3.55, "Congé",
                       ["− identifiant", "− employee_id",
                        "− date_debut", "− date_fin",
                        "− motif", "− statut"],
                       ["+ soumettre()", "+ valider()", "+ rejeter()"])
    remu = _class_box(ax, 8.10, top2, 3.70, "Rémunération",
                      ["− identifiant", "− employee_id",
                       "− periode", "− salaire_base",
                       "− prime", "− total_indicatif",
                       "− statut"],
                      ["+ calculerTotal()"])
    ev = _class_box(ax, 12.20, top2, 3.50, "Évaluation",
                    ["− identifiant", "− employee_id",
                     "− evaluateur_id", "− periode",
                     "− note", "− statut"],
                    ["+ evaluer()"])

    def assoc_h(a: B, b: B, left_m, right_m, y=None):
        yy = y if y is not None else min(a.cy, b.cy)
        _line(ax, a.right, yy, b.left, yy, lw=1.25)
        ax.text(a.right + 0.12, yy + 0.10, left_m, fontsize=7.5, ha="left")
        ax.text(b.left - 0.12, yy + 0.10, right_m, fontsize=7.5, ha="right")

    assoc_h(role, user, "1", "0..*", y=role.cy + 0.15)
    assoc_h(user, emp, "0..1", "0..1", y=user.cy + 0.35)
    assoc_h(emp, dept, "0..*", "0..1", y=dept.cy + 0.15)

    # Rôle — Employé (au-dessus des boîtes)
    y_over = top + 0.28
    _line(ax, role.cx, role.top, role.cx, y_over, lw=1.25)
    _line(ax, emp.cx, emp.top, emp.cx, y_over, lw=1.25)
    _line(ax, role.cx, y_over, emp.cx, y_over, lw=1.25)
    ax.text(role.cx + 0.12, y_over + 0.08, "1", fontsize=7.5)
    ax.text(emp.cx - 0.12, y_over + 0.08, "0..*", fontsize=7.5, ha="right")

    # Employé — classes métier (bus)
    bus_y = (emp.bottom + max(c.top for c in (pres, conge, remu, ev))) / 2
    _line(ax, emp.cx, emp.bottom, emp.cx, bus_y, lw=1.25)
    children = [pres, conge, remu, ev]
    _line(ax, children[0].cx, bus_y, children[-1].cx, bus_y, lw=1.25)
    for child in children:
        _line(ax, child.cx, bus_y, child.cx, child.top, lw=1.25)
        ax.text(child.cx + 0.10, bus_y - 0.16, "1", fontsize=7.5)
        ax.text(child.cx + 0.10, child.top + 0.08, "0..*", fontsize=7.5)

    _source(ax, 8.0, 0.22)
    _save(fig, "fig_iii3_diagramme_classes.png")


# ── Figure III.4 — Diagramme de séquence (pointage) ─────────────────────

def fig_iii4_sequence_pointage():
    fig, ax = plt.subplots(figsize=(15.6, 11.6))
    ax.set_xlim(0, 14.0)
    ax.set_ylim(0, 11.4)
    ax.axis("off")

    xs = [1.35, 4.05, 6.85, 9.75, 12.45]
    labels = ["Agent", "Interface", "Application",
              "Service biométrique", "ZK-9500"]
    y_box = 10.15
    for x, label in zip(xs, labels):
        ax.add_patch(Rectangle((x - 1.05, y_box), 2.10, 0.70,
                               lw=LW, edgecolor="black", facecolor="white", zorder=3))
        ax.text(x, y_box + 0.35, label, ha="center", va="center",
                fontsize=8.5, fontweight="bold")
        _line(ax, x, y_box, x, 0.85, dashed=True, lw=1.0)

    a, i, p, s, z = xs
    _activation(ax, i, 9.55, 1.55)
    _activation(ax, p, 8.75, 2.15)
    _activation(ax, s, 7.95, 4.75)
    _activation(ax, z, 7.15, 5.55)

    def call(x1, x2, y, label):
        _arrow(ax, x1, y, x2, y)
        ax.text((x1 + x2) / 2, y + 0.13, label, ha="center", va="bottom", fontsize=10)

    def ret(x1, x2, y, label):
        _arrow(ax, x1, y, x2, y, dashed=True, open_head=True)
        ax.text((x1 + x2) / 2, y + 0.13, label, ha="center", va="bottom", fontsize=10)

    def self_call(x, y, label, width=0.85):
        _line(ax, x, y, x + width, y, lw=1.4)
        _line(ax, x + width, y, x + width, y - 0.38, lw=1.4)
        _arrow(ax, x + width, y - 0.38, x, y - 0.38)
        ax.text(x + width + 0.10, y - 0.19, label, ha="left", va="center", fontsize=8)

    call(a, i, 9.45, "Demander scan")
    call(i, p, 8.65, "Demander scan")
    call(p, s, 7.85, "Demander scan")
    call(s, z, 7.05, "Capturer")
    ret(z, s, 6.25, "Template")
    ret(s, p, 5.45, "Template")
    self_call(p, 4.65, "Identifier")
    self_call(p, 3.55, "Enregistrer entrée/sortie")
    ret(p, i, 2.45, "Accusé")
    ret(i, a, 1.65, "Accusé")

    _source(ax, 7.0, 0.32)
    _save(fig, "fig_iii4_sequence_pointage.png")


# ── Figure III.5 — Diagramme d'activité (congé) ─────────────────────────

def fig_iii5_activite_conge():
    fig, ax = plt.subplots(figsize=(11.4, 13.6))
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0, 13.0)
    ax.axis("off")

    _start(ax, 5.1, 12.35)
    soumettre = B(2.55, 10.55, 5.1, 1.05)
    _rounded(ax, soumettre, "Soumettre demande\n(statut : En attente)")
    _arrow(ax, 5.1, 12.18, 5.1, soumettre.top)

    _arrow(ax, 5.1, soumettre.bottom, 5.1, 9.85)
    _diamond(ax, 5.1, 9.20, "Avis\nmanager")

    decision = B(2.55, 6.85, 5.1, 0.95)
    _rounded(ax, decision, "Décision RH")
    _arrow(ax, 5.1, 8.62, 5.1, decision.top)
    ax.text(5.55, 8.95, "favorable", fontsize=7.5, style="italic")

    rej = B(0.85, 2.15, 3.55, 0.90)
    app = B(5.80, 2.15, 3.55, 0.90)
    _rounded(ax, rej, "Rejeté")
    _rounded(ax, app, "Approuvé")

    _elbow(ax, [(4.15, 9.20), (0.55, 9.20), (0.55, rej.cy), (rej.left, rej.cy)],
           open_head=False, lw=1.5)
    ax.text(0.70, 9.38, "défavorable", fontsize=7.5, style="italic")

    _arrow(ax, 5.1, decision.bottom, 5.1, 6.15)
    _diamond(ax, 5.1, 5.50, "Décision ?")

    _elbow(ax, [(6.05, 5.50), (app.cx, 5.50), (app.cx, app.top)],
           open_head=False, lw=1.5)
    ax.text(6.25, 5.68, "approuvé", fontsize=7.5, style="italic")

    _elbow(ax, [(4.15, 5.50), (rej.cx, 5.50), (rej.cx, rej.top)],
           open_head=False, lw=1.5)
    ax.text(2.85, 5.68, "rejeté", fontsize=7.5, style="italic")

    _end(ax, 5.1, 0.70)
    _elbow(ax, [(app.cx, app.bottom), (app.cx, 0.70), (5.32, 0.70)],
           open_head=False, lw=1.5)
    _elbow(ax, [(rej.cx, rej.bottom), (rej.cx, 0.70), (4.88, 0.70)],
           open_head=False, lw=1.5)

    _source(ax, 5.1, 0.22)
    _save(fig, "fig_iii5_activite_conge.png")


# ── Figure III.5b — Diagramme d'activité (pointage) ─────────────────────

def fig_iii5b_activite_pointage():
    """Second diagramme d'activités : entrée / sortie biométrique ou RFID."""
    fig, ax = plt.subplots(figsize=(12.4, 15.2))
    ax.set_xlim(0, 12.4)
    ax.set_ylim(0, 16.2)
    ax.axis("off")

    ax.text(6.2, 15.75, "Processus de pointage quotidien",
            ha="center", fontsize=13, fontweight="bold")

    _start(ax, 6.2, 15.15)
    presenter = B(3.35, 13.55, 5.7, 1.00)
    _rounded(ax, presenter, "Présenter l'empreinte\nou le badge RFID")
    _arrow(ax, 6.2, 14.98, 6.2, presenter.top)

    capturer = B(3.35, 11.85, 5.7, 1.00)
    _rounded(ax, capturer, "Capturer / lire\nl'identifiant")
    _arrow(ax, 6.2, presenter.bottom, 6.2, capturer.top)

    identifier = B(3.35, 10.15, 5.7, 1.00)
    _rounded(ax, identifier, "Identifier l'agent (1:N)\nou par identifiant RFID")
    _arrow(ax, 6.2, capturer.bottom, 6.2, identifier.top)

    _arrow(ax, 6.2, identifier.bottom, 6.2, 9.45)
    _diamond(ax, 6.2, 8.85, "Agent\nreconnu ?", rx=1.15, ry=0.62, fs=9.5)

    refus_id = B(0.35, 6.55, 3.55, 0.95)
    _rounded(ax, refus_id, "Refuser\n(agent inconnu)")
    _elbow(ax, [(5.05, 8.85), (0.55, 8.85), (0.55, refus_id.cy),
                (refus_id.left, refus_id.cy)],
           open_head=False, lw=1.5)
    ax.text(1.35, 9.05, "non", fontsize=9, style="italic")

    _arrow(ax, 6.2, 8.22, 6.2, 7.55)
    ax.text(6.55, 7.85, "oui", fontsize=9, style="italic")
    _diamond(ax, 6.2, 6.95, "Journée\ndéjà close ?", rx=1.15, ry=0.62, fs=9.5)

    refus_409 = B(8.55, 5.55, 3.50, 0.95)
    _rounded(ax, refus_409, "Refuser\n(journée clôturée)")
    _elbow(ax, [(7.35, 6.95), (refus_409.cx, 6.95), (refus_409.cx, refus_409.top)],
           open_head=False, lw=1.5)
    ax.text(8.15, 7.15, "oui", fontsize=9, style="italic")

    _arrow(ax, 6.2, 6.32, 6.2, 5.65)
    ax.text(6.55, 5.95, "non", fontsize=9, style="italic")
    _diamond(ax, 6.2, 5.05, "Entrée déjà\nenregistrée ?", rx=1.20, ry=0.62, fs=9.5)

    entree = B(0.45, 2.55, 3.70, 0.95)
    sortie = B(8.25, 2.55, 3.70, 0.95)
    _rounded(ax, entree, "Enregistrer\nl'entrée")
    _rounded(ax, sortie, "Enregistrer la sortie\net calculer les heures")

    _elbow(ax, [(5.00, 5.05), (entree.cx, 5.05), (entree.cx, entree.top)],
           open_head=False, lw=1.5)
    ax.text(2.85, 5.25, "non", fontsize=9, style="italic")

    _elbow(ax, [(7.40, 5.05), (sortie.cx, 5.05), (sortie.cx, sortie.top)],
           open_head=False, lw=1.5)
    ax.text(8.55, 5.25, "oui", fontsize=9, style="italic")

    accuse = B(3.55, 1.15, 5.30, 0.85)
    _rounded(ax, accuse, "Afficher l'accusé de pointage")
    _elbow(ax, [(entree.cx, entree.bottom), (entree.cx, accuse.cy),
                (accuse.left, accuse.cy)],
           open_head=False, lw=1.5)
    _elbow(ax, [(sortie.cx, sortie.bottom), (sortie.cx, accuse.cy),
                (accuse.right, accuse.cy)],
           open_head=False, lw=1.5)

    _end(ax, 6.2, 0.48)
    _arrow(ax, 6.2, accuse.bottom, 6.2, 0.64)
    _elbow(ax, [(refus_id.cx, refus_id.bottom), (refus_id.cx, 0.48), (5.98, 0.48)],
           open_head=False, lw=1.2)
    _elbow(ax, [(refus_409.cx, refus_409.bottom), (refus_409.cx, 0.48), (6.42, 0.48)],
           open_head=False, lw=1.2)

    _source(ax, 6.2, 0.16)
    _save(fig, "fig_iii5b_activite_pointage.png")


# ── Figure III.6 — Diagramme de déploiement ─────────────────────────────

def fig_iii6_deploiement():
    fig, ax = plt.subplots(figsize=(15.4, 9.8))
    ax.set_xlim(0, 14.0)
    ax.set_ylim(0, 9.0)
    ax.axis("off")

    srv = B(0.45, 4.15, 5.6, 4.05)
    post = B(7.55, 4.15, 5.8, 4.05)
    _node(ax, srv, "<<nœud>>", "Serveur applicatif")
    _node(ax, post, "<<nœud>>", "Poste terminal RH")

    _artifact(ax, B(0.85, 5.85, 4.7, 0.95),
              "« artefact »  Application de gestion")
    _artifact(ax, B(0.85, 4.55, 4.7, 0.95),
              "« artefact »  Base de données")
    _artifact(ax, B(7.95, 5.85, 4.9, 0.95),
              "« artefact »  Interface web")
    _artifact(ax, B(7.95, 4.55, 4.9, 0.95),
              "« artefact »  Service biométrique")

    zk = B(7.55, 1.15, 2.55, 1.55)
    rfid = B(10.80, 1.15, 2.55, 1.55)
    _node(ax, zk, "<<dispositif>>", "ZK-9500", depth=0.16)
    _node(ax, rfid, "<<dispositif>>", "RFID", depth=0.16)

    _arrow(ax, post.left, 6.28, srv.right + 0.20, 6.28)
    _arrow(ax, srv.right + 0.20, 6.02, post.left, 6.02)
    ax.text(6.90, 6.48, "échange", ha="center", fontsize=8, style="italic")

    _arrow(ax, zk.cx, zk.top + 0.16, 8.85, post.bottom)
    ax.text(8.15, 3.35, "USB", fontsize=8, style="italic")
    _arrow(ax, rfid.cx, rfid.top + 0.16, 11.70, post.bottom)
    ax.text(12.15, 3.35, "lecture", fontsize=8, style="italic")

    _source(ax, 7.0, 0.35)
    _save(fig, "fig_iii6_deploiement.png")


# ── Figure III.7 — Modèle entité-association / MLD ──────────────────────

def fig_iii7_mer():
    """MLD cœur métier — libellés français, sans faute, lisible en impression."""
    fig, ax = plt.subplots(figsize=(18.0, 13.2))
    ax.set_xlim(0, 19.2)
    ax.set_ylim(0, 14.2)
    ax.axis("off")

    ax.text(9.6, 13.75, "Modèle logique de données — cœur métier de SGRH Pro",
            ha="center", va="center", fontsize=14, fontweight="bold")

    top = 13.15
    role = _entity(ax, 0.35, top, 3.55, "RÔLE",
                   ["# id_role", "    nom"])
    user = _entity(ax, 5.05, top, 4.15, "UTILISATEUR",
                   ["# id_utilisateur", "    nom_utilisateur",
                    "    mot_de_passe", "* id_employe", "* id_role"])
    emp = _entity(ax, 10.35, top, 4.35, "EMPLOYÉ",
                  ["# id_employe", "    prénom", "    nom", "    matricule",
                   "    email", "    téléphone", "    date_embauche",
                   "    empreinte", "    identifiant_rfid",
                   "* id_departement", "* id_role"])
    dept = _entity(ax, 15.55, top, 3.35, "DÉPARTEMENT",
                   ["# id_departement", "    nom", "    budget",
                    "* id_responsable"])

    top2 = 5.85
    pres = _entity(ax, 0.35, top2, 4.15, "PRÉSENCE",
                   ["# id_presence", "* id_employe",
                    "    heure_entrée", "    heure_sortie",
                    "    heures_travaillées", "    minutes_retard",
                    "    source"])
    conge = _entity(ax, 5.15, top2, 4.05, "CONGÉ",
                    ["# id_conge", "* id_employe",
                     "    date_debut", "    date_fin",
                     "    motif", "    statut"])
    remu = _entity(ax, 9.85, top2, 4.35, "RÉMUNÉRATION",
                   ["# id_remuneration", "* id_employe",
                    "    periode", "    salaire_base",
                    "    prime", "    total_indicatif", "    statut"])
    ev = _entity(ax, 14.85, top2, 4.05, "ÉVALUATION",
                 ["# id_evaluation", "* id_employe",
                  "* id_evaluateur", "    periode",
                  "    note", "    statut"])

    def link_h(a: B, b: B, m1, m2, y=None):
        yy = y if y is not None else min(a.cy, b.cy)
        _line(ax, a.right, yy, b.left, yy, lw=1.5)
        ax.text(a.right + 0.12, yy + 0.14, m1, fontsize=9.5, fontweight="bold")
        ax.text(b.left - 0.12, yy + 0.14, m2, fontsize=9.5, fontweight="bold", ha="right")

    # Merise : (min, max) du côté de l'entité, pour UNE occurrence de l'autre
    link_h(role, user, "(1,1)", "(0,n)", y=role.cy)
    link_h(user, emp, "(0,1)", "(0,1)", y=user.cy + 0.20)
    link_h(emp, dept, "(0,n)", "(0,1)", y=dept.cy)

    y_over = top + 0.28
    _line(ax, role.cx, role.top, role.cx, y_over, lw=1.5)
    _line(ax, emp.cx, emp.top, emp.cx, y_over, lw=1.5)
    _line(ax, role.cx, y_over, emp.cx, y_over, lw=1.5)
    ax.text(role.cx + 0.14, y_over + 0.14, "(1,1)", fontsize=9.5, fontweight="bold")
    ax.text(emp.cx - 0.14, y_over + 0.14, "(0,n)", fontsize=9.5,
            fontweight="bold", ha="right")

    bus_y = (emp.bottom + max(c.top for c in (pres, conge, remu, ev))) / 2
    _line(ax, emp.cx, emp.bottom, emp.cx, bus_y, lw=1.5)
    kids = [pres, conge, remu, ev]
    _line(ax, kids[0].cx, bus_y, kids[-1].cx, bus_y, lw=1.5)
    ax.text(emp.cx + 0.16, emp.bottom - 0.22, "(1,1)", fontsize=9.5, fontweight="bold")
    for child in kids:
        _line(ax, child.cx, bus_y, child.cx, child.top, lw=1.5)
        ax.text(child.cx + 0.10, child.top + 0.10, "(0,n)", fontsize=9.5, fontweight="bold")

    ax.text(9.6, 1.05,
            "Notation Merise : (min, max) inscrit à côté d'une entité = nombre "
            "d'occurrences de cette entité pour une occurrence de l'entité liée.",
            ha="center", fontsize=10.5, style="italic")
    ax.text(9.6, 0.68,
            "#  clé primaire          *  clé étrangère"
            "          (les tables satellites sont détaillées au MPD)",
            ha="center", fontsize=11)
    _source(ax, 9.6, 0.28)
    _save(fig, "fig_iii7_mer.png")


# ── Figure III.8 — Architecture en couches ──────────────────────────────

def fig_iii8_couches_backend():
    fig, ax = plt.subplots(figsize=(12.6, 10.0))
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 9.2)
    ax.axis("off")

    pres = B(2.15, 7.05, 7.70, 1.45)
    app = B(2.15, 4.75, 7.70, 1.45)
    data = B(0.40, 1.55, 5.20, 1.70)
    bio = B(6.40, 1.55, 5.20, 1.70)
    _draw(ax, pres, "Interface web, formulaires,\ntableaux de bord et consultation",
          fs=9, bold_title="Présentation")
    _draw(ax, app, "Règles métier, workflows,\nauthentification et identification",
          fs=9, bold_title="Application")
    _draw(ax, data, "Dossiers, présences, congés\net éléments de rémunération",
          fs=9, bold_title="Données")
    _draw(ax, bio, "Capture d'empreinte (ZK-9500)\net lecture de badge RFID",
          fs=9, bold_title="Acquisition biométrique")

    _arrow_down(ax, pres, app)
    _arrow(ax, app.cx - 1.55, app.bottom, data.cx, data.top)
    _arrow(ax, app.cx + 1.55, app.bottom, bio.cx, bio.top)
    ax.text(3.05, 3.95, "persistance", fontsize=9, style="italic", ha="center")
    ax.text(8.95, 3.95, "identification", fontsize=9, style="italic", ha="center")

    _source(ax, 6.0, 0.50)
    _save(fig, "fig_iii8_couches_backend.png")


def main():
    print("Generation des figures Chapitre III (UML academique)...")
    fig_iii1_architecture()
    fig_iii2_usecase()
    fig_iii3_classes()
    fig_iii4_sequence_pointage()
    fig_iii5_activite_conge()
    fig_iii5b_activite_pointage()
    fig_iii6_deploiement()
    fig_iii7_mer()
    fig_iii8_couches_backend()
    print("Termine.")


if __name__ == "__main__":
    main()

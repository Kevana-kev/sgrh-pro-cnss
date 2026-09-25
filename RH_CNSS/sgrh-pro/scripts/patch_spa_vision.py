from pathlib import Path

path = Path(__file__).resolve().parents[1] / "resources" / "views" / "spa.blade.php"
html = path.read_text(encoding="utf-8")

html = html.replace(
    """    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
    <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="{{ asset('css/dashboard.css') }}?v=20260809" />
    <link rel="stylesheet" href="{{ asset('css/dashboard-pro.css') }}?v=20260809" />
""",
    """    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Source+Serif+4:opsz,wght@8..60,500;8..60,700&display=swap" rel="stylesheet" />
    <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    <link rel="stylesheet" href="{{ asset('css/dashboard.css') }}?v=20260809b" />
    <link rel="stylesheet" href="{{ asset('css/dashboard-pro.css') }}?v=20260809b" />
    <link rel="stylesheet" href="{{ asset('css/sgrh-vision.css') }}?v=20260809b" />
""",
)

html = html.replace('data-theme="dark"', 'data-theme="light"')

html = html.replace(
    """        <h1>Connexion</h1>
        <p>Accédez à votre espace de gestion du personnel.</p>
        <form id="loginForm" class="form-grid">
          <label>
            Identifiant (matricule, username ou email)
            <input id="username" type="text" value="superadmin" required />
          </label>
          <label>
            Mot de passe
            <input id="password" type="password" value="superadmin123" required />
          </label>
""",
    """        <h1>Espace sécurisé</h1>
        <p>Pilot RH, pointage biométrique et suivi individuel — CNSS.</p>
        <form id="loginForm" class="form-grid">
          <label>
            Identifiant (matricule, username ou email)
            <input id="username" type="text" autocomplete="username" placeholder="ex. superadmin" required />
          </label>
          <label>
            Mot de passe
            <input id="password" type="password" autocomplete="current-password" required />
          </label>
""",
)

old_nav_start = html.find('<nav class="sidebar-nav" id="menuNav">')
old_nav_end = html.find("</nav>", old_nav_start) + len("</nav>")
new_nav = """<nav class=\"sidebar-nav\" id=\"menuNav\">
          <span class=\"menu-section-label\">Cœur du système</span>
          <div class=\"menu\">
            <button data-section=\"overview\" class=\"menu-item active\">
              <i class=\"ri-dashboard-horizontal-line\"></i><span>Pilot de bord</span>
            </button>
            <button data-section=\"punch\" class=\"menu-item menu-item--accent\">
              <i class=\"ri-fingerprint-2-line\"></i><span>Pointage</span>
            </button>
            <button data-section=\"myspace\" class=\"menu-item\">
              <i class=\"ri-user-heart-line\"></i><span>Mon espace</span>
            </button>
            <button data-section=\"attendances\" class=\"menu-item\">
              <i class=\"ri-calendar-check-line\"></i><span>Présences</span>
            </button>
            <button data-section=\"biometric\" class=\"menu-item\">
              <i class=\"ri-shield-keyhole-line\"></i><span>Enrôlement biométrique</span>
            </button>
          </div>

          <span class=\"menu-section-label\">Ressources Humaines</span>
          <div class=\"menu\">
            <button data-section=\"employees\" class=\"menu-item\">
              <i class=\"ri-user-line\"></i><span>Employés</span>
            </button>
            <button data-section=\"departments\" class=\"menu-item\">
              <i class=\"ri-building-2-line\"></i><span>Départements</span>
            </button>
            <button data-section=\"team\" class=\"menu-item\">
              <i class=\"ri-team-line\"></i><span>Équipe</span>
            </button>
            <button data-section=\"roles\" class=\"menu-item\">
              <i class=\"ri-shield-user-line\"></i><span>Rôles &amp; Permissions</span>
            </button>
            <button data-section=\"contracts\" class=\"menu-item\">
              <i class=\"ri-file-text-line\"></i><span>Contrats</span>
            </button>
            <button data-section=\"leaves\" class=\"menu-item\">
              <i class=\"ri-calendar-todo-line\"></i><span>Congés</span>
            </button>
            <button data-section=\"medical-leaves\" class=\"menu-item\">
              <i class=\"ri-heart-pulse-line\"></i><span>Congés médicaux</span>
            </button>
          </div>

          <span class=\"menu-section-label\">Talents &amp; Finance</span>
          <div class=\"menu\">
            <button data-section=\"training\" class=\"menu-item\">
              <i class=\"ri-book-open-line\"></i><span>Formations</span>
            </button>
            <button data-section=\"performance\" class=\"menu-item\">
              <i class=\"ri-bar-chart-grouped-line\"></i><span>Évaluations</span>
            </button>
            <button data-section=\"recruitment\" class=\"menu-item\">
              <i class=\"ri-user-add-line\"></i><span>Recrutement</span>
            </button>
            <button data-section=\"payrolls\" class=\"menu-item\">
              <i class=\"ri-money-dollar-circle-line\"></i><span>Rémunération</span>
            </button>
            <button data-section=\"accounting\" class=\"menu-item\">
              <i class=\"ri-pie-chart-2-line\"></i><span>États finance</span>
            </button>
          </div>

          <span class=\"menu-section-label\">Administration</span>
          <div class=\"menu\">
            <button data-section=\"messages\" class=\"menu-item\">
              <i class=\"ri-message-2-line\"></i>
              <span>Messagerie</span>
              <span id=\"messagesUnreadBadge\" class=\"menu-badge hidden\">0</span>
            </button>
            <button data-section=\"notifications\" class=\"menu-item\">
              <i class=\"ri-notification-3-line\"></i>
              <span>Notifications</span>
              <span id=\"notifUnreadBadge\" class=\"menu-badge hidden\">0</span>
            </button>
            <button data-section=\"accounts\" class=\"menu-item\">
              <i class=\"ri-user-settings-line\"></i><span>Comptes agents</span>
            </button>
            <button data-section=\"reports\" class=\"menu-item\">
              <i class=\"ri-file-chart-line\"></i><span>Reporting</span>
            </button>
            <button data-section=\"settings\" class=\"menu-item\">
              <i class=\"ri-settings-3-line\"></i><span>Paramétrage</span>
            </button>
          </div>
        </nav>"""
if old_nav_start != -1:
    html = html[:old_nav_start] + new_nav + html[old_nav_end:]

strip = """
            <div class=\"presence-strip\" id=\"overviewPresenceStrip\">
              <div class=\"presence-stat\" onclick=\"navigate('punch')\"><div class=\"lbl\">Effectif attendu</div><div class=\"val\" id=\"ovExpected\">—</div></div>
              <div class=\"presence-stat\" onclick=\"navigate('punch')\"><div class=\"lbl\">Présents</div><div class=\"val ok\" id=\"ovPresent\">—</div></div>
              <div class=\"presence-stat\" onclick=\"navigate('punch')\"><div class=\"lbl\">Journée close</div><div class=\"val\" id=\"ovCompleted\">—</div></div>
              <div class=\"presence-stat\" onclick=\"navigate('punch')\"><div class=\"lbl\">Retards</div><div class=\"val warn\" id=\"ovLate\">—</div></div>
              <div class=\"presence-stat\" onclick=\"navigate('punch')\"><div class=\"lbl\">Absents</div><div class=\"val bad\" id=\"ovAbsent\">—</div></div>
            </div>
            <div class=\"chart-grid-2\" style=\"margin-bottom:14px\">
              <div class=\"chart-card-v2\">
                <div class=\"chart-header\"><div class=\"chart-header-left\"><h3 class=\"chart-title\">Temps réel — présence</h3><span class=\"chart-subtitle\"><span class=\"live-dot\"></span> Tableau du jour</span></div></div>
                <canvas id=\"presenceStatusChart\" height=\"160\"></canvas>
              </div>
              <div class=\"chart-card-v2\">
                <div class=\"chart-header\"><div class=\"chart-header-left\"><h3 class=\"chart-title\">Assiduité du jour</h3><span class=\"chart-subtitle\">Entrées biométriques</span></div></div>
                <div class=\"presence-ring-wrap\"><div class=\"presence-ring\" id=\"ovPresenceRing\" style=\"--p:0\"><div><strong>—</strong><span>taux présence</span></div></div></div>
                <div style=\"text-align:center;padding-bottom:12px\"><button class=\"btn btn-primary btn-sm\" onclick=\"navigate('punch')\"><i class=\"ri-fingerprint-line\"></i> Ouvrir le pointage</button></div>
              </div>
            </div>
"""
marker = "<!-- Quick actions -->"
if marker in html and "overviewPresenceStrip" not in html:
    html = html.replace(marker, strip + "\n            " + marker)

sections = """
          <section id=\"section-punch\" class=\"section\">
            <div class=\"punch-hero\">
              <div class=\"punch-stage\">
                <span class=\"punch-kicker\"><span class=\"live-dot\"></span> Terminal de présence</span>
                <h2>Pointage biométrique</h2>
                <p class=\"punch-lead\">Entrée le matin, sortie en fin de journée — empreinte ZK-9500 ou carte RFID. Une seule logique, traçable et fiable.</p>
                <div class=\"punch-clock\" id=\"punchClock\">--:--:--</div>
                <div class=\"punch-date\" id=\"punchDate\">—</div>
                <div class=\"punch-actions\">
                  <button type=\"button\" class=\"btn punch-btn-fp\" id=\"btnPunchFingerprint\"><i class=\"ri-fingerprint-line\"></i> Empreinte digitale</button>
                  <button type=\"button\" class=\"btn punch-btn-rfid\" id=\"btnPunchRfid\"><i class=\"ri-bank-card-line\"></i> Carte RFID</button>
                  <button type=\"button\" class=\"btn punch-btn-ghost\" id=\"btnRefreshPresence\"><i class=\"ri-refresh-line\"></i> Actualiser</button>
                </div>
                <div class=\"punch-result\" id=\"punchResult\">
                  <strong>En attente d'un badge ou d'une empreinte</strong>
                  <span>Le premier scan du jour enregistre l'arrivée ; le second enregistre la sortie.</span>
                </div>
              </div>
              <div class=\"presence-side\">
                <div class=\"presence-stat-grid\">
                  <div class=\"presence-stat\"><div class=\"lbl\">Attendus</div><div class=\"val\" id=\"punchStatExpected\">—</div></div>
                  <div class=\"presence-stat\"><div class=\"lbl\">Présents</div><div class=\"val ok\" id=\"punchStatPresent\">—</div></div>
                  <div class=\"presence-stat\"><div class=\"lbl\">Sortis</div><div class=\"val\" id=\"punchStatCompleted\">—</div></div>
                  <div class=\"presence-stat\"><div class=\"lbl\">Retards</div><div class=\"val warn\" id=\"punchStatLate\">—</div></div>
                </div>
                <div class=\"live-feed\">
                  <div class=\"live-feed-head\">
                    <h3>Flux en direct</h3>
                    <span style=\"color:var(--muted);font-size:.78rem\">Absents: <strong id=\"punchStatAbsent\">—</strong></span>
                  </div>
                  <div class=\"live-feed-list\" id=\"liveFeedList\"></div>
                </div>
              </div>
            </div>
            <div class=\"board-wrap\">
              <div class=\"board-toolbar\">
                <div>
                  <h3 style=\"margin:0;font-size:1.05rem\">Tableau de présence — aujourd'hui</h3>
                  <span style=\"color:var(--muted);font-size:.82rem\">Statuts calculés sur les pointages entrée / sortie</span>
                </div>
                <div class=\"filter-chips\">
                  <button type=\"button\" class=\"filter-chip active\" data-board-filter=\"all\">Tous</button>
                  <button type=\"button\" class=\"filter-chip\" data-board-filter=\"present\">Présents</button>
                  <button type=\"button\" class=\"filter-chip\" data-board-filter=\"completed\">Terminés</button>
                  <button type=\"button\" class=\"filter-chip\" data-board-filter=\"not_arrived\">Non arrivés</button>
                  <button type=\"button\" class=\"filter-chip\" data-board-filter=\"absent\">Absents</button>
                </div>
              </div>
              <div class=\"table-wrap\">
                <table class=\"board-table\">
                  <thead>
                    <tr>
                      <th>Agent</th><th>Département</th><th>Statut</th><th>Entrée</th><th>Sortie</th><th>Heures</th><th>Retard</th>
                    </tr>
                  </thead>
                  <tbody id=\"presenceBoardBody\"></tbody>
                </table>
              </div>
            </div>
          </section>

          <section id=\"section-myspace\" class=\"section\">
            <div id=\"myspaceRoot\">
              <div class=\"agent-card\"><h2>Mon espace</h2><p class=\"agent-meta\">Chargement du profil agent…</p></div>
            </div>
          </section>

"""
emp_marker = "<!-- EMPLOYÉS -->"
if "section-punch" not in html:
    html = html.replace(emp_marker, sections + "          " + emp_marker)

modal = """
    <div class=\"rfid-modal-backdrop\" id=\"rfidModal\">
      <div class=\"rfid-modal\">
        <h3>Pointage par carte RFID</h3>
        <p>Présentez la carte au lecteur ou saisissez l'identifiant.</p>
        <input id=\"rfidPunchInput\" type=\"text\" placeholder=\"ID carte RFID\" autocomplete=\"off\" />
        <div class=\"row\">
          <button type=\"button\" class=\"btn btn-secondary\" id=\"rfidPunchCancel\">Annuler</button>
          <button type=\"button\" class=\"btn btn-primary\" id=\"rfidPunchConfirm\">Valider le pointage</button>
        </div>
      </div>
    </div>
"""

if "rfidModal" not in html:
    html = html.replace("</body>", modal + "\n  </body>")

# Ensure JS includes
if "sgrh-vision.js" not in html:
    for old in [
        "{{ asset('js/dashboard.js') }}?v=20260809\"></script>",
        "{{ asset('js/dashboard.js') }}?v=20260809b\"></script>",
    ]:
        if old in html:
            html = html.replace(
                old,
                "{{ asset('js/dashboard.js') }}?v=20260809b\"></script>\n    <script src=\"{{ asset('js/sgrh-vision.js') }}?v=20260809b\"></script>",
            )
            break

path.write_text(html, encoding="utf-8")
print(
    "OK",
    "punch=" + str("section-punch" in html),
    "myspace=" + str("section-myspace" in html),
    "vision=" + str("sgrh-vision" in html),
    "strip=" + str("overviewPresenceStrip" in html),
)

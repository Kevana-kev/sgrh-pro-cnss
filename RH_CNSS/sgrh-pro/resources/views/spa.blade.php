<!doctype html>
<!--
  SGRH Pro — Système de Gestion des Ressources Humaines
  CNSS — Conception et implémentation d'un SIGRH intelligent
-->
<html lang="fr" data-theme="light">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SGRH Pro — CNSS</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Source+Serif+4:opsz,wght@8..60,500;8..60,700&display=swap" rel="stylesheet" />
    <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    <link rel="stylesheet" href="{{ asset('css/dashboard.css') }}?v=20260925a" />
    <link rel="stylesheet" href="{{ asset('css/dashboard-pro.css') }}?v=20260925a" />
    <link rel="stylesheet" href="{{ asset('css/sgrh-vision.css') }}?v=20260925a" />
    <meta name="biometric-bridge-url" content="http://127.0.0.1:5002" />
    <meta name="biometric-bridge-key" content="{{ config('services.biometric.bridge_api_key', 'local-secret-key') }}" />
  </head>
  <body>
    <div class="bg-orb orb-1"></div>
    <div class="bg-orb orb-2"></div>

    <!-- ====================================================== LOGIN SCREEN ====================================================== -->
    <div id="loginScreen" class="login-screen">
      <div class="login-shell">
        <aside class="login-hero" aria-hidden="false">
          <div class="login-hero-glow" aria-hidden="true"></div>
          <div class="login-hero-grid" aria-hidden="true"></div>
          <div class="login-hero-inner">
            <div class="login-hero-logo-wrap">
              <img
                src="{{ asset('images/cnss-logo.png') }}"
                alt="CNSS — Caisse Nationale de Sécurité Sociale"
                class="cnss-logo login-hero-logo"
              />
            </div>
            <p class="login-hero-site">Kinshasa — République Démocratique du Congo</p>
            <h2 class="login-hero-title">SGRH Pro</h2>
            <p class="login-hero-lead">
              Système de Gestion des Ressources Humaines — pilotage RH,
              pointage biométrique et suivi individuel des agents.
            </p>
            <ul class="login-features">
              <li>
                <span class="login-feature-icon"><i class="ri-fingerprint-2-line"></i></span>
                <span>Pointage empreinte ZK-9500 et badge RFID</span>
              </li>
              <li>
                <span class="login-feature-icon"><i class="ri-dashboard-3-line"></i></span>
                <span>Tableaux de bord et indicateurs en temps réel</span>
              </li>
              <li>
                <span class="login-feature-icon"><i class="ri-shield-check-line"></i></span>
                <span>Accès sécurisé par rôles et journal d'audit</span>
              </li>
            </ul>
            <p class="login-hero-foot">
              Caisse Nationale de Sécurité Sociale — Direction des Ressources Humaines
            </p>
          </div>
        </aside>

        <main class="login-panel">
          <div class="login-card">
            <header class="login-card-head">
              <div class="login-logo-wrap">
                <img
                  src="{{ asset('images/cnss-logo.png') }}"
                  alt="CNSS"
                  class="cnss-logo login-card-logo"
                />
              </div>
              <div class="login-card-intro">
                <strong>Connexion sécurisée</strong>
                <span>Identifiez-vous pour accéder à la plateforme</span>
              </div>
            </header>

            <div id="loginError" class="login-error hidden" role="alert" aria-live="polite"></div>

            <form id="loginForm" class="login-form" novalidate>
              <div class="login-field">
                <label for="username">Identifiant</label>
                <div class="login-input-wrap">
                  <i class="ri-user-3-line login-input-icon" aria-hidden="true"></i>
                  <input
                    id="username"
                    type="text"
                    name="username"
                    autocomplete="username"
                    placeholder="Matricule, nom d'utilisateur ou e-mail"
                    required
                  />
                </div>
              </div>

              <div class="login-field">
                <label for="password">Mot de passe</label>
                <div class="login-input-wrap">
                  <i class="ri-lock-2-line login-input-icon" aria-hidden="true"></i>
                  <input
                    id="password"
                    type="password"
                    name="password"
                    autocomplete="current-password"
                    placeholder="Saisissez votre mot de passe"
                    required
                  />
                  <button
                    type="button"
                    id="loginTogglePassword"
                    class="login-toggle-password"
                    aria-label="Afficher le mot de passe"
                    tabindex="-1"
                  >
                    <i class="ri-eye-line" id="loginTogglePasswordIcon" aria-hidden="true"></i>
                  </button>
                </div>
              </div>

              <button type="submit" id="loginSubmitBtn" class="btn btn-primary login-submit">
                <span class="login-submit-label">
                  <i class="ri-login-circle-line" aria-hidden="true"></i>
                  Se connecter
                </span>
                <span class="login-submit-spinner" aria-hidden="true"></span>
              </button>
            </form>
          </div>
        </main>
      </div>
    </div>

    <!-- ====================================================== APP SHELL ====================================================== -->
    <div id="appShell" class="app-shell hidden">

      <!-- SIDEBAR -->
      <aside class="sidebar">
        <div class="sidebar-header">
          <div class="brand">
            <div class="brand-logo-wrap">
              <img
                src="{{ asset('images/cnss-logo.png') }}"
                alt="CNSS"
                class="cnss-logo brand-logo"
              />
            </div>
            <div>
              <h2 id="sidebarCompanyName">SGRH Pro</h2>
              <small>Gestion RH &amp; Finance</small>
            </div>
          </div>
        </div>

        <div class="sidebar-owner">
          <small class="owner-label">Connecté en tant que</small>
          <article class="owner-card">
            <strong id="ownerName">Utilisateur</strong>
            <span id="ownerRole">Rôle non défini</span>
          </article>
        </div>

        <nav class="sidebar-nav" id="menuNav">
          <span class="menu-section-label">Cœur du système</span>
          <div class="menu">
            <button data-section="overview" class="menu-item active">
              <i class="ri-dashboard-horizontal-line"></i><span>Pilot de bord</span>
            </button>
            <button data-section="punch" class="menu-item menu-item--accent">
              <i class="ri-fingerprint-2-line"></i><span>Pointage</span>
            </button>
            <button data-section="myspace" class="menu-item">
              <i class="ri-user-heart-line"></i><span>Mon espace</span>
            </button>
            <button data-section="attendances" class="menu-item">
              <i class="ri-calendar-check-line"></i><span>Présences</span>
            </button>
            <button data-section="biometric" class="menu-item">
              <i class="ri-shield-keyhole-line"></i><span>Enrôlement biométrique</span>
            </button>
          </div>

          <span class="menu-section-label">Ressources Humaines</span>
          <div class="menu">
            <button data-section="employees" class="menu-item">
              <i class="ri-user-line"></i><span>Employés</span>
            </button>
            <button data-section="departments" class="menu-item">
              <i class="ri-building-2-line"></i><span>Départements</span>
            </button>
            <button data-section="team" class="menu-item">
              <i class="ri-team-line"></i><span>Équipe</span>
            </button>
            <button data-section="roles" class="menu-item">
              <i class="ri-shield-user-line"></i><span>Rôles &amp; Permissions</span>
            </button>
            <button data-section="contracts" class="menu-item">
              <i class="ri-file-text-line"></i><span>Contrats</span>
            </button>
            <button data-section="leaves" class="menu-item">
              <i class="ri-calendar-todo-line"></i><span>Congés</span>
            </button>
            <button data-section="medical-leaves" class="menu-item">
              <i class="ri-heart-pulse-line"></i><span>Congés médicaux</span>
            </button>
          </div>

          <span class="menu-section-label">Talents &amp; Finance</span>
          <div class="menu">
            <button data-section="training" class="menu-item">
              <i class="ri-book-open-line"></i><span>Formations</span>
            </button>
            <button data-section="performance" class="menu-item">
              <i class="ri-bar-chart-grouped-line"></i><span>Évaluations</span>
            </button>
            <button data-section="recruitment" class="menu-item">
              <i class="ri-user-add-line"></i><span>Recrutement</span>
            </button>
            <button data-section="payrolls" class="menu-item">
              <i class="ri-money-dollar-circle-line"></i><span>Rémunération</span>
            </button>
            <button data-section="accounting" class="menu-item">
              <i class="ri-pie-chart-2-line"></i><span>États finance</span>
            </button>
          </div>

          <span class="menu-section-label">Administration</span>
          <div class="menu">
            <button data-section="messages" class="menu-item">
              <i class="ri-message-2-line"></i>
              <span>Messagerie</span>
              <span id="messagesUnreadBadge" class="menu-badge hidden">0</span>
            </button>
            <button data-section="notifications" class="menu-item">
              <i class="ri-notification-3-line"></i>
              <span>Notifications</span>
              <span id="notifUnreadBadge" class="menu-badge hidden">0</span>
            </button>
            <button data-section="accounts" class="menu-item">
              <i class="ri-user-settings-line"></i><span>Comptes agents</span>
            </button>
            <button data-section="reports" class="menu-item">
              <i class="ri-file-chart-line"></i><span>Reporting</span>
            </button>
            <button data-section="settings" class="menu-item">
              <i class="ri-settings-3-line"></i><span>Paramétrage</span>
            </button>
          </div>
        </nav>

        <div class="sidebar-footer">
          <button id="themeToggle" class="theme-toggle-btn" type="button">
            <i class="ri-moon-line" id="themeIcon"></i>
            <span id="themeLabel">Mode clair</span>
          </button>
          <button id="logoutBtn" class="btn btn-danger">
            <i class="ri-logout-circle-r-line"></i> Déconnexion
          </button>
        </div>
      </aside>

      <!-- MAIN CONTENT -->
      <main class="main-content">
        <header class="topbar">
          <div class="topbar-left">
            <button type="button" class="menu-toggle-btn" id="btnSidebarToggle" aria-label="Ouvrir le menu">
              <i class="ri-menu-2-line"></i>
            </button>
            <div class="company-badge">
              <span class="company-dot" aria-hidden="true"></span>
              <div>
                <small class="company-label">Entreprise</small>
                <strong id="companyName">CNSS</strong>
              </div>
            </div>
            <h1 id="sectionTitle">Vue d'ensemble</h1>
          </div>
          <div class="topbar-right">
            <button id="refreshBtn" class="btn btn-secondary btn-sm topbar-refresh">
              <i class="ri-refresh-line"></i> <span class="btn-label">Actualiser</span>
            </button>
            <button class="topbar-icon-btn" onclick="navigate('notifications')" title="Notifications">
              <i class="ri-notification-3-line"></i>
              <span class="notif-dot hidden" id="topbarNotifDot"></span>
            </button>
            <button class="topbar-icon-btn" onclick="navigate('messages')" title="Messages">
              <i class="ri-message-2-line"></i>
              <span class="notif-dot hidden" id="topbarMsgDot"></span>
            </button>
            <div class="user-menu-btn" id="topbarUserBtn">
              <div class="user-menu-avatar" id="topbarAvatar">U</div>
              <span class="user-menu-name" id="topbarUserName">Utilisateur</span>
              <i class="ri-arrow-down-s-line user-menu-caret" style="color:var(--text-2);font-size:1rem"></i>
            </div>
          </div>
        </header>
        <div class="sidebar-backdrop" id="sidebarBackdrop" aria-hidden="true"></div>

        <div class="sections-wrap">

          <!-- VUE D'ENSEMBLE -->
          <section id="section-overview" class="section active">

            <div class="dash-toolbar">
              <div class="dash-toolbar-left">
                <h2 class="dash-heading">Pilot de bord</h2>
                <p class="dash-sub">KPIs, présence du jour et indicateurs sélectionnés</p>
              </div>
              <div class="dash-toolbar-right">
                <button type="button" class="btn btn-secondary btn-sm" id="btnDashCustomize">
                  <i class="ri-layout-grid-line"></i> Personnaliser l'affichage
                </button>
                <button type="button" class="btn btn-secondary btn-sm" id="btnDashReset" title="Réinitialiser">
                  <i class="ri-restart-line"></i>
                </button>
              </div>
            </div>

            <div class="dash-customize-panel" id="dashCustomizePanel" hidden>
              <div class="dash-customize-head">
                <strong>Graphiques &amp; blocs visibles</strong>
                <span>Choisis ce que tu veux voir sur le tableau de bord. Préférence mémorisée.</span>
              </div>
              <div class="dash-customize-grid" id="dashCustomizeGrid"></div>
              <div class="dash-customize-actions">
                <button type="button" class="btn btn-secondary btn-sm" id="btnDashSelectAll">Tout afficher</button>
                <button type="button" class="btn btn-secondary btn-sm" id="btnDashSelectDefaults">Essentiels</button>
                <button type="button" class="btn btn-primary btn-sm" id="btnDashApply">Appliquer</button>
              </div>
            </div>

            <!-- KPIs v2 -->
            <div class="kpi-grid-v2" id="overviewKpiGrid" data-dash-widget="kpis">
              <article class="kpi-card-v2 kpi-blue">
                <div class="kpi-top">
                  <div class="kpi-icon-wrap blue"><i class="ri-team-fill"></i></div>
                  <span class="kpi-delta up" id="kpiNewBadge">+0 ce mois</span>
                </div>
                <div class="kpi-label">Effectif total</div>
                <div class="kpi-number" id="kpiEmployees">—</div>
                <div class="kpi-sub"><i class="ri-user-follow-line"></i> <span id="kpiActive">0 actifs</span></div>
              </article>
              <article class="kpi-card-v2 kpi-green">
                <div class="kpi-top">
                  <div class="kpi-icon-wrap green"><i class="ri-money-dollar-circle-fill"></i></div>
                  <span class="kpi-delta flat" id="kpiPayrollDelta">Masse salariale</span>
                </div>
                <div class="kpi-label">Salaire moyen</div>
                <div class="kpi-number" id="kpiAvgSalary">—</div>
                <div class="kpi-sub"><i class="ri-bank-line"></i> <span id="kpiTotalPayroll">Total: 0</span></div>
              </article>
              <article class="kpi-card-v2 kpi-orange">
                <div class="kpi-top">
                  <div class="kpi-icon-wrap orange"><i class="ri-user-unfollow-fill"></i></div>
                  <span class="kpi-delta" id="kpiAbsDelta">Absentéisme</span>
                </div>
                <div class="kpi-label">Taux d'absence</div>
                <div class="kpi-number" id="kpiAbsence">—</div>
                <div class="kpi-sub"><i class="ri-calendar-close-line"></i> <span id="kpiAbsCount">0 absences</span></div>
              </article>
              <article class="kpi-card-v2 kpi-purple">
                <div class="kpi-top">
                  <div class="kpi-icon-wrap purple"><i class="ri-star-fill"></i></div>
                  <span class="kpi-delta flat">Score moyen</span>
                </div>
                <div class="kpi-label">Performance</div>
                <div class="kpi-number" id="kpiPerf">—</div>
                <div class="kpi-sub"><i class="ri-bar-chart-2-line"></i> <span id="kpiPerfCount">0 évaluations</span></div>
              </article>
              <article class="kpi-card-v2 kpi-teal">
                <div class="kpi-top">
                  <div class="kpi-icon-wrap teal"><i class="ri-book-fill"></i></div>
                  <span class="kpi-delta up" id="kpiTrainDelta">Formations</span>
                </div>
                <div class="kpi-label">Inscriptions</div>
                <div class="kpi-number" id="kpiTraining">—</div>
                <div class="kpi-sub"><i class="ri-check-double-line"></i> <span id="kpiTrainDone">0 terminées</span></div>
              </article>
              <article class="kpi-card-v2 kpi-red">
                <div class="kpi-top">
                  <div class="kpi-icon-wrap red"><i class="ri-user-add-fill"></i></div>
                  <span class="kpi-delta" id="kpiRecruitDelta">Recrutement</span>
                </div>
                <div class="kpi-label">Candidatures</div>
                <div class="kpi-number" id="kpiRecruitApps">—</div>
                <div class="kpi-sub"><i class="ri-briefcase-line"></i> <span id="kpiOpenOffers">0 offres</span></div>
              </article>
              <article class="kpi-card-v2 kpi-indigo">
                <div class="kpi-top">
                  <div class="kpi-icon-wrap indigo"><i class="ri-calendar-todo-fill"></i></div>
                  <span class="kpi-delta flat">Congés</span>
                </div>
                <div class="kpi-label">Demandes congés</div>
                <div class="kpi-number" id="kpiLeaves">—</div>
                <div class="kpi-sub"><i class="ri-time-line"></i> <span id="kpiLeavesPending">0 en attente</span></div>
              </article>
              <article class="kpi-card-v2 kpi-pink">
                <div class="kpi-top">
                  <div class="kpi-icon-wrap pink"><i class="ri-file-text-fill"></i></div>
                  <span class="kpi-delta warn" id="kpiContractExp">Contrats</span>
                </div>
                <div class="kpi-label">Contrats actifs</div>
                <div class="kpi-number" id="kpiContracts">—</div>
                <div class="kpi-sub"><i class="ri-alarm-warning-line"></i> <span id="kpiContractsExp">0 expirent bientôt</span></div>
              </article>
            </div>

            <div data-dash-widget="presence" class="dash-widget-block">
              <div class="presence-strip" id="overviewPresenceStrip">
                <div class="presence-stat" onclick="navigate('punch')"><div class="lbl">Effectif attendu</div><div class="val" id="ovExpected">—</div></div>
                <div class="presence-stat" onclick="navigate('punch')"><div class="lbl">Présents</div><div class="val ok" id="ovPresent">—</div></div>
                <div class="presence-stat" onclick="navigate('punch')"><div class="lbl">Journée close</div><div class="val" id="ovCompleted">—</div></div>
                <div class="presence-stat" onclick="navigate('punch')"><div class="lbl">Retards</div><div class="val warn" id="ovLate">—</div></div>
                <div class="presence-stat" onclick="navigate('punch')"><div class="lbl">Absents</div><div class="val bad" id="ovAbsent">—</div></div>
              </div>
              <div class="chart-grid-2" style="margin-bottom:14px">
                <div class="chart-card-v2">
                  <div class="chart-header"><div class="chart-header-left"><h3 class="chart-title">Temps réel — présence</h3><span class="chart-subtitle"><span class="live-dot"></span> Tableau du jour</span></div></div>
                  <canvas id="presenceStatusChart" height="160"></canvas>
                </div>
                <div class="chart-card-v2">
                  <div class="chart-header"><div class="chart-header-left"><h3 class="chart-title">Assiduité du jour</h3><span class="chart-subtitle">Entrées biométriques</span></div></div>
                  <div class="presence-ring-wrap"><div class="presence-ring" id="ovPresenceRing" style="--p:0"><div><strong>—</strong><span>taux présence</span></div></div></div>
                  <div style="text-align:center;padding-bottom:12px"><button class="btn btn-primary btn-sm" onclick="navigate('punch')"><i class="ri-fingerprint-line"></i> Ouvrir le pointage</button></div>
                </div>
              </div>
            </div>

            <!-- Quick actions -->
            <div class="quick-actions" data-dash-widget="actions">
              <button class="quick-action-btn" onclick="navigate('punch')">
                <i class="ri-fingerprint-2-line"></i> Terminal de pointage
              </button>
              <button class="quick-action-btn" onclick="navigate('myspace')">
                <i class="ri-user-heart-line"></i> Mon espace
              </button>
              <button class="quick-action-btn" onclick="navigate('employees')">
                <i class="ri-user-add-line"></i> Employés
              </button>
              <button class="quick-action-btn" onclick="navigate('leaves')">
                <i class="ri-calendar-todo-line"></i> Congés
              </button>
              <button class="quick-action-btn" onclick="navigate('performance')">
                <i class="ri-bar-chart-grouped-line"></i> Évaluations
              </button>
              <button class="quick-action-btn" onclick="navigate('reports')">
                <i class="ri-file-chart-line"></i> Rapports
              </button>
            </div>

            <div class="dash-charts-stack" id="dashChartsStack">
              <div class="dash-widget-block" data-dash-widget="payroll">
                <div class="chart-card-v2">
                  <div class="chart-header">
                    <div class="chart-header-left">
                      <h3 class="chart-title">Évolution de la masse salariale</h3>
                      <span class="chart-subtitle">12 derniers mois</span>
                    </div>
                  </div>
                  <div class="chart-canvas-wrap">
                    <canvas id="payrollTrendChart" height="120"></canvas>
                  </div>
                </div>
              </div>

              <div class="dash-widget-block" data-dash-widget="dept">
                <div class="chart-card-v2">
                  <div class="chart-header">
                    <div class="chart-header-left">
                      <h3 class="chart-title">Répartition par département</h3>
                      <span class="chart-subtitle">Effectifs</span>
                    </div>
                  </div>
                  <canvas id="deptChart" height="180"></canvas>
                </div>
              </div>

              <div class="dash-widget-block" data-dash-widget="attend">
                <div class="chart-card-v2">
                  <div class="chart-header">
                    <div class="chart-header-left">
                      <h3 class="chart-title">Présences vs Absences</h3>
                      <span class="chart-subtitle">12 derniers mois</span>
                    </div>
                  </div>
                  <canvas id="attendChart" height="180"></canvas>
                </div>
              </div>

              <div class="dash-widget-block" data-dash-widget="leaves">
                <div class="chart-card-v2">
                  <div class="chart-header">
                    <div class="chart-header-left">
                      <h3 class="chart-title">Statut des congés</h3>
                      <span class="chart-subtitle">Vue globale</span>
                    </div>
                  </div>
                  <canvas id="leaveChart" height="180"></canvas>
                </div>
              </div>

              <div class="dash-widget-block" data-dash-widget="perf">
                <div class="chart-card-v2">
                  <div class="chart-header">
                    <div class="chart-header-left">
                      <h3 class="chart-title">Distribution des scores</h3>
                      <span class="chart-subtitle">Évaluations de performance</span>
                    </div>
                  </div>
                  <canvas id="perfDistChart" height="180"></canvas>
                </div>
              </div>

              <div class="dash-widget-block" data-dash-widget="deptPayroll">
                <div class="chart-card-v2">
                  <div class="chart-header">
                    <div class="chart-header-left">
                      <h3 class="chart-title">Masse salariale par département</h3>
                      <span class="chart-subtitle">Distribution financière</span>
                    </div>
                  </div>
                  <canvas id="deptPayrollChart" height="140"></canvas>
                </div>
              </div>

              <div class="dash-widget-block" data-dash-widget="recruit">
                <div class="chart-card-v2">
                  <div class="chart-header">
                    <div class="chart-header-left">
                      <h3 class="chart-title">Entonnoir de recrutement</h3>
                      <span class="chart-subtitle">Pipeline des candidatures</span>
                    </div>
                  </div>
                  <canvas id="recruitFunnelChart" height="140"></canvas>
                </div>
              </div>

              <div class="dash-widget-block" data-dash-widget="stats">
                <div class="chart-card-v2">
                  <div class="chart-header">
                    <div class="chart-header-left">
                      <h3 class="chart-title">Indicateurs clés</h3>
                    </div>
                  </div>
                  <div id="overviewStatRows"></div>
                </div>
              </div>

              <div class="dash-widget-block" data-dash-widget="activity">
                <div class="chart-card-v2">
                  <div class="chart-header">
                    <div class="chart-header-left">
                      <h3 class="chart-title">Activité récente</h3>
                      <span class="chart-subtitle">Derniers événements RH</span>
                    </div>
                  </div>
                  <div class="activity-feed" id="overviewActivityFeed">
                    <div class="empty-state">
                      <i class="ri-time-line"></i>
                      <p>Aucune activité récente</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

          </section>

          
          <section id="section-punch" class="section">
            <div class="punch-hero">
              <div class="punch-stage" id="punchStage">
                <span class="punch-kicker"><span class="live-dot"></span> Terminal de présence</span>
                <h2>Pointage biométrique</h2>
                <p class="punch-lead">Entrée le matin, sortie en fin de journée — empreinte ZK-9500 ou carte RFID. Une seule logique, traçable et fiable.</p>
                <div class="punch-clock" id="punchClock">--:--:--</div>
                <div class="punch-date" id="punchDate">—</div>
                <p class="punch-next-hint" id="punchNextHint">Premier scan = entrée · second scan = sortie</p>
                <div class="punch-logic">
                  <div class="punch-logic-step"><span>1</span><div><strong>Arrivée</strong><small>Scan du matin</small></div></div>
                  <div class="punch-logic-step"><span>2</span><div><strong>Présence</strong><small>Journée ouverte</small></div></div>
                  <div class="punch-logic-step"><span>3</span><div><strong>Sortie</strong><small>Scan de fin de journée</small></div></div>
                </div>
                <div class="punch-actions">
                  <button type="button" class="btn punch-btn-fp" id="btnPunchFingerprint"><i class="ri-fingerprint-line"></i> Empreinte digitale</button>
                  <button type="button" class="btn punch-btn-rfid" id="btnPunchRfid"><i class="ri-bank-card-line"></i> Carte RFID</button>
                  <button type="button" class="btn punch-btn-ghost" id="btnRefreshPresence"><i class="ri-refresh-line"></i> Actualiser</button>
                </div>
                <div class="punch-result" id="punchResult">
                  <strong>En attente d'un badge ou d'une empreinte</strong>
                  <span>Le premier scan du jour enregistre l'arrivée ; le second enregistre la sortie.</span>
                </div>
              </div>
              <div class="presence-side">
                <div class="presence-stat-grid">
                  <div class="presence-stat"><div class="lbl">Attendus</div><div class="val" id="punchStatExpected">—</div></div>
                  <div class="presence-stat"><div class="lbl">Présents</div><div class="val ok" id="punchStatPresent">—</div></div>
                  <div class="presence-stat"><div class="lbl">Sortis</div><div class="val" id="punchStatCompleted">—</div></div>
                  <div class="presence-stat"><div class="lbl">Retards</div><div class="val warn" id="punchStatLate">—</div></div>
                </div>
                <div class="live-feed">
                  <div class="live-feed-head">
                    <h3>Flux en direct</h3>
                    <span style="color:var(--muted);font-size:.78rem">Absents: <strong id="punchStatAbsent">—</strong></span>
                  </div>
                  <div class="live-feed-list" id="liveFeedList"></div>
                </div>
              </div>
            </div>
            <div class="chart-grid-2">
              <div class="chart-card-v2">
                <div class="chart-header">
                  <div class="chart-header-left">
                    <h3 class="chart-title">Courbe horaire des pointages</h3>
                    <span class="chart-subtitle">Entrées vs sorties — aujourd'hui</span>
                  </div>
                </div>
                <canvas id="arrivalTimelineChart" height="140"></canvas>
              </div>
              <div class="chart-card-v2">
                <div class="chart-header">
                  <div class="chart-header-left">
                    <h3 class="chart-title">Règle opérationnelle</h3>
                    <span class="chart-subtitle">Conforme au mémoire SGRH Pro</span>
                  </div>
                </div>
                <ul class="ops-list">
                  <li><strong>Empreinte ZK-9500</strong> — identification 1:N via bridge local</li>
                  <li><strong>Carte RFID</strong> — lecture badge actif rattaché à l'agent</li>
                  <li><strong>Entrée / Sortie</strong> — 1er scan = check-in, 2e scan = check-out</li>
                  <li><strong>Retard</strong> — calculé vs heure d'ouverture + tolérance</li>
                  <li><strong>Espace agent</strong> — chaque compte suit ses propres performances</li>
                </ul>
              </div>
            </div>
            <div class="board-wrap">
              <div class="board-toolbar">
                <div>
                  <h3 style="margin:0;font-size:1.05rem">Tableau de présence — aujourd'hui</h3>
                  <span style="color:var(--muted);font-size:.82rem">Statuts calculés sur les pointages entrée / sortie</span>
                </div>
                <div class="filter-chips">
                  <button type="button" class="filter-chip active" data-board-filter="all">Tous</button>
                  <button type="button" class="filter-chip" data-board-filter="present">Présents</button>
                  <button type="button" class="filter-chip" data-board-filter="completed">Terminés</button>
                  <button type="button" class="filter-chip" data-board-filter="not_arrived">Non arrivés</button>
                  <button type="button" class="filter-chip" data-board-filter="absent">Absents</button>
                </div>
              </div>
              <div class="table-wrap">
                <table class="board-table">
                  <thead>
                    <tr>
                      <th>Agent</th><th>Département</th><th>Statut</th><th>Entrée</th><th>Sortie</th><th>Heures</th><th>Retard</th><th>Bio</th>
                    </tr>
                  </thead>
                  <tbody id="presenceBoardBody"></tbody>
                </table>
              </div>
            </div>
          </section>

          <section id="section-myspace" class="section">
            <div id="myspaceRoot">
              <div class="agent-card"><h2>Mon espace</h2><p class="agent-meta">Chargement du profil agent…</p></div>
            </div>
          </section>

          <!-- EMPLOYÉS -->
          <section id="section-employees" class="section">
            <!-- Stats -->
            <div class="section-stats-row">
              <div class="stat-badge blue"><i class="ri-team-fill"></i><div><div class="stat-badge-num" id="empStatTotal">—</div><div class="stat-badge-lbl">Total</div></div></div>
              <div class="stat-badge green"><i class="ri-user-follow-fill"></i><div><div class="stat-badge-num" id="empStatActif">—</div><div class="stat-badge-lbl">Actifs</div></div></div>
              <div class="stat-badge orange"><i class="ri-user-forbid-fill"></i><div><div class="stat-badge-num" id="empStatSuspendu">—</div><div class="stat-badge-lbl">Suspendus</div></div></div>
              <div class="stat-badge red"><i class="ri-user-minus-fill"></i><div><div class="stat-badge-num" id="empStatDemis">—</div><div class="stat-badge-lbl">Démissionnés</div></div></div>
            </div>
            <!-- Toolbar -->
            <div class="section-toolbar">
              <div class="section-toolbar-left">
                <div class="search-wrap">
                  <i class="ri-search-line"></i>
                  <input class="search-input" id="empSearch" placeholder="Nom, email, matricule…" type="text" oninput="filterEmployeesUI()" />
                </div>
                <div class="filter-chips">
                  <button class="filter-chip active" data-filter="" onclick="setEmpFilter(this)">Tous</button>
                  <button class="filter-chip" data-filter="Actif" onclick="setEmpFilter(this)">Actifs</button>
                  <button class="filter-chip" data-filter="Suspendu" onclick="setEmpFilter(this)">Suspendus</button>
                  <button class="filter-chip" data-filter="Démissionné" onclick="setEmpFilter(this)">Démissionnés</button>
                </div>
                <select class="search-input" id="empDeptFilter" style="width:auto;padding:8px 12px" onchange="filterEmployeesUI()">
                  <option value="">Tous les départements</option>
                </select>
              </div>
              <div class="section-toolbar-right">
                <div class="view-toggle-group">
                  <button class="view-toggle-btn active" id="empViewList" title="Vue liste" onclick="setEmpView('list')"><i class="ri-list-check"></i></button>
                  <button class="view-toggle-btn" id="empViewGrid" title="Vue cartes" onclick="setEmpView('grid')"><i class="ri-grid-fill"></i></button>
                </div>
                <button id="btnNewEmployee" class="btn btn-primary btn-sm" onclick="openDrawer('emp')">
                  <i class="ri-user-add-line"></i> Ajouter un employé
                </button>
              </div>
            </div>
            <!-- Data Panel -->
            <div class="panel">
              <div id="employeesTable" class="table-wrap"></div>
              <div id="employeesGrid" class="employee-cards-grid" style="display:none"></div>
            </div>
          </section>

          <!-- MODAL PROFIL EMPLOYÉ -->
          <div id="empProfileModal" class="modal-overlay" style="display:none" onclick="if(event.target===this)closeEmpProfile()">
            <div class="modal-v2">
              <button class="modal-v2-close" onclick="closeEmpProfile()"><i class="ri-close-line"></i></button>
              <div class="emp-profile-header">
                <div class="emp-profile-avatar" id="empModalAvatar">?</div>
                <div class="emp-profile-info">
                  <h2 id="empModalName">Nom Prénom</h2>
                  <p id="empModalRole" class="emp-profile-role">Rôle</p>
                  <span class="status-pill" id="empModalStatus">Actif</span>
                </div>
              </div>
              <div class="emp-profile-body">
                <div class="emp-profile-stat"><i class="ri-mail-line"></i><span id="empModalEmail">—</span></div>
                <div class="emp-profile-stat"><i class="ri-phone-line"></i><span id="empModalPhone">—</span></div>
                <div class="emp-profile-stat"><i class="ri-building-2-line"></i><span id="empModalDept">—</span></div>
                <div class="emp-profile-stat"><i class="ri-calendar-line"></i><span id="empModalHire">—</span></div>
              </div>
            </div>
          </div>

          <!-- ÉQUIPE -->
          <section id="section-team" class="section">
            <div class="section-stats-row" id="teamStatsRow">
              <div class="stat-badge blue"><i class="ri-team-fill"></i><div><div class="stat-badge-num" id="teamStatMembers">—</div><div class="stat-badge-lbl">Collaborateurs</div></div></div>
              <div class="stat-badge green"><i class="ri-user-follow-fill"></i><div><div class="stat-badge-num" id="teamStatPresent">—</div><div class="stat-badge-lbl">Présents</div></div></div>
              <div class="stat-badge orange"><i class="ri-time-fill"></i><div><div class="stat-badge-num" id="teamStatLate">—</div><div class="stat-badge-lbl">Retards</div></div></div>
              <div class="stat-badge red"><i class="ri-calendar-todo-fill"></i><div><div class="stat-badge-num" id="teamStatLeaves">—</div><div class="stat-badge-lbl">Congés à valider</div></div></div>
            </div>
            <div class="section-toolbar">
              <div class="section-toolbar-left">
                <div class="search-wrap">
                  <i class="ri-search-line"></i>
                  <input class="search-input" id="teamSearch" placeholder="Rechercher un collaborateur…" type="text" />
                </div>
              </div>
              <div class="section-toolbar-right">
                <button type="button" class="btn btn-secondary btn-sm" id="btnRefreshTeam"><i class="ri-refresh-line"></i> Actualiser</button>
              </div>
            </div>
            <div id="teamPanel" class="team-panel"></div>
          </section>

          <!-- DÉPARTEMENTS -->
          <section id="section-departments" class="section">
            <div class="section-toolbar">
              <div class="section-toolbar-left">
                <div class="search-wrap">
                  <i class="ri-search-line"></i>
                  <input class="search-input" id="deptSearch" placeholder="Rechercher un département…" type="text" />
                </div>
              </div>
              <div class="section-toolbar-right">
                <button id="btnNewDept" class="btn btn-primary btn-sm" onclick="openDrawer('dept')">
                  <i class="ri-building-2-line"></i> Nouveau département
                </button>
              </div>
            </div>
            <div class="panel">
              <div id="departmentsTable" class="table-wrap"></div>
            </div>
          </section>

          <!-- RÔLES & PERMISSIONS -->
          <section id="section-roles" class="section">
            <div class="split roles-layout">
              <form id="roleForm" class="panel form-grid role-create-form">
                <h3>Créer un rôle</h3>
                <label>Nom<input name="name" required /></label>
                <label>
                  Permissions
                  <div id="rolePermissionsChecklist" class="permissions-checklist">
                    <div class="perm-empty">Chargement des permissions...</div>
                  </div>
                </label>
                <button class="btn btn-primary">
                  <i class="ri-shield-user-line"></i> Créer
                </button>
              </form>
              <div class="panel roles-management-panel">
                <h3>Rôles &amp; permissions</h3>
                <div id="rolesTable" class="table-wrap"></div>
                <h3 class="roles-update-title">Modifier permissions d'un rôle</h3>
                <div class="form-grid roles-update-grid">
                  <label>Rôle
                    <select id="rolePermissionRoleId"><option value="">Sélectionner</option></select>
                  </label>
                  <label>Permissions
                    <div id="updateRolePermissionsChecklist" class="permissions-checklist">
                      <div class="perm-empty">Sélectionne un rôle pour afficher les permissions.</div>
                    </div>
                  </label>
                  <button id="btnRolePermissions" class="btn btn-secondary" type="button">
                    <i class="ri-save-line"></i> Mettre à jour
                  </button>
                </div>
              </div>
            </div>
          </section>

          <!-- SALAIRES -->
          <section id="section-payrolls" class="section">
            <div class="section-stats-row">
              <div class="stat-badge blue"><i class="ri-file-text-fill"></i><div><div class="stat-badge-num" id="payStatTotal">—</div><div class="stat-badge-lbl">Bulletins</div></div></div>
              <div class="stat-badge green"><i class="ri-money-dollar-circle-fill"></i><div><div class="stat-badge-num" id="payStatMasse">—</div><div class="stat-badge-lbl">Masse salariale</div></div></div>
              <div class="stat-badge purple"><i class="ri-bar-chart-fill"></i><div><div class="stat-badge-num" id="payStatAvg">—</div><div class="stat-badge-lbl">Salaire moyen net</div></div></div>
            </div>
            <div class="section-toolbar">
              <div class="section-toolbar-left">
                <div class="search-wrap">
                  <i class="ri-search-line"></i>
                  <input class="search-input" id="payrollSearch" placeholder="Rechercher un employé…" type="text" />
                </div>
              </div>
              <div class="section-toolbar-right">
                <button id="btnNewPayroll" class="btn btn-primary btn-sm" onclick="openDrawer('payroll')">
                  <i class="ri-money-dollar-circle-line"></i> Nouveau bulletin
                </button>
              </div>
            </div>
            <div class="panel">
              <div id="payrollsTable" class="table-wrap"></div>
            </div>
          </section>

          <!-- PRÉSENCES -->
          <section id="section-attendances" class="section">
            <div class="board-wrap" style="margin-bottom:14px">
              <div class="board-toolbar">
                <div>
                  <h3 style="margin:0;font-size:1.05rem">Registre historique</h3>
                  <span style="color:var(--muted);font-size:.82rem">Le pointage live (entrée/sortie) se fait dans le terminal biométrique</span>
                </div>
                <button type="button" class="btn btn-primary btn-sm" onclick="navigate('punch')"><i class="ri-fingerprint-2-line"></i> Ouvrir le pointage</button>
              </div>
            </div>

            <div class="section-toolbar">
              <div class="section-toolbar-left">
                <div class="search-wrap">
                  <i class="ri-search-line"></i>
                  <input class="search-input" id="attendSearch" placeholder="Rechercher un agent…" type="text" />
                </div>
              </div>
              <div class="section-toolbar-right">
                <button class="btn btn-secondary btn-sm" onclick="openDrawer('attend-summary')">
                  <i class="ri-calendar-check-line"></i> Synthèse mensuelle
                </button>
                <button class="btn btn-primary btn-sm" onclick="openDrawer('attendance')">
                  <i class="ri-login-circle-line"></i> Enregistrer pointage
                </button>
              </div>
            </div>
            <div class="panel">
              <div id="attendancesTable" class="table-wrap"></div>
            </div>
            <div class="panel" id="attendanceSummaryPanel" style="margin-top:14px;display:none">
              <div class="panel-header">
                <h3>Synthèse mensuelle</h3>
                <div class="actions-inline" style="display:flex;gap:8px;align-items:center">
                  <input id="attendanceSummaryMonth" type="month" style="width:150px" />
                  <button id="btnAttendanceSummary" class="btn btn-secondary btn-sm" type="button">
                    <i class="ri-calendar-check-line"></i> Voir
                  </button>
                </div>
              </div>
              <div id="attendanceSummaryTable" class="table-wrap"></div>
            </div>
          </section>

          <!-- CONGÉS -->
          <section id="section-leaves" class="section">
            <!-- Stats -->
            <div class="section-stats-row">
              <div class="stat-badge orange"><i class="ri-time-fill"></i><div><div class="stat-badge-num" id="leaveStatPending">—</div><div class="stat-badge-lbl">En attente</div></div></div>
              <div class="stat-badge green"><i class="ri-checkbox-circle-fill"></i><div><div class="stat-badge-num" id="leaveStatApproved">—</div><div class="stat-badge-lbl">Approuvés</div></div></div>
              <div class="stat-badge red"><i class="ri-close-circle-fill"></i><div><div class="stat-badge-num" id="leaveStatRejected">—</div><div class="stat-badge-lbl">Refusés</div></div></div>
            </div>
            <!-- Pending approvals queue -->
            <div id="leaveApprovalQueue" class="approval-queue" style="display:none"></div>
            <!-- Toolbar -->
            <div class="section-toolbar">
              <div class="section-toolbar-left">
                <div class="search-wrap">
                  <i class="ri-search-line"></i>
                  <input class="search-input" id="leaveSearch" placeholder="Rechercher par employé…" type="text" />
                </div>
                <div class="filter-chips">
                  <button class="filter-chip active" data-leave-filter="" onclick="setLeaveFilter(this)">Tous</button>
                  <button class="filter-chip" data-leave-filter="En attente" onclick="setLeaveFilter(this)">En attente</button>
                  <button class="filter-chip" data-leave-filter="Approuvé" onclick="setLeaveFilter(this)">Approuvés</button>
                  <button class="filter-chip" data-leave-filter="Rejeté" onclick="setLeaveFilter(this)">Refusés</button>
                </div>
              </div>
              <div class="section-toolbar-right">
                <button class="btn btn-primary btn-sm" onclick="openDrawer('leave')">
                  <i class="ri-calendar-todo-line"></i> Nouvelle demande
                </button>
              </div>
            </div>
            <div class="panel">
              <div id="leavesTable" class="table-wrap"></div>
            </div>
          </section>

          <!-- BIOMÉTRIE & RFID -->
          <section id="section-biometric" class="section">
            <div class="biometric-status-bar">
              <span class="status-dot checking" id="biometricDot"></span>
              <i class="ri-radio-line"></i>
              <span id="biometricBridgeStatus">Vérification du lecteur biométrique (port 5002)...</span>
              <button id="btnRefreshBiometricStatus" class="btn btn-secondary btn-sm" style="margin-left:auto" type="button">
                <i class="ri-refresh-line"></i> Vérifier
              </button>
            </div>
            <div class="split">
              <div class="panel">
                <h3><i class="ri-fingerprint-line"></i> Enrôlement biométrique</h3>
                <div class="fp-scanner-area">
                  <div class="fp-icon" id="fpIcon">
                    <i class="ri-fingerprint-line"></i>
                  </div>
                  <p id="fingerprintStatus">Sélectionnez un employé puis enregistrez 3 doigts distincts</p>
                  <div class="fp-progress" id="fpProgress">
                    <span class="fp-step" data-step="1">Doigt 1</span>
                    <span class="fp-step" data-step="2">Doigt 2</span>
                    <span class="fp-step" data-step="3">Doigt 3</span>
                  </div>
                </div>
                <div class="form-grid">
                  <label>Employé à enrôler
                    <select id="biometricEmployeeSelect">
                      <option value="">Sélectionner un employé</option>
                    </select>
                  </label>
                  <div class="fp-enroll-actions">
                    <button id="btnEnrollFingerprint" class="btn btn-primary" type="button">
                      <i class="ri-fingerprint-2-line"></i> Scanner le doigt 1/3
                    </button>
                    <button id="btnResetEnrollment" class="btn btn-secondary" type="button">
                      <i class="ri-restart-line"></i> Recommencer
                    </button>
                  </div>
                </div>
              </div>
              <div class="panel">
                <h3><i class="ri-nfc-line"></i> Gestion des cartes RFID</h3>
                <form id="rfidAssignForm" class="form-grid">
                  <label>Employé
                    <select id="rfidEmployeeId" name="employee_id" required>
                      <option value="">Sélectionner un employé</option>
                    </select>
                  </label>
                  <label>Numéro de carte RFID
                    <input name="rfid_card_id" placeholder="Ex: RFID-00123456" required />
                  </label>
                  <button class="btn btn-primary" type="submit">
                    <i class="ri-nfc-line"></i> Assigner la carte
                  </button>
                </form>
                <div style="margin-top:18px;display:flex;justify-content:space-between;align-items:center">
                  <h3 style="margin:0;font-size:0.9rem">Employés enrôlés</h3>
                  <button id="btnRefreshEnrolled" class="btn btn-secondary btn-sm" type="button">
                    <i class="ri-refresh-line"></i>
                  </button>
                </div>
                <div id="biometricEnrolledTable" class="table-wrap" style="margin-top:10px"></div>
              </div>
            </div>
          </section>

          <!-- CONTRATS -->
          <section id="section-contracts" class="section">
            <div id="contractExpiryAlert" class="expiry-alert" style="display:none">
              <i class="ri-alarm-warning-fill"></i>
              <span id="contractExpiryMsg">Des contrats expirent dans les 30 jours</span>
            </div>
            <div class="section-stats-row">
              <div class="stat-badge blue"><i class="ri-file-text-fill"></i><div><div class="stat-badge-num" id="contractStatTotal">—</div><div class="stat-badge-lbl">Total</div></div></div>
              <div class="stat-badge green"><i class="ri-file-shield-fill"></i><div><div class="stat-badge-num" id="contractStatCdi">—</div><div class="stat-badge-lbl">CDI</div></div></div>
              <div class="stat-badge orange"><i class="ri-file-warning-fill"></i><div><div class="stat-badge-num" id="contractStatCdd">—</div><div class="stat-badge-lbl">CDD</div></div></div>
              <div class="stat-badge teal"><i class="ri-file-unknow-fill"></i><div><div class="stat-badge-num" id="contractStatStage">—</div><div class="stat-badge-lbl">Stages</div></div></div>
            </div>
            <div class="section-toolbar">
              <div class="section-toolbar-left">
                <div class="search-wrap">
                  <i class="ri-search-line"></i>
                  <input class="search-input" id="contractSearch" placeholder="Rechercher un contrat…" type="text" />
                </div>
                <div class="filter-chips">
                  <button class="filter-chip active" data-ctype-filter="" onclick="setContractFilter(this)">Tous</button>
                  <button class="filter-chip" data-ctype-filter="CDI" onclick="setContractFilter(this)">CDI</button>
                  <button class="filter-chip" data-ctype-filter="CDD" onclick="setContractFilter(this)">CDD</button>
                  <button class="filter-chip" data-ctype-filter="Stage" onclick="setContractFilter(this)">Stage</button>
                </div>
              </div>
              <div class="section-toolbar-right">
                <button id="btnNewContract" class="btn btn-primary btn-sm" onclick="openDrawer('contract')">
                  <i class="ri-file-add-line"></i> Nouveau contrat
                </button>
              </div>
            </div>
            <div class="panel">
              <div id="contractsTable" class="table-wrap"></div>
            </div>
          </section>

          <!-- MESSAGERIE -->
          <section id="section-messages" class="section">
            <div class="chat-shell">
              <aside class="chat-sidebar">
                <div class="chat-sidebar-top">
                  <input id="messagesSearch" type="text" placeholder="Rechercher une discussion..." />
                  <button id="btnMessagesRefresh" class="btn btn-secondary btn-sm" type="button">
                    <i class="ri-refresh-line"></i>
                  </button>
                </div>
                <div class="chat-sidebar-actions">
                  <select id="newConversationRecipient"><option value="">Choisir un agent...</option></select>
                  <button id="btnNewConversation" class="btn btn-primary btn-sm" type="button">
                    <i class="ri-add-line"></i> Nouveau
                  </button>
                </div>
                <div id="messagesConversations" class="chat-conversations"></div>
              </aside>
              <section class="chat-main">
                <header class="chat-header">
                  <h3 id="chatTitle">Sélectionne une discussion</h3>
                  <small id="chatSubtitle">Aucun message chargé</small>
                </header>
                <div id="chatMessages" class="chat-messages"></div>
                <form id="chatComposerForm" class="chat-composer">
                  <input id="chatMessageInput" name="content" type="text" maxlength="2000" placeholder="Écris un message..." required />
                  <button class="btn btn-primary" type="submit">
                    <i class="ri-send-plane-line"></i>
                  </button>
                </form>
              </section>
            </div>
          </section>

          <!-- COMPTES AGENTS -->
          <section id="section-accounts" class="section">
            <div class="panel">
              <h3>Administration des comptes agents</h3>
              <div class="actions-inline">
                <input id="accountUserQuery" type="text" placeholder="Rechercher..." list="accountSuggestionsList" autocomplete="off" />
                <select id="accountUserId"><option value="">Sélectionner un agent</option></select>
                <select id="accountRoleId"><option value="">Rôle</option></select>
                <select id="accountStatus">
                  <option value="">Statut</option>
                  <option value="Actif">Actif</option>
                  <option value="Suspendu">Suspendu</option>
                  <option value="Démissionné">Démissionné</option>
                </select>
                <button id="btnAccountRole" class="btn btn-secondary btn-sm" type="button">Changer rôle</button>
                <button id="btnAccountStatus" class="btn btn-secondary btn-sm" type="button">Changer statut</button>
                <button id="btnAccountReset" class="btn btn-danger btn-sm" type="button">Reset MDP</button>
              </div>
              <div id="accountsTable" class="table-wrap"></div>
              <h3 style="margin-top:20px">Historique des actions admin</h3>
              <div class="actions-inline logs-filters">
                <input id="logUsername" type="text" placeholder="Filtre utilisateur" />
                <input id="logAction" type="text" placeholder="Filtre action" />
                <input id="logStartDate" type="date" />
                <input id="logEndDate" type="date" />
                <button id="btnLogsFilter" class="btn btn-secondary btn-sm" type="button">Filtrer</button>
                <button id="btnLogsClear" class="btn btn-secondary btn-sm" type="button">Réinitialiser</button>
                <button id="btnLogsExportCsv" class="btn btn-primary btn-sm" type="button">
                  <i class="ri-file-excel-line"></i> CSV
                </button>
                <button id="btnLogsExportPdf" class="btn btn-primary btn-sm" type="button">
                  <i class="ri-file-pdf-line"></i> PDF
                </button>
              </div>
              <div id="accountLogsTable" class="table-wrap"></div>
            </div>
          </section>

          <!-- REPORTING -->
          <section id="section-reports" class="section">
            <div class="panel">
              <h3>Reporting global</h3>
              <div class="reports-layout">
                <pre id="reportsInfo" class="json-box">Ouvre cette section pour charger le reporting.</pre>
                <div id="reportsCards" class="kpi-grid"></div>
                <div id="reportsDepartments" class="table-wrap"></div>
              </div>
            </div>
          </section>

          <!-- COMPTABILITÉ -->
          <section id="section-accounting" class="section">
            <div class="panel">
              <h3>Comptabilité avancée</h3>
              <div class="reports-layout">
                <pre id="accountingInfo" class="json-box">Ouvre cette section pour charger la comptabilité.</pre>
                <div id="accountingCards" class="kpi-grid"></div>
                <div class="charts-grid">
                  <div class="chart-card">
                    <h3>Évolution mensuelle (brut/net/impôts)</h3>
                    <canvas id="accountingMonthlyChart"></canvas>
                  </div>
                  <div class="chart-card">
                    <h3>Structure des coûts</h3>
                    <canvas id="accountingCostChart"></canvas>
                  </div>
                </div>
                <div class="chart-card" style="margin-top:12px">
                  <h3>Net par département</h3>
                  <canvas id="accountingDepartmentsChart"></canvas>
                </div>
                <div id="accountingDepartmentsTable" class="table-wrap"></div>
              </div>
            </div>
          </section>

          <div id="toast" class="toast hidden"></div>

          <!-- MODAL FICHE DE PAIE -->
          <div id="payslipModal" class="modal-overlay" style="display:none" onclick="if(event.target===this)closePayslipModal()">
            <div class="modal-v2" style="max-width:780px;width:95%">
              <div class="modal-v2-header">
                <div style="display:flex;align-items:center;gap:10px">
                  <i class="ri-file-text-line" style="color:var(--primary);font-size:1.2rem"></i>
                  <h3 style="margin:0">Bulletin de Paie</h3>
                </div>
                <div style="display:flex;gap:8px;align-items:center">
                  <button class="btn btn-secondary btn-sm" onclick="window.print()">
                    <i class="ri-printer-line"></i> Imprimer
                  </button>
                  <button class="modal-v2-close" onclick="closePayslipModal()"><i class="ri-close-line"></i></button>
                </div>
              </div>
              <div class="modal-v2-body">
                <div class="payslip-card" id="payslipCardContent">
                  <div class="payslip-header">
                    <div class="payslip-company">
                      CNSS – Caisse Nationale de Sécurité Sociale
                      <small>Direction des Ressources Humaines</small>
                    </div>
                    <div class="payslip-period">
                      Bulletin de salaire<strong id="psMonth">—</strong>
                    </div>
                  </div>
                  <div class="payslip-emp-row">
                    <div class="payslip-emp-field">
                      <label>Employé</label>
                      <span id="psEmpName">—</span>
                    </div>
                    <div class="payslip-emp-field">
                      <label>Département</label>
                      <span id="psEmpDept">—</span>
                    </div>
                    <div class="payslip-emp-field">
                      <label>N° Employé</label>
                      <span id="psEmpId">—</span>
                    </div>
                    <div class="payslip-emp-field">
                      <label>Date de paiement</label>
                      <span id="psPaidAt">—</span>
                    </div>
                  </div>
                  <table class="payslip-table">
                    <thead>
                      <tr><th>Désignation</th><th style="text-align:right">Montant (XAF)</th></tr>
                    </thead>
                    <tbody>
                      <tr><td>Salaire de base</td><td class="td-amount" id="psBase">0</td></tr>
                      <tr><td>Primes &amp; bonus</td><td class="td-amount" id="psBonus">0</td></tr>
                      <tr><td>Heures supplémentaires</td><td class="td-amount" id="psOvertime">0</td></tr>
                      <tr><td style="color:var(--danger)">Déductions</td><td class="td-amount" style="color:var(--danger)" id="psDeductions">0</td></tr>
                      <tr><td style="color:var(--danger)">Impôts &amp; cotisations</td><td class="td-amount" style="color:var(--danger)" id="psTaxes">0</td></tr>
                    </tbody>
                  </table>
                  <div class="payslip-net-row">
                    <span style="color:var(--text-2);margin-right:16px">SALAIRE NET À PAYER</span>
                    <strong id="psNet">0 XAF</strong>
                  </div>
                  <p style="font-size:0.72rem;color:var(--text-3);margin-top:14px;text-align:center">
                    Document généré automatiquement par le SIGRH — CNSS
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- ══ FORMATION ══ -->
          <section id="section-training" class="section">
            <!-- KPIs formations -->
            <div class="kpi-grid-v2" style="grid-template-columns:repeat(4,1fr);margin-bottom:16px">
              <article class="kpi-card-v2 kpi-teal" style="padding:14px 16px">
                <div class="kpi-label">Total formations</div>
                <div class="kpi-number" id="trainKpiTotal" style="font-size:1.8rem">—</div>
              </article>
              <article class="kpi-card-v2 kpi-blue" style="padding:14px 16px">
                <div class="kpi-label">En cours</div>
                <div class="kpi-number" id="trainKpiInProgress" style="font-size:1.8rem">—</div>
              </article>
              <article class="kpi-card-v2 kpi-green" style="padding:14px 16px">
                <div class="kpi-label">Terminées</div>
                <div class="kpi-number" id="trainKpiDone" style="font-size:1.8rem">—</div>
              </article>
              <article class="kpi-card-v2 kpi-purple" style="padding:14px 16px">
                <div class="kpi-label">Inscriptions</div>
                <div class="kpi-number" id="trainKpiEnroll" style="font-size:1.8rem">—</div>
              </article>
            </div>
            <!-- Grille cartes formations -->
            <div class="panel" style="margin-bottom:16px">
              <div class="panel-header">
                <h3>Catalogue des formations</h3>
                <button id="btnNewTraining" class="btn btn-primary btn-sm" type="button">
                  <i class="ri-add-line"></i> Nouvelle formation
                </button>
              </div>
              <div id="trainingCardGrid" class="formation-card-grid"></div>
              <div id="trainingList" class="table-wrap" style="display:none"></div>
            </div>
            <div class="split">
              <div class="panel">
                <h3>Nouvelle formation</h3>
                <form id="trainingForm" class="form-grid">
                  <label>Titre <input type="text" name="title" required /></label>
                  <label>Formateur <input type="text" name="trainer" /></label>
                  <label>Date début <input type="date" name="start_date" required /></label>
                  <label>Date fin <input type="date" name="end_date" required /></label>
                  <label>Places max <input type="number" name="max_participants" value="20" min="1" /></label>
                  <label>Statut
                    <select name="status">
                      <option value="planifié">Planifié</option>
                      <option value="en cours">En cours</option>
                      <option value="terminé">Terminé</option>
                      <option value="annulé">Annulé</option>
                    </select>
                  </label>
                  <label style="grid-column:1/-1">Description
                    <textarea name="description" rows="3"></textarea>
                  </label>
                  <button class="btn btn-primary" type="submit">
                    <i class="ri-save-line"></i> Enregistrer
                  </button>
                </form>
              </div>
              <div class="panel">
                <h3>Compétences</h3>
                <form id="skillForm" class="form-grid" style="grid-template-columns:1fr 1fr auto">
                  <label>Compétence <input type="text" name="skill_name" placeholder="ex: Python, Management…" /></label>
                  <label>Catégorie <input type="text" name="skill_category" placeholder="ex: Technique, Soft skill…" /></label>
                  <button class="btn btn-secondary" type="submit" style="align-self:flex-end">
                    <i class="ri-add-line"></i>
                  </button>
                </form>
                <div id="skillList" class="table-wrap" style="margin-top:10px"></div>
              </div>
            </div>
          </section>

          <!-- ══ ÉVALUATION PERFORMANCES ══ -->
          <section id="section-performance" class="section">
            <!-- Graphiques performance -->
            <div class="grid-2-1" style="margin-bottom:16px">
              <div class="chart-card-v2">
                <div class="chart-header">
                  <div class="chart-header-left">
                    <h3 class="chart-title">Scores de performance</h3>
                    <span class="chart-subtitle">Distribution globale des évaluations</span>
                  </div>
                </div>
                <canvas id="perfRadarChart" height="200"></canvas>
              </div>
              <div class="chart-card-v2">
                <div class="chart-header">
                  <div class="chart-header-left">
                    <h3 class="chart-title">Top performers</h3>
                    <span class="chart-subtitle">Meilleurs scores</span>
                  </div>
                </div>
                <div id="perfTopList" style="padding:4px 0"></div>
              </div>
            </div>
            <div class="split">
              <div class="panel">
                <div class="panel-header">
                  <h3>Évaluations de performance</h3>
                  <button id="btnNewEval" class="btn btn-primary btn-sm" type="button">
                    <i class="ri-add-line"></i> Nouvelle évaluation
                  </button>
                </div>
                <div id="performanceStats" class="kpi-grid" style="margin-bottom:14px"></div>
                <div id="evaluationList" class="table-wrap"></div>
              </div>
              <div class="panel">
                <h3>Créer / modifier une évaluation</h3>
                <form id="evaluationForm" class="form-grid">
                  <label>Employé
                    <select id="evalEmployeeSelect" name="employee_id" required>
                      <option value="">-- Choisir --</option>
                    </select>
                  </label>
                  <label>Évaluateur
                    <select id="evalEvaluatorSelect" name="evaluator_id">
                      <option value="">-- Optionnel --</option>
                    </select>
                  </label>
                  <label>Période <input type="text" name="period" placeholder="ex: T1-2025" required /></label>
                  <label>Score (0-100) <input type="number" name="score" min="0" max="100" step="0.1" /></label>
                  <label>Statut
                    <select name="status">
                      <option value="en cours">En cours</option>
                      <option value="finalisé">Finalisé</option>
                      <option value="validé">Validé</option>
                    </select>
                  </label>
                  <label style="grid-column:1/-1">Objectifs
                    <textarea name="objectives" rows="2" placeholder="Objectifs fixés…"></textarea>
                  </label>
                  <label style="grid-column:1/-1">Commentaires
                    <textarea name="comments" rows="2"></textarea>
                  </label>
                  <button class="btn btn-primary" type="submit">
                    <i class="ri-save-line"></i> Enregistrer
                  </button>
                </form>
              </div>
            </div>
          </section>

          <!-- ══ CONGÉS MÉDICAUX ══ -->
          <section id="section-medical-leaves" class="section">
            <div class="split">
              <div class="panel">
                <div class="panel-header">
                  <h3>Arrêts maladie &amp; congés médicaux</h3>
                  <button id="btnRefreshMedical" class="btn btn-secondary btn-sm" type="button">
                    <i class="ri-refresh-line"></i>
                  </button>
                </div>
                <div id="medicalLeaveList" class="table-wrap"></div>
              </div>
              <div class="panel">
                <h3>Déclarer un arrêt maladie</h3>
                <form id="medicalLeaveForm" class="form-grid">
                  <label>Employé
                    <select id="medEmployeeSelect" name="employee_id" required>
                      <option value="">-- Choisir --</option>
                    </select>
                  </label>
                  <label>Date début <input type="date" name="start_date" required /></label>
                  <label>Date fin <input type="date" name="end_date" required /></label>
                  <label>Diagnostic <input type="text" name="diagnosis" /></label>
                  <label>Indemnité journalière (FCFA)
                    <input type="number" name="daily_allowance" value="0" min="0" />
                  </label>
                  <label>Statut
                    <select name="status">
                      <option value="En attente">En attente</option>
                      <option value="Validé">Validé</option>
                      <option value="Refusé">Refusé</option>
                    </select>
                  </label>
                  <button class="btn btn-primary" type="submit">
                    <i class="ri-save-line"></i> Déclarer
                  </button>
                </form>
              </div>
            </div>
          </section>

          <!-- ══ NOTIFICATIONS ══ -->
          <section id="section-notifications" class="section">
            <div class="panel">
              <div class="panel-header">
                <h3>Centre de notifications</h3>
                <div style="display:flex;gap:8px">
                  <button id="btnGenerateAlerts" class="btn btn-secondary btn-sm" type="button">
                    <i class="ri-alarm-warning-line"></i> Générer alertes
                  </button>
                  <button id="btnMarkAllRead" class="btn btn-secondary btn-sm" type="button">
                    <i class="ri-check-double-line"></i> Tout marquer lu
                  </button>
                </div>
              </div>
              <!-- KPIs Notifs -->
              <div class="kpi-grid-v2" style="grid-template-columns:repeat(4,1fr);margin-bottom:18px" id="notifKpiRow">
                <article class="kpi-card-v2 kpi-blue" style="padding:14px 16px">
                  <div class="kpi-label" style="font-size:.75rem">Total</div>
                  <div class="kpi-number" id="notifKpiTotal" style="font-size:1.6rem">—</div>
                </article>
                <article class="kpi-card-v2 kpi-red" style="padding:14px 16px">
                  <div class="kpi-label" style="font-size:.75rem">Non lues</div>
                  <div class="kpi-number" id="notifKpiUnread" style="font-size:1.6rem">—</div>
                </article>
                <article class="kpi-card-v2 kpi-orange" style="padding:14px 16px">
                  <div class="kpi-label" style="font-size:.75rem">Alertes</div>
                  <div class="kpi-number" id="notifKpiAlerts" style="font-size:1.6rem">—</div>
                </article>
                <article class="kpi-card-v2 kpi-green" style="padding:14px 16px">
                  <div class="kpi-label" style="font-size:.75rem">Succès</div>
                  <div class="kpi-number" id="notifKpiSuccess" style="font-size:1.6rem">—</div>
                </article>
              </div>
              <form id="notifForm" class="form-grid" style="grid-template-columns:1fr 1fr 1fr auto;margin-bottom:16px">
                <label>Titre <input type="text" name="title" placeholder="Titre de la notification" /></label>
                <label>Type
                  <select name="type">
                    <option value="info">Info</option>
                    <option value="warning">Alerte</option>
                    <option value="success">Succès</option>
                    <option value="error">Erreur</option>
                  </select>
                </label>
                <label>Message <input type="text" name="message" placeholder="Contenu…" /></label>
                <button class="btn btn-primary" type="submit" style="align-self:flex-end">
                  <i class="ri-send-plane-line"></i>
                </button>
              </form>
              <div id="notificationList" class="notifications-wrap"></div>
            </div>
          </section>

          <!-- ══ RECRUTEMENT ══ -->
          <section id="section-recruitment" class="section">
            <!-- Pipeline visuel -->
            <div class="chart-card-v2" style="margin-bottom:16px">
              <div class="chart-header">
                <div class="chart-header-left">
                  <h3 class="chart-title">Pipeline de recrutement</h3>
                  <span class="chart-subtitle">Vue entonnoir des candidatures</span>
                </div>
                <button id="btnRefreshPipeline" class="btn btn-secondary btn-sm" type="button">
                  <i class="ri-refresh-line"></i>
                </button>
              </div>
              <div id="recruitPipelineStats" class="pipeline-stats"></div>
            </div>
            <div class="split">
              <div class="panel">
                <div class="panel-header">
                  <h3>Offres d'emploi</h3>
                  <button id="btnNewOffer" class="btn btn-primary btn-sm" type="button">
                    <i class="ri-add-line"></i> Nouvelle offre
                  </button>
                </div>
                <div id="recruitmentStats" class="kpi-grid" style="margin-bottom:14px"></div>
                <div id="jobOfferList" class="table-wrap"></div>
              </div>
              <div class="panel">
                <h3>Créer une offre d'emploi</h3>
                <form id="jobOfferForm" class="form-grid">
                  <label>Titre du poste <input type="text" name="title" required /></label>
                  <label>Département
                    <select id="jobDeptSelect" name="department_id">
                      <option value="">-- Aucun --</option>
                    </select>
                  </label>
                  <label>Statut
                    <select name="status">
                      <option value="ouvert">Ouvert</option>
                      <option value="fermé">Fermé</option>
                    </select>
                  </label>
                  <label style="grid-column:1/-1">Description
                    <textarea name="description" rows="3"></textarea>
                  </label>
                  <label style="grid-column:1/-1">Exigences
                    <textarea name="requirements" rows="2"></textarea>
                  </label>
                  <button class="btn btn-primary" type="submit">
                    <i class="ri-save-line"></i> Publier
                  </button>
                </form>
                <hr style="margin:18px 0" />
                <h3>Candidatures reçues</h3>
                <div id="applicationList" class="table-wrap"></div>
              </div>
            </div>
          </section>

          <!-- ══ PARAMÉTRAGE SYSTÈME ══ -->
          <section id="section-settings" class="section">
            <div class="split">
              <div class="panel">
                <div class="panel-header">
                  <h3>Paramètres système</h3>
                  <button id="btnSaveParams" class="btn btn-primary btn-sm" type="button">
                    <i class="ri-save-line"></i> Sauvegarder
                  </button>
                </div>
                <div id="settingsParamList" class="form-grid" style="margin-top:12px"></div>
              </div>
              <div class="panel">
                <div class="panel-header">
                  <h3>Jours fériés</h3>
                  <button id="btnRefreshHolidays" class="btn btn-secondary btn-sm" type="button">
                    <i class="ri-refresh-line"></i>
                  </button>
                </div>
                <form id="holidayForm" class="form-grid" style="grid-template-columns:1fr 1fr auto;margin-bottom:12px">
                  <label>Nom <input type="text" name="name" required /></label>
                  <label>Date <input type="date" name="date" required /></label>
                  <button class="btn btn-primary" type="submit" style="align-self:flex-end">
                    <i class="ri-add-line"></i>
                  </button>
                </form>
                <div id="holidayList" class="table-wrap"></div>
              </div>
            </div>
          </section>

        </div><!-- .sections-wrap -->
      </main>
    </div><!-- #appShell -->

    <datalist id="employeeSuggestionsList"></datalist>
    <datalist id="accountSuggestionsList"></datalist>

    <!-- MODALS -->
    <div id="passwordModal" class="password-modal hidden">
      <div class="password-card">
        <h3>Sécurité du compte</h3>
        <p>Tu dois changer le mot de passe par défaut pour continuer (minimum 6 caractères, différent de l'actuel).</p>
        <form id="passwordUpdateForm" class="form-grid">
          <label>Mot de passe actuel
            <input type="password" name="current_password" minlength="6" autocomplete="current-password" required />
          </label>
          <label>Nouveau mot de passe
            <input type="password" name="new_password" minlength="6" autocomplete="new-password" required />
          </label>
          <label>Confirmer le nouveau mot de passe
            <input type="password" name="confirm_new_password" minlength="6" autocomplete="new-password" required />
          </label>
          <button class="btn btn-primary" type="submit">
            <i class="ri-lock-password-line"></i> Mettre à jour
          </button>
        </form>
      </div>
    </div>

    <div id="editModal" class="password-modal hidden" role="dialog" aria-modal="true" aria-labelledby="editModalTitle">
      <div class="password-card edit-card">
        <h3 id="editModalTitle">Modifier</h3>
        <form id="editModalForm" class="form-grid"></form>
        <div class="edit-modal-actions">
          <button id="editModalCancel" class="btn btn-secondary" type="button">Annuler</button>
          <button id="editModalSubmit" class="btn btn-primary" type="button">
            <i class="ri-save-line"></i> Enregistrer
          </button>
        </div>
      </div>
    </div>

    <div id="confirmModal" class="password-modal hidden" role="dialog" aria-modal="true" aria-labelledby="confirmModalTitle">
      <div class="password-card confirm-card">
        <h3 id="confirmModalTitle">Confirmation</h3>
        <p id="confirmModalMessage">Es-tu sûr de vouloir continuer ?</p>
        <div class="edit-modal-actions">
          <button id="confirmModalCancel" class="btn btn-secondary" type="button">Annuler</button>
          <button id="confirmModalSubmit" class="btn btn-danger" type="button">Confirmer</button>
        </div>
      </div>
    </div>

    <div id="feedbackModal" class="password-modal hidden" role="dialog" aria-modal="true" aria-labelledby="feedbackModalTitle">
      <div class="password-card confirm-card feedback-card">
        <h3 id="feedbackModalTitle">Information</h3>
        <p id="feedbackModalMessage">Opération terminée.</p>
        <div class="edit-modal-actions">
          <button id="feedbackModalClose" class="btn btn-secondary" type="button">Fermer</button>
        </div>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════
         SLIDE-OVER DRAWERS — formulaires déportés
    ══════════════════════════════════════════════════════════ -->
    <div class="drawer-overlay" id="drawerOverlay" onclick="closeAllDrawers()"></div>

    <!-- ── Drawer Employé ── -->
    <div class="drawer" id="empDrawer">
      <div class="drawer-header">
        <div class="drawer-title">
          <i class="ri-user-add-line"></i>
          <div>Ajouter un employé<small>Créer un nouveau dossier agent</small></div>
        </div>
        <button class="drawer-close" onclick="closeAllDrawers()"><i class="ri-close-line"></i></button>
      </div>
      <div class="drawer-body">
        <form id="employeeForm" class="form-grid">
          <div class="drawer-section-title">Identité</div>
          <label>Prénom <input name="first_name" required /></label>
          <label>Nom <input name="last_name" required /></label>
          <label>Email professionnel <input name="email" type="email" required /></label>
          <label>Téléphone <input name="phone" required /></label>
          <label>Adresse <input name="address" required /></label>
          <div class="drawer-section-title">Informations RH</div>
          <label>Date d'embauche <input name="hire_date" type="date" required /></label>
          <label>Photo URL <input name="photo_url" placeholder="https://…" /></label>
          <label>Statut
            <select name="status">
              <option>Actif</option><option>Suspendu</option><option>Démissionné</option>
            </select>
          </label>
          <label>Département
            <select name="department_id" id="employeeDepartmentSelect">
              <option value="">Non assigné</option>
            </select>
          </label>
          <label>Rôle <span style="color:var(--danger)">*</span>
            <select name="role_id" id="employeeRoleSelect" required>
              <option value="">Sélectionner un rôle</option>
            </select>
          </label>
          <button class="btn btn-primary" style="margin-top:8px">
            <i class="ri-user-add-line"></i> Créer l'employé
          </button>
        </form>
      </div>
    </div>

    <!-- ── Drawer Département ── -->
    <div class="drawer" id="deptDrawer">
      <div class="drawer-header">
        <div class="drawer-title">
          <i class="ri-building-2-line"></i>
          <div>Nouveau département<small>Créer une unité organisationnelle</small></div>
        </div>
        <button class="drawer-close" onclick="closeAllDrawers()"><i class="ri-close-line"></i></button>
      </div>
      <div class="drawer-body">
        <form id="departmentForm" class="form-grid">
          <label>Nom du département <input name="name" required /></label>
          <label>Budget annuel (FCFA) <input name="budget" type="number" step="0.01" min="0" required /></label>
          <button class="btn btn-primary" style="margin-top:8px">
            <i class="ri-building-2-line"></i> Créer le département
          </button>
        </form>
      </div>
    </div>

    <!-- ── Drawer Bulletin de Paie ── -->
    <div class="drawer" id="payrollDrawer">
      <div class="drawer-header">
        <div class="drawer-title">
          <i class="ri-money-dollar-circle-line"></i>
          <div>Nouveau bulletin de paie<small>Créer et calculer le salaire</small></div>
        </div>
        <button class="drawer-close" onclick="closeAllDrawers()"><i class="ri-close-line"></i></button>
      </div>
      <div class="drawer-body">
        <form id="payrollForm" class="form-grid">
          <div class="drawer-section-title">Employé</div>
          <label>Rechercher un agent
            <input id="payrollEmployeeQuery" type="text" placeholder="Tapez le nom…" list="employeeSuggestionsList" autocomplete="off" />
          </label>
          <label>Agent sélectionné
            <select id="payrollEmployeeId" name="employee_id" required>
              <option value="">Sélectionner un agent</option>
            </select>
          </label>
          <div class="drawer-section-title">Période</div>
          <label>Mois de paie <input name="payroll_month" type="month" required /></label>
          <div class="drawer-section-title">Rémunération</div>
          <label>Salaire de base (FCFA) <input name="base_salary" type="number" step="0.01" min="0" required /></label>
          <label>Primes / Bonus <input name="bonus" type="number" step="0.01" value="0" min="0" /></label>
          <label>Heures supplémentaires <input name="overtime_hours" type="number" step="0.01" value="0" min="0" /></label>
          <label>Déductions <input name="deductions" type="number" step="0.01" value="0" min="0" /></label>
          <label>Impôts &amp; cotisations <input name="taxes" type="number" step="0.01" value="0" min="0" /></label>
          <button class="btn btn-primary" style="margin-top:8px">
            <i class="ri-calculator-line"></i> Calculer &amp; enregistrer
          </button>
        </form>
      </div>
    </div>

    <!-- ── Drawer Pointage ── -->
    <div class="drawer" id="attendanceDrawer">
      <div class="drawer-header">
        <div class="drawer-title">
          <i class="ri-login-circle-line"></i>
          <div>Enregistrer un pointage<small>Check-in ou check-out manuel</small></div>
        </div>
        <button class="drawer-close" onclick="closeAllDrawers()"><i class="ri-close-line"></i></button>
      </div>
      <div class="drawer-body">
        <form id="attendanceForm" class="form-grid">
          <div class="drawer-section-title">Employé</div>
          <label>Rechercher un agent
            <input id="attendanceEmployeeQuery" type="text" placeholder="Tapez le nom…" list="employeeSuggestionsList" autocomplete="off" />
          </label>
          <label>Agent sélectionné
            <select id="attendanceEmployeeId" name="employee_id" required>
              <option value="">Sélectionner un agent</option>
            </select>
          </label>
          <div class="drawer-section-title">Entrée</div>
          <label>Heure d'arrivée <input name="check_in" type="datetime-local" required /></label>
          <label>Absence non justifiée
            <select name="is_absent">
              <option value="false">Non</option>
              <option value="true">Oui (absent)</option>
            </select>
          </label>
          <label>Retard (minutes) <input name="late_minutes" type="number" value="0" min="0" /></label>
          <button class="btn btn-primary" style="margin-top:4px">
            <i class="ri-login-circle-line"></i> Enregistrer l'entrée
          </button>
        </form>
        <hr style="margin:20px 0;border-color:var(--border)" />
        <div class="drawer-section-title">Sortie</div>
        <div class="form-grid">
          <label>Heure de sortie <input id="attendanceCheckOutAt" type="datetime-local" /></label>
          <button id="btnAttendanceCheckout" class="btn btn-secondary" type="button">
            <i class="ri-logout-circle-r-line"></i> Enregistrer la sortie
          </button>
        </div>
      </div>
    </div>

    <!-- ── Drawer Synthèse Présences ── -->
    <div class="drawer" id="attendSummaryDrawer">
      <div class="drawer-header">
        <div class="drawer-title">
          <i class="ri-calendar-check-line"></i>
          <div>Synthèse mensuelle<small>Résumé présences par mois</small></div>
        </div>
        <button class="drawer-close" onclick="closeAllDrawers()"><i class="ri-close-line"></i></button>
      </div>
      <div class="drawer-body">
        <div class="form-grid">
          <label>Mois à analyser
            <input id="attendanceSummaryMonthDrawer" type="month" />
          </label>
          <button id="btnAttendanceSummaryDrawer" class="btn btn-primary" type="button">
            <i class="ri-calendar-check-line"></i> Charger la synthèse
          </button>
        </div>
        <div id="attendanceSummaryTableDrawer" class="table-wrap" style="margin-top:14px"></div>
      </div>
    </div>

    <!-- ── Drawer Congé ── -->
    <div class="drawer" id="leaveDrawer">
      <div class="drawer-header">
        <div class="drawer-title">
          <i class="ri-calendar-todo-line"></i>
          <div>Demande de congé<small>Soumettre une absence</small></div>
        </div>
        <button class="drawer-close" onclick="closeAllDrawers()"><i class="ri-close-line"></i></button>
      </div>
      <div class="drawer-body">
        <form id="leaveForm" class="form-grid">
          <div class="drawer-section-title">Employé concerné</div>
          <label>Rechercher un agent
            <input id="leaveEmployeeQuery" type="text" placeholder="Tapez le nom…" list="employeeSuggestionsList" autocomplete="off" />
          </label>
          <label>Agent sélectionné
            <select id="leaveEmployeeId" name="employee_id" required>
              <option value="">Sélectionner un agent</option>
            </select>
          </label>
          <div class="drawer-section-title">Période</div>
          <label>Date de début <input name="start_date" type="date" required /></label>
          <label>Date de fin <input name="end_date" type="date" required /></label>
          <label>Motif du congé <input name="reason" placeholder="Congé annuel, familial…" required /></label>
          <button class="btn btn-primary" style="margin-top:8px">
            <i class="ri-send-plane-line"></i> Soumettre la demande
          </button>
        </form>
      </div>
    </div>

    <!-- ── Drawer Contrat ── -->
    <div class="drawer" id="contractDrawer">
      <div class="drawer-header">
        <div class="drawer-title">
          <i class="ri-file-add-line"></i>
          <div>Nouveau contrat<small>Créer un contrat de travail</small></div>
        </div>
        <button class="drawer-close" onclick="closeAllDrawers()"><i class="ri-close-line"></i></button>
      </div>
      <div class="drawer-body">
        <form id="contractForm" class="form-grid">
          <div class="drawer-section-title">Employé</div>
          <label>Rechercher un agent
            <input id="contractEmployeeQuery" type="text" placeholder="Tapez le nom…" list="employeeSuggestionsList" autocomplete="off" />
          </label>
          <label>Agent sélectionné
            <select id="contractEmployeeId" name="employee_id" required>
              <option value="">Sélectionner un agent</option>
            </select>
          </label>
          <div class="drawer-section-title">Contrat</div>
          <label>Type de contrat
            <select name="contract_type">
              <option value="CDI">CDI — Durée indéterminée</option>
              <option value="CDD">CDD — Durée déterminée</option>
              <option value="Stage">Stage</option>
            </select>
          </label>
          <label>Date de début <input name="start_date" type="date" required /></label>
          <label>Date de fin (CDD) <input name="end_date" type="date" /></label>
          <label>Salaire contractuel (FCFA) <input name="contractual_salary" type="number" step="0.01" min="0" required /></label>
          <label>Chemin document PDF <input name="document_path" placeholder="uploads/contrats/…" /></label>
          <button class="btn btn-primary" style="margin-top:8px">
            <i class="ri-file-add-line"></i> Créer le contrat
          </button>
        </form>
      </div>
    </div>

    <!-- Scroll to top button -->
    <button id="scrollTopBtn" onclick="window.scrollTo({top:0,behavior:'smooth'})" title="Haut de page">
      <i class="ri-arrow-up-line"></i>
    </button>

    <script>
      // Scroll to top visibility
      const mainContent = document.querySelector('.sections-wrap');
      if (mainContent) {
        mainContent.addEventListener('scroll', () => {
          const btn = document.getElementById('scrollTopBtn');
          if (btn) btn.classList.toggle('visible', mainContent.scrollTop > 300);
        });
      }
    </script>
    <script src="{{ asset('js/biometric-bridge-client.js') }}?v=20260925a"></script>
    <script src="{{ asset('js/dashboard.js') }}?v=20260925a"></script>
    <script src="{{ asset('js/sgrh-vision.js') }}?v=20260925a"></script>
  
    <div class="rfid-modal-backdrop" id="rfidModal">
      <div class="rfid-modal">
        <h3>Pointage par carte RFID</h3>
        <p>Présentez la carte au lecteur ou saisissez l'identifiant.</p>
        <input id="rfidPunchInput" type="text" placeholder="ID carte RFID" autocomplete="off" />
        <div class="row">
          <button type="button" class="btn btn-secondary" id="rfidPunchCancel">Annuler</button>
          <button type="button" class="btn btn-primary" id="rfidPunchConfirm">Valider le pointage</button>
        </div>
      </div>
    </div>

  </body>
</html>


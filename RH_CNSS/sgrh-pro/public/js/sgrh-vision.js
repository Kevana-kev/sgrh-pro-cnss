/**
 * SGRH Pro Vision — Pointage biométrique + Espace agent + charts présence
 */
(function () {
  const state = {
    today: null,
    me: null,
    clockTimer: null,
    pollTimer: null,
    boardFilter: "all",
    charts: {},
  };

  function $(id) {
    return document.getElementById(id);
  }

  function fmtTime(iso) {
    if (!iso) return "—";
    try {
      return new Date(iso).toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" });
    } catch {
      return "—";
    }
  }

  function fmtHours(v) {
    if (v == null || v === "") return "—";
    return Number(v).toFixed(1) + " h";
  }

  function fmtMoney(v) {
    if (v == null || v === "") return "—";
    return Number(v).toLocaleString("fr-FR", { maximumFractionDigits: 0 }) + " FC";
  }

  function initials(first, last) {
    return `${(first || "?")[0] || ""}${(last || "")[0] || ""}`.toUpperCase();
  }

  function fmtDateShort(iso) {
    if (!iso) return "—";
    try {
      return new Date(iso).toLocaleDateString("fr-FR", { day: "2-digit", month: "short", year: "numeric" });
    } catch {
      return "—";
    }
  }

  function statusLabel(s) {
    return (
      {
        not_arrived: "Non arrivé",
        present: "Présent",
        completed: "Journée terminée",
        absent: "Absent",
      }[s] || s
    );
  }

  function startClock() {
    const clock = $("punchClock");
    const dateEl = $("punchDate");
    if (!clock) return;
    const tick = () => {
      const now = new Date();
      clock.textContent = now.toLocaleTimeString("fr-FR", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });
      if (dateEl) {
        dateEl.textContent = now.toLocaleDateString("fr-FR", {
          weekday: "long",
          day: "numeric",
          month: "long",
          year: "numeric",
        });
      }
    };
    tick();
    clearInterval(state.clockTimer);
    state.clockTimer = setInterval(tick, 1000);
  }

  function setPunchResult(ok, title, detail) {
    const box = $("punchResult");
    if (!box) return;
    box.className = "punch-result " + (ok === null ? "is-wait" : ok ? "is-ok" : "is-err");
    box.innerHTML = `<strong>${title}</strong><span>${detail || ""}</span>`;
  }

  function setScanning(active) {
    $("punchStage")?.classList.toggle("is-scanning", !!active);
    $("btnPunchFingerprint")?.classList.toggle("is-busy", !!active);
  }

  async function loadTodayBoard() {
    if (typeof api !== "function") return;
    try {
      const data = await api("/api/presence/today");
      state.today = data;
      renderPresenceStats(data.stats || {});
      renderLiveFeed(data.live_feed || []);
      renderBoard(data.board || []);
      renderOverviewPresenceStrip(data.stats || {});
      renderPresenceDayChart(data);
      renderArrivalTimeline(data.live_feed || []);
      updateNextActionHint(data);
    } catch (e) {
      console.warn("presence/today", e);
    }
  }

  function updateNextActionHint(data) {
    const hint = $("punchNextHint");
    if (!hint) return;
    const hour = new Date().getHours();
    const phase = hour < 14 ? "entrée" : "sortie";
    const stats = data.stats || {};
    const checkedIn = (stats.present || 0) + (stats.completed || 0);
    hint.textContent =
      phase === "entrée"
        ? `${checkedIn}/${stats.expected || 0} agents déjà pointés — phase d'arrivée`
        : `${stats.completed || 0} sorties enregistrées — phase de départ`;
  }

  function renderPresenceStats(stats) {
    const map = {
      punchStatExpected: stats.expected,
      punchStatPresent: stats.present,
      punchStatCompleted: stats.completed,
      punchStatLate: stats.late,
      punchStatAbsent: stats.absent,
      ovPresent: stats.present,
      ovCompleted: stats.completed,
      ovLate: stats.late,
      ovAbsent: stats.absent,
      ovExpected: stats.expected,
    };
    Object.entries(map).forEach(([id, val]) => {
      const el = $(id);
      if (el) el.textContent = val ?? "—";
    });
  }

  function renderOverviewPresenceStrip(stats) {
    const ring = $("ovPresenceRing");
    if (ring && stats.expected) {
      const rate = Math.round(
        (((stats.present || 0) + (stats.completed || 0)) / Math.max(stats.expected, 1)) * 100
      );
      ring.style.setProperty("--p", String(rate));
      const strong = ring.querySelector("strong");
      if (strong) strong.textContent = rate + "%";
    }
  }

  function renderLiveFeed(items) {
    const list = $("liveFeedList");
    if (!list) return;
    if (!items.length) {
      list.innerHTML = `<div class="empty-soft">Aucun pointage pour l'instant aujourd'hui.</div>`;
      return;
    }
    list.innerHTML = items
      .map((item) => {
        const initials = (item.employee_name || "?")
          .split(" ")
          .map((p) => p[0])
          .slice(0, 2)
          .join("")
          .toUpperCase();
        const pill =
          item.action === "checkout"
            ? `<span class="pill out">Sortie</span>`
            : `<span class="pill in">Entrée</span>`;
        const late = item.late_minutes > 0 ? ` · retard ${item.late_minutes} min` : "";
        return `<div class="live-feed-item">
          <div class="live-avatar">${initials}</div>
          <div>
            <div class="name">${item.employee_name || "—"}</div>
            <div class="meta">${fmtTime(item.at)} · ${(item.source || "—").toUpperCase()}${late}</div>
          </div>
          ${pill}
        </div>`;
      })
      .join("");
  }

  function renderBoard(board) {
    const body = $("presenceBoardBody");
    if (!body) return;
    let rows = board;
    if (state.boardFilter !== "all") {
      rows = board.filter((r) => r.status === state.boardFilter);
    }
    if (!rows.length) {
      body.innerHTML = `<tr><td colspan="8" class="empty-soft">Aucun agent dans ce filtre.</td></tr>`;
      return;
    }
    body.innerHTML = rows
      .map(
        (r) => `<tr>
        <td>
          <strong>${r.full_name}</strong>
          <div class="meta" style="color:var(--muted);font-size:.78rem">${r.matricule || ""}</div>
        </td>
        <td>${r.department || "—"}</td>
        <td><span class="status-chip ${r.status}">${statusLabel(r.status)}</span></td>
        <td>${fmtTime(r.check_in)}</td>
        <td>${fmtTime(r.check_out)}</td>
        <td>${fmtHours(r.worked_hours)}</td>
        <td>${r.late_minutes ? r.late_minutes + " min" : "—"}</td>
        <td>
          <span class="bio-flags">
            ${r.has_fingerprint ? '<i class="ri-fingerprint-line" title="Empreinte"></i>' : ""}
            ${r.has_rfid ? '<i class="ri-bank-card-line" title="RFID"></i>' : ""}
          </span>
        </td>
      </tr>`
      )
      .join("");
  }

  function chartFont() {
    return { family: "Outfit", size: 11 };
  }

  function renderPresenceDayChart(data) {
    const canvas = $("presenceStatusChart");
    if (!canvas || typeof Chart === "undefined") return;
    const stats = data.stats || {};
    const notArrived = Math.max(
      (stats.expected || 0) - ((stats.present || 0) + (stats.completed || 0) + (stats.absent || 0)),
      0
    );
    const cfg = {
      type: "doughnut",
      data: {
        labels: ["Présents", "Journée close", "Retards", "Absents", "Non arrivés"],
        datasets: [
          {
            data: [
              Math.max((stats.present || 0) - (stats.late || 0), 0),
              stats.completed || 0,
              stats.late || 0,
              stats.absent || 0,
              notArrived,
            ],
            backgroundColor: ["#067647", "#0d5c4d", "#c27803", "#b42318", "#8b96a8"],
            borderWidth: 0,
            hoverOffset: 6,
          },
        ],
      },
      options: {
        cutout: "70%",
        plugins: {
          legend: {
            position: "bottom",
            labels: { boxWidth: 10, font: chartFont(), color: "#5b6578" },
          },
        },
      },
    };
    if (state.charts.presenceStatus) state.charts.presenceStatus.destroy();
    state.charts.presenceStatus = new Chart(canvas, cfg);
  }

  function renderArrivalTimeline(feed) {
    const canvas = $("arrivalTimelineChart");
    if (!canvas || typeof Chart === "undefined") return;

    const buckets = {};
    for (let h = 6; h <= 19; h++) buckets[h] = { in: 0, out: 0 };
    (feed || []).forEach((item) => {
      if (!item.at) return;
      const h = new Date(item.at).getHours();
      if (buckets[h] == null) return;
      if (item.action === "checkout") buckets[h].out += 1;
      else buckets[h].in += 1;
    });

    const labels = Object.keys(buckets).map((h) => String(h).padStart(2, "0") + "h");
    const ins = Object.values(buckets).map((b) => b.in);
    const outs = Object.values(buckets).map((b) => b.out);

    if (state.charts.arrivalTimeline) state.charts.arrivalTimeline.destroy();
    state.charts.arrivalTimeline = new Chart(canvas, {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Entrées",
            data: ins,
            backgroundColor: "rgba(13,92,77,0.85)",
            borderRadius: 6,
            maxBarThickness: 14,
          },
          {
            label: "Sorties",
            data: outs,
            backgroundColor: "rgba(194,120,3,0.85)",
            borderRadius: 6,
            maxBarThickness: 14,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: "bottom", labels: { boxWidth: 10, font: chartFont() } },
        },
        scales: {
          x: { stacked: false, grid: { display: false }, ticks: { font: { family: "Outfit", size: 9 } } },
          y: {
            beginAtZero: true,
            ticks: { stepSize: 1, font: chartFont() },
            grid: { color: "rgba(11,18,32,0.06)" },
          },
        },
      },
    });
  }

  async function punchFingerprint() {
    setScanning(true);
    setPunchResult(null, "Scan en cours…", "Posez le doigt à plat sur le lecteur ZK-9500.");
    try {
      const scan = await api("/api/biometric/scan", {
        method: "POST",
        headers: { Accept: "application/json", "Content-Type": "application/json" },
        body: "{}",
      });
      if (!scan.template) throw new Error("Aucun template reçu du bridge.");
      setPunchResult(null, "Identification…", "Comparaison 1:N avec les empreintes enrôlées.");
      const result = await api("/api/presence/punch", {
        method: "POST",
        body: JSON.stringify({ method: "fingerprint", template: scan.template }),
      });
      announcePunch(result);
      await loadTodayBoard();
    } catch (e) {
      setPunchResult(false, "Échec du pointage", e.message || String(e));
    } finally {
      setScanning(false);
    }
  }

  function openRfidModal() {
    const m = $("rfidModal");
    if (!m) return;
    m.classList.add("open");
    const input = $("rfidPunchInput");
    if (input) {
      input.value = "";
      setTimeout(() => input.focus(), 50);
    }
  }

  function closeRfidModal() {
    $("rfidModal")?.classList.remove("open");
  }

  async function submitRfidPunch() {
    const card = ($("rfidPunchInput")?.value || "").trim();
    if (!card) {
      setPunchResult(false, "Carte requise", "Saisissez ou scannez l'identifiant RFID.");
      return;
    }
    closeRfidModal();
    setPunchResult(null, "Lecture RFID…", card);
    try {
      const result = await api("/api/presence/punch", {
        method: "POST",
        body: JSON.stringify({ method: "rfid", rfid_card_id: card }),
      });
      announcePunch(result);
      await loadTodayBoard();
    } catch (e) {
      setPunchResult(false, "Carte non reconnue", e.message || String(e));
    }
  }

  function announcePunch(result) {
    const name = result.employee?.full_name || "Agent";
    const action = result.action === "checkout" ? "Sortie enregistrée" : "Arrivée enregistrée";
    const extra =
      result.action === "checkout"
        ? `Temps travaillé : ${fmtHours(result.attendance?.worked_hours)}`
        : result.attendance?.late_minutes
          ? `Retard : ${result.attendance.late_minutes} min`
          : "À l'heure";
    setPunchResult(true, `${action} — ${name}`, `${result.message || ""} · ${extra}`);
    if (typeof notify === "function") {
      notify(`${action} — ${name}`);
    }
  }

  async function loadMySpace() {
    if (typeof api !== "function") return;
    const box = $("myspaceRoot");
    if (!box) return;
    try {
      const data = await api("/api/presence/me");
      state.me = data;
      renderMySpace(data);
    } catch (e) {
      box.innerHTML = `<div class="agent-card">
        <h2>Espace agent</h2>
        <p class="agent-meta">${e.message || "Aucun profil employé lié à ce compte. Demandez à la RH de rattacher votre fiche."}</p>
      </div>`;
    }
  }

  function renderMySpace(data) {
    const emp = data.employee || {};
    const today = data.today || {};
    const month = data.month || {};
    const balance = data.leave_balance || {};
    const payroll = data.last_payroll;
    const contract = data.contract;
    const root = $("myspaceRoot");
    if (!root) return;

    const present = month.present_days || 0;
    const absent = month.absence_days || 0;
    const rate = Math.min(100, Math.round((present / Math.max(present + absent, 1)) * 100));
    const score = (data.evaluations || [])[0]?.score;
    const av = initials(emp.first_name, emp.last_name);

    root.innerHTML = `
      <div class="ms-toolbar">
        <div>
          <div class="punch-kicker">Espace personnel</div>
          <h2 class="ms-title">Bonjour, ${emp.first_name || "Agent"} 👋</h2>
          <p class="agent-meta">${emp.matricule || "—"} · ${emp.department || "Département"} · ${emp.role || ""}</p>
        </div>
        <div class="ms-toolbar-actions">
          <button type="button" class="btn btn-primary" onclick="navigate('punch')"><i class="ri-fingerprint-line"></i> Pointage</button>
          <button type="button" class="btn btn-secondary" onclick="navigate('leaves')"><i class="ri-calendar-todo-line"></i> Congés</button>
          <button type="button" class="btn btn-secondary" onclick="navigate('messages')"><i class="ri-mail-line"></i> Messages${data.unread_messages ? ` <span class="ms-pill">${data.unread_messages}</span>` : ""}</button>
        </div>
      </div>

      <div class="ms-hero">
        <div class="agent-card agent-card--hero ms-profile-card">
          <div class="ms-profile-top">
            <div class="ms-avatar">${av}</div>
            <div class="ms-profile-meta">
              <h3>${emp.first_name || ""} ${emp.last_name || ""}</h3>
              <span class="status-chip ${today.status || "not_arrived"}">${statusLabel(today.status || "not_arrived")}</span>
            </div>
          </div>
          <div class="agent-today">
            <div class="agent-metric"><div class="lbl">Arrivée</div><div class="val">${fmtTime(today.check_in)}</div></div>
            <div class="agent-metric"><div class="lbl">Sortie</div><div class="val">${fmtTime(today.check_out)}</div></div>
            <div class="agent-metric"><div class="lbl">Heures</div><div class="val">${fmtHours(today.worked_hours)}</div></div>
            <div class="agent-metric"><div class="lbl">Retard</div><div class="val">${today.late_minutes ? today.late_minutes + " min" : "—"}</div></div>
          </div>
        </div>

        <div class="ms-quick-grid">
          <article class="ms-quick-card ms-quick-blue">
            <i class="ri-calendar-check-line"></i>
            <div><div class="lbl">Congés restants</div><div class="val">${balance.remaining_days ?? "—"} j</div></div>
          </article>
          <article class="ms-quick-card ms-quick-green">
            <i class="ri-money-dollar-circle-line"></i>
            <div><div class="lbl">Dernier net</div><div class="val">${payroll ? fmtMoney(payroll.net_salary) : "—"}</div></div>
          </article>
          <article class="ms-quick-card ms-quick-purple">
            <i class="ri-book-open-line"></i>
            <div><div class="lbl">Formations</div><div class="val">${(data.trainings || []).length}</div></div>
          </article>
          <article class="ms-quick-card ms-quick-orange">
            <i class="ri-notification-3-line"></i>
            <div><div class="lbl">Alertes</div><div class="val">${data.unread_notifications ?? 0}</div></div>
          </article>
        </div>
      </div>

      <div class="ms-widgets">
        <div class="agent-card ms-widget">
          <div class="ms-widget-head"><h3><i class="ri-file-list-3-line"></i> Bulletin récent</h3></div>
          ${payroll ? `
            <div class="ms-payroll">
              <div class="ms-payroll-row"><span>Période</span><strong>${payroll.payroll_month || "—"}</strong></div>
              <div class="ms-payroll-row"><span>Base</span><strong>${fmtMoney(payroll.base_salary)}</strong></div>
              <div class="ms-payroll-row"><span>Primes</span><strong>${fmtMoney(payroll.bonus)}</strong></div>
              <div class="ms-payroll-row"><span>Retenues</span><strong>${fmtMoney(payroll.deductions)}</strong></div>
              <div class="ms-payroll-total"><span>Net à payer</span><strong>${fmtMoney(payroll.net_salary)}</strong></div>
            </div>` : `<div class="empty-soft">Aucun bulletin disponible</div>`}
        </div>

        <div class="agent-card ms-widget">
          <div class="ms-widget-head"><h3><i class="ri-article-line"></i> Contrat</h3></div>
          ${contract ? `
            <div class="ms-contract">
              <div class="ms-payroll-row"><span>Type</span><strong>${contract.contract_type || "—"}</strong></div>
              <div class="ms-payroll-row"><span>Début</span><strong>${contract.start_date || "—"}</strong></div>
              <div class="ms-payroll-row"><span>Fin</span><strong>${contract.end_date || "Indéterminée"}</strong></div>
              <div class="ms-payroll-row"><span>Salaire contractuel</span><strong>${fmtMoney(contract.contractual_salary)}</strong></div>
            </div>` : `<div class="empty-soft">Aucun contrat enregistré</div>`}
        </div>

        <div class="agent-card ms-widget">
          <div class="ms-widget-head"><h3><i class="ri-graduation-cap-line"></i> Formations</h3><button class="btn btn-secondary btn-sm" type="button" onclick="navigate('training')">Voir tout</button></div>
          <div class="ms-list">
            ${(data.trainings || []).slice(0, 4).map((t) =>
              `<div class="ms-list-item"><div><strong>${t.training_title || t.title || "Formation"}</strong><span>${t.status || ""}</span></div><i class="ri-arrow-right-s-line"></i></div>`
            ).join("") || `<div class="empty-soft">Aucune formation</div>`}
          </div>
        </div>

        <div class="agent-card ms-widget">
          <div class="ms-widget-head"><h3><i class="ri-notification-badge-line"></i> Notifications</h3><button class="btn btn-secondary btn-sm" type="button" onclick="navigate('notifications')">Centre</button></div>
          <div class="ms-list">
            ${(data.notifications || []).slice(0, 4).map((n) =>
              `<div class="ms-list-item ${n.is_read ? "" : "is-unread"}"><div><strong>${n.title || "—"}</strong><span>${n.message || ""}</span></div></div>`
            ).join("") || `<div class="empty-soft">Aucune notification</div>`}
          </div>
        </div>
      </div>

      <div class="agent-card" style="margin-bottom:14px">
        <h3 style="margin:0 0 12px;font-size:1rem">Performance & assiduité</h3>
        <div class="presence-stat-grid">
          <div class="presence-stat"><div class="lbl">Jours présents</div><div class="val ok">${present}</div></div>
          <div class="presence-stat"><div class="lbl">Retards</div><div class="val warn">${month.late_days ?? 0}</div></div>
          <div class="presence-stat"><div class="lbl">Heures</div><div class="val">${Number(month.total_hours || 0).toFixed(1)}</div></div>
          <div class="presence-stat"><div class="lbl">Score RH</div><div class="val">${score ?? "—"}</div></div>
        </div>
        <div class="presence-ring-wrap" style="margin-top:16px">
          <div class="presence-ring" style="--p:${rate}">
            <div><strong>${rate}%</strong><span>assiduité</span></div>
          </div>
        </div>
      </div>

      ${(data.skills || []).length ? `
      <div class="agent-card" style="margin-bottom:14px">
        <h3 style="margin:0 0 12px;font-size:1rem"><i class="ri-medal-line"></i> Mes compétences</h3>
        <div class="ms-skills">
          ${(data.skills || []).map((s) =>
            `<span class="ms-skill-chip">${s.skill_name || s.name || "—"} · ${s.level || ""}</span>`
          ).join("")}
        </div>
      </div>` : ""}

      <div class="chart-grid-2">
        <div class="chart-card-v2">
          <div class="chart-header"><div class="chart-header-left"><h3 class="chart-title">Mes heures (14 jours)</h3><span class="chart-subtitle">Suivi individuel</span></div></div>
          <canvas id="myHoursChart" height="140"></canvas>
        </div>
        <div class="chart-card-v2">
          <div class="chart-header"><div class="chart-header-left"><h3 class="chart-title">Mes retards</h3><span class="chart-subtitle">Minutes / jour</span></div></div>
          <canvas id="myLateChart" height="140"></canvas>
        </div>
      </div>
      <div class="chart-grid-2">
        <div class="board-wrap">
          <div class="board-toolbar"><h3 style="margin:0;font-size:1rem">Dernières présences</h3></div>
          <div class="table-wrap"><table class="board-table"><thead><tr><th>Date</th><th>Entrée</th><th>Sortie</th><th>Heures</th><th>Source</th></tr></thead>
          <tbody>
            ${(data.recent_attendances || []).slice(0, 12).map((a) => `<tr>
              <td>${a.check_in ? new Date(a.check_in).toLocaleDateString("fr-FR") : "—"}</td>
              <td>${fmtTime(a.check_in)}</td>
              <td>${fmtTime(a.check_out)}</td>
              <td>${fmtHours(a.worked_hours)}</td>
              <td>${(a.source || "—").toUpperCase()}</td>
            </tr>`).join("") || `<tr><td colspan="5" class="empty-soft">Aucune donnée</td></tr>`}
          </tbody></table></div>
        </div>
        <div class="board-wrap">
          <div class="board-toolbar"><h3 style="margin:0;font-size:1rem">Évaluations & congés</h3></div>
          <div style="padding:14px 16px">
            <h4 style="margin:0 0 8px;font-size:.85rem;color:var(--muted)">Évaluations</h4>
            ${(data.evaluations || []).slice(0, 4).map((e) =>
              `<div class="soft-row"><strong>${e.period || "—"}</strong> · score ${e.score ?? "—"} <span style="color:var(--muted)">· ${e.status || ""}</span></div>`
            ).join("") || `<div class="empty-soft">Aucune évaluation</div>`}
            <h4 style="margin:16px 0 8px;font-size:.85rem;color:var(--muted)">Congés</h4>
            ${(data.leaves || []).slice(0, 4).map((l) =>
              `<div class="soft-row">${l.start_date || ""} → ${l.end_date || ""} · <strong>${l.status || ""}</strong></div>`
            ).join("") || `<div class="empty-soft">Aucun congé</div>`}
          </div>
        </div>
      </div>
    `;

    renderMyCharts(data.series || {});
  }

  function renderMyCharts(series) {
    if (typeof Chart === "undefined") return;
    const labels = series.labels || [];
    const hours = series.hours || [];
    const late = series.late || [];

    const hoursCanvas = $("myHoursChart");
    const lateCanvas = $("myLateChart");
    if (hoursCanvas) {
      if (state.charts.myHours) state.charts.myHours.destroy();
      state.charts.myHours = new Chart(hoursCanvas, {
        type: "bar",
        data: {
          labels,
          datasets: [
            {
              label: "Heures",
              data: hours,
              backgroundColor: "rgba(13,92,77,0.85)",
              borderRadius: 8,
              maxBarThickness: 22,
            },
          ],
        },
        options: {
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { display: false }, ticks: { font: { family: "Outfit", size: 10 } } },
            y: { beginAtZero: true, grid: { color: "rgba(11,18,32,0.06)" } },
          },
        },
      });
    }
    if (lateCanvas) {
      if (state.charts.myLate) state.charts.myLate.destroy();
      state.charts.myLate = new Chart(lateCanvas, {
        type: "line",
        data: {
          labels,
          datasets: [
            {
              label: "Retard (min)",
              data: late,
              borderColor: "#c27803",
              backgroundColor: "rgba(194,120,3,0.15)",
              fill: true,
              tension: 0.35,
              pointRadius: 3,
              pointBackgroundColor: "#c27803",
            },
          ],
        },
        options: {
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { display: false }, ticks: { font: { family: "Outfit", size: 10 } } },
            y: { beginAtZero: true, grid: { color: "rgba(11,18,32,0.06)" } },
          },
        },
      });
    }
  }

  function bindUi() {
    $("btnPunchFingerprint")?.addEventListener("click", punchFingerprint);
    $("btnPunchRfid")?.addEventListener("click", openRfidModal);
    $("btnRefreshPresence")?.addEventListener("click", loadTodayBoard);
    $("rfidPunchConfirm")?.addEventListener("click", submitRfidPunch);
    $("rfidPunchCancel")?.addEventListener("click", closeRfidModal);
    $("rfidPunchInput")?.addEventListener("keydown", (e) => {
      if (e.key === "Enter") submitRfidPunch();
    });
    document.querySelectorAll("[data-board-filter]").forEach((btn) => {
      btn.addEventListener("click", () => {
        state.boardFilter = btn.getAttribute("data-board-filter") || "all";
        document.querySelectorAll("[data-board-filter]").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        renderBoard(state.today?.board || []);
      });
    });
  }

  function startPresencePolling() {
    clearInterval(state.pollTimer);
    state.pollTimer = setInterval(() => {
      const punchActive = $("section-punch")?.classList.contains("active");
      const overviewActive = $("section-overview")?.classList.contains("active");
      if (punchActive || overviewActive) loadTodayBoard();
    }, 20000);
  }

  async function onNavigate(section) {
    if (section === "punch" || section === "overview") {
      startClock();
      await loadTodayBoard();
    }
    if (section === "myspace") {
      await loadMySpace();
    }
  }

  function closeSidebar() {
    document.querySelector(".sidebar")?.classList.remove("is-open");
    $("sidebarBackdrop")?.classList.remove("is-open");
    document.body.classList.remove("sidebar-open");
  }

  function openSidebar() {
    document.querySelector(".sidebar")?.classList.add("is-open");
    $("sidebarBackdrop")?.classList.add("is-open");
    document.body.classList.add("sidebar-open");
  }

  function toggleSidebar() {
    const side = document.querySelector(".sidebar");
    if (!side) return;
    if (side.classList.contains("is-open")) closeSidebar();
    else openSidebar();
  }

  function bindResponsiveShell() {
    $("btnSidebarToggle")?.addEventListener("click", toggleSidebar);
    $("sidebarBackdrop")?.addEventListener("click", closeSidebar);
    document.querySelectorAll(".menu-item").forEach((btn) => {
      btn.addEventListener("click", () => {
        if (window.matchMedia("(max-width: 980px)").matches) closeSidebar();
      });
    });
    window.addEventListener("resize", () => {
      if (!window.matchMedia("(max-width: 980px)").matches) closeSidebar();
    });
  }

  /* ── Dashboard widget picker ─────────────────────────── */
  const DASH_STORAGE_KEY = "sgrh_dash_widgets_v1";
  const DASH_WIDGETS = [
    { id: "kpis", label: "Indicateurs KPI", desc: "Effectif, salaires, absences…", defaultOn: true },
    { id: "presence", label: "Présence du jour", desc: "Bandeau live + taux", defaultOn: true },
    { id: "actions", label: "Actions rapides", desc: "Raccourcis navigation", defaultOn: true },
    { id: "payroll", label: "Masse salariale", desc: "Évolution 12 mois", defaultOn: true },
    { id: "dept", label: "Départements", desc: "Répartition des effectifs", defaultOn: true },
    { id: "attend", label: "Présences / Absences", desc: "Tendance mensuelle", defaultOn: true },
    { id: "leaves", label: "Congés", desc: "Répartition des statuts", defaultOn: false },
    { id: "perf", label: "Performances", desc: "Distribution des scores", defaultOn: false },
    { id: "deptPayroll", label: "Paie par département", desc: "Masse salariale détaillée", defaultOn: false },
    { id: "recruit", label: "Recrutement", desc: "Entonnoir candidatures", defaultOn: false },
    { id: "stats", label: "Indicateurs clés", desc: "Tableau récapitulatif", defaultOn: true },
    { id: "activity", label: "Activité récente", desc: "Fil d'événements RH", defaultOn: true },
  ];

  function defaultDashPrefs() {
    const prefs = {};
    DASH_WIDGETS.forEach((w) => {
      prefs[w.id] = !!w.defaultOn;
    });
    return prefs;
  }

  function loadDashPrefs() {
    try {
      const raw = localStorage.getItem(DASH_STORAGE_KEY);
      if (!raw) return defaultDashPrefs();
      return { ...defaultDashPrefs(), ...JSON.parse(raw) };
    } catch {
      return defaultDashPrefs();
    }
  }

  function saveDashPrefs(prefs) {
    localStorage.setItem(DASH_STORAGE_KEY, JSON.stringify(prefs));
  }

  function applyDashPrefs(prefs) {
    document.querySelectorAll("[data-dash-widget]").forEach((el) => {
      const id = el.getAttribute("data-dash-widget");
      const on = prefs[id] !== false;
      el.classList.toggle("is-hidden", !on);
    });
    // Resize visible Chart.js instances
    requestAnimationFrame(() => {
      try {
        if (typeof Chart !== "undefined" && Chart.getChart) {
          document.querySelectorAll("canvas").forEach((c) => {
            const chart = Chart.getChart(c);
            if (chart && c.offsetParent !== null) chart.resize();
          });
        }
        if (appState?.charts) {
          Object.values(appState.charts).forEach((ch) => {
            try { ch?.resize?.(); } catch (_) {}
          });
        }
      } catch (_) {}
    });
  }

  function renderDashCustomizeGrid(prefs) {
    const grid = $("dashCustomizeGrid");
    if (!grid) return;
    grid.innerHTML = DASH_WIDGETS.map((w) => {
      const on = prefs[w.id] !== false;
      return `<label class="dash-opt ${on ? "is-on" : ""}" data-opt="${w.id}">
        <input type="checkbox" ${on ? "checked" : ""} data-dash-opt="${w.id}" />
        <span>
          <span class="opt-title">${w.label}</span>
          <span class="opt-desc">${w.desc}</span>
        </span>
      </label>`;
    }).join("");

    grid.querySelectorAll("input[data-dash-opt]").forEach((input) => {
      input.addEventListener("change", () => {
        const label = input.closest(".dash-opt");
        label?.classList.toggle("is-on", input.checked);
      });
    });
  }

  function readCustomizeForm() {
    const prefs = defaultDashPrefs();
    document.querySelectorAll("input[data-dash-opt]").forEach((input) => {
      prefs[input.getAttribute("data-dash-opt")] = input.checked;
    });
    return prefs;
  }

  function bindDashCustomize() {
    const panel = $("dashCustomizePanel");
    if (!panel) return;

    const prefs = loadDashPrefs();
    applyDashPrefs(prefs);
    renderDashCustomizeGrid(prefs);

    $("btnDashCustomize")?.addEventListener("click", () => {
      const open = panel.hasAttribute("hidden");
      if (open) {
        panel.removeAttribute("hidden");
        renderDashCustomizeGrid(loadDashPrefs());
      } else {
        panel.setAttribute("hidden", "");
      }
    });

    $("btnDashApply")?.addEventListener("click", () => {
      const next = readCustomizeForm();
      saveDashPrefs(next);
      applyDashPrefs(next);
      panel.setAttribute("hidden", "");
      if (typeof notify === "function") notify("Affichage du tableau de bord mis à jour");
      if (typeof loadOverview === "function") loadOverview().catch(() => {});
      if (window.SgrhVision?.loadTodayBoard) window.SgrhVision.loadTodayBoard();
    });

    $("btnDashSelectAll")?.addEventListener("click", () => {
      const all = {};
      DASH_WIDGETS.forEach((w) => { all[w.id] = true; });
      renderDashCustomizeGrid(all);
    });

    $("btnDashSelectDefaults")?.addEventListener("click", () => {
      renderDashCustomizeGrid(defaultDashPrefs());
    });

    $("btnDashReset")?.addEventListener("click", () => {
      const defaults = defaultDashPrefs();
      saveDashPrefs(defaults);
      applyDashPrefs(defaults);
      renderDashCustomizeGrid(defaults);
      if (typeof notify === "function") notify("Affichage réinitialisé (essentiels)");
    });
  }

  document.addEventListener("sgrh:navigate", (e) => {
    onNavigate(e.detail?.section);
    if (window.matchMedia("(max-width: 980px)").matches) closeSidebar();
  });

  document.addEventListener("DOMContentLoaded", () => {
    // Ensure punch stage id for scan animation
    const stage = document.querySelector(".punch-stage");
    if (stage && !stage.id) stage.id = "punchStage";

    bindUi();
    bindResponsiveShell();
    bindDashCustomize();
    startClock();
    startPresencePolling();

    if ($("appShell") && !$("appShell").classList.contains("hidden")) {
      loadTodayBoard();
    }
  });

  window.SgrhVision = {
    loadTodayBoard,
    loadMySpace,
    punchFingerprint,
    toggleSidebar,
    closeSidebar,
    applyDashPrefs,
    loadDashPrefs,
  };
})();

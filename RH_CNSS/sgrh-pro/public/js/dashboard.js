/*
 * Rôle du fichier:
 * Pilote l'interface du dashboard côté client (état global, appels API, rendu des tables/charts, interactions UI).
 */

const appState = {
  token: localStorage.getItem("ems_token") || "",
  username: localStorage.getItem("ems_username") || "",
  role: localStorage.getItem("ems_role") || "",
  accountHolderName: localStorage.getItem("ems_account_holder_name") || "",
  accountHolderFunction: localStorage.getItem("ems_account_holder_function") || "",
  permissions: JSON.parse(localStorage.getItem("ems_permissions") || "[]"),
  mustChangePassword: localStorage.getItem("ems_must_change_password") === "1",
  roles: [],
  employees: [],
  employeeById: {},
  accounts: [],
  conversations: [],
  messageRecipients: [],
  activeChatUserId: null,
  activeChatRecipientEmployeeId: null,
  activeThreadMessages: [],
  oldestThreadMessageId: null,
  hasMoreThreadMessages: false,
  isLoadingOlderMessages: false,
  charts: {
    dept: null,
    leave: null,
    accountingMonthly: null,
    accountingCost: null,
    accountingDepartments: null,
  },
  feedbackModalHandlers: null,
  messagesAutoRefreshTimer: null,
};

const $ = (id) => document.getElementById(id);
const sectionTitleMap = {
  overview: "Pilot de bord RH",
  punch: "Pointage du jour",
  myspace: "Mon espace",
  employees: "Employés",
  departments: "Départements",
  roles: "Rôles & Permissions",
  payrolls: "Éléments de rémunération",
  attendances: "Registre des présences",
  team: "Équipe",
  leaves: "Congés",
  biometric: "Enrôlement biométrique",
  contracts: "Contrats",
  messages: "Messagerie",
  accounts: "Comptes Agents",
  accounting: "Comptabilité",
  reports: "Reporting",
  training: "Formations & Compétences",
  performance: "Évaluation des performances",
  "medical-leaves": "Congés médicaux",
  notifications: "Notifications & Alertes",
  recruitment: "Recrutement",
  settings: "Paramétrage système",
};

const sectionAccessRules = {
  overview: () => true,
  punch: () => true,
  myspace: () => true,
  employees: () => can("Voir employés"),
  departments: () => can("Voir employés"),
  roles: () => can("Voir employés") && ["SuperAdmin", "Admin RH"].includes(appState.role),
  team: () => can("Voir équipe") || appState.role === "Manager",
  payrolls: () => can("Voir salaires"),
  attendances: () => can("Voir employés") || can("Voir équipe") || true,
  leaves: () => true,
  contracts: () => can("Voir employés"),
  messages: () => true,
  accounts: () => can("Modifier employés") && ["SuperAdmin", "Admin RH", "RH"].includes(appState.role),
  accounting: () => can("Voir comptabilité"),
  reports: () => can("Exporter rapports"),
  biometric: () => can("Modifier employés") || ["SuperAdmin", "Admin RH", "RH"].includes(appState.role),
  training: () => true,
  performance: () => true,
  "medical-leaves": () => true,
  notifications: () => true,
  recruitment: () => can("Modifier employés") || ["SuperAdmin", "Admin RH", "RH"].includes(appState.role),
  settings: () => ["SuperAdmin", "Admin RH"].includes(appState.role) || can("Modifier employés"),
};

const DEFAULT_PERMISSION_NAMES = [
  "Voir employés",
  "Modifier employés",
  "Voir salaires",
  "Voir comptabilité",
  "Exporter rapports",
  "Valider congés",
  // Manager / team-level
  "Voir équipe",
  "Valider congés équipe",
  "Attribuer tâches",
  "Gérer objectifs",
  "Gérer évaluations",
  "Voir performances",
  "Exporter rapports équipe",
];

function notify(message, isError = false) {
  const feedbackModal = $("feedbackModal");
  const feedbackCard = feedbackModal ? feedbackModal.querySelector(".feedback-card") : null;
  const titleElement = $("feedbackModalTitle");
  const messageElement = $("feedbackModalMessage");
  const closeButton = $("feedbackModalClose");

  if (feedbackModal && feedbackCard && titleElement && messageElement && closeButton) {
    titleElement.textContent = isError ? "Erreur" : "Succès";
    messageElement.textContent = message;
    feedbackCard.classList.remove("feedback-success", "feedback-error");
    feedbackCard.classList.add(isError ? "feedback-error" : "feedback-success");
    feedbackModal.classList.remove("hidden");

    const previousHandlers = appState.feedbackModalHandlers;
    if (previousHandlers) {
      closeButton.removeEventListener("click", previousHandlers.onCloseClick);
      feedbackModal.removeEventListener("click", previousHandlers.onBackdropClick);
      document.removeEventListener("keydown", previousHandlers.onEscape);
    }

    const close = () => {
      feedbackModal.classList.add("hidden");
      closeButton.removeEventListener("click", onCloseClick);
      feedbackModal.removeEventListener("click", onBackdropClick);
      document.removeEventListener("keydown", onEscape);
      appState.feedbackModalHandlers = null;
    };

    const onCloseClick = () => close();
    const onBackdropClick = (event) => {
      if (event.target === feedbackModal) {
        close();
      }
    };
    const onEscape = (event) => {
      if (event.key === "Escape") {
        close();
      }
    };

    closeButton.addEventListener("click", onCloseClick);
    feedbackModal.addEventListener("click", onBackdropClick);
    document.addEventListener("keydown", onEscape);
    appState.feedbackModalHandlers = { onCloseClick, onBackdropClick, onEscape };
    return;
  }

  const toast = $("toast");
  toast.textContent = message;
  toast.style.borderColor = isError ? "rgba(255,93,122,.85)" : "rgba(31,222,154,.85)";
  toast.classList.remove("hidden");
  toast.classList.add("show");
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.classList.add("hidden"), 250);
  }, 2200);
}

function can(permissionName) {
  return appState.permissions.includes(permissionName);
}

function renderOwnerAccountInfo() {
  const accountName = appState.accountHolderName || appState.username || "Utilisateur";
  const accountRole = appState.accountHolderFunction || appState.role || "Rôle non défini";

  const ownerName = $("ownerName");
  const ownerRole = $("ownerRole");
  if (ownerName) ownerName.textContent = accountName;
  if (ownerRole) ownerRole.textContent = accountRole;

  // Update topbar user info
  const topbarUserName = $("topbarUserName");
  if (topbarUserName) topbarUserName.textContent = accountName;
  const topbarAvatar = $("topbarAvatar");
  if (topbarAvatar) topbarAvatar.textContent = accountName.charAt(0).toUpperCase();
}

function updateAccountHolderInfo(name, functionName) {
  appState.accountHolderName = String(name || "").trim();
  appState.accountHolderFunction = String(functionName || "").trim();
  localStorage.setItem("ems_account_holder_name", appState.accountHolderName);
  localStorage.setItem("ems_account_holder_function", appState.accountHolderFunction);
}

function clearAccountHolderInfo() {
  appState.accountHolderName = "";
  appState.accountHolderFunction = "";
  localStorage.removeItem("ems_account_holder_name");
  localStorage.removeItem("ems_account_holder_function");
}

function setMustChangePassword(value) {
  appState.mustChangePassword = !!value;
  localStorage.setItem("ems_must_change_password", value ? "1" : "0");
  const shouldShow = !!value && !$("appShell").classList.contains("hidden");
  $("passwordModal").classList.toggle("hidden", !shouldShow);
}

function ensureSectionAccess() {
  document.querySelectorAll(".menu-item").forEach((button) => {
    const section = button.dataset.section;
    const allowed = sectionAccessRules[section] ? sectionAccessRules[section]() : true;
    button.classList.toggle("hidden", !allowed);
    const sectionElement = $(`section-${section}`);
    if (sectionElement) {
      sectionElement.classList.toggle("hidden", !allowed);
    }
  });

  const activeButton = document.querySelector(".menu-item.active:not(.hidden)");
  if (!activeButton) {
    const firstVisible = document.querySelector(".menu-item:not(.hidden)");
    if (firstVisible) {
      firstVisible.click();
    }
  }
}

function applyFormPermissions() {
  const formPermissions = [
    { id: "employeeForm", btnId: "btnNewEmployee", allowed: can("Modifier employés") },
    { id: "departmentForm", btnId: "btnNewDept",  allowed: can("Modifier employés") },
    { id: "roleForm",       btnId: null,           allowed: can("Modifier employés") && ["SuperAdmin", "Admin RH"].includes(appState.role) },
    { id: "payrollForm",    btnId: "btnNewPayroll", allowed: can("Voir salaires") },
    { id: "attendanceForm", btnId: null,           allowed: can("Voir employés") },
    { id: "leaveForm",      btnId: null,           allowed: true },
    { id: "contractForm",   btnId: "btnNewContract", allowed: can("Modifier employés") },
  ];

  formPermissions.forEach(({ id, btnId, allowed }) => {
    const form = $(id);
    if (form) form.classList.toggle("hidden", !allowed);
    if (btnId) {
      const btn = $(btnId);
      if (btn) btn.classList.toggle("hidden", !allowed);
    }
  });
}

function formatMoney(value) {
  return Number(value || 0).toLocaleString("fr-FR", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 2,
  });
}

function getFormJSON(form) {
  const formData = new FormData(form);
  const payload = {};
  for (const [key, value] of formData.entries()) {
    if (value === "") continue;
    payload[key] = value;
  }
  return payload;
}

function normalizePayload(payload, fieldsAsNumber = []) {
  const normalized = { ...payload };
  fieldsAsNumber.forEach((field) => {
    if (normalized[field] !== undefined) {
      normalized[field] = Number(normalized[field]);
    }
  });
  return normalized;
}

function openEditModal({ title, fields, submitLabel = "Enregistrer" }) {
  const modal = $("editModal");
  const titleElement = $("editModalTitle");
  const formElement = $("editModalForm");
  const cancelButton = $("editModalCancel");
  const submitButton = $("editModalSubmit");

  if (!modal || !titleElement || !formElement || !cancelButton || !submitButton) {
    return Promise.resolve(null);
  }

  titleElement.textContent = title || "Modifier";
  submitButton.textContent = submitLabel;
  formElement.innerHTML = "";

  const controls = {};
  fields.forEach((field) => {
    const label = document.createElement("label");
    label.textContent = field.label;

    let control;
    if (field.type === "select") {
      control = document.createElement("select");
      (field.options || []).forEach((option) => {
        const optionElement = document.createElement("option");
        optionElement.value = String(option.value);
        optionElement.textContent = option.label;
        control.appendChild(optionElement);
      });
      control.value = String(field.value ?? "");
    } else if (field.type === "textarea") {
      control = document.createElement("textarea");
      control.value = String(field.value ?? "");
      if (field.placeholder) {
        control.placeholder = field.placeholder;
      }
    } else {
      control = document.createElement("input");
      control.type = field.type || "text";
      control.value = String(field.value ?? "");
      if (field.placeholder) {
        control.placeholder = field.placeholder;
      }
      if (field.step) {
        control.step = String(field.step);
      }
      if (field.min !== undefined) {
        control.min = String(field.min);
      }
    }

    control.name = field.name;
    label.appendChild(control);
    formElement.appendChild(label);
    controls[field.name] = control;
  });

  modal.classList.remove("hidden");
  const firstControl = formElement.querySelector("input, select, textarea");
  if (firstControl) {
    firstControl.focus();
  }

  return new Promise((resolve) => {
    const close = (payload) => {
      modal.classList.add("hidden");
      cancelButton.removeEventListener("click", onCancel);
      submitButton.removeEventListener("click", onSubmit);
      modal.removeEventListener("click", onBackdropClick);
      document.removeEventListener("keydown", onEscape);
      resolve(payload);
    };

    const onCancel = () => close(null);

    const onSubmit = () => {
      try {
        const values = {};
        fields.forEach((field) => {
          const control = controls[field.name];
          const rawValue = control ? control.value : "";
          const trimmed = typeof rawValue === "string" ? rawValue.trim() : rawValue;

          if (field.required && !trimmed) {
            throw new Error(`Le champ ${field.label} est requis`);
          }

          if ((field.type === "number") && trimmed !== "") {
            const numberValue = Number(trimmed);
            if (Number.isNaN(numberValue)) {
              throw new Error(`${field.label} invalide`);
            }
            values[field.name] = numberValue;
          } else {
            values[field.name] = trimmed;
          }

          if (typeof field.parse === "function") {
            values[field.name] = field.parse(values[field.name]);
          }
        });
        close(values);
      } catch (error) {
        notify(error.message, true);
      }
    };

    const onBackdropClick = (event) => {
      if (event.target === modal) {
        close(null);
      }
    };

    const onEscape = (event) => {
      if (event.key === "Escape") {
        close(null);
      }
    };

    cancelButton.addEventListener("click", onCancel);
    submitButton.addEventListener("click", onSubmit);
    modal.addEventListener("click", onBackdropClick);
    document.addEventListener("keydown", onEscape);
  });
}

function confirmAction({ title, message, confirmLabel = "Confirmer" }) {
  const modal = $("confirmModal");
  const titleElement = $("confirmModalTitle");
  const messageElement = $("confirmModalMessage");
  const cancelButton = $("confirmModalCancel");
  const submitButton = $("confirmModalSubmit");

  if (!modal || !titleElement || !messageElement || !cancelButton || !submitButton) {
    return Promise.resolve(false);
  }

  titleElement.textContent = title || "Confirmation";
  messageElement.textContent = message || "Es-tu sûr de vouloir continuer ?";
  submitButton.textContent = confirmLabel;

  modal.classList.remove("hidden");

  return new Promise((resolve) => {
    const close = (accepted) => {
      modal.classList.add("hidden");
      cancelButton.removeEventListener("click", onCancel);
      submitButton.removeEventListener("click", onSubmit);
      modal.removeEventListener("click", onBackdropClick);
      document.removeEventListener("keydown", onEscape);
      resolve(accepted);
    };

    const onCancel = () => close(false);
    const onSubmit = () => close(true);

    const onBackdropClick = (event) => {
      if (event.target === modal) {
        close(false);
      }
    };

    const onEscape = (event) => {
      if (event.key === "Escape") {
        close(false);
      }
    };

    cancelButton.addEventListener("click", onCancel);
    submitButton.addEventListener("click", onSubmit);
    modal.addEventListener("click", onBackdropClick);
    document.addEventListener("keydown", onEscape);
  });
}

async function api(path, options = {}) {
  const headers = {
    ...(options.body ? { "Content-Type": "application/json" } : {}),
    ...(options.headers || {}),
  };

  if (appState.token) {
    headers.Authorization = `Bearer ${appState.token}`;
  }

  const response = await fetch(path, { ...options, headers });
  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json") ? await response.json() : {};

  if (!response.ok) {
    if (payload.errors && typeof payload.errors === "object") {
      const firstKey = Object.keys(payload.errors)[0];
      const firstVal = payload.errors[firstKey];
      const firstMsg = Array.isArray(firstVal) ? firstVal[0] : firstVal;
      if (firstMsg) throw new Error(firstMsg);
    }

    const errorPayload = payload.error;
    if (Array.isArray(errorPayload) && errorPayload.length > 0) {
      const firstError = errorPayload[0] || {};
      const errorMessage = firstError.msg || firstError.message || payload.message || `Erreur HTTP ${response.status}`;
      throw new Error(errorMessage);
    }

    const message = payload.error || payload.message || `Erreur HTTP ${response.status}`;
    throw new Error(typeof message === "string" ? message : JSON.stringify(message));
  }

  return payload;
}

// Alias — certaines sections utilisent apiFetch
const apiFetch = api;

// ═══════════════════════════════════════════════════════════════════════
// DRAWER SYSTEM — slide-over panels for forms
// ═══════════════════════════════════════════════════════════════════════
const DRAWER_MAP = {
  emp:            "empDrawer",
  dept:           "deptDrawer",
  payroll:        "payrollDrawer",
  attendance:     "attendanceDrawer",
  "attend-summary": "attendSummaryDrawer",
  leave:          "leaveDrawer",
  contract:       "contractDrawer",
};

function openDrawer(name) {
  const id = DRAWER_MAP[name];
  if (!id) return;
  closeAllDrawers();
  const overlay = document.getElementById("drawerOverlay");
  const drawer  = document.getElementById(id);
  if (overlay) overlay.classList.add("open");
  if (drawer)  drawer.classList.add("open");
  // Focus first input
  setTimeout(() => {
    const first = drawer && drawer.querySelector("input:not([type=hidden]), select, textarea");
    if (first) first.focus();
  }, 300);
}

function closeAllDrawers() {
  const overlay = document.getElementById("drawerOverlay");
  if (overlay) overlay.classList.remove("open");
  Object.values(DRAWER_MAP).forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.remove("open");
  });
}

// Close drawers with Escape key
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    const anyOpen = Object.values(DRAWER_MAP).some(id => {
      const el = document.getElementById(id);
      return el && el.classList.contains("open");
    });
    if (anyOpen) closeAllDrawers();
  }
});

// ═══════════════════════════════════════════════════════════════════════
// EMPLOYEE FILTER / SEARCH
// ═══════════════════════════════════════════════════════════════════════
const _empFilter = { status: "", dept: "", search: "" };

function setEmpFilter(btn) {
  document.querySelectorAll(".filter-chips .filter-chip").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  _empFilter.status = btn.dataset.filter || "";
  filterEmployeesUI();
}

function filterEmployeesUI() {
  const search = (document.getElementById("empSearch")?.value || "").toLowerCase().trim();
  const dept   = document.getElementById("empDeptFilter")?.value || "";
  _empFilter.search = search;
  _empFilter.dept   = dept;

  const filtered = (appState.employees || []).filter(emp => {
    const matchStatus = !_empFilter.status || emp.status === _empFilter.status;
    const matchDept   = !dept || (emp.department || "") === dept;
    const matchSearch = !search ||
      (emp.first_name + " " + emp.last_name).toLowerCase().includes(search) ||
      (emp.email || "").toLowerCase().includes(search) ||
      (emp.matricule || "").toLowerCase().includes(search);
    return matchStatus && matchDept && matchSearch;
  });

  const mode = appState.empViewMode || "list";
  if (mode === "grid") {
    renderEmployeeCards(filtered);
  } else {
    const wrap = document.getElementById("employeesTable");
    if (!wrap) return;
    if (!filtered.length) {
      wrap.innerHTML = `<div class="empty-state"><i class="ri-search-line"></i><h3>Aucun résultat</h3><p>Modifiez les filtres pour afficher des employés.</p></div>`;
      return;
    }
    const canModify = can("Modifier employés");
    renderTable("employeesTable",
      canModify ? ["ID","Nom","Email","Département","Rôle","Statut","Actions"] : ["ID","Nom","Email","Département","Rôle","Statut"],
      filtered.map(emp => [
        emp.id,
        `${emp.first_name} ${emp.last_name}`,
        emp.email,
        emp.department,
        emp.role,
        emp.status,
        ...(canModify ? [`<button class="btn btn-secondary btn-sm" onclick="editEmployee(${emp.id})"><i class="ri-edit-line"></i></button><button class="btn btn-secondary btn-sm" onclick="openEmpProfile(${emp.id})" title="Profil"><i class="ri-user-line"></i></button><button class="btn btn-danger btn-sm" onclick="deleteEmployee(${emp.id})"><i class="ri-delete-bin-line"></i></button>`] : []),
      ])
    );
  }
}

// Update employee stats badges
function updateEmpStats(employees) {
  const total    = employees.length;
  const actif    = employees.filter(e => e.status === "Actif").length;
  const suspendu = employees.filter(e => e.status === "Suspendu").length;
  const demis    = employees.filter(e => e.status === "Démissionné").length;
  const _s = id => document.getElementById(id);
  if (_s("empStatTotal"))   _s("empStatTotal").textContent   = total;
  if (_s("empStatActif"))   _s("empStatActif").textContent   = actif;
  if (_s("empStatSuspendu")) _s("empStatSuspendu").textContent = suspendu;
  if (_s("empStatDemis"))   _s("empStatDemis").textContent   = demis;
  // Populate dept filter
  const deptSel = document.getElementById("empDeptFilter");
  if (deptSel) {
    const depts = [...new Set(employees.map(e => e.department).filter(Boolean))].sort();
    const current = deptSel.value;
    deptSel.innerHTML = '<option value="">Tous les départements</option>' +
      depts.map(d => `<option value="${d}"${d === current ? " selected" : ""}>${d}</option>`).join("");
  }
}

// ═══════════════════════════════════════════════════════════════════════
// LEAVE FILTER
// ═══════════════════════════════════════════════════════════════════════
function setLeaveFilter(btn) {
  btn.closest(".filter-chips").querySelectorAll(".filter-chip").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
}

// Update leave stats + approval queue
function updateLeaveStats(leaves) {
  const pending  = leaves.filter(l => l.status === "En attente").length;
  const approved = leaves.filter(l => l.status === "Approuvé").length;
  const rejected = leaves.filter(l => l.status === "Rejeté").length;
  const _s = id => document.getElementById(id);
  if (_s("leaveStatPending"))  _s("leaveStatPending").textContent  = pending;
  if (_s("leaveStatApproved")) _s("leaveStatApproved").textContent = approved;
  if (_s("leaveStatRejected")) _s("leaveStatRejected").textContent = rejected;

  // Approval queue
  const queue = document.getElementById("leaveApprovalQueue");
  if (queue) {
    const pendingLeaves = leaves.filter(l => l.status === "En attente").slice(0, 5);
    if (pendingLeaves.length && can("Valider congés")) {
      queue.style.display = "flex";
      queue.innerHTML = `<div class="approval-queue-title"><i class="ri-alarm-warning-line"></i> ${pendingLeaves.length} demande(s) en attente d'approbation</div>` +
        pendingLeaves.map(l => {
          const emp = appState.employeeById[String(l.employee_id)] || {};
          const name = emp.first_name ? `${emp.first_name} ${emp.last_name}` : `Agent #${l.employee_id}`;
          return `<div class="approval-item">
            <div class="approval-item-icon"><i class="ri-calendar-todo-line"></i></div>
            <div class="approval-item-info">
              <div class="approval-item-name">${name}</div>
              <div class="approval-item-sub">${l.start_date || ""} → ${l.end_date || ""} · ${l.reason || ""}</div>
            </div>
            <div class="approval-item-actions">
              <button class="btn btn-success btn-sm" onclick="approveLeave(${l.id},'Approuvé')"><i class="ri-check-line"></i></button>
              <button class="btn btn-danger btn-sm" onclick="approveLeave(${l.id},'Rejeté')"><i class="ri-close-line"></i></button>
            </div>
          </div>`;
        }).join("");
    } else {
      queue.style.display = "none";
    }
  }
}

// Quick approve/reject from queue
async function approveLeave(leaveId, status) {
  try {
    await api(`/api/leaves/${leaveId}/approval`, { method: "PATCH", body: JSON.stringify({ status, decision_comment: "" }) });
    notify(`Congé ${status === "Approuvé" ? "approuvé" : "rejeté"}`);
    await loadLeaves();
  } catch (err) { notify(err.message, true); }
}

// ═══════════════════════════════════════════════════════════════════════
// PAYROLL STATS
// ═══════════════════════════════════════════════════════════════════════
function updatePayrollStats(payrolls) {
  const total = payrolls.length;
  const masse = payrolls.reduce((s, p) => s + Number(p.net_salary || 0), 0);
  const avg   = total ? masse / total : 0;
  const _s = id => document.getElementById(id);
  if (_s("payStatTotal")) _s("payStatTotal").textContent = total;
  if (_s("payStatMasse")) _s("payStatMasse").textContent = formatMoney(masse);
  if (_s("payStatAvg"))   _s("payStatAvg").textContent   = formatMoney(avg);
}

// ═══════════════════════════════════════════════════════════════════════
// CONTRACT FILTER / STATS / EXPIRY ALERT
// ═══════════════════════════════════════════════════════════════════════
function setContractFilter(btn) {
  btn.closest(".filter-chips").querySelectorAll(".filter-chip").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
}

function updateContractStats(contracts) {
  const total = contracts.length;
  const cdi   = contracts.filter(c => c.contract_type === "CDI").length;
  const cdd   = contracts.filter(c => c.contract_type === "CDD").length;
  const stage = contracts.filter(c => c.contract_type === "Stage").length;
  const _s = id => document.getElementById(id);
  if (_s("contractStatTotal")) _s("contractStatTotal").textContent = total;
  if (_s("contractStatCdi"))   _s("contractStatCdi").textContent   = cdi;
  if (_s("contractStatCdd"))   _s("contractStatCdd").textContent   = cdd;
  if (_s("contractStatStage")) _s("contractStatStage").textContent = stage;

  // Expiry alert: CDD ending in 30 days
  const now = new Date();
  const in30 = new Date(now.getTime() + 30 * 86400000);
  const expiring = contracts.filter(c => {
    if (!c.end_date) return false;
    const d = new Date(c.end_date);
    return d >= now && d <= in30;
  });
  const alert = document.getElementById("contractExpiryAlert");
  const msg   = document.getElementById("contractExpiryMsg");
  if (alert) {
    if (expiring.length) {
      alert.style.display = "flex";
      if (msg) msg.textContent = `${expiring.length} contrat(s) expirent dans les 30 prochains jours`;
    } else {
      alert.style.display = "none";
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════
// ATTENDANCE SUMMARY DRAWER
// ═══════════════════════════════════════════════════════════════════════
function setupAttendanceSummaryDrawer() {
  const btn = document.getElementById("btnAttendanceSummaryDrawer");
  if (!btn || btn._drawerBound) return;
  btn._drawerBound = true;
  btn.addEventListener("click", async () => {
    const month = document.getElementById("attendanceSummaryMonthDrawer")?.value;
    if (!month) { notify("Sélectionne un mois", true); return; }
    try {
      const data = await api(`/api/attendances/summary/monthly?month=${month}`);
      const wrap = document.getElementById("attendanceSummaryTableDrawer");
      if (!wrap) return;
      const rows = Array.isArray(data) ? data : (data.summary || []);
      if (!rows.length) { wrap.innerHTML = `<div class="empty-state"><p>Aucune donnée pour ce mois.</p></div>`; return; }
      renderTable("attendanceSummaryTableDrawer",
        ["Employé", "Présences", "Absences", "Heures travaillées", "Retards (min)"],
        rows.map(r => [r.employee_name || r.employee_id, r.present_days || 0, r.absent_days || 0, r.total_hours || 0, r.total_late_minutes || 0])
      );
    } catch (err) { notify(err.message, true); }
  });
}

async function navigate(section) {
  if (!section) return;
  const target = $(`section-${section}`);
  if (!target) return;

  const menuBtn = document.querySelector(`.menu-item[data-section="${section}"]`);
  document.querySelectorAll(".menu-item").forEach((item) => item.classList.remove("active"));
  if (menuBtn) menuBtn.classList.add("active");

  document.querySelectorAll(".section").forEach((element) => element.classList.remove("active"));
  target.classList.add("active");
  if ($("sectionTitle")) {
    $("sectionTitle").textContent = sectionTitleMap[section] || "Dashboard";
  }

  if (section === "overview") {
    await loadOverview();
  }
  if (section === "reports") {
    await loadReportsSection();
  }
  if (section === "accounting") {
    await loadAccountingSection();
  }
  if (section === "biometric") {
    await loadBiometricSection();
  }
  if (section === "training") {
    await loadTrainingSection();
  }
  if (section === "performance") {
    await loadPerformanceSection();
  }
  if (section === "medical-leaves") {
    await loadMedicalLeavesSection();
  }
  if (section === "notifications") {
    await loadNotificationsSection();
  }
  if (section === "recruitment") {
    await loadRecruitmentSection();
  }
  if (section === "settings") {
    await loadSettingsSection();
  }
  if (section === "attendances") {
    await loadAttendances();
  }
  if (section === "team") {
    await loadTeamSection();
  }
  if (section === "messages") {
    const query = ($("messagesSearch")?.value || "").trim();
    await loadMessageRecipients();
    await loadConversations(query);
    const firstConversation = (appState.conversations || [])[0];
    if (firstConversation && !appState.activeChatUserId) {
      await openConversation(firstConversation.user_id);
    } else if (appState.activeChatUserId) {
      await loadConversationThread(appState.activeChatUserId);
    } else {
      setActiveConversationInfo(null);
      renderChatThread([]);
    }
  }

  document.dispatchEvent(new CustomEvent("sgrh:navigate", { detail: { section } }));
}

function bindNavigation() {
  document.querySelectorAll(".menu-item").forEach((button) => {
    button.addEventListener("click", async () => {
      await navigate(button.dataset.section);
    });
  });
}

window.navigate = navigate;
window.loadOverview = loadOverview;

// ── Chart helpers ──────────────────────────────────────────────────────────
function chartColors(n, alpha = 0.85) {
  const base = [
    `rgba(13,92,77,${alpha})`,    `rgba(43,184,154,${alpha})`,
    `rgba(194,120,3,${alpha})`,   `rgba(36,48,68,${alpha})`,
    `rgba(6,118,71,${alpha})`,    `rgba(180,35,24,${alpha})`,
    `rgba(20,122,102,${alpha})`,  `rgba(91,101,120,${alpha})`,
    `rgba(154,95,2,${alpha})`,    `rgba(11,18,32,${alpha})`,
  ];
  const out = [];
  for (let i = 0; i < n; i++) out.push(base[i % base.length]);
  return out;
}

function chartGridColor() {
  return document.documentElement.getAttribute("data-theme") === "light"
    ? "rgba(20,40,100,0.08)" : "rgba(255,255,255,0.07)";
}
function chartTickColor() {
  return document.documentElement.getAttribute("data-theme") === "light"
    ? "#5a6a8a" : "#7a8db5";
}

function destroyChart(key) {
  if (appState.charts[key]) { appState.charts[key].destroy(); appState.charts[key] = null; }
}

function makeGradient(ctx, color1, color2) {
  const g = ctx.createLinearGradient(0, 0, 0, 200);
  g.addColorStop(0, color1);
  g.addColorStop(1, color2);
  return g;
}

function animateCounter(el, target, duration = 1000, formatter = (v) => v) {
  if (!el) return;
  const start = 0;
  const step = (timestamp) => {
    if (!step.startTime) step.startTime = timestamp;
    const progress = Math.min((timestamp - step.startTime) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = formatter(Math.round(start + (target - start) * eased));
    if (progress < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

// ── Overview ───────────────────────────────────────────────────────────────
async function loadOverview() {
  // Fetch the rich dashboard stats
  const [data, basicStats] = await Promise.all([
    api("/api/reports/dashboard").catch(() => null),
    can("Exporter rapports") ? api("/api/reports/stats").catch(() => null) : Promise.resolve(null),
  ]);

  if (!data) return;

  const em  = data.employees   || {};
  const pay = data.payroll     || {};
  const att = data.attendance  || {};
  const lv  = data.leaves      || {};
  const dept= data.departments || {};
  const tr  = data.training    || {};
  const pf  = data.performance || {};
  const rec = data.recruitment || {};
  const con = data.contracts   || {};

  // ── KPI counters ──
  if ($("kpiEmployees")) {
    animateCounter($("kpiEmployees"), em.total || 0, 900, (v) => v.toLocaleString("fr-FR"));
  }
  if ($("kpiNewBadge")) $("kpiNewBadge").textContent = `+${em.new_this_month || 0} ce mois`;
  if ($("kpiActive"))   $("kpiActive").textContent   = `${em.active || 0} actifs`;

  const avgSalary  = pay.average || 0;
  const totalPay   = pay.total   || 0;
  if ($("kpiAvgSalary")) {
    animateCounter($("kpiAvgSalary"), Math.round(avgSalary), 900, (v) => formatMoney(v));
  }
  if ($("kpiTotalPayroll")) $("kpiTotalPayroll").textContent = `Total: ${formatMoney(totalPay)}`;

  const absRate = att.absence_rate || 0;
  if ($("kpiAbsence")) {
    animateCounter($("kpiAbsence"), absRate * 10, 900, (v) => `${(v/10).toFixed(1)}%`);
  }
  const absDelta = $("kpiAbsDelta");
  if (absDelta) {
    absDelta.className = "kpi-delta " + (absRate > 10 ? "down" : absRate > 5 ? "flat" : "up");
    absDelta.textContent = absRate > 10 ? "Élevé" : absRate > 5 ? "Moyen" : "Faible";
  }
  if ($("kpiAbsCount")) $("kpiAbsCount").textContent = `${att.absences || 0} absences`;

  if ($("kpiPerf")) {
    animateCounter($("kpiPerf"), Math.round((pf.average_score || 0) * 10), 900, (v) => `${(v/10).toFixed(1)}/10`);
  }
  if ($("kpiPerfCount")) $("kpiPerfCount").textContent = `${pf.total_evaluations || 0} évaluations`;

  if ($("kpiTraining")) {
    animateCounter($("kpiTraining"), tr.enrollments || 0, 900, (v) => v.toLocaleString("fr-FR"));
  }
  if ($("kpiTrainDone")) $("kpiTrainDone").textContent = `${tr.completed || 0} terminées`;
  if ($("kpiTrainDelta")) $("kpiTrainDelta").textContent = `${tr.total || 0} formations`;

  if ($("kpiRecruitApps")) {
    animateCounter($("kpiRecruitApps"), rec.total_applications || 0, 900, (v) => v.toLocaleString("fr-FR"));
  }
  if ($("kpiOpenOffers")) $("kpiOpenOffers").textContent = `${rec.open_offers || 0} offres`;
  const recruitDelta = $("kpiRecruitDelta");
  if (recruitDelta) {
    recruitDelta.className = "kpi-delta " + (rec.open_offers > 0 ? "up" : "flat");
    recruitDelta.textContent = rec.open_offers > 0 ? `${rec.open_offers} ouvertes` : "Aucune offre";
  }

  if ($("kpiLeaves")) {
    animateCounter($("kpiLeaves"), lv.total || 0, 900, (v) => v.toLocaleString("fr-FR"));
  }
  const lvPending = (lv.status || {})["En attente"] || 0;
  if ($("kpiLeavesPending")) $("kpiLeavesPending").textContent = `${lvPending} en attente`;

  if ($("kpiContracts")) {
    animateCounter($("kpiContracts"), con.total || 0, 900, (v) => v.toLocaleString("fr-FR"));
  }
  if ($("kpiContractsExp")) $("kpiContractsExp").textContent = `${con.expiring_soon || 0} expirent bientôt`;
  const contractExpDelta = $("kpiContractExp");
  if (contractExpDelta) {
    contractExpDelta.className = "kpi-delta " + (con.expiring_soon > 0 ? "down" : "up");
    contractExpDelta.textContent = con.expiring_soon > 0 ? `${con.expiring_soon} à renouveler` : "À jour";
  }

  // Also update legacy IDs if present (backward compat)
  if ($("kpiPayroll")) $("kpiPayroll").textContent = formatMoney(totalPay);

  setReportsContent(basicStats || data);

  // ── Chart 1: Payroll trend (line + gradient) ──
  const payByMonth = pay.by_month || { labels: [], values: [] };
  destroyChart("payrollTrend");
  const payCanvas = $("payrollTrendChart");
  if (payCanvas) {
    const ctx = payCanvas.getContext("2d");
    const gradient = ctx.createLinearGradient(0, 0, 0, 200);
    gradient.addColorStop(0, "rgba(79,127,255,0.35)");
    gradient.addColorStop(1, "rgba(79,127,255,0.02)");
    appState.charts.payrollTrend = new Chart(payCanvas, {
      type: "line",
      data: {
        labels: payByMonth.labels.map(l => {
          const [y, m] = l.split("-");
          return new Date(+y, +m-1).toLocaleDateString("fr-FR", { month: "short", year: "2-digit" });
        }),
        datasets: [{
          label: "Masse salariale (XAF)",
          data: payByMonth.values,
          borderColor: "#4f7fff",
          backgroundColor: gradient,
          borderWidth: 2.5,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: "#4f7fff",
          pointRadius: 3,
          pointHoverRadius: 6,
        }]
      },
      options: {
        responsive: true,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => ` ${formatMoney(ctx.raw)}`
            }
          }
        },
        scales: {
          x: { ticks: { color: chartTickColor(), font: { size: 11 } }, grid: { color: chartGridColor() } },
          y: { ticks: { color: chartTickColor(), font: { size: 11 }, callback: (v) => formatMoney(v) }, grid: { color: chartGridColor() } }
        }
      }
    });
  }

  // ── Chart 2: Department distribution (doughnut) ──
  destroyChart("dept");
  const deptCanvas = $("deptChart");
  if (deptCanvas) {
    const colors = chartColors(dept.names.length);
    appState.charts.dept = new Chart(deptCanvas, {
      type: "doughnut",
      data: {
        labels: dept.names,
        datasets: [{
          data: dept.counts,
          backgroundColor: colors,
          borderWidth: 0,
          hoverOffset: 8,
        }]
      },
      options: {
        responsive: true,
        cutout: "65%",
        plugins: {
          legend: { position: "bottom", labels: { color: chartTickColor(), font: { size: 11 }, padding: 10 } },
          tooltip: { callbacks: { label: (ctx) => ` ${ctx.label}: ${ctx.raw} employés` } }
        }
      }
    });
  }

  // ── Chart 3: Attendance (stacked bar) ──
  const attByMonth = att.by_month || { labels: [], present: [], absent: [] };
  destroyChart("attend");
  const attendCanvas = $("attendChart");
  if (attendCanvas) {
    const shortLabels = attByMonth.labels.map(l => {
      const [y, m] = l.split("-");
      return new Date(+y, +m-1).toLocaleDateString("fr-FR", { month: "short" });
    });
    appState.charts.attend = new Chart(attendCanvas, {
      type: "bar",
      data: {
        labels: shortLabels,
        datasets: [
          {
            label: "Présences",
            data: attByMonth.present,
            backgroundColor: "rgba(0,204,144,0.75)",
            borderRadius: 4, stack: "s"
          },
          {
            label: "Absences",
            data: attByMonth.absent,
            backgroundColor: "rgba(255,77,109,0.75)",
            borderRadius: 4, stack: "s"
          }
        ]
      },
      options: {
        responsive: true, plugins: {
          legend: { position: "bottom", labels: { color: chartTickColor(), font: { size: 11 }, padding: 10 } }
        },
        scales: {
          x: { stacked: true, ticks: { color: chartTickColor(), font: { size: 10 } }, grid: { display: false } },
          y: { stacked: true, ticks: { color: chartTickColor(), font: { size: 10 } }, grid: { color: chartGridColor() } }
        }
      }
    });
  }

  // ── Chart 4: Leave status (doughnut) ──
  destroyChart("leave");
  const leaveCanvas = $("leaveChart");
  if (leaveCanvas) {
    const lvStatus = lv.status || {};
    appState.charts.leave = new Chart(leaveCanvas, {
      type: "doughnut",
      data: {
        labels: Object.keys(lvStatus),
        datasets: [{
          data: Object.values(lvStatus),
          backgroundColor: ["rgba(255,176,32,0.85)", "rgba(0,204,144,0.85)", "rgba(255,77,109,0.85)"],
          borderWidth: 0,
          hoverOffset: 8,
        }]
      },
      options: {
        responsive: true,
        cutout: "60%",
        plugins: {
          legend: { position: "bottom", labels: { color: chartTickColor(), font: { size: 11 }, padding: 10 } }
        }
      }
    });
  }

  // ── Chart 5: Performance distribution (horizontal bar) ──
  destroyChart("perfDist");
  const perfCanvas = $("perfDistChart");
  if (perfCanvas) {
    const sd = pf.score_distribution || {};
    appState.charts.perfDist = new Chart(perfCanvas, {
      type: "bar",
      data: {
        labels: Object.keys(sd),
        datasets: [{
          label: "Employés",
          data: Object.values(sd),
          backgroundColor: ["rgba(0,204,144,0.8)", "rgba(79,127,255,0.8)", "rgba(255,176,32,0.8)", "rgba(255,77,109,0.8)"],
          borderRadius: 6,
        }]
      },
      options: {
        indexAxis: "y",
        responsive: true,
        plugins: {
          legend: { display: false },
        },
        scales: {
          x: { ticks: { color: chartTickColor(), font: { size: 10 } }, grid: { color: chartGridColor() } },
          y: { ticks: { color: chartTickColor(), font: { size: 10 } }, grid: { display: false } }
        }
      }
    });
  }

  // ── Chart 6: Department payroll (bar) ──
  destroyChart("deptPayroll");
  const deptPayCanvas = $("deptPayrollChart");
  if (deptPayCanvas && dept.names.length) {
    appState.charts.deptPayroll = new Chart(deptPayCanvas, {
      type: "bar",
      data: {
        labels: dept.names,
        datasets: [{
          label: "Masse salariale",
          data: dept.payroll,
          backgroundColor: chartColors(dept.names.length, 0.75),
          borderRadius: 6,
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { ticks: { color: chartTickColor(), font: { size: 10 } }, grid: { display: false } },
          y: {
            ticks: { color: chartTickColor(), font: { size: 10 }, callback: (v) => formatMoney(v) },
            grid: { color: chartGridColor() }
          }
        }
      }
    });
  }

  // ── Chart 7: Recruitment funnel (horizontal bar) ──
  destroyChart("recruitFunnel");
  const recruitCanvas = $("recruitFunnelChart");
  if (recruitCanvas) {
    const appStatus = rec.application_status || {};
    appState.charts.recruitFunnel = new Chart(recruitCanvas, {
      type: "bar",
      data: {
        labels: Object.keys(appStatus),
        datasets: [{
          label: "Candidatures",
          data: Object.values(appStatus),
          backgroundColor: ["rgba(79,127,255,0.8)", "rgba(255,176,32,0.8)", "rgba(0,204,144,0.8)", "rgba(255,77,109,0.8)"],
          borderRadius: 6,
        }]
      },
      options: {
        indexAxis: "y",
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { ticks: { color: chartTickColor(), font: { size: 10 } }, grid: { color: chartGridColor() } },
          y: { ticks: { color: chartTickColor(), font: { size: 10 } }, grid: { display: false } }
        }
      }
    });
  }

  // ── Stat rows ──
  const statRowsEl = $("overviewStatRows");
  if (statRowsEl) {
    const rows = [
      { icon: "ri-team-fill",             label: "Effectif total",         value: `${em.total || 0} employés`,        color: "#4f7fff" },
      { icon: "ri-user-follow-line",      label: "Employés actifs",        value: `${em.active || 0} (${em.total ? Math.round(em.active/em.total*100) : 0}%)`, color: "#00cc90" },
      { icon: "ri-building-2-line",       label: "Départements",           value: dept.names.length || 0,             color: "#a855f7" },
      { icon: "ri-money-dollar-circle-line", label: "Salaire moyen",       value: formatMoney(avgSalary),             color: "#00cc90" },
      { icon: "ri-calendar-close-line",  label: "Taux d'absentéisme",     value: `${absRate}%`,                       color: absRate > 10 ? "#ff4d6d" : "#ffb020" },
      { icon: "ri-file-text-line",        label: "Contrats actifs",        value: con.total || 0,                     color: "#14b8a6" },
      { icon: "ri-alarm-warning-line",    label: "Contrats expirant",      value: con.expiring_soon || 0,             color: con.expiring_soon > 0 ? "#ff4d6d" : "#00cc90" },
      { icon: "ri-book-open-line",        label: "Formations actives",     value: tr.in_progress || 0,                color: "#6366f1" },
    ];
    statRowsEl.innerHTML = rows.map(r => `
      <div class="stat-row">
        <span class="stat-row-label" style="color:${r.color}"><i class="${r.icon}" style="color:${r.color}"></i> ${r.label}</span>
        <span class="stat-row-value">${r.value}</span>
      </div>`).join("");
  }

  // ── Activity feed ──
  const activityEl = $("overviewActivityFeed");
  if (activityEl) {
    const activities = [];
    if (em.new_this_month > 0) activities.push({ icon: "ri-user-add-line", bg: "rgba(79,127,255,0.15)", color: "#4f7fff", text: `${em.new_this_month} nouvel(s) employé(s) ce mois`, detail: "Ressources humaines", time: "Ce mois" });
    if (lvPending > 0) activities.push({ icon: "ri-calendar-todo-line", bg: "rgba(255,176,32,0.15)", color: "#ffb020", text: `${lvPending} demande(s) de congé en attente`, detail: "Gestion des congés", time: "En cours" });
    if (con.expiring_soon > 0) activities.push({ icon: "ri-alarm-warning-line", bg: "rgba(255,77,109,0.15)", color: "#ff4d6d", text: `${con.expiring_soon} contrat(s) expirent bientôt`, detail: "Gestion des contrats", time: "Urgent" });
    if (rec.open_offers > 0) activities.push({ icon: "ri-briefcase-line", bg: "rgba(0,204,144,0.15)", color: "#00cc90", text: `${rec.open_offers} offre(s) d'emploi ouverte(s)`, detail: "Recrutement", time: "Actif" });
    if (tr.in_progress > 0) activities.push({ icon: "ri-book-open-line", bg: "rgba(99,102,241,0.15)", color: "#6366f1", text: `${tr.in_progress} formation(s) en cours`, detail: "Formation", time: "En cours" });
    if (data.notifications?.unread > 0) activities.push({ icon: "ri-notification-3-line", bg: "rgba(255,77,109,0.15)", color: "#ff4d6d", text: `${data.notifications.unread} notification(s) non lue(s)`, detail: "Notifications", time: "Nouveau" });

    if (activities.length === 0) {
      activityEl.innerHTML = `<div class="empty-state"><i class="ri-checkbox-circle-line" style="color:var(--ok)"></i><h3>Tout est à jour</h3><p>Aucune activité urgente détectée</p></div>`;
    } else {
      activityEl.innerHTML = activities.map(a => `
        <div class="activity-item">
          <div class="activity-icon-wrap" style="background:${a.bg};color:${a.color}">
            <i class="${a.icon}"></i>
          </div>
          <div class="activity-text">
            <strong>${a.text}</strong>
            <span>${a.detail}</span>
          </div>
          <span class="activity-time">${a.time}</span>
        </div>`).join("");
    }
  }
}

async function loadOverviewSection() {
  await loadOverview();
}

// ─────────────────────────────────────────────────────────────────────
// EMPLOYEE CARD VIEW TOGGLE
// ─────────────────────────────────────────────────────────────────────

function setEmpView(mode) {
  const tableEl = $("employeesTable");
  const gridEl  = $("employeesGrid");
  const btnList = $("empViewList");
  const btnGrid = $("empViewGrid");
  if (!tableEl || !gridEl) return;

  if (mode === "grid") {
    tableEl.style.display = "none";
    gridEl.style.display  = "";
    if (btnList) btnList.classList.remove("active");
    if (btnGrid) btnGrid.classList.add("active");
    // Render cards from cached employees
    renderEmployeeCards(appState.employees || []);
  } else {
    tableEl.style.display = "";
    gridEl.style.display  = "none";
    if (btnList) btnList.classList.add("active");
    if (btnGrid) btnGrid.classList.remove("active");
  }
}

function renderEmployeeCards(employees) {
  const grid = $("employeesGrid");
  if (!grid) return;
  if (!employees.length) {
    grid.innerHTML = '<div class="empty-state"><i class="ri-team-line"></i><p>Aucun employé</p></div>';
    return;
  }
  grid.innerHTML = employees.map(e => {
    const initials = `${(e.first_name || "?")[0]}${(e.last_name || "?")[0]}`.toUpperCase();
    const statusCls = { Actif: "actif", Suspendu: "suspendu", "Démissionné": "demissionne" }[e.status] || "actif";
    return `
    <div class="employee-card" onclick="openEmpProfile(${e.id})">
      <div class="employee-avatar">
        ${e.photo_url ? `<img src="${e.photo_url}" alt="${initials}" onerror="this.style.display='none';this.parentNode.textContent='${initials}'"/>` : initials}
      </div>
      <div class="employee-name">${e.first_name} ${e.last_name}</div>
      <div class="employee-role">${e.role || "—"}</div>
      <div class="employee-dept"><i class="ri-building-2-line"></i> ${e.department || "—"}</div>
      <span class="status-pill ${statusCls}">${e.status || "Actif"}</span>
    </div>`;
  }).join("");
}

function openEmpProfile(empId) {
  const emp = appState.employeeById[String(empId)];
  if (!emp) return;
  const modal = $("empProfileModal");
  if (!modal) return;

  const initials = `${(emp.first_name || "?")[0]}${(emp.last_name || "?")[0]}`.toUpperCase();
  const avatar = $("empModalAvatar");
  if (avatar) {
    if (emp.photo_url) {
      avatar.innerHTML = `<img src="${emp.photo_url}" alt="${initials}" style="width:100%;height:100%;border-radius:50%;object-fit:cover" onerror="this.style.display='none';this.parentNode.textContent='${initials}'" />`;
    } else {
      avatar.textContent = initials;
    }
  }
  const statusCls = { Actif: "actif", Suspendu: "suspendu", "Démissionné": "demissionne" }[emp.status] || "actif";
  if ($("empModalName"))   $("empModalName").textContent   = `${emp.first_name} ${emp.last_name}`;
  if ($("empModalRole"))   $("empModalRole").textContent   = emp.role || "—";
  if ($("empModalStatus")) { $("empModalStatus").textContent = emp.status || "Actif"; $("empModalStatus").className = `status-pill ${statusCls}`; }
  if ($("empModalEmail"))  $("empModalEmail").textContent  = emp.email || "—";
  if ($("empModalPhone"))  $("empModalPhone").textContent  = emp.phone || "—";
  if ($("empModalDept"))   $("empModalDept").textContent   = emp.department || "—";
  if ($("empModalHire"))   $("empModalHire").textContent   = emp.hire_date ? new Date(emp.hire_date).toLocaleDateString("fr-FR") : "—";

  modal.style.display = "flex";
}

function closeEmpProfile() {
  const modal = $("empProfileModal");
  if (modal) modal.style.display = "none";
}

// ─────────────────────────────────────────────────────────────────────
// PAYSLIP MODAL
// ─────────────────────────────────────────────────────────────────────

function openPayslipModal(payrollId) {
  const modal = $("payslipModal");
  if (!modal) return;
  // Find payroll data from API
  apiFetch(`/api/payrolls/${payrollId}`).then(p => {
    if (!p) return;
    const emp = appState.employeeById[String(p.employee_id)] || {};
    if ($("psMonth"))       $("psMonth").textContent       = p.payroll_month || "—";
    if ($("psEmpName"))     $("psEmpName").textContent     = `${emp.first_name || ""} ${emp.last_name || ""}`.trim() || "—";
    if ($("psEmpDept"))     $("psEmpDept").textContent     = emp.department || "—";
    if ($("psEmpId"))       $("psEmpId").textContent       = `EMP-${String(p.employee_id).padStart(4,"0")}`;
    if ($("psPaidAt"))      $("psPaidAt").textContent      = p.paid_at ? new Date(p.paid_at).toLocaleDateString("fr-FR") : "Non payé";
    if ($("psBase"))        $("psBase").textContent        = formatMoney(p.base_salary || 0);
    if ($("psBonus"))       $("psBonus").textContent       = formatMoney(p.bonus || 0);
    if ($("psOvertime"))    $("psOvertime").textContent    = formatMoney(p.overtime_pay || 0);
    if ($("psDeductions"))  $("psDeductions").textContent  = `– ${formatMoney(p.deductions || 0)}`;
    if ($("psTaxes"))       $("psTaxes").textContent       = `– ${formatMoney(p.taxes || 0)}`;
    if ($("psNet"))         $("psNet").textContent         = `${formatMoney(p.net_salary || 0)} XAF`;
    modal.style.display = "flex";
  });
}

function closePayslipModal() {
  const modal = $("payslipModal");
  if (modal) modal.style.display = "none";
}

// ─────────────────────────────────────────────────────────────────────
// RECRUITMENT PIPELINE
// ─────────────────────────────────────────────────────────────────────

function renderPipelineStats(stats) {
  const wrap = $("recruitPipelineStats");
  if (!wrap) return;
  const stages = [
    { label: "Reçues", count: (stats.by_status || {})["Reçue"] || 0, color: "#4f7fff", bg: "rgba(79,127,255,0.12)", icon: "ri-mail-open-line" },
    { label: "En cours", count: (stats.by_status || {})["En cours"] || 0, color: "#ffb020", bg: "rgba(255,176,32,0.12)", icon: "ri-time-line" },
    { label: "Retenus", count: (stats.by_status || {})["Retenu"] || 0, color: "#00cc90", bg: "rgba(0,204,144,0.12)", icon: "ri-user-star-line" },
    { label: "Rejetés", count: (stats.by_status || {})["Rejeté"] || 0, color: "#ff4d6d", bg: "rgba(255,77,109,0.12)", icon: "ri-close-circle-line" },
  ];
  const total = stages.reduce((s, st) => s + st.count, 0);
  wrap.style.display = "grid";
  wrap.style.gridTemplateColumns = `repeat(${stages.length}, 1fr) 0.2fr`.repeat(stages.length - 1).split(" 0.2fr")[0] || `repeat(${stages.length},1fr)`;

  let html = "";
  stages.forEach((st, i) => {
    const pct = total ? Math.round(st.count / total * 100) : 0;
    html += `
      <div class="pipeline-stage">
        <div class="pipeline-stage-icon" style="background:${st.bg};color:${st.color}">
          <i class="${st.icon}"></i>
        </div>
        <div class="pipeline-stage-count" style="color:${st.color}">${st.count}</div>
        <div class="pipeline-stage-label">${st.label}</div>
        <div style="font-size:0.7rem;color:var(--text-3)">${pct}%</div>
      </div>`;
    if (i < stages.length - 1) {
      html += `<div class="pipeline-stage-arrow"><i class="ri-arrow-right-line"></i></div>`;
    }
  });

  // Wrap in grid with arrows
  const gridStyle = `display:grid;grid-template-columns:${stages.map(() => "1fr").join(" 40px ").replace(/1fr 40px$/, "1fr")};gap:8px;align-items:start`;
  // Simpler version - just put stages side by side
  wrap.style.cssText = `display:grid;grid-template-columns:repeat(${stages.length},1fr);gap:12px;margin-bottom:0`;
  wrap.innerHTML = stages.map((st, i) => {
    const pct = total ? Math.round(st.count / total * 100) : 0;
    return `
    <div class="pipeline-stage">
      <div class="pipeline-stage-icon" style="background:${st.bg};color:${st.color}">
        <i class="${st.icon}"></i>
      </div>
      <div class="pipeline-stage-count" style="color:${st.color}">${st.count}</div>
      <div class="pipeline-stage-label">${st.label}</div>
      <div style="font-size:0.7rem;color:var(--text-3)">${pct}% du total</div>
      <div style="height:4px;background:var(--border);border-radius:999px;width:100%;margin-top:8px">
        <div style="height:100%;width:${pct}%;background:${st.color};border-radius:999px;transition:width .8s ease"></div>
      </div>
    </div>`;
  }).join("");
}

// ─────────────────────────────────────────────────────────────────────
// PERFORMANCE RADAR CHART
// ─────────────────────────────────────────────────────────────────────

function renderPerfRadar(evaluations) {
  destroyChart("perfRadar");
  const canvas = $("perfRadarChart");
  if (!canvas) return;
  if (!evaluations || !evaluations.length) {
    canvas.parentElement.innerHTML = `<div class="empty-state" style="padding:40px 0"><i class="ri-bar-chart-2-line"></i><p>Aucune évaluation disponible</p></div>`;
    return;
  }
  // Compute score distribution across periods
  const periodMap = {};
  evaluations.forEach(ev => {
    const period = ev.period || "Inconnu";
    if (!periodMap[period]) periodMap[period] = [];
    periodMap[period].push(parseFloat(ev.score || 0));
  });
  const periods = Object.keys(periodMap).slice(0, 6);
  const avgByPeriod = periods.map(p => {
    const scores = periodMap[p];
    return Math.round(scores.reduce((a, b) => a + b, 0) / scores.length * 10) / 10;
  });

  if (periods.length < 3) {
    // Bar chart fallback for <3 periods
    appState.charts.perfRadar = new Chart(canvas, {
      type: "bar",
      data: {
        labels: periods,
        datasets: [{
          label: "Score moyen",
          data: avgByPeriod,
          backgroundColor: chartColors(periods.length, 0.7),
          borderRadius: 6,
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          y: { min: 0, max: 100, ticks: { color: chartTickColor() }, grid: { color: chartGridColor() } },
          x: { ticks: { color: chartTickColor() }, grid: { display: false } }
        }
      }
    });
    return;
  }

  appState.charts.perfRadar = new Chart(canvas, {
    type: "radar",
    data: {
      labels: periods,
      datasets: [{
        label: "Score moyen / période",
        data: avgByPeriod,
        borderColor: "#4f7fff",
        backgroundColor: "rgba(79,127,255,0.18)",
        borderWidth: 2,
        pointBackgroundColor: "#4f7fff",
        pointRadius: 4,
        pointHoverRadius: 7,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        r: {
          min: 0, max: 100,
          ticks: { color: chartTickColor(), backdropColor: "transparent", font: { size: 10 } },
          grid: { color: chartGridColor() },
          pointLabels: { color: chartTickColor(), font: { size: 11 } }
        }
      }
    }
  });
}

function renderPerfTopList(evaluations) {
  const wrap = $("perfTopList");
  if (!wrap || !evaluations) return;
  const sorted = [...evaluations].sort((a, b) => (b.score || 0) - (a.score || 0)).slice(0, 7);
  if (!sorted.length) { wrap.innerHTML = '<p class="text-muted" style="padding:16px">Aucune évaluation</p>'; return; }
  const rankCls = ["gold", "silver", "bronze"];
  wrap.innerHTML = sorted.map((ev, i) => {
    const emp = appState.employeeById[String(ev.employee_id)] || {};
    const name = emp.first_name ? `${emp.first_name} ${emp.last_name}` : (ev.employee_name || `Employé #${ev.employee_id}`);
    return `<div class="perf-top-item">
      <div class="perf-rank ${rankCls[i] || ""}">${i + 1}</div>
      <div class="perf-top-name">${name}</div>
      <span class="perf-top-score">${Number(ev.score || 0).toFixed(1)}</span>
    </div>`;
  }).join("");
}

// ─────────────────────────────────────────────────────────────────────
// TRAINING CARD GRID
// ─────────────────────────────────────────────────────────────────────

function renderTrainingCards(trainings) {
  const grid = $("trainingCardGrid");
  if (!grid) return;
  if (!trainings || !trainings.length) {
    grid.innerHTML = '<div class="empty-state"><i class="ri-book-open-line"></i><p>Aucune formation</p></div>';
    return;
  }
  const statusMap = {
    "planifié": { cls: "planifie", label: "Planifié", icon: "ri-calendar-line" },
    "en cours": { cls: "en-cours",  label: "En cours",  icon: "ri-play-circle-line" },
    "terminé":  { cls: "termine",   label: "Terminé",   icon: "ri-checkbox-circle-line" },
    "annulé":   { cls: "annule",    label: "Annulé",    icon: "ri-close-circle-line" },
  };
  grid.innerHTML = trainings.map(t => {
    const st = statusMap[t.status] || statusMap["planifié"];
    const enrolled = t.enrolled_count || 0;
    const max      = t.max_participants || 20;
    const pct      = Math.min(100, Math.round(enrolled / max * 100));
    const dateRange = (t.start_date && t.end_date)
      ? `${new Date(t.start_date).toLocaleDateString("fr-FR")} → ${new Date(t.end_date).toLocaleDateString("fr-FR")}`
      : (t.start_date || "—");
    return `
    <div class="formation-card-pro">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px">
        <div class="formation-card-title">${t.title}</div>
        <span class="formation-card-status ${st.cls}"><i class="${st.icon}"></i> ${st.label}</span>
      </div>
      ${t.trainer ? `<div class="formation-card-trainer"><i class="ri-user-voice-line"></i> ${t.trainer}</div>` : ""}
      <div class="formation-card-dates"><i class="ri-calendar-event-line"></i> ${dateRange}</div>
      ${t.description ? `<div style="font-size:0.76rem;color:var(--text-2);line-height:1.4">${t.description.slice(0,90)}${t.description.length > 90 ? "…" : ""}</div>` : ""}
      <div class="formation-card-progress">
        <div class="formation-card-progress-label">
          <span><i class="ri-group-line"></i> ${enrolled} / ${max} inscrits</span>
          <span>${pct}%</span>
        </div>
        <div class="formation-progress-bar">
          <div class="formation-progress-fill" style="width:${pct}%"></div>
        </div>
      </div>
      <div class="formation-card-actions">
        <button class="btn btn-secondary btn-sm" onclick="openTrainingDetail(${t.id})">
          <i class="ri-eye-line"></i> Détails
        </button>
        ${can("Modifier formations") ? `<button class="btn btn-danger btn-sm" onclick="deleteTraining(${t.id})"><i class="ri-delete-bin-line"></i></button>` : ""}
      </div>
    </div>`;
  }).join("");

  // Update KPIs
  const total      = trainings.length;
  const inProgress = trainings.filter(t => t.status === "en cours").length;
  const done       = trainings.filter(t => t.status === "terminé").length;
  const totalEnroll= trainings.reduce((s, t) => s + (t.enrolled_count || 0), 0);
  if ($("trainKpiTotal"))      $("trainKpiTotal").textContent      = total;
  if ($("trainKpiInProgress")) $("trainKpiInProgress").textContent = inProgress;
  if ($("trainKpiDone"))       $("trainKpiDone").textContent       = done;
  if ($("trainKpiEnroll"))     $("trainKpiEnroll").textContent     = totalEnroll;
}

// ─────────────────────────────────────────────────────────────────────
// NOTIFICATIONS V2
// ─────────────────────────────────────────────────────────────────────

function renderNotificationsV2(notifs) {
  const wrap = $("notificationList");
  if (!wrap) return;

  // Update KPIs
  const total   = notifs.length;
  const unread  = notifs.filter(n => !n.is_read).length;
  const alerts  = notifs.filter(n => n.type === "warning" || n.type === "error").length;
  const success = notifs.filter(n => n.type === "success").length;
  if ($("notifKpiTotal"))   $("notifKpiTotal").textContent   = total;
  if ($("notifKpiUnread"))  $("notifKpiUnread").textContent  = unread;
  if ($("notifKpiAlerts"))  $("notifKpiAlerts").textContent  = alerts;
  if ($("notifKpiSuccess")) $("notifKpiSuccess").textContent = success;

  if (!notifs.length) {
    wrap.innerHTML = `<div class="empty-state"><i class="ri-notification-off-line"></i><h3>Aucune notification</h3><p>Tout est à jour.</p></div>`;
    return;
  }

  const iconMap = {
    info:            "ri-information-line",
    warning:         "ri-alarm-warning-line",
    success:         "ri-checkbox-circle-line",
    error:           "ri-close-circle-line",
    contract_expiry: "ri-file-warning-line",
    leave_pending:   "ri-calendar-todo-line",
  };
  wrap.className = "notif-list-v2";
  wrap.innerHTML = notifs.map(n => {
    const type    = n.type || "info";
    const icon    = iconMap[type] || "ri-notification-3-line";
    const timeStr = n.created_at ? new Date(n.created_at).toLocaleString("fr-FR", { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit" }) : "";
    return `
    <div class="notif-item-v2 ${n.is_read ? "" : "unread"} ${type}">
      <div class="notif-icon-v2 ${type}"><i class="${icon}"></i></div>
      <div class="notif-body-v2">
        <div class="notif-title-v2">${n.title || "Notification"}</div>
        <div class="notif-msg-v2">${n.message || ""}</div>
        ${timeStr ? `<div class="notif-time-v2"><i class="ri-time-line"></i> ${timeStr}</div>` : ""}
      </div>
      <div class="notif-actions-v2">
        ${!n.is_read ? `<button class="btn btn-secondary btn-sm" onclick="markNotifRead(${n.id})" title="Marquer lu"><i class="ri-check-line"></i></button>` : ""}
        <button class="btn btn-danger btn-sm" onclick="deleteNotif(${n.id})" title="Supprimer"><i class="ri-delete-bin-line"></i></button>
      </div>
    </div>`;
  }).join("");
}

function drawDeptChart(deptData = {}) {
  const labels = Object.keys(deptData);
  const values = Object.values(deptData);
  destroyChart("dept");
  const canvas = $("deptChart");
  if (!canvas) return;
  appState.charts.dept = new Chart(canvas, {
    type: "doughnut",
    data: {
      labels,
      datasets: [{ data: values, backgroundColor: chartColors(labels.length), borderWidth: 0, hoverOffset: 8 }]
    },
    options: {
      responsive: true,
      cutout: "65%",
      plugins: { legend: { position: "bottom", labels: { color: chartTickColor(), font: { size: 11 }, padding: 10 } } }
    }
  });
}

function drawLeaveChart(leaves = []) {
  const statusMap = leaves.reduce((acc, leave) => {
    acc[leave.status] = (acc[leave.status] || 0) + 1;
    return acc;
  }, {});
  destroyChart("leave");
  const canvas = $("leaveChart");
  if (!canvas) return;
  appState.charts.leave = new Chart(canvas, {
    type: "doughnut",
    data: {
      labels: Object.keys(statusMap),
      datasets: [{ data: Object.values(statusMap), backgroundColor: chartColors(Object.keys(statusMap).length), borderWidth: 0, hoverOffset: 8 }]
    },
    options: {
      responsive: true,
      cutout: "60%",
      plugins: { legend: { position: "bottom", labels: { color: chartTickColor(), font: { size: 11 } } } }
    }
  });
}

function renderTable(containerId, headers, rows) {
  const container = $(containerId);
  const head = `<tr>${headers.map((header) => `<th>${header}</th>`).join("")}</tr>`;
  const body = rows.length
    ? rows
        .map((row) => `<tr>${row.map((cell) => `<td>${cell ?? "-"}</td>`).join("")}</tr>`)
        .join("")
    : `<tr><td colspan="${headers.length}">Aucune donnée</td></tr>`;

  container.innerHTML = `<table><thead>${head}</thead><tbody>${body}</tbody></table>`;
}

function actionButtons(entity, id) {
  return `
    <div class="action-row">
      <button class="mini-btn" type="button" data-entity="${entity}" data-action="edit" data-id="${id}">Modifier</button>
      <button class="mini-btn" type="button" data-entity="${entity}" data-action="delete" data-id="${id}">Supprimer</button>
    </div>
  `;
}

function fillSelectOptions(selectId, options, includeEmpty = false) {
  const select = $(selectId);
  if (!select) return;

  const emptyOption = includeEmpty ? `<option value="">Non assigné</option>` : `<option value="">Sélectionner</option>`;
  select.innerHTML = `${emptyOption}${options
    .map((option) => `<option value="${option.value}">${option.label}</option>`)
    .join("")}`;
}

function employeeOptionLabel(employee) {
  return [
    `${employee.first_name} ${employee.last_name}`,
    employee.matricule || "N/A",
    employee.department || "Sans département",
    employee.role || "Sans rôle",
  ].join(" | ");
}

function accountOptionLabel(account) {
  return [
    account.employee_name || "Sans agent",
    account.username || "-",
    account.role || "Sans rôle",
    account.status || "Sans statut",
  ].join(" | ");
}

function messageRecipientOptionLabel(recipient) {
  return [
    recipient.name || "-",
    recipient.matricule || "N/A",
    recipient.department || "Sans département",
    recipient.role || "Sans rôle",
    recipient.username || "-",
  ].join(" | ");
}

function populateMessageRecipientSelect() {
  const select = $("newConversationRecipient");
  if (!select) return;

  const recipients = (appState.messageRecipients || []).filter((item) => Number(item.employee_id || 0) > 0);
  const options = recipients
    .map((recipient) => {
      const hasUserId = Number(recipient.user_id || 0) > 0;
      const value = hasUserId ? `u:${recipient.user_id}` : `e:${recipient.employee_id}`;
      return `<option value="${value}">${messageRecipientOptionLabel(recipient)}</option>`;
    })
    .join("");
  select.innerHTML = `<option value="">Choisir un agent...</option>${options}`;
}

function formatChatDateTime(value) {
  if (!value) return "";
  try {
    return new Date(value).toLocaleString("fr-FR", {
      day: "2-digit",
      month: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch (_error) {
    return "";
  }
}

function updateMessagesUnreadBadgeFromConversations(conversations = []) {
  const total = (conversations || []).reduce((acc, item) => acc + Number(item.unread_count || 0), 0);
  setMessagesUnreadBadgeCount(total);
}

function renderConversations(conversations = []) {
  const container = $("messagesConversations");
  if (!container) return;

  if (!conversations.length) {
    container.innerHTML = '<div class="perm-empty" style="padding: 12px;">Aucune discussion trouvée.</div>';
    return;
  }

  container.innerHTML = conversations
    .map((conversation) => {
      const isActive = Number(appState.activeChatUserId || 0) === Number(conversation.user_id || 0);
      const unread = Number(conversation.unread_count || 0);
      return `
        <button class="chat-conversation-item ${isActive ? "active" : ""}" type="button" data-chat-userid="${conversation.user_id}">
          <div class="chat-row-top">
            <span class="chat-name">${conversation.display_name || conversation.username || "Utilisateur"}</span>
            <span class="chat-time">${formatChatDateTime(conversation.last_message_at)}</span>
          </div>
          <div class="chat-row-bottom">
            <span class="chat-preview">${conversation.last_message || ""}</span>
            ${unread > 0 ? `<span class="chat-unread">${unread > 99 ? "99+" : unread}</span>` : ""}
          </div>
        </button>
      `;
    })
    .join("");
}

function renderChatThread(messages = []) {
  const container = $("chatMessages");
  if (!container) return;

  if (!messages.length) {
    appState.activeThreadMessages = [];
    appState.oldestThreadMessageId = null;
    appState.hasMoreThreadMessages = false;
    container.innerHTML = '<div class="perm-empty">Aucun message dans cette discussion.</div>';
    return;
  }

  const previousScrollHeight = container.scrollHeight;
  const previousScrollTop = container.scrollTop;

  container.innerHTML = messages
    .map((message, index) => {
      const isMe = String(message.sender_username || "") === String(appState.username || "");
      const canEdit = !!message.can_edit;
      const canDelete = !!message.can_delete;
      const actionButtons = isMe && (canEdit || canDelete)
        ? `
            <div class="chat-actions">
              ${canEdit ? `<button class="chat-action-btn" type="button" data-chat-action="edit" data-message-id="${message.id}">Modifier</button>` : ""}
              ${canDelete ? `<button class="chat-action-btn danger" type="button" data-chat-action="delete" data-message-id="${message.id}">Supprimer</button>` : ""}
            </div>
          `
        : "";
      const editedLabel = message.edited_at ? " • modifié" : "";
      if (index === 0 && appState.hasMoreThreadMessages) {
        return `
          <div class="chat-load-more-wrap">
            <button id="chatLoadMoreBtn" class="chat-load-more-btn" type="button">Charger les anciens messages</button>
          </div>
          <div class="chat-bubble ${isMe ? "me" : "them"}">
            <div>${message.content || ""}</div>
            ${actionButtons}
            <span class="chat-meta">${formatChatDateTime(message.sent_at)}${editedLabel}${isMe ? (message.is_read ? " • lu" : " • envoyé") : ""}</span>
          </div>
        `;
      }
      return `
        <div class="chat-bubble ${isMe ? "me" : "them"}">
          <div>${message.content || ""}</div>
          ${actionButtons}
          <span class="chat-meta">${formatChatDateTime(message.sent_at)}${editedLabel}${isMe ? (message.is_read ? " • lu" : " • envoyé") : ""}</span>
        </div>
      `;
    })
    .join("");

  if (appState.isLoadingOlderMessages) {
    const newScrollHeight = container.scrollHeight;
    container.scrollTop = previousScrollTop + (newScrollHeight - previousScrollHeight);
  } else {
    container.scrollTop = container.scrollHeight;
  }
}

function setActiveConversationInfo(conversation) {
  const title = $("chatTitle");
  const subtitle = $("chatSubtitle");
  if (!title || !subtitle) return;

  if (!conversation) {
    title.textContent = "Sélectionne une discussion";
    subtitle.textContent = "Aucun message chargé";
    return;
  }

  title.textContent = conversation.display_name || conversation.username || "Discussion";
  subtitle.textContent = conversation.username ? `@${conversation.username}` : "Discussion interne";
}

function normalizeSearchText(value) {
  return String(value || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

function employeeSuggestionLabel(employee) {
  return employeeOptionLabel(employee);
}

function syncSelectFromQuery(queryText, selectId) {
  const select = $(selectId);
  if (!select) return;

  const normalizedQuery = normalizeSearchText(queryText);
  if (!normalizedQuery) {
    select.value = "";
    return;
  }

  const options = Array.from(select.options).filter((option) => option.value);
  const exact = options.find((option) => normalizeSearchText(option.textContent) === normalizedQuery);
  if (exact) {
    select.value = exact.value;
    return;
  }

  if (options.length === 1) {
    select.value = options[0].value;
  }
}

function populateEmployeeQuerySuggestions() {
  const datalist = $("employeeSuggestionsList");
  if (!datalist) return;

  const labels = (appState.employees || []).map((employee) => employeeSuggestionLabel(employee));
  const uniqueLabels = Array.from(new Set(labels));
  datalist.innerHTML = uniqueLabels.map((label) => `<option value="${label}"></option>`).join("");
}

function populateAccountQuerySuggestions() {
  const datalist = $("accountSuggestionsList");
  if (!datalist) return;

  const labels = (appState.accounts || []).map((account) => accountOptionLabel(account));
  const uniqueLabels = Array.from(new Set(labels));
  datalist.innerHTML = uniqueLabels.map((label) => `<option value="${label}"></option>`).join("");
}

function getEmployeeDisplay(employeeId) {
  const employee = appState.employeeById[String(employeeId)];
  if (!employee) {
    return "Agent non trouvé";
  }
  return `${employee.first_name} ${employee.last_name}${employee.matricule ? ` (${employee.matricule})` : ""}`;
}

function setReportsContent(value) {
  const reportsInfo = $("reportsInfo");
  const reportsCards = $("reportsCards");
  const reportsDepartments = $("reportsDepartments");
  if (!reportsInfo || !reportsCards || !reportsDepartments) return;

  if (typeof value === "string") {
    reportsInfo.textContent = value;
    reportsInfo.classList.remove("hidden");
    reportsCards.innerHTML = "";
    reportsDepartments.innerHTML = "";
    return;
  }

  reportsInfo.classList.add("hidden");

  const totalPayroll = Number(value.total_payroll || 0);
  const averageSalary = Number(value.average_salary || 0);
  const absenceRate = Number(value.absence_rate || 0);
  const departmentEntries = Object.entries(value.employees_by_department || {});

  reportsCards.innerHTML = [
    { title: "Masse salariale", metric: formatMoney(totalPayroll) },
    { title: "Salaire moyen", metric: formatMoney(averageSalary) },
    { title: "Taux d'absence", metric: `${absenceRate}%` },
    { title: "Départements", metric: String(departmentEntries.length) },
  ]
    .map(
      (card) => `
        <article class="kpi-card glass">
          <h3>${card.title}</h3>
          <p>${card.metric}</p>
        </article>
      `
    )
    .join("");

  renderTable(
    "reportsDepartments",
    ["Département", "Nombre d'employés"],
    departmentEntries.map(([departmentName, employeeCount]) => [departmentName, employeeCount])
  );
}

async function loadReportsSection() {
  if (!can("Exporter rapports")) {
    setReportsContent("Reporting avancé réservé aux rôles avec permission 'Exporter rapports'.");
    return;
  }

  setReportsContent("Chargement des statistiques...");
  try {
    const stats = await api("/api/reports/stats");
    setReportsContent(stats);
  } catch (error) {
    setReportsContent(`Impossible de charger le reporting: ${error.message}`);
  }
}

function drawAccountingMonthlyChart(monthly = {}) {
  const canvas = $("accountingMonthlyChart");
  if (!canvas) return;

  if (appState.charts.accountingMonthly) {
    appState.charts.accountingMonthly.destroy();
  }

  const labels = monthly.labels || [];
  appState.charts.accountingMonthly = new Chart(canvas, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: "Brut",
          data: monthly.gross || [],
          borderColor: "rgba(33, 212, 253, 1)",
          backgroundColor: "rgba(33, 212, 253, .2)",
          tension: 0.3,
          fill: false,
        },
        {
          label: "Net",
          data: monthly.net || [],
          borderColor: "rgba(31, 222, 154, 1)",
          backgroundColor: "rgba(31, 222, 154, .2)",
          tension: 0.3,
          fill: false,
        },
        {
          label: "Impôts",
          data: monthly.taxes || [],
          borderColor: "rgba(255, 176, 32, 1)",
          backgroundColor: "rgba(255, 176, 32, .2)",
          tension: 0.3,
          fill: false,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { labels: { color: "#eaf0ff" } },
      },
      scales: {
        x: { ticks: { color: "#a9b5d6" }, grid: { color: "rgba(255,255,255,.08)" } },
        y: { ticks: { color: "#a9b5d6" }, grid: { color: "rgba(255,255,255,.08)" } },
      },
    },
  });
}

function drawAccountingCostChart(costStructure = {}) {
  const canvas = $("accountingCostChart");
  if (!canvas) return;

  if (appState.charts.accountingCost) {
    appState.charts.accountingCost.destroy();
  }

  appState.charts.accountingCost = new Chart(canvas, {
    type: "doughnut",
    data: {
      labels: costStructure.labels || [],
      datasets: [
        {
          data: costStructure.values || [],
          backgroundColor: ["#6d8dff", "#ffb020", "#ff5d7a", "#1fde9a"],
          borderWidth: 0,
        },
      ],
    },
    options: {
      plugins: {
        legend: { labels: { color: "#eaf0ff" } },
      },
    },
  });
}

function drawAccountingDepartmentsChart(departmentNet = {}) {
  const canvas = $("accountingDepartmentsChart");
  if (!canvas) return;

  if (appState.charts.accountingDepartments) {
    appState.charts.accountingDepartments.destroy();
  }

  appState.charts.accountingDepartments = new Chart(canvas, {
    type: "bar",
    data: {
      labels: departmentNet.labels || [],
      datasets: [
        {
          label: "Net par département",
          data: departmentNet.values || [],
          backgroundColor: "rgba(109, 141, 255, .65)",
          borderColor: "rgba(109, 141, 255, 1)",
          borderWidth: 1,
          borderRadius: 8,
        },
      ],
    },
    options: {
      responsive: true,
      indexAxis: "y",
      plugins: {
        legend: { labels: { color: "#eaf0ff" } },
      },
      scales: {
        x: { ticks: { color: "#a9b5d6" }, grid: { color: "rgba(255,255,255,.08)" } },
        y: { ticks: { color: "#a9b5d6" }, grid: { color: "rgba(255,255,255,.08)" } },
      },
    },
  });
}

function setAccountingContent(value) {
  const accountingInfo = $("accountingInfo");
  const accountingCards = $("accountingCards");
  if (!accountingInfo || !accountingCards) return;

  if (typeof value === "string") {
    accountingInfo.textContent = value;
    accountingInfo.classList.remove("hidden");
    accountingCards.innerHTML = "";
    renderTable("accountingDepartmentsTable", ["Département", "Net"], []);
    return;
  }

  const totals = value.totals || {};
  const monthly = value.monthly || {};
  const departmentNet = value.department_net || {};
  const costStructure = value.cost_structure || {};

  accountingInfo.classList.add("hidden");
  accountingCards.innerHTML = [
    { title: "Masse salariale brute", metric: formatMoney(totals.gross_payroll || 0) },
    { title: "Masse salariale nette", metric: formatMoney(totals.net_payroll || 0) },
    { title: "Total impôts", metric: formatMoney(totals.taxes || 0) },
    { title: "Total déductions", metric: formatMoney(totals.deductions || 0) },
    { title: "Total primes", metric: formatMoney(totals.bonuses || 0) },
    { title: "Heures supplémentaires", metric: String(totals.overtime_hours || 0) },
  ]
    .map(
      (card) => `
        <article class="kpi-card glass">
          <h3>${card.title}</h3>
          <p>${card.metric}</p>
        </article>
      `
    )
    .join("");

  drawAccountingMonthlyChart(monthly);
  drawAccountingCostChart(costStructure);
  drawAccountingDepartmentsChart(departmentNet);

  renderTable(
    "accountingDepartmentsTable",
    ["Département", "Net"],
    (departmentNet.labels || []).map((departmentName, index) => [departmentName, formatMoney((departmentNet.values || [])[index] || 0)])
  );
}

async function loadAccountingSection() {
  if (!can("Voir comptabilité")) {
    setAccountingContent("Espace comptabilité réservé aux rôles avec permission 'Voir comptabilité'.");
    return;
  }

  setAccountingContent("Chargement des indicateurs comptables...");
  try {
    const stats = await api("/api/reports/accounting");
    setAccountingContent(stats);
  } catch (error) {
    setAccountingContent(`Impossible de charger la comptabilité: ${error.message}`);
  }
}

function populateEmployeeActionSelects() {
  const configs = [
    { selectId: "payrollEmployeeId", queryId: "payrollEmployeeQuery" },
    { selectId: "attendanceEmployeeId", queryId: "attendanceEmployeeQuery" },
    { selectId: "leaveEmployeeId", queryId: "leaveEmployeeQuery" },
    { selectId: "contractEmployeeId", queryId: "contractEmployeeQuery" },
  ];

  configs.forEach(({ selectId, queryId }) => {
    const queryText = ($(queryId)?.value || "").trim();
    const query = normalizeSearchText(queryText);
    const options = (appState.employees || [])
      .filter((employee) => {
        if (!query) return true;
        const haystack = [
          `${employee.first_name} ${employee.last_name}`,
          employee.matricule || "",
          employee.department || "",
          employee.role || "",
        ]
          .join(" ")
          .normalize("NFD")
          .replace(/[\u0300-\u036f]/g, "")
          .toLowerCase();
        return haystack.includes(query);
      })
      .map((employee) => ({
        value: employee.id,
        label: employeeOptionLabel(employee),
      }));

    fillSelectOptions(selectId, options, false);
    syncSelectFromQuery(queryText, selectId);
  });

  populateEmployeeQuerySuggestions();
}

function populateAccountActionSelect() {
  const queryText = ($("accountUserQuery")?.value || "").trim();
  const query = normalizeSearchText(queryText);
  const options = (appState.accounts || [])
    .filter((account) => {
      if (!query) return true;
      const haystack = [
        account.employee_name || "",
        account.username || "",
        account.matricule || "",
        account.role || "",
        account.status || "",
      ]
        .join(" ")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase();
      return haystack.includes(query);
    })
    .map((account) => ({
      value: account.id,
      label: accountOptionLabel(account),
    }));
  fillSelectOptions("accountUserId", options, false);
  syncSelectFromQuery(queryText, "accountUserId");
  populateAccountQuerySuggestions();
}

function renderPermissionChecklist(containerId, permissions = [], selectedValues = []) {
  const container = $(containerId);
  if (!container) return;

  if (!permissions || permissions.length === 0) {
    container.innerHTML = '<div class="perm-empty">Aucune permission disponible.</div>';
    return;
  }

  const selected = new Set(selectedValues || []);
  container.innerHTML = (permissions || [])
    .map(
      (permissionName) => `
        <label class="perm-item">
          <input type="checkbox" value="${permissionName}" ${selected.has(permissionName) ? "checked" : ""} />
          <span>${permissionName}</span>
        </label>
      `
    )
    .join("");
}

function getCheckedPermissions(containerId) {
  const container = $(containerId);
  if (!container) return [];
  return Array.from(container.querySelectorAll('input[type="checkbox"]:checked')).map((checkbox) => checkbox.value);
}

function setCheckedPermissions(containerId, values = []) {
  const container = $(containerId);
  if (!container) return;
  const selectedValues = new Set(values || []);
  container.querySelectorAll('input[type="checkbox"]').forEach((checkbox) => {
    checkbox.checked = selectedValues.has(checkbox.value);
  });
}

async function loadOverviewLegacy() {
  const [employees, leaves, departments, payrolls, attendances, stats] = await Promise.all([
    can("Voir employés") ? api("/api/employees") : Promise.resolve([]),
    can("Voir employés") ? api("/api/leaves") : Promise.resolve([]),
    can("Voir employés") ? api("/api/departments") : Promise.resolve([]),
    can("Voir salaires") ? api("/api/payrolls") : Promise.resolve([]),
    can("Voir employés") ? api("/api/attendances") : Promise.resolve([]),
    can("Exporter rapports") ? api("/api/reports/stats") : Promise.resolve(null),
  ]);

  setReportsContent(
    stats || "Reporting avancé réservé aux rôles avec permission 'Exporter rapports'."
  );

  const totalPayroll = stats ? stats.total_payroll : payrolls.reduce((acc, payroll) => acc + Number(payroll.net_salary || 0), 0);
  const averageSalary = stats
    ? stats.average_salary
    : payrolls.length
    ? totalPayroll / payrolls.length
    : 0;
  const absenceRate = stats
    ? stats.absence_rate
    : attendances.length
    ? ((attendances.filter((attendance) => attendance.is_absent).length / attendances.length) * 100).toFixed(2)
    : 0;

  const deptMap = stats
    ? stats.employees_by_department || {}
    : departments.reduce((acc, department) => {
        acc[department.name] = (department.employees || []).length;
        return acc;
      }, {});

  if ($("kpiPayroll")) $("kpiPayroll").textContent = can("Voir salaires") ? formatMoney(totalPayroll || 0) : "-";
  if ($("kpiAvgSalary")) $("kpiAvgSalary").textContent = can("Voir salaires") ? formatMoney(averageSalary || 0) : "-";
  if ($("kpiAbsence")) $("kpiAbsence").textContent = can("Voir employés") ? `${absenceRate || 0}%` : "-";
  if ($("kpiEmployees")) $("kpiEmployees").textContent = can("Voir employés") ? String(employees.length) : "-";

  drawDeptChart(deptMap);
  drawLeaveChart(leaves);
}

async function loadEmployees() {
  if (!can("Voir employés")) {
    return;
  }
  const employees = await api("/api/employees");
  appState.employees = employees || [];
  appState.employeeById = (appState.employees || []).reduce((acc, employee) => {
    acc[String(employee.id)] = employee;
    return acc;
  }, {});
  populateEmployeeActionSelects();
  // Update stats badges & dept filter
  updateEmpStats(appState.employees);
  // Render via filter function (respects active filters)
  filterEmployeesUI();
  // Also pre-render cards for quick toggle
  renderEmployeeCards(appState.employees);
}

async function loadDepartments() {
  if (!can("Voir employés")) {
    return;
  }
  const departments = await api("/api/departments");
  fillSelectOptions(
    "employeeDepartmentSelect",
    departments.map((department) => ({ value: department.id, label: `${department.name} (#${department.id})` })),
    true
  );
  const canModifyEmployees = can("Modifier employés");
  renderTable(
    "departmentsTable",
    canModifyEmployees ? ["ID", "Nom", "Budget", "Manager", "Nb employés", "Actions"] : ["ID", "Nom", "Budget", "Manager", "Nb employés"],
    departments.map((department) => [
      department.id,
      department.name,
      formatMoney(department.budget),
      department.manager_id || "-",
      (department.employees || []).length,
      ...(canModifyEmployees ? [actionButtons("department", department.id)] : []),
    ])
  );
}

async function editEmployee(employeeId) {
  const employee = (appState.employees || []).find((entry) => entry.id === employeeId);
  if (!employee) {
    notify("Employé introuvable", true);
    return;
  }

  const payload = await openEditModal({
    title: "Modifier employé",
    fields: [
      { name: "first_name", label: "Prénom", value: employee.first_name || "", required: true },
      { name: "last_name", label: "Nom", value: employee.last_name || "", required: true },
      { name: "email", label: "Email", type: "email", value: employee.email || "", required: true },
      { name: "phone", label: "Téléphone", value: employee.phone || "" },
      { name: "address", label: "Adresse", value: employee.address || "" },
      {
        name: "status",
        label: "Statut",
        type: "select",
        value: employee.status || "Actif",
        options: [
          { value: "Actif", label: "Actif" },
          { value: "Suspendu", label: "Suspendu" },
          { value: "Démissionné", label: "Démissionné" },
        ],
        required: true,
      },
    ],
  });
  if (!payload) return;

  await api(`/api/employees/${employeeId}`, {
    method: "PUT",
    body: JSON.stringify({
      first_name: payload.first_name,
      last_name: payload.last_name,
      email: payload.email,
      phone: payload.phone,
      address: payload.address,
      status: payload.status,
      department_id: employee.department_id,
      role_id: employee.role_id,
    }),
  });

  notify("Employé modifié");
  await Promise.all([loadEmployees(), loadOverview(), loadAccounts()]);
}

async function deleteEmployee(employeeId) {
  const accepted = await confirmAction({
    title: "Supprimer employé",
    message: "Confirmer la suppression de cet employé ?",
    confirmLabel: "Supprimer",
  });
  if (!accepted) {
    return;
  }

  await api(`/api/employees/${employeeId}`, {
    method: "DELETE",
  });

  notify("Employé supprimé");
  await Promise.all([loadEmployees(), loadOverview(), loadAccounts(), loadDepartments()]);
}

async function editDepartment(departmentId) {
  const departments = await api("/api/departments");
  const department = (departments || []).find((entry) => entry.id === departmentId);
  if (!department) {
    notify("Département introuvable", true);
    return;
  }

  const payload = await openEditModal({
    title: "Modifier département",
    fields: [
      { name: "name", label: "Nom du département", value: department.name || "", required: true },
      { name: "budget", label: "Budget", type: "number", value: department.budget ?? 0, step: "0.01", required: true },
    ],
  });
  if (!payload) return;

  await api(`/api/departments/${departmentId}`, {
    method: "PUT",
    body: JSON.stringify({
      name: payload.name,
      budget: payload.budget,
      manager_id: department.manager_id,
    }),
  });

  notify("Département modifié");
  await Promise.all([loadDepartments(), loadOverview(), loadEmployees()]);
}

async function deleteDepartment(departmentId) {
  const accepted = await confirmAction({
    title: "Supprimer département",
    message: "Confirmer la suppression de ce département ?",
    confirmLabel: "Supprimer",
  });
  if (!accepted) {
    return;
  }

  await api(`/api/departments/${departmentId}`, {
    method: "DELETE",
  });

  notify("Département supprimé");
  await Promise.all([loadDepartments(), loadOverview(), loadEmployees()]);
}

async function loadRoles() {
  if (!(can("Voir employés") && ["SuperAdmin", "Admin RH", "RH"].includes(appState.role))) {
    return;
  }
  const roles = await api("/api/roles");
  let permissions = [];
  try {
    permissions = await api("/api/roles/permissions");
  } catch (_error) {
    permissions = [];
  }
  appState.roles = roles || [];

  const permissionsFromRoles = (roles || []).flatMap((role) => role.permissions || []);
  const availablePermissions = Array.from(
    new Set([...(permissions || []), ...DEFAULT_PERMISSION_NAMES, ...permissionsFromRoles])
  ).sort((left, right) => left.localeCompare(right, "fr", { sensitivity: "base" }));

  renderPermissionChecklist("rolePermissionsChecklist", availablePermissions, []);

  fillSelectOptions(
    "employeeRoleSelect",
    roles.map((role) => ({ value: role.id, label: `${role.name} (#${role.id})` })),
    false
  );
  fillSelectOptions(
    "accountRoleId",
    roles.map((role) => ({ value: role.id, label: `${role.name} (#${role.id})` })),
    false
  );

  fillSelectOptions(
    "rolePermissionRoleId",
    roles.map((role) => ({ value: role.id, label: `${role.name} (#${role.id})` })),
    false
  );

  const selectedRoleId = Number($("rolePermissionRoleId")?.value || 0);
  if (selectedRoleId) {
    const currentRole = appState.roles.find((role) => role.id === selectedRoleId);
    renderPermissionChecklist("updateRolePermissionsChecklist", availablePermissions, currentRole?.permissions || []);
  } else {
    renderPermissionChecklist("updateRolePermissionsChecklist", availablePermissions, []);
  }

  renderTable(
    "rolesTable",
    ["ID", "Rôle", "Permissions"],
    roles.map((role) => [role.id, role.name, (role.permissions || []).join(", ")])
  );
}

async function updateRolePermissions() {
  const roleId = Number($("rolePermissionRoleId")?.value || 0);
  const permissionNames = getCheckedPermissions("updateRolePermissionsChecklist");

  if (!roleId) {
    notify("Sélectionne un rôle", true);
    return;
  }

  await api(`/api/roles/${roleId}/permissions`, {
    method: "PATCH",
    body: JSON.stringify({ permission_names: permissionNames }),
  });

  notify("Permissions du rôle mises à jour");
  await Promise.all([loadRoles(), loadEmployees(), loadAccounts()]);
}

async function loadPayrolls() {
  if (!can("Voir salaires")) {
    return;
  }
  const payrolls = await api("/api/payrolls");
  // Update stats badges
  updatePayrollStats(payrolls || []);
  const canManage = can("Voir salaires");
  renderTable(
    "payrollsTable",
    canManage
      ? ["ID", "Employé", "Mois", "Base", "Prime", "Déductions", "Impôts", "Net", "Date", "Actions"]
      : ["ID", "Employé", "Mois", "Base", "Prime", "Déductions", "Impôts", "Net", "Date"],
    payrolls.map((payroll) => [
      payroll.id,
      payroll.employee_name,
      payroll.payroll_month || "-",
      formatMoney(payroll.base_salary),
      formatMoney(payroll.bonus),
      formatMoney(payroll.deductions),
      formatMoney(payroll.taxes),
      formatMoney(payroll.net_salary),
      payroll.paid_at ? new Date(payroll.paid_at).toLocaleString("fr-FR") : "—",
      ...(canManage ? [`<button class="btn btn-secondary btn-sm" onclick="openPayslipModal(${payroll.id})" title="Fiche de paie"><i class="ri-file-text-line"></i></button>${actionButtons("payroll", payroll.id)}`] : []),
    ])
  );
}

async function loadAttendances() {
  if (!can("Voir employés")) {
    return;
  }
  const attendances = await api("/api/attendances");
  const canManage = can("Voir employés");
  renderTable(
    "attendancesTable",
    canManage
      ? ["ID", "Employé", "Entrée", "Sortie", "Heures", "Retard", "Absence", "Actions"]
      : ["ID", "Employé", "Entrée", "Sortie", "Heures", "Retard", "Absence"],
    attendances.map((attendance) => [
      attendance.id,
      getEmployeeDisplay(attendance.employee_id),
      new Date(attendance.check_in).toLocaleString("fr-FR"),
      attendance.check_out ? new Date(attendance.check_out).toLocaleString("fr-FR") : "-",
      attendance.worked_hours,
      attendance.late_minutes,
      attendance.is_absent ? "Oui" : "Non",
      ...(canManage ? [actionButtons("attendance", attendance.id)] : []),
    ])
  );
}

async function loadAttendanceMonthlySummary(month) {
  if (!month) {
    throw new Error("Sélectionne un mois");
  }

  const summary = await api(`/api/attendances/summary/monthly?month=${encodeURIComponent(month)}`);
  renderTable(
    "attendanceSummaryTable",
    ["Employé", "Mois", "Présences", "Absences", "Absences non justifiées"],
    (summary || []).map((item) => [
      item.employee_name,
      item.month,
      item.presence_days,
      item.absence_days,
      item.unjustified_absence_days,
    ])
  );
}

async function loadLeaves() {
  // Allow all authenticated users to request and view their own leaves.
  // Server filters results: HR (permission 'Valider congés') will receive all leaves.
  const leaves = await api("/api/leaves");
  // Update stats badges & approval queue
  updateLeaveStats(leaves || []);
  const canManage = can("Valider congés");
  renderTable(
    "leavesTable",
    canManage ? ["ID", "Employé", "Période", "Motif", "Statut", "Actions"] : ["ID", "Employé", "Période", "Motif", "Statut"],
    leaves.map((leave) => [
      leave.id,
      getEmployeeDisplay(leave.employee_id),
      `${leave.start_date} → ${leave.end_date}`,
      leave.reason,
      leave.status,
      ...(canManage ? [actionButtons("leave", leave.id)] : []),
    ])
  );
}

async function loadContracts() {
  if (!can("Voir employés")) {
    return;
  }
  const contracts = await api("/api/contracts");
  // Update stats badges & expiry alert
  updateContractStats(contracts || []);
  const canManage = can("Modifier employés");
  renderTable(
    "contractsTable",
    canManage
      ? ["ID", "Employé", "Type", "Début", "Fin", "Salaire", "Actions"]
      : ["ID", "Employé", "Type", "Début", "Fin", "Salaire"],
    contracts.map((contract) => [
      contract.id,
      getEmployeeDisplay(contract.employee_id),
      contract.contract_type,
      contract.start_date,
      contract.end_date || "-",
      formatMoney(contract.contractual_salary),
      ...(canManage ? [actionButtons("contract", contract.id)] : []),
    ])
  );
}

async function editPayroll(payrollId) {
  const payrolls = await api("/api/payrolls");
  const payroll = (payrolls || []).find((entry) => entry.id === payrollId);
  if (!payroll) throw new Error("Paie introuvable");

  const payload = await openEditModal({
    title: "Modifier paie",
    fields: [
      { name: "bonus", label: "Prime", type: "number", value: payroll.bonus ?? 0, step: "0.01", required: true },
      { name: "deductions", label: "Déductions", type: "number", value: payroll.deductions ?? 0, step: "0.01", required: true },
      { name: "taxes", label: "Impôts", type: "number", value: payroll.taxes ?? 0, step: "0.01", required: true },
    ],
  });
  if (!payload) return;

  await api(`/api/payrolls/${payrollId}`, {
    method: "PUT",
    body: JSON.stringify({
      bonus: payload.bonus,
      deductions: payload.deductions,
      taxes: payload.taxes,
    }),
  });

  notify("Paie modifiée");
  await Promise.all([loadPayrolls(), loadOverview()]);
}

async function deletePayroll(payrollId) {
  const accepted = await confirmAction({
    title: "Supprimer paie",
    message: "Confirmer la suppression de cette paie ?",
    confirmLabel: "Supprimer",
  });
  if (!accepted) return;
  await api(`/api/payrolls/${payrollId}`, { method: "DELETE" });
  notify("Paie supprimée");
  await Promise.all([loadPayrolls(), loadOverview()]);
}

async function editAttendance(attendanceId) {
  const attendances = await api("/api/attendances");
  const attendance = (attendances || []).find((entry) => entry.id === attendanceId);
  if (!attendance) throw new Error("Pointage introuvable");

  const payload = await openEditModal({
    title: "Modifier pointage",
    fields: [
      { name: "late_minutes", label: "Retard (minutes)", type: "number", value: attendance.late_minutes ?? 0, min: 0, required: true },
      {
        name: "is_absent",
        label: "Absence non justifiée",
        type: "select",
        value: attendance.is_absent ? "oui" : "non",
        options: [
          { value: "non", label: "Non" },
          { value: "oui", label: "Oui" },
        ],
        required: true,
      },
    ],
  });
  if (!payload) return;

  await api(`/api/attendances/${attendanceId}`, {
    method: "PUT",
    body: JSON.stringify({
      late_minutes: payload.late_minutes,
      is_absent: normalizeSearchText(payload.is_absent) === "oui",
    }),
  });

  notify("Pointage modifié");
  await Promise.all([loadAttendances(), loadOverview()]);
}

async function deleteAttendance(attendanceId) {
  const accepted = await confirmAction({
    title: "Supprimer pointage",
    message: "Confirmer la suppression de ce pointage ?",
    confirmLabel: "Supprimer",
  });
  if (!accepted) return;
  await api(`/api/attendances/${attendanceId}`, { method: "DELETE" });
  notify("Pointage supprimé");
  await Promise.all([loadAttendances(), loadOverview()]);
}

async function editLeave(leaveId) {
  const leaves = await api("/api/leaves");
  const leave = (leaves || []).find((entry) => entry.id === leaveId);
  if (!leave) throw new Error("Congé introuvable");

  const payload = await openEditModal({
    title: "Modifier congé",
    fields: [
      {
        name: "status",
        label: "Statut",
        type: "select",
        value: leave.status || "En attente",
        options: [
          { value: "En attente", label: "En attente" },
          { value: "Approuvé", label: "Approuvé" },
          { value: "Rejeté", label: "Rejeté" },
        ],
        required: true,
      },
      {
        name: "decision_comment",
        label: "Justification (optionnel)",
        type: "textarea",
        value: leave.decision_comment || "",
        placeholder: "Ajouter une justification (ex: raison du refus)",
      },
    ],
  });
  if (!payload) return;

  await api(`/api/leaves/${leaveId}`, {
    method: "PUT",
    body: JSON.stringify({ status: payload.status, decision_comment: payload.decision_comment }),
  });
  notify("Congé mis à jour");
  await Promise.all([loadLeaves(), loadOverview()]);
}

async function deleteLeave(leaveId) {
  const accepted = await confirmAction({
    title: "Supprimer congé",
    message: "Confirmer la suppression de ce congé ?",
    confirmLabel: "Supprimer",
  });
  if (!accepted) return;
  await api(`/api/leaves/${leaveId}`, { method: "DELETE" });
  notify("Congé supprimé");
  await Promise.all([loadLeaves(), loadOverview()]);
}

async function editContract(contractId) {
  const contracts = await api("/api/contracts");
  const contract = (contracts || []).find((entry) => entry.id === contractId);
  if (!contract) throw new Error("Contrat introuvable");

  const payload = await openEditModal({
    title: "Modifier contrat",
    fields: [
      {
        name: "contractual_salary",
        label: "Salaire contractuel",
        type: "number",
        value: contract.contractual_salary ?? 0,
        step: "0.01",
        min: 0,
        required: true,
      },
    ],
  });
  if (!payload) return;

  await api(`/api/contracts/${contractId}`, {
    method: "PUT",
    body: JSON.stringify({ contractual_salary: payload.contractual_salary }),
  });
  notify("Contrat modifié");
  await Promise.all([loadContracts(), loadOverview()]);
}

async function deleteContract(contractId) {
  const accepted = await confirmAction({
    title: "Supprimer contrat",
    message: "Confirmer la suppression de ce contrat ?",
    confirmLabel: "Supprimer",
  });
  if (!accepted) return;
  await api(`/api/contracts/${contractId}`, { method: "DELETE" });
  notify("Contrat supprimé");
  await Promise.all([loadContracts(), loadOverview()]);
}

async function loadAccounts() {
  if (!(can("Modifier employés") && ["SuperAdmin", "Admin RH", "RH"].includes(appState.role))) {
    return;
  }
  const accounts = await api("/api/accounts");
  appState.accounts = accounts || [];
  populateAccountActionSelect();
  renderTable(
    "accountsTable",
    ["ID", "Username", "Agent", "Matricule", "Rôle", "Statut", "Reset requis"],
    accounts.map((account) => [
      account.id,
      account.username,
      account.employee_name || "-",
      account.matricule || "-",
      account.role || "-",
      account.status || "-",
      account.must_change_password ? "Oui" : "Non",
    ])
  );
}

function updateMessagesUnreadBadge(messages = []) {
  const badge = $("messagesUnreadBadge");
  if (!badge) return;

  const unreadCount = (messages || []).filter((message) => !message.is_read).length;
  if (unreadCount <= 0) {
    badge.classList.add("hidden");
    badge.textContent = "0";
    return;
  }

  badge.textContent = unreadCount > 99 ? "99+" : String(unreadCount);
  badge.classList.remove("hidden");
}

function setMessagesUnreadBadgeCount(unreadCount) {
  const badge = $("messagesUnreadBadge");
  const dot   = $("topbarMsgDot");
  const count = Number(unreadCount || 0);
  if (badge) {
    if (count <= 0) { badge.classList.add("hidden"); badge.textContent = "0"; }
    else { badge.textContent = count > 99 ? "99+" : String(count); badge.classList.remove("hidden"); }
  }
  if (dot) dot.classList.toggle("hidden", count === 0);
}

function isMessagesSectionActive() {
  const section = $("section-messages");
  return !!section && section.classList.contains("active");
}

function isAccountingSectionActive() {
  const section = $("section-accounting");
  return !!section && section.classList.contains("active");
}

async function loadMessageRecipients() {
  const recipients = await api("/api/messages/recipients");
  appState.messageRecipients = recipients || [];
  populateMessageRecipientSelect();
}

async function loadConversations(query = "") {
  const conversations = await api(`/api/messages/conversations?q=${encodeURIComponent(query || "")}`);
  appState.conversations = conversations || [];
  updateMessagesUnreadBadgeFromConversations(appState.conversations);
  renderConversations(appState.conversations);
}

async function loadConversationThread(userId, options = {}) {
  const { beforeId = null } = options;
  if (!userId) {
    renderChatThread([]);
    return;
  }

  const limit = 40;
  const queryParams = new URLSearchParams({ limit: String(limit) });
  if (beforeId) {
    queryParams.set("before_id", String(beforeId));
  }

  const messages = await api(`/api/messages/thread/${userId}?${queryParams.toString()}`);
  const chunk = messages || [];

  if (beforeId) {
    appState.activeThreadMessages = [...chunk, ...(appState.activeThreadMessages || [])];
  } else {
    appState.activeThreadMessages = chunk;
  }

  const firstMessage = (appState.activeThreadMessages || [])[0];
  appState.oldestThreadMessageId = firstMessage ? Number(firstMessage.id) : null;
  appState.hasMoreThreadMessages = chunk.length >= limit && !!appState.oldestThreadMessageId;
  renderChatThread(appState.activeThreadMessages || []);
}

async function loadOlderThreadMessages() {
  if (!appState.activeChatUserId || !appState.hasMoreThreadMessages || appState.isLoadingOlderMessages) {
    return;
  }

  appState.isLoadingOlderMessages = true;
  const button = $("chatLoadMoreBtn");
  if (button) {
    button.disabled = true;
    button.textContent = "Chargement...";
  }

  try {
    await loadConversationThread(appState.activeChatUserId, { beforeId: appState.oldestThreadMessageId });
  } finally {
    appState.isLoadingOlderMessages = false;
  }
}

async function loadMessagesUnreadCount() {
  const result = await api("/api/messages/unread-count");
  setMessagesUnreadBadgeCount(result?.unread_count || 0);
}

async function refreshMessagesSilently() {
  try {
    if (isMessagesSectionActive()) {
      const query = ($("messagesSearch")?.value || "").trim();
      await loadConversations(query);
      if (appState.activeChatUserId) {
        await loadConversationThread(appState.activeChatUserId);
      }
    } else {
      await loadMessagesUnreadCount();
    }
  } catch (_error) {}
}

function stopMessagesAutoRefresh() {
  if (appState.messagesAutoRefreshTimer) {
    clearInterval(appState.messagesAutoRefreshTimer);
    appState.messagesAutoRefreshTimer = null;
  }
}

function startMessagesAutoRefresh() {
  stopMessagesAutoRefresh();
  appState.messagesAutoRefreshTimer = setInterval(() => {
    if (!appState.token || appState.mustChangePassword) {
      return;
    }
    refreshMessagesSilently();
  }, 30000);
}

async function openConversation(userId) {
  const conversationId = Number(userId || 0);
  if (!conversationId) return;
  appState.activeChatUserId = conversationId;
  appState.activeChatRecipientEmployeeId = null;

  renderConversations(appState.conversations || []);
  const selectedConversation = (appState.conversations || []).find((item) => Number(item.user_id) === conversationId);
  setActiveConversationInfo(selectedConversation || null);
  await loadConversationThread(conversationId);

  const query = ($("messagesSearch")?.value || "").trim();
  await loadConversations(query);
}

async function startNewConversation() {
  const select = $("newConversationRecipient");
  if (!select) return;

  const selectedValue = String(select.value || "").trim();
  if (!selectedValue) {
    throw new Error("Sélectionne un agent pour démarrer la discussion");
  }

  const [kind, rawId] = selectedValue.split(":");
  const parsedId = Number(rawId || 0);
  if (!parsedId) {
    throw new Error("Sélection invalide");
  }

  const recipient = (appState.messageRecipients || []).find((item) => {
    if (kind === "u") {
      return Number(item.user_id || 0) === parsedId;
    }
    return Number(item.employee_id || 0) === parsedId;
  });

  if (!recipient) {
    throw new Error("Destinataire introuvable");
  }

  const userId = Number(recipient.user_id || 0);
  const employeeId = Number(recipient.employee_id || 0);

  if (userId) {
    const existingConversation = (appState.conversations || []).find((item) => Number(item.user_id) === userId);
    if (existingConversation) {
      await openConversation(userId);
      return;
    }

    appState.activeChatUserId = userId;
    appState.activeChatRecipientEmployeeId = null;
  } else {
    appState.activeChatUserId = null;
    appState.activeChatRecipientEmployeeId = employeeId || null;
  }
  appState.activeThreadMessages = [];
  appState.oldestThreadMessageId = null;
  appState.hasMoreThreadMessages = false;

  setActiveConversationInfo(
    recipient
      ? {
          user_id: userId || null,
          username: recipient.username,
          display_name: recipient.name,
        }
      : {
          user_id: userId,
          display_name: "Nouvelle discussion",
        }
  );
  renderConversations(appState.conversations || []);
  renderChatThread([]);
  $("chatMessageInput")?.focus();
}

async function editOwnMessage(messageId) {
  const id = Number(messageId || 0);
  if (!id) return;

  const message = (appState.activeThreadMessages || []).find((item) => Number(item.id) === id);
  if (!message) {
    throw new Error("Message introuvable");
  }

  if (!message.can_edit) {
    throw new Error("Le délai de modification est dépassé");
  }

  const payload = await openEditModal({
    title: "Modifier le message",
    submitLabel: "Mettre à jour",
    fields: [
      {
        name: "content",
        label: "Message",
        type: "text",
        value: message.content || "",
        required: true,
      },
    ],
  });

  if (!payload) return;
  await api(`/api/messages/${id}`, {
    method: "PATCH",
    body: JSON.stringify({ content: payload.content }),
  });

  if (appState.activeChatUserId) {
    await openConversation(appState.activeChatUserId);
  }
}

async function deleteOwnMessage(messageId) {
  const id = Number(messageId || 0);
  if (!id) return;

  const message = (appState.activeThreadMessages || []).find((item) => Number(item.id) === id);
  if (!message) {
    throw new Error("Message introuvable");
  }

  if (!message.can_delete) {
    throw new Error("Le délai de suppression est dépassé");
  }

  const confirmed = await confirmAction({
    title: "Supprimer le message",
    message: "Ce message sera supprimé définitivement. Continuer ?",
    confirmLabel: "Supprimer",
  });
  if (!confirmed) return;

  await api(`/api/messages/${id}`, { method: "DELETE" });
  if (appState.activeChatUserId) {
    await openConversation(appState.activeChatUserId);
  }
}

async function loadAccountLogs() {
  if (!(can("Modifier employés") && ["SuperAdmin", "Admin RH", "RH"].includes(appState.role))) {
    return;
  }

  const query = buildLogFiltersQuery();
  const logs = await api(`/api/accounts/activity${query ? `?${query}` : ""}`);
  renderTable(
    "accountLogsTable",
    ["ID", "Utilisateur", "Action", "Date"],
    logs.map((log) => [
      log.id,
      log.username,
      log.action,
      new Date(log.created_at).toLocaleString("fr-FR"),
    ])
  );
}

function buildLogFiltersQuery() {
  const username = ($("logUsername")?.value || "").trim();
  const action = ($("logAction")?.value || "").trim();
  const startDate = ($("logStartDate")?.value || "").trim();
  const endDate = ($("logEndDate")?.value || "").trim();

  const params = new URLSearchParams();
  if (username) params.set("username", username);
  if (action) params.set("action", action);
  if (startDate) params.set("start_date", startDate);
  if (endDate) params.set("end_date", endDate);

  return params.toString();
}

async function exportAccountLogs(format) {
  if (!(can("Modifier employés") && ["SuperAdmin", "Admin RH", "RH"].includes(appState.role))) {
    notify("Accès refusé", true);
    return;
  }

  const query = buildLogFiltersQuery();
  const endpoint = `/api/accounts/activity/export.${format}${query ? `?${query}` : ""}`;

  const response = await fetch(endpoint, {
    headers: {
      Authorization: `Bearer ${appState.token}`,
    },
  });

  if (!response.ok) {
    let errorMessage = `HTTP ${response.status}`;
    try {
      const data = await response.json();
      errorMessage = data.error || data.message || errorMessage;
    } catch (_error) {}
    throw new Error(errorMessage);
  }

  const blob = await response.blob();
  const objectUrl = window.URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = objectUrl;
  anchor.download = `activity_logs.${format}`;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  window.URL.revokeObjectURL(objectUrl);
}

async function refreshAll() {
  if (appState.mustChangePassword) {
    return;
  }
  const messageQuery = ($("messagesSearch")?.value || "").trim();
  const jobs = [loadOverview(), loadLeaves(), loadConversations(messageQuery), loadMessageRecipients()];
  if (can("Voir employés")) {
    await loadEmployees();
    jobs.push(loadDepartments(), loadAttendances(), loadContracts());
  }
  if (can("Voir salaires")) {
    jobs.push(loadPayrolls());
  }
  if (can("Voir employés") && ["SuperAdmin", "Admin RH", "RH"].includes(appState.role)) {
    jobs.push(loadRoles());
  }
  if (can("Modifier employés") && ["SuperAdmin", "Admin RH", "RH"].includes(appState.role)) {
    jobs.push(loadAccounts(), loadAccountLogs());
  }
  await Promise.all(jobs);

  if (isAccountingSectionActive()) {
    await loadAccountingSection();
  }

  if (appState.activeChatUserId && isMessagesSectionActive()) {
    await loadConversationThread(appState.activeChatUserId);
  }
}

async function updateAccountRole() {
  const userId = Number($("accountUserId").value);
  const roleId = Number($("accountRoleId").value);
  if (!userId || !roleId) {
    notify("Sélectionne un agent et un rôle", true);
    return;
  }
  await api(`/api/accounts/${userId}/role`, {
    method: "PATCH",
    body: JSON.stringify({ role_id: roleId }),
  });
  notify("Rôle du compte mis à jour");
  await Promise.all([loadAccounts(), loadAccountLogs(), loadRoles(), loadEmployees()]);
}

async function updateAccountStatus() {
  const userId = Number($("accountUserId").value);
  const status = $("accountStatus").value;
  if (!userId || !status) {
    notify("Sélectionne un agent et un statut", true);
    return;
  }
  await api(`/api/accounts/${userId}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status }),
  });
  notify("Statut du compte mis à jour");
  await Promise.all([loadAccounts(), loadAccountLogs(), loadEmployees()]);
}

async function resetAccountPassword() {
  const userId = Number($("accountUserId").value);
  if (!userId) {
    notify("Sélectionne un agent", true);
    return;
  }
  await api(`/api/accounts/${userId}/reset-password`, {
    method: "PATCH",
  });
  notify("Mot de passe réinitialisé (mot de passe par défaut)");
  await Promise.all([loadAccounts(), loadAccountLogs()]);
}

function bindForms() {
  $("employeeForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const payload = normalizePayload(getFormJSON(event.target), ["role_id", "department_id"]);
      await api("/api/employees", { method: "POST", body: JSON.stringify(payload) });
      event.target.reset();
      closeAllDrawers();
      notify("Employé créé avec succès");
      await Promise.all([loadEmployees(), loadOverview()]);
    } catch (error) {
      notify(error.message, true);
    }
  });

  $("departmentForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const payload = normalizePayload(getFormJSON(event.target), ["budget"]);
      await api("/api/departments", { method: "POST", body: JSON.stringify(payload) });
      event.target.reset();
      closeAllDrawers();
      notify("Département créé");
      await Promise.all([loadDepartments(), loadOverview()]);
    } catch (error) {
      notify(error.message, true);
    }
  });

  $("roleForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const payload = getFormJSON(event.target);
      const selectedPermissions = getCheckedPermissions("rolePermissionsChecklist");

      await api("/api/roles", {
        method: "POST",
        body: JSON.stringify({
          name: payload.name,
          permission_names: selectedPermissions,
        }),
      });
      event.target.reset();
      setCheckedPermissions("rolePermissionsChecklist", []);
      notify("Rôle créé");
      await loadRoles();
    } catch (error) {
      notify(error.message, true);
    }
  });

  $("payrollForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const payload = normalizePayload(getFormJSON(event.target), [
        "employee_id",
        "base_salary",
        "bonus",
        "overtime_hours",
        "deductions",
        "taxes",
      ]);
      if (!payload.employee_id) {
        throw new Error("Sélectionne un employé valide dans la liste");
      }
      await api("/api/payrolls", { method: "POST", body: JSON.stringify(payload) });
      event.target.reset();
      closeAllDrawers();
      notify("Fiche de paie créée");
      await Promise.all([loadPayrolls(), loadOverview()]);
    } catch (error) {
      notify(error.message, true);
    }
  });

  $("attendanceForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const payload = normalizePayload(getFormJSON(event.target), ["employee_id", "late_minutes"]);
      if (!payload.employee_id) {
        throw new Error("Sélectionne un employé valide dans la liste");
      }

      payload.is_absent = String(payload.is_absent || "false") === "true";
      await api("/api/attendances/checkin", { method: "POST", body: JSON.stringify(payload) });
      event.target.reset();
      closeAllDrawers();
      notify("Pointage d'entrée enregistré");
      await Promise.all([loadAttendances(), loadOverview()]);
    } catch (error) {
      notify(error.message, true);
    }
  });

  $("leaveForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const payload = normalizePayload(getFormJSON(event.target), ["employee_id"]);
      if (!payload.employee_id) {
        throw new Error("Sélectionne un employé valide dans la liste");
      }
      await api("/api/leaves", { method: "POST", body: JSON.stringify(payload) });
      event.target.reset();
      closeAllDrawers();
      notify("Demande de congé envoyée");
      await Promise.all([loadLeaves(), loadOverview()]);
    } catch (error) {
      notify(error.message, true);
    }
  });

  $("contractForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const payload = normalizePayload(getFormJSON(event.target), ["employee_id", "contractual_salary"]);
      if (!payload.employee_id) {
        throw new Error("Sélectionne un employé valide dans la liste");
      }
      await api("/api/contracts", { method: "POST", body: JSON.stringify(payload) });
      event.target.reset();
      closeAllDrawers();
      notify("Contrat créé");
      await loadContracts();
    } catch (error) {
      notify(error.message, true);
    }
  });

  $("chatComposerForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const activeUserId = Number(appState.activeChatUserId || 0);
      const activeRecipientEmployeeId = Number(appState.activeChatRecipientEmployeeId || 0);
      if (!activeUserId && !activeRecipientEmployeeId) {
        throw new Error("Sélectionne d'abord une discussion");
      }

      const payload = getFormJSON(event.target);
      if (!String(payload.content || "").trim()) {
        throw new Error("Le message ne peut pas être vide");
      }

      if (activeUserId) {
        await api(`/api/messages/thread/${activeUserId}`, {
          method: "POST",
          body: JSON.stringify(payload),
        });
      } else {
        const createdMessage = await api(`/api/messages`, {
          method: "POST",
          body: JSON.stringify({
            recipient_employee_id: activeRecipientEmployeeId,
            content: payload.content,
          }),
        });
        appState.activeChatUserId = Number(createdMessage?.recipient_user_id || 0) || null;
        appState.activeChatRecipientEmployeeId = null;
      }

      event.target.reset();
      await loadMessageRecipients();
      if (appState.activeChatUserId) {
        await openConversation(appState.activeChatUserId);
      } else {
        const query = ($("messagesSearch")?.value || "").trim();
        await loadConversations(query);
      }
    } catch (error) {
      notify(error.message, true);
    }
  });
}

function bindPasswordModal() {
  $("passwordUpdateForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const payload = getFormJSON(event.target);
      const currentPassword = (payload.current_password || "").trim();
      const newPassword = (payload.new_password || "").trim();
      const confirmNewPassword = (payload.confirm_new_password || "").trim();

      if (currentPassword.length < 6 || newPassword.length < 6 || confirmNewPassword.length < 6) {
        throw new Error("Le mot de passe doit contenir au moins 6 caractères");
      }

      if (currentPassword === newPassword) {
        throw new Error("Le nouveau mot de passe doit être différent de l'actuel");
      }

      if (newPassword !== confirmNewPassword) {
        throw new Error("La confirmation du nouveau mot de passe ne correspond pas");
      }

      const response = await api("/api/auth/change-password", {
        method: "POST",
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });
      if (response.access_token) {
        appState.token = response.access_token;
        localStorage.setItem("ems_token", response.access_token);
      }
      setMustChangePassword(false);
      event.target.reset();
      notify("Mot de passe mis à jour");
      await refreshAll();
    } catch (error) {
      notify(error.message, true);
    }
  });
}

function setLoginError(message = "") {
  const box = $("loginError");
  if (!box) return;
  if (!message) {
    box.textContent = "";
    box.classList.add("hidden");
    return;
  }
  box.textContent = message;
  box.classList.remove("hidden");
}

function setLoginLoading(isLoading) {
  const btn = $("loginSubmitBtn");
  const username = $("username");
  const password = $("password");
  if (btn) {
    btn.disabled = isLoading;
    btn.classList.toggle("is-loading", isLoading);
  }
  if (username) username.disabled = isLoading;
  if (password) password.disabled = isLoading;
}

function setupLoginUI() {
  const toggleBtn = $("loginTogglePassword");
  const passwordInput = $("password");
  const toggleIcon = $("loginTogglePasswordIcon");
  if (toggleBtn && passwordInput) {
    toggleBtn.addEventListener("click", () => {
      const show = passwordInput.type === "password";
      passwordInput.type = show ? "text" : "password";
      if (toggleIcon) {
        toggleIcon.className = show ? "ri-eye-off-line" : "ri-eye-line";
      }
      toggleBtn.setAttribute(
        "aria-label",
        show ? "Masquer le mot de passe" : "Afficher le mot de passe",
      );
    });
  }

  ["username", "password"].forEach((id) => {
    const input = $(id);
    if (!input) return;
    input.addEventListener("input", () => setLoginError(""));
  });
}

function setupAuthFlow() {
  setupLoginUI();

  $("loginForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    setLoginError("");
    setLoginLoading(true);
    try {
      const username = $("username").value.trim();
      const password = $("password").value;
      if (!username || !password) {
        throw new Error("Veuillez renseigner l'identifiant et le mot de passe.");
      }
      const loginResult = await api("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ username, password }),
      });

      appState.token = loginResult.access_token;

      localStorage.setItem("ems_token", appState.token);

      const me = await api("/api/auth/me");
      appState.username = me.username || loginResult.username || "";
      appState.role = me.role || loginResult.role || "";
      appState.permissions = me.permissions || loginResult.permissions || [];
      updateAccountHolderInfo(
        me.account_holder_name || loginResult.account_holder_name || appState.username,
        me.account_holder_function || loginResult.account_holder_function || appState.role
      );

      localStorage.setItem("ems_username", appState.username);
      localStorage.setItem("ems_role", appState.role);
      localStorage.setItem("ems_permissions", JSON.stringify(appState.permissions));

      renderOwnerAccountInfo();
      ensureSectionAccess();
      applyFormPermissions();
      $("loginScreen").classList.add("hidden");
      $("appShell").classList.remove("hidden");
      setMustChangePassword(!!(me.must_change_password ?? loginResult.must_change_password));
      await loadReportsSection();
      notify("Connexion réussie");
      if (!appState.mustChangePassword) {
        await refreshAll();
      }
      startMessagesAutoRefresh();
    } catch (error) {
      setLoginError(error.message || "Connexion impossible. Vérifiez vos identifiants.");
      notify(error.message, true);
    } finally {
      setLoginLoading(false);
    }
  });

  $("logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("ems_token");
    localStorage.removeItem("ems_username");
    localStorage.removeItem("ems_role");
    localStorage.removeItem("ems_permissions");
    localStorage.removeItem("ems_must_change_password");
    appState.token = "";
    appState.username = "";
    appState.role = "";
    appState.permissions = [];
    clearAccountHolderInfo();
    renderOwnerAccountInfo();
    setMustChangePassword(false);
    stopMessagesAutoRefresh();
    $("appShell").classList.add("hidden");
    $("loginScreen").classList.remove("hidden");
    setLoginError("");
    notify("Déconnecté");
  });

  if (appState.token) {
    api("/api/auth/me")
      .then(async (me) => {
        appState.username = me.username || appState.username;
        appState.role = me.role || appState.role;
        appState.permissions = me.permissions || [];
        updateAccountHolderInfo(
          me.account_holder_name || appState.username,
          me.account_holder_function || appState.role
        );
        localStorage.setItem("ems_username", appState.username);
        localStorage.setItem("ems_role", appState.role);
        localStorage.setItem("ems_permissions", JSON.stringify(appState.permissions));

        renderOwnerAccountInfo();
        ensureSectionAccess();
        applyFormPermissions();
        $("loginScreen").classList.add("hidden");
        $("appShell").classList.remove("hidden");
        setMustChangePassword(!!me.must_change_password);
        await loadReportsSection();
        if (!appState.mustChangePassword) {
          await refreshAll();
        }
        startMessagesAutoRefresh();
      })
      .catch((error) => {
        localStorage.removeItem("ems_token");
        localStorage.removeItem("ems_username");
        localStorage.removeItem("ems_role");
        localStorage.removeItem("ems_permissions");
        localStorage.removeItem("ems_must_change_password");
        appState.token = "";
        appState.username = "";
        appState.role = "";
        appState.permissions = [];
        clearAccountHolderInfo();
        renderOwnerAccountInfo();
        setMustChangePassword(false);
        stopMessagesAutoRefresh();
        $("appShell").classList.add("hidden");
        $("loginScreen").classList.remove("hidden");
        notify(`Session expirée: ${error.message}`, true);
      });
  }
}

function setupActions() {
  $("refreshBtn").addEventListener("click", async () => {
    try {
      await refreshAll();
      notify("Données rafraîchies");
    } catch (error) {
      notify(error.message, true);
    }
  });

  const roleButton = $("btnAccountRole");
  const statusButton = $("btnAccountStatus");
  const resetButton = $("btnAccountReset");

  if (roleButton) {
    roleButton.addEventListener("click", async () => {
      try {
        await updateAccountRole();
      } catch (error) {
        notify(error.message, true);
      }
    });
  }

  if (statusButton) {
    statusButton.addEventListener("click", async () => {
      try {
        await updateAccountStatus();
      } catch (error) {
        notify(error.message, true);
      }
    });
  }

  if (resetButton) {
    resetButton.addEventListener("click", async () => {
      try {
        await resetAccountPassword();
      } catch (error) {
        notify(error.message, true);
      }
    });
  }

  const logsFilterButton = $("btnLogsFilter");
  const logsClearButton = $("btnLogsClear");
  const logsExportCsvButton = $("btnLogsExportCsv");
  const logsExportPdfButton = $("btnLogsExportPdf");
  const rolePermissionsButton = $("btnRolePermissions");
  const rolePermissionsRoleSelect = $("rolePermissionRoleId");
  const attendanceCheckoutButton = $("btnAttendanceCheckout");
  const attendanceSummaryButton = $("btnAttendanceSummary");
  const messagesRefreshButton = $("btnMessagesRefresh");
  const messagesSearchInput = $("messagesSearch");
  const newConversationButton = $("btnNewConversation");
  const chatMessagesContainer = $("chatMessages");

  ["payrollEmployeeQuery", "attendanceEmployeeQuery", "leaveEmployeeQuery", "contractEmployeeQuery"].forEach((queryId) => {
    const input = $(queryId);
    if (!input) return;
    input.addEventListener("input", () => {
      populateEmployeeActionSelects();
    });
  });

  const accountUserQuery = $("accountUserQuery");
  if (accountUserQuery) {
    accountUserQuery.addEventListener("input", () => {
      populateAccountActionSelect();
    });
  }

  if (logsFilterButton) {
    logsFilterButton.addEventListener("click", async () => {
      try {
        await loadAccountLogs();
        notify("Filtres de logs appliqués");
      } catch (error) {
        notify(error.message, true);
      }
    });
  }

  if (logsClearButton) {
    logsClearButton.addEventListener("click", async () => {
      if ($("logUsername")) $("logUsername").value = "";
      if ($("logAction")) $("logAction").value = "";
      if ($("logStartDate")) $("logStartDate").value = "";
      if ($("logEndDate")) $("logEndDate").value = "";
      try {
        await loadAccountLogs();
        notify("Filtres de logs réinitialisés");
      } catch (error) {
        notify(error.message, true);
      }
    });
  }

  if (logsExportCsvButton) {
    logsExportCsvButton.addEventListener("click", async () => {
      try {
        await exportAccountLogs("csv");
        notify("Export CSV lancé");
      } catch (error) {
        notify(error.message, true);
      }
    });
  }

  if (logsExportPdfButton) {
    logsExportPdfButton.addEventListener("click", async () => {
      try {
        await exportAccountLogs("pdf");
        notify("Export PDF lancé");
      } catch (error) {
        notify(error.message, true);
      }
    });
  }

  if (rolePermissionsRoleSelect) {
    rolePermissionsRoleSelect.addEventListener("change", () => {
      const roleId = Number(rolePermissionsRoleSelect.value || 0);
      const role = appState.roles.find((entry) => entry.id === roleId);
      setCheckedPermissions("updateRolePermissionsChecklist", role?.permissions || []);
    });
  }

  if (rolePermissionsButton) {
    rolePermissionsButton.addEventListener("click", async () => {
      try {
        await updateRolePermissions();
      } catch (error) {
        notify(error.message, true);
      }
    });
  }

  if (attendanceCheckoutButton) {
    attendanceCheckoutButton.addEventListener("click", async () => {
      try {
        const employeeId = Number($("attendanceEmployeeId")?.value || 0);
        const checkOut = $("attendanceCheckOutAt")?.value || "";
        if (!employeeId) {
          throw new Error("Sélectionne un employé");
        }
        if (!checkOut) {
          throw new Error("Saisis la date/heure de sortie");
        }

        await api("/api/attendances/checkout-employee", {
          method: "POST",
          body: JSON.stringify({ employee_id: employeeId, check_out: checkOut }),
        });

        notify("Pointage de sortie enregistré");
        await Promise.all([loadAttendances(), loadOverview()]);
      } catch (error) {
        notify(error.message, true);
      }
    });
  }

  if (attendanceSummaryButton) {
    attendanceSummaryButton.addEventListener("click", async () => {
      try {
        const month = $("attendanceSummaryMonth")?.value || "";
        await loadAttendanceMonthlySummary(month);
        notify("Synthèse mensuelle chargée");
      } catch (error) {
        notify(error.message, true);
      }
    });
  }

  if (messagesRefreshButton) {
    messagesRefreshButton.addEventListener("click", async () => {
      try {
        const query = ($("messagesSearch")?.value || "").trim();
        await loadConversations(query);
        if (appState.activeChatUserId) {
          await loadConversationThread(appState.activeChatUserId);
        }
        notify("Messagerie actualisée");
      } catch (error) {
        notify(error.message, true);
      }
    });
  }

  if (messagesSearchInput) {
    messagesSearchInput.addEventListener("input", async () => {
      try {
        await loadConversations((messagesSearchInput.value || "").trim());
      } catch (_error) {}
    });
  }

  if (newConversationButton) {
    newConversationButton.addEventListener("click", async () => {
      try {
        await startNewConversation();
      } catch (error) {
        notify(error.message, true);
      }
    });
  }

  if (chatMessagesContainer) {
    chatMessagesContainer.addEventListener("scroll", () => {
      if (chatMessagesContainer.scrollTop <= 24) {
        loadOlderThreadMessages().catch(() => {});
      }
    });
  }

  document.addEventListener("click", async (event) => {
    const loadMoreButton = event.target.closest("#chatLoadMoreBtn");
    if (loadMoreButton) {
      try {
        await loadOlderThreadMessages();
      } catch (error) {
        notify(error.message, true);
      }
      return;
    }

    const chatConversationButton = event.target.closest("[data-chat-userid]");
    if (chatConversationButton) {
      const userId = Number(chatConversationButton.dataset.chatUserid || 0);
      if (!userId) return;
      try {
        await openConversation(userId);
      } catch (error) {
        notify(error.message, true);
      }
      return;
    }

    const chatActionButton = event.target.closest("[data-chat-action][data-message-id]");
    if (chatActionButton) {
      const action = String(chatActionButton.dataset.chatAction || "").trim();
      const messageId = Number(chatActionButton.dataset.messageId || 0);
      if (!messageId) return;

      try {
        if (action === "edit") {
          await editOwnMessage(messageId);
          notify("Message modifié");
        } else if (action === "delete") {
          await deleteOwnMessage(messageId);
          notify("Message supprimé");
        }
      } catch (error) {
        notify(error.message, true);
      }
      return;
    }

    const actionButton = event.target.closest("[data-entity][data-action][data-id]");
    if (!actionButton) return;

    const entity = actionButton.dataset.entity;
    const action = actionButton.dataset.action;
    const id = Number(actionButton.dataset.id || 0);
    if (!id) return;

    try {
      if (entity === "employee" && action === "edit") {
        await editEmployee(id);
      } else if (entity === "employee" && action === "delete") {
        await deleteEmployee(id);
      } else if (entity === "department" && action === "edit") {
        await editDepartment(id);
      } else if (entity === "department" && action === "delete") {
        await deleteDepartment(id);
      } else if (entity === "payroll" && action === "edit") {
        await editPayroll(id);
      } else if (entity === "payroll" && action === "delete") {
        await deletePayroll(id);
      } else if (entity === "attendance" && action === "edit") {
        await editAttendance(id);
      } else if (entity === "attendance" && action === "delete") {
        await deleteAttendance(id);
      } else if (entity === "leave" && action === "edit") {
        await editLeave(id);
      } else if (entity === "leave" && action === "delete") {
        await deleteLeave(id);
      } else if (entity === "contract" && action === "edit") {
        await editContract(id);
      } else if (entity === "contract" && action === "delete") {
        await deleteContract(id);
      }
    } catch (error) {
      notify(error.message, true);
    }
  });

}

/* ============================================================
   THEME TOGGLE
   ============================================================ */
function initThemeToggle() {
  const savedTheme = localStorage.getItem("ems_theme") || "dark";
  document.documentElement.setAttribute("data-theme", savedTheme);
  updateThemeUI(savedTheme);

  const btn = $("themeToggle");
  if (btn) {
    btn.addEventListener("click", () => {
      const current = document.documentElement.getAttribute("data-theme") || "dark";
      const next = current === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      localStorage.setItem("ems_theme", next);
      updateThemeUI(next);
    });
  }
}

function updateThemeUI(theme) {
  const icon  = $("themeIcon");
  const label = $("themeLabel");
  if (icon)  icon.className  = theme === "dark" ? "ri-moon-line" : "ri-sun-line";
  if (label) label.textContent = theme === "dark" ? "Mode clair" : "Mode sombre";
}

/* ============================================================
   TEAM SECTION (Manager)
   ============================================================ */
function teamStatusLabel(status) {
  const map = {
    present: "Présent",
    completed: "Journée close",
    absent: "Absent",
    not_arrived: "Non arrivé",
  };
  return map[status] || status || "—";
}

function teamStatusClass(status) {
  if (status === "present") return "badge-ok";
  if (status === "completed") return "badge-info";
  if (status === "absent") return "badge-danger";
  return "badge-warn";
}

async function loadTeamSection() {
  const panel = $("teamPanel");
  if (!panel) return;
  panel.innerHTML = '<p style="color:var(--text-2);padding:12px">Chargement de l\'équipe…</p>';

  try {
    const data = await api("/api/team/overview");
    const stats = data.stats || {};
    if ($("teamStatMembers")) $("teamStatMembers").textContent = stats.members ?? 0;
    if ($("teamStatPresent")) $("teamStatPresent").textContent = stats.present ?? 0;
    if ($("teamStatLate")) $("teamStatLate").textContent = stats.late ?? 0;
    if ($("teamStatLeaves")) $("teamStatLeaves").textContent = stats.pending_leaves ?? 0;

    const departments = data.departments || [];
    if (!departments.length) {
      panel.innerHTML = '<div class="empty-state"><i class="ri-team-line"></i><p>Aucune équipe à afficher pour ce profil.</p></div>';
      return;
    }

    const query = ($("teamSearch")?.value || "").trim().toLowerCase();
    panel.innerHTML = departments.map((block) => {
      const dept = block.department || {};
      const members = (block.members || []).filter((m) => {
        if (!query) return true;
        const e = m.employee || {};
        const hay = `${e.first_name || ""} ${e.last_name || ""} ${e.matricule || ""} ${e.email || ""}`.toLowerCase();
        return hay.includes(query);
      });
      if (!members.length) return "";

      return `<div class="team-dept-block">
        <div class="team-dept-head">
          <div>
            <h3>${dept.name || "Département"}</h3>
            <p>${members.length} collaborateur(s) · Budget ${Number(dept.budget || 0).toLocaleString("fr-FR")} FC</p>
          </div>
          <span class="badge badge-info">${data.is_hr_view ? "Vue RH" : "Mon équipe"}</span>
        </div>
        <div class="team-member-grid">
          ${members.map((m) => {
            const e = m.employee || {};
            const ini = `${(e.first_name || "?")[0] || ""}${(e.last_name || "")[0] || ""}`.toUpperCase();
            const checkIn = m.check_in ? new Date(m.check_in).toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" }) : "—";
            return `<article class="team-member-card">
              <div class="team-member-top">
                <div class="team-avatar">${ini}</div>
                <div>
                  <strong>${e.first_name || ""} ${e.last_name || ""}</strong>
                  <span>${e.matricule || "—"} · ${e.role || ""}</span>
                </div>
              </div>
              <div class="team-member-meta">
                <span class="badge ${teamStatusClass(m.today_status)}">${teamStatusLabel(m.today_status)}</span>
                <span><i class="ri-time-line"></i> ${checkIn}</span>
                ${m.late_minutes ? `<span class="team-late"><i class="ri-alarm-warning-line"></i> +${m.late_minutes} min</span>` : ""}
              </div>
              <div class="team-member-actions">
                <button type="button" class="btn btn-secondary btn-sm" onclick="navigate('employees')"><i class="ri-user-line"></i> Fiche</button>
                <button type="button" class="btn btn-secondary btn-sm" onclick="navigate('leaves')"><i class="ri-calendar-line"></i> Congés</button>
              </div>
            </article>`;
          }).join("")}
        </div>
      </div>`;
    }).join("") || '<div class="empty-state"><i class="ri-search-line"></i><p>Aucun collaborateur ne correspond à la recherche.</p></div>';
  } catch (err) {
    panel.innerHTML = `<p style="color:var(--danger);padding:12px">Erreur : ${err.message}</p>`;
  }
}

function setupTeamActions() {
  $("teamSearch")?.addEventListener("input", () => loadTeamSection());
  $("btnRefreshTeam")?.addEventListener("click", () => loadTeamSection());
}

/* ============================================================
   BIOMETRIC & RFID SECTION
   ============================================================ */
const BIOMETRIC_BRIDGE_URL = "http://localhost:5002";
const REQUIRED_FINGERPRINTS = 3;

const enrollmentState = {
  templates: [],
};

function closeAllBioActionMenus() {
  document.querySelectorAll(".bio-action-menu").forEach((menu) => {
    menu.hidden = true;
  });
}

function updateEnrollmentUI() {
  const fpProgress = $("fpProgress");
  const enrollBtn = $("btnEnrollFingerprint");
  const fpStatus = $("fingerprintStatus");
  const done = enrollmentState.templates.length;
  const next = Math.min(done + 1, REQUIRED_FINGERPRINTS);

  if (fpProgress) {
    fpProgress.removeAttribute("aria-hidden");
    fpProgress.querySelectorAll(".fp-step").forEach((el) => {
      const step = Number(el.dataset.step);
      el.classList.remove("done", "active", "error");
      if (step <= done) el.classList.add("done");
      else if (step === next && done < REQUIRED_FINGERPRINTS) el.classList.add("active");
    });
  }

  if (enrollBtn) {
    if (done >= REQUIRED_FINGERPRINTS) {
      enrollBtn.disabled = true;
      enrollBtn.innerHTML = '<i class="ri-check-line"></i> Enrôlement terminé';
    } else {
      enrollBtn.disabled = false;
      enrollBtn.innerHTML = `<i class="ri-fingerprint-2-line"></i> Scanner le doigt ${next}/${REQUIRED_FINGERPRINTS}`;
    }
  }

  if (fpStatus && done === 0) {
    fpStatus.textContent = "Sélectionnez un employé puis enregistrez 3 doigts distincts";
  } else if (fpStatus && done > 0 && done < REQUIRED_FINGERPRINTS) {
    fpStatus.textContent = `${done} doigt(s) capturé(s) — scannez le doigt ${next}`;
  }
}

function resetEnrollmentSession(keepEmployee = true) {
  enrollmentState.templates = [];
  const fpIcon = $("fpIcon");
  if (fpIcon) fpIcon.className = "fp-icon";
  if (!keepEmployee) {
    const sel = $("biometricEmployeeSelect");
    if (sel) sel.value = "";
  }
  updateEnrollmentUI();
}

function buildBioActionMenu(e) {
  const items = [];

  if (e.has_fingerprint) {
    items.push(`<button type="button" data-action="delete-fingerprint" data-id="${e.id}"><i class="ri-fingerprint-line"></i> Supprimer l'empreinte</button>`);
    items.push(`<button type="button" data-action="reenroll" data-id="${e.id}"><i class="ri-refresh-line"></i> Relancer l'enrôlement (3 doigts)</button>`);
  } else {
    items.push(`<button type="button" data-action="reenroll" data-id="${e.id}"><i class="ri-fingerprint-2-line"></i> Enrôler (3 doigts)</button>`);
  }

  if (e.rfid_card_id) {
    if (items.length) items.push('<div class="bio-menu-divider"></div>');
    if (e.rfid_card_active) {
      items.push(`<button type="button" data-action="deactivate-rfid" data-id="${e.id}"><i class="ri-forbid-line"></i> Désactiver la carte</button>`);
    } else {
      items.push(`<button type="button" data-action="reactivate-rfid" data-id="${e.id}"><i class="ri-checkbox-circle-line"></i> Réactiver la carte</button>`);
    }
    items.push(`<button type="button" data-action="update-rfid" data-id="${e.id}" data-card="${e.rfid_card_id || ""}"><i class="ri-edit-line"></i> Modifier la carte</button>`);
    items.push(`<button type="button" class="danger" data-action="delete-rfid" data-id="${e.id}"><i class="ri-delete-bin-line"></i> Supprimer la carte</button>`);
  } else {
    if (items.length) items.push('<div class="bio-menu-divider"></div>');
    items.push(`<button type="button" data-action="assign-rfid" data-id="${e.id}"><i class="ri-nfc-line"></i> Assigner une carte</button>`);
  }

  return `<div class="bio-action-wrap">
    <button type="button" class="btn btn-secondary btn-sm bio-action-trigger" data-menu-for="${e.id}" aria-label="Actions">
      <i class="ri-more-2-fill"></i>
    </button>
    <div class="bio-action-menu" id="bioMenu-${e.id}" hidden>
      ${items.join("")}
    </div>
  </div>`;
}

async function verifyFingerprintTemplate(template, employeeId, pendingTemplates) {
  const result = await api("/api/biometric/verify-template", {
    method: "POST",
    body: JSON.stringify({
      template,
      employee_id: employeeId ? parseInt(employeeId, 10) : null,
      pending_templates: pendingTemplates,
    }),
  });

  if (!result.valid) {
    throw new Error(result.message || "Empreinte déjà enregistrée ou identique à un doigt précédent.");
  }
}

async function scanFingerprintFromBridge() {
  const pingData = await api("/api/biometric/status");
  if (!pingData.status || pingData.status !== "ok") {
    throw new Error("Lecteur biométrique non connecté");
  }

  const scanData = await api("/api/biometric/scan", {
    method: "POST",
    body: "{}",
    signal: AbortSignal.timeout(35000),
  });

  if (!scanData.template) {
    throw new Error("Aucun gabarit reçu du lecteur");
  }

  return scanData.template;
}

async function checkBiometricBridgeStatus() {
  const dot    = $("biometricDot");
  const status = $("biometricBridgeStatus");
  if (dot) { dot.className = "status-dot checking"; }
  if (status) status.textContent = "Vérification du lecteur biométrique...";

  try {
    const data = await api("/api/biometric/status");
    if (data.status === "ok") {
      if (dot) { dot.className = "status-dot online"; }
      if (status) status.textContent = "Lecteur biométrique connecté et opérationnel";
    } else {
      throw new Error("bridge non disponible");
    }
  } catch {
    if (dot)    { dot.className = "status-dot offline"; }
    if (status) status.textContent = "Lecteur biométrique non disponible — vérifiez que le service est démarré sur le port 5002";
  }
}

async function loadBiometricSection() {
  await checkBiometricBridgeStatus();

  // Populate employee selects
  const employees = appState.employees || [];
  ["biometricEmployeeSelect", "rfidEmployeeId"].forEach((selId) => {
    const sel = $(selId);
    if (!sel) return;
    const current = sel.value;
    sel.innerHTML = '<option value="">Sélectionner un employé</option>' +
      employees.map((e) => `<option value="${e.id}">${e.first_name} ${e.last_name} — ${e.matricule || e.id}</option>`).join("");
    if (current) sel.value = current;
  });

  const bioSel = $("biometricEmployeeSelect");
  if (bioSel && !bioSel.dataset.enrollBound) {
    bioSel.dataset.enrollBound = "1";
    bioSel.addEventListener("change", () => resetEnrollmentSession(true));
  }

  await loadEnrolledEmployees();
}

async function loadEnrolledEmployees() {
  try {
    const data = await api("/api/biometric/enrolled");
    const wrap = $("biometricEnrolledTable");
    if (!wrap) return;
    const employees = Array.isArray(data) ? data : (data.employees || []);
    if (employees.length === 0) {
      wrap.innerHTML = '<p style="color:var(--text-2);padding:8px">Aucun employé enrôlé pour l\'instant.</p>';
      return;
    }
    wrap.innerHTML = `<table>
      <thead><tr>
        <th>Employé</th>
        <th>Empreinte</th>
        <th>Carte RFID</th>
        <th>N° carte</th>
        <th></th>
      </tr></thead>
      <tbody>${employees.map((e) => `
        <tr>
          <td>${e.name || "—"}</td>
          <td>${e.has_fingerprint
            ? (e.fingerprint_complete
              ? `<span class="badge badge-ok"><i class="ri-fingerprint-line"></i> ${e.fingerprint_count || 3}/3</span>`
              : `<span class="badge badge-warn"><i class="ri-fingerprint-line"></i> ${e.fingerprint_count || 0}/3</span>`)
            : '<span class="badge badge-warn">Non enrôlé</span>'}</td>
          <td>${e.rfid_card_id
            ? (e.rfid_card_active
              ? '<span class="badge badge-ok"><i class="ri-nfc-line"></i> Active</span>'
              : '<span class="badge badge-danger">Désactivée</span>')
            : '<span class="badge" style="background:var(--inp-bg);color:var(--text-2);border:1px solid var(--border)">Aucune</span>'}</td>
          <td style="color:var(--text-2)">${e.rfid_card_id || "—"}</td>
          <td class="bio-actions-cell">${buildBioActionMenu(e)}</td>
        </tr>`).join("")}
      </tbody>
    </table>`;
  } catch (err) {
    const wrap = $("biometricEnrolledTable");
    if (wrap) wrap.innerHTML = `<p style="color:var(--danger);padding:8px">Erreur: ${err.message}</p>`;
  }
}

async function deactivateRfid(employeeId) {
  if (!confirm("Désactiver la carte RFID de cet employé ?")) return;
  try {
    await api("/api/biometric/rfid/deactivate", {
      method: "POST",
      body: JSON.stringify({ employee_id: employeeId }),
    });
    notify("Carte RFID désactivée");
    await loadEnrolledEmployees();
  } catch (err) {
    notify(err.message, true);
  }
}

async function reactivateRfidCard(employeeId) {
  try {
    await api("/api/biometric/rfid/reactivate", {
      method: "POST",
      body: JSON.stringify({ employee_id: employeeId }),
    });
    notify("Carte RFID réactivée");
    await loadEnrolledEmployees();
  } catch (err) {
    notify(err.message, true);
  }
}

async function deleteRfidCard(employeeId) {
  if (!confirm("Supprimer définitivement la carte RFID de cet employé ?")) return;
  try {
    await api("/api/biometric/rfid/delete", {
      method: "POST",
      body: JSON.stringify({ employee_id: employeeId }),
    });
    notify("Carte RFID supprimée");
    await loadEnrolledEmployees();
  } catch (err) {
    notify(err.message, true);
  }
}

async function updateRfidCard(employeeId, currentCard) {
  const cardId = prompt("Nouveau numéro de carte RFID :", currentCard || "");
  if (!cardId || !cardId.trim()) return;
  try {
    await api("/api/biometric/rfid/update", {
      method: "POST",
      body: JSON.stringify({ employee_id: employeeId, rfid_card_id: cardId.trim() }),
    });
    notify("Carte RFID mise à jour");
    await loadEnrolledEmployees();
  } catch (err) {
    notify(err.message, true);
  }
}

async function assignRfidToEmployee(employeeId) {
  const cardId = prompt("Numéro de la carte RFID à assigner :");
  if (!cardId || !cardId.trim()) return;
  try {
    await api("/api/biometric/rfid/assign", {
      method: "POST",
      body: JSON.stringify({ employee_id: employeeId, rfid_card_id: cardId.trim() }),
    });
    notify("Carte RFID assignée");
    await loadEnrolledEmployees();
  } catch (err) {
    notify(err.message, true);
  }
}

async function deleteEmployeeFingerprint(employeeId) {
  if (!confirm("Supprimer toutes les empreintes de cet employé ?")) return;
  try {
    await api("/api/biometric/fingerprint/delete", {
      method: "POST",
      body: JSON.stringify({ employee_id: employeeId }),
    });
    notify("Empreintes supprimées");
    await loadEnrolledEmployees();
  } catch (err) {
    notify(err.message, true);
  }
}

function startReenrollmentForEmployee(employeeId) {
  const sel = $("biometricEmployeeSelect");
  if (sel) sel.value = String(employeeId);
  resetEnrollmentSession(true);
  const fpStatus = $("fingerprintStatus");
  if (fpStatus) fpStatus.textContent = "Placez le premier doigt sur le lecteur (doigt 1/3)";
  document.getElementById("biometricEmployeeSelect")?.scrollIntoView({ behavior: "smooth", block: "center" });
  notify("Sélectionnez « Scanner le doigt 1/3 » pour relancer l'enrôlement");
}

async function handleBioMenuAction(action, employeeId, cardId) {
  closeAllBioActionMenus();
  switch (action) {
    case "deactivate-rfid":
      await deactivateRfid(employeeId);
      break;
    case "reactivate-rfid":
      await reactivateRfidCard(employeeId);
      break;
    case "delete-rfid":
      await deleteRfidCard(employeeId);
      break;
    case "update-rfid":
      await updateRfidCard(employeeId, cardId);
      break;
    case "assign-rfid":
      await assignRfidToEmployee(employeeId);
      break;
    case "delete-fingerprint":
      await deleteEmployeeFingerprint(employeeId);
      break;
    case "reenroll":
      startReenrollmentForEmployee(employeeId);
      break;
    default:
      break;
  }
}

function setupBiometricActions() {
  updateEnrollmentUI();

  const resetBtn = $("btnResetEnrollment");
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      resetEnrollmentSession(true);
      const fpStatus = $("fingerprintStatus");
      if (fpStatus) fpStatus.textContent = "Enrôlement réinitialisé — 3 doigts distincts requis";
      notify("Enrôlement réinitialisé");
    });
  }

  const enrolledWrap = $("biometricEnrolledTable");
  if (enrolledWrap) {
    enrolledWrap.addEventListener("click", async (event) => {
      const trigger = event.target.closest(".bio-action-trigger");
      if (trigger) {
        event.stopPropagation();
        const menuId = trigger.getAttribute("data-menu-for");
        const menu = menuId ? document.getElementById(`bioMenu-${menuId}`) : null;
        if (!menu) return;
        const willOpen = menu.hidden;
        closeAllBioActionMenus();
        menu.hidden = !willOpen;
        return;
      }

      const actionBtn = event.target.closest("[data-action]");
      if (!actionBtn) return;
      const action = actionBtn.getAttribute("data-action");
      const employeeId = parseInt(actionBtn.getAttribute("data-id"), 10);
      const cardId = actionBtn.getAttribute("data-card") || "";
      if (!action || !employeeId) return;
      await handleBioMenuAction(action, employeeId, cardId);
    });
  }

  document.addEventListener("click", (event) => {
    if (!event.target.closest(".bio-action-wrap")) {
      closeAllBioActionMenus();
    }
  });

  const enrollBtn = $("btnEnrollFingerprint");
  if (enrollBtn) {
    enrollBtn.addEventListener("click", async () => {
      const empId = $("biometricEmployeeSelect")?.value;
      if (!empId) { notify("Sélectionnez un employé", true); return; }
      if (enrollmentState.templates.length >= REQUIRED_FINGERPRINTS) return;

      const fpIcon = $("fpIcon");
      const fpStatus = $("fingerprintStatus");
      const fingerNum = enrollmentState.templates.length + 1;

      if (fpIcon) fpIcon.className = "fp-icon scanning";
      if (fpStatus) fpStatus.textContent = `Scan en cours — placez le doigt ${fingerNum}/${REQUIRED_FINGERPRINTS}...`;
      enrollBtn.disabled = true;

      try {
        const template = await scanFingerprintFromBridge();

        if (fpStatus) fpStatus.textContent = "Vérification anti-doublon...";
        await verifyFingerprintTemplate(template, empId, enrollmentState.templates);

        enrollmentState.templates.push(template);
        updateEnrollmentUI();

        if (enrollmentState.templates.length < REQUIRED_FINGERPRINTS) {
          if (fpIcon) fpIcon.className = "fp-icon success";
          if (fpStatus) {
            fpStatus.textContent = `Doigt ${fingerNum} enregistré — scannez le doigt ${fingerNum + 1}/${REQUIRED_FINGERPRINTS}`;
          }
          notify(`Doigt ${fingerNum}/${REQUIRED_FINGERPRINTS} capturé`);
          setTimeout(() => {
            if (fpIcon) fpIcon.className = "fp-icon";
          }, 2000);
          return;
        }

        if (fpStatus) fpStatus.textContent = "Enregistrement des 3 empreintes...";
        await api(`/api/biometric/enroll/${empId}`, {
          method: "POST",
          body: JSON.stringify({ templates: enrollmentState.templates }),
        });

        if (fpIcon) fpIcon.className = "fp-icon success";
        if (fpStatus) fpStatus.textContent = "Enrôlement terminé — 3 doigts enregistrés !";
        notify("Trois empreintes enrôlées avec succès");
        resetEnrollmentSession(true);
        await loadEnrolledEmployees();
      } catch (err) {
        if (fpIcon) fpIcon.className = "fp-icon error";
        const msg = err.message === "Failed to fetch"
          ? "Lecteur biométrique inaccessible — vérifiez que le service bridge est démarré sur le port 5002"
          : err.message;
        if (fpStatus) fpStatus.textContent = `Erreur : ${msg}`;
        notify(msg, true);
        const failedStep = $("fpProgress")?.querySelector(`.fp-step[data-step="${fingerNum}"]`);
        if (failedStep) failedStep.classList.add("error");
      } finally {
        if (enrollmentState.templates.length < REQUIRED_FINGERPRINTS) {
          enrollBtn.disabled = false;
          updateEnrollmentUI();
        }
      }
    });
  }

  // RFID assignment
  const rfidForm = $("rfidAssignForm");
  if (rfidForm) {
    rfidForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const empId  = $("rfidEmployeeId")?.value;
      const cardId = rfidForm.querySelector('[name="rfid_card_id"]')?.value?.trim();
      if (!empId || !cardId) { notify("Remplissez tous les champs", true); return; }
      try {
        await api("/api/biometric/rfid/assign", {
          method: "POST",
          body: JSON.stringify({ employee_id: parseInt(empId), rfid_card_id: cardId }),
        });
        notify("Carte RFID assignée avec succès");
        rfidForm.reset();
        await loadEnrolledEmployees();
      } catch (err) {
        notify(err.message, true);
      }
    });
  }

  // Refresh biometric status
  const refreshBioBtn = $("btnRefreshBiometricStatus");
  if (refreshBioBtn) {
    refreshBioBtn.addEventListener("click", () => checkBiometricBridgeStatus());
  }

  // Refresh enrolled list
  const refreshEnrolledBtn = $("btnRefreshEnrolled");
  if (refreshEnrolledBtn) {
    refreshEnrolledBtn.addEventListener("click", () => loadEnrolledEmployees());
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// MODULE 8 — Formation & Compétences
// ═══════════════════════════════════════════════════════════════════════════

async function loadTrainingSection() {
  await Promise.all([loadTrainings(), loadSkills()]);
  setupTrainingActions();
}

async function loadTrainings() {
  const trainings = await apiFetch("/api/trainings") || [];
  // Card view (primary)
  renderTrainingCards(trainings);
  // Keep old table hidden (used if trainingList is visible)
  const wrap = $("trainingList");
  if (wrap) {
    if (!trainings.length) { wrap.innerHTML = '<p class="text-muted">Aucune formation.</p>'; return; }
    const rows = trainings.map(t => `
      <tr>
        <td>${t.title}</td>
        <td>${t.trainer || "—"}</td>
        <td>${t.start_date || "—"}</td>
        <td>${t.end_date || "—"}</td>
        <td><span class="pill pill-${(t.status || "").replace(/ /g,'-')}">${t.status}</span></td>
        <td>${t.enrolled_count}/${t.max_participants}</td>
        <td>
          <button class="btn btn-secondary btn-sm" onclick="openTrainingDetail(${t.id})"><i class="ri-eye-line"></i></button>
          <button class="btn btn-danger btn-sm" onclick="deleteTraining(${t.id})"><i class="ri-delete-bin-line"></i></button>
        </td>
      </tr>`).join("");
    wrap.innerHTML = `<table class="data-table"><thead><tr><th>Titre</th><th>Formateur</th><th>Début</th><th>Fin</th><th>Statut</th><th>Inscrits</th><th></th></tr></thead><tbody>${rows}</tbody></table>`;
  }
}

function openTrainingDetail(id) {
  // Simple notification of details - could open a modal in the future
  notify(`Voir détail formation #${id}`);
}

async function loadSkills() {
  const skills = await apiFetch("/api/trainings/skills") || [];
  const wrap = $("skillList");
  if (!wrap) return;
  if (!skills.length) { wrap.innerHTML = '<p class="text-muted">Aucune compétence.</p>'; return; }
  const rows = skills.map(s => `<tr><td>${s.name}</td><td>${s.category || "—"}</td></tr>`).join("");
  wrap.innerHTML = `<table class="data-table"><thead><tr><th>Compétence</th><th>Catégorie</th></tr></thead><tbody>${rows}</tbody></table>`;
}

async function deleteTraining(id) {
  if (!confirm("Supprimer cette formation ?")) return;
  await apiFetch(`/api/trainings/${id}`, { method: "DELETE" });
  loadTrainings();
}

function setupTrainingActions() {
  const form = $("trainingForm");
  if (form && !form._bound) {
    form._bound = true;
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = formToObj(form);
      await apiFetch("/api/trainings", { method: "POST", body: JSON.stringify(data) });
      form.reset();
      notify("Formation créée");
      loadTrainings();
    });
  }
  const skillForm = $("skillForm");
  if (skillForm && !skillForm._bound) {
    skillForm._bound = true;
    skillForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const raw = formToObj(skillForm);
      await apiFetch("/api/trainings/skills", { method: "POST", body: JSON.stringify({ name: raw.skill_name, category: raw.skill_category }) });
      skillForm.reset();
      notify("Compétence ajoutée");
      loadSkills();
    });
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// MODULE 9 — Évaluation des performances
// ═══════════════════════════════════════════════════════════════════════════

async function loadPerformanceSection() {
  await Promise.all([loadEvaluations(), populateEvalEmployeeSelects()]);
  setupPerformanceActions();
}

async function loadEvaluations() {
  const evals = await apiFetch("/api/evaluations") || [];
  const wrap = $("evaluationList");
  // Render radar chart & top list
  renderPerfRadar(evals);
  renderPerfTopList(evals);
  if (!wrap) return;
  if (!evals.length) { wrap.innerHTML = '<p class="text-muted">Aucune évaluation.</p>'; return; }
  const rows = evals.map(ev => {
    const s = ev.score !== null ? `<span class="score-badge score-${scoreClass(ev.score)}">${ev.score}/100</span>` : "—";
    return `<tr>
      <td>${ev.employee_name || "—"}</td>
      <td>${ev.evaluator_name || "—"}</td>
      <td>${ev.period}</td>
      <td>${s}</td>
      <td><span class="pill">${ev.status}</span></td>
      <td>
        <button class="btn btn-danger btn-sm" onclick="deleteEvaluation(${ev.id})"><i class="ri-delete-bin-line"></i></button>
      </td>
    </tr>`;
  }).join("");
  wrap.innerHTML = `<table class="data-table"><thead><tr><th>Employé</th><th>Évaluateur</th><th>Période</th><th>Score</th><th>Statut</th><th></th></tr></thead><tbody>${rows}</tbody></table>`;

  // Stats
  const statsWrap = $("performanceStats");
  if (statsWrap) {
    const stats = await apiFetch("/api/evaluations/stats") || {};
    statsWrap.innerHTML = `
      <div class="kpi-card"><div class="kpi-label">Total</div><div class="kpi-value">${stats.total || 0}</div></div>
      <div class="kpi-card"><div class="kpi-label">Score moyen</div><div class="kpi-value">${stats.avg_score || 0}</div></div>
    `;
  }
}

function scoreClass(score) {
  if (score >= 80) return "excellent";
  if (score >= 60) return "good";
  if (score >= 40) return "average";
  return "low";
}

async function populateEvalEmployeeSelects() {
  const employees = await apiFetch("/api/employees") || [];
  ["evalEmployeeSelect", "evalEvaluatorSelect"].forEach(selId => {
    const sel = $(selId);
    if (!sel) return;
    const first = sel.options[0];
    sel.innerHTML = "";
    sel.appendChild(first);
    employees.forEach(emp => {
      const opt = document.createElement("option");
      opt.value = emp.id;
      opt.textContent = `${emp.first_name} ${emp.last_name}`;
      sel.appendChild(opt);
    });
  });
}

async function deleteEvaluation(id) {
  if (!confirm("Supprimer cette évaluation ?")) return;
  await apiFetch(`/api/evaluations/${id}`, { method: "DELETE" });
  loadEvaluations();
}

function setupPerformanceActions() {
  const form = $("evaluationForm");
  if (form && !form._bound) {
    form._bound = true;
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = formToObj(form);
      if (data.evaluator_id === "") delete data.evaluator_id;
      await apiFetch("/api/evaluations", { method: "POST", body: JSON.stringify(data) });
      form.reset();
      notify("Évaluation créée");
      loadEvaluations();
    });
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// MODULE 10 — Congés médicaux
// ═══════════════════════════════════════════════════════════════════════════

async function loadMedicalLeavesSection() {
  await populateMedEmployeeSelect();
  await loadMedicalLeaves();
  setupMedicalLeaveActions();
}

async function populateMedEmployeeSelect() {
  const sel = $("medEmployeeSelect");
  if (!sel) return;
  const employees = await apiFetch("/api/employees") || [];
  const first = sel.options[0];
  sel.innerHTML = "";
  sel.appendChild(first);
  employees.forEach(emp => {
    const opt = document.createElement("option");
    opt.value = emp.id;
    opt.textContent = `${emp.first_name} ${emp.last_name}`;
    sel.appendChild(opt);
  });
}

async function loadMedicalLeaves() {
  const leaves = await apiFetch("/api/medical-leaves") || [];
  const wrap = $("medicalLeaveList");
  if (!wrap) return;
  if (!leaves.length) { wrap.innerHTML = '<p class="text-muted">Aucun congé médical.</p>'; return; }
  const rows = leaves.map(ml => `<tr>
    <td>${ml.employee_name || "—"}</td>
    <td>${ml.start_date || "—"}</td>
    <td>${ml.end_date || "—"}</td>
    <td>${ml.diagnosis || "—"}</td>
    <td><span class="pill pill-${(ml.status || "").replace(/ /g,'-').toLowerCase()}">${ml.status}</span></td>
    <td>${ml.daily_allowance ? ml.daily_allowance.toLocaleString() + " FCFA" : "—"}</td>
    <td>
      <button class="btn btn-danger btn-sm" onclick="deleteMedicalLeave(${ml.id})"><i class="ri-delete-bin-line"></i></button>
    </td>
  </tr>`).join("");
  wrap.innerHTML = `<table class="data-table"><thead><tr><th>Employé</th><th>Début</th><th>Fin</th><th>Diagnostic</th><th>Statut</th><th>Indemnité/j</th><th></th></tr></thead><tbody>${rows}</tbody></table>`;
}

async function deleteMedicalLeave(id) {
  if (!confirm("Supprimer cet arrêt maladie ?")) return;
  await apiFetch(`/api/medical-leaves/${id}`, { method: "DELETE" });
  loadMedicalLeaves();
}

function setupMedicalLeaveActions() {
  const form = $("medicalLeaveForm");
  if (form && !form._bound) {
    form._bound = true;
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = formToObj(form);
      await apiFetch("/api/medical-leaves", { method: "POST", body: JSON.stringify(data) });
      form.reset();
      notify("Arrêt maladie déclaré");
      loadMedicalLeaves();
    });
  }
  const refreshBtn = $("btnRefreshMedical");
  if (refreshBtn && !refreshBtn._bound) {
    refreshBtn._bound = true;
    refreshBtn.addEventListener("click", () => loadMedicalLeaves());
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// MODULE 11 — Notifications & Alertes
// ═══════════════════════════════════════════════════════════════════════════

async function loadNotificationsSection() {
  await loadNotifications();
  setupNotificationActions();
}

async function loadNotifications() {
  const notifs = await apiFetch("/api/notifications") || [];
  renderNotificationsV2(notifs);
  updateNotifBadge();
}

async function markNotifRead(id) {
  await apiFetch(`/api/notifications/${id}/read`, { method: "PUT" });
  loadNotifications();
}

async function deleteNotif(id) {
  await apiFetch(`/api/notifications/${id}`, { method: "DELETE" });
  loadNotifications();
}

async function updateNotifBadge() {
  const data = await apiFetch("/api/notifications/unread-count");
  const badge = $("notifUnreadBadge");
  const dot   = $("topbarNotifDot");
  const count = data?.count || 0;
  if (badge) { badge.textContent = count; badge.classList.toggle("hidden", count === 0); }
  if (dot)   dot.classList.toggle("hidden", count === 0);
}

function setupNotificationActions() {
  const btnGen = $("btnGenerateAlerts");
  if (btnGen && !btnGen._bound) {
    btnGen._bound = true;
    btnGen.addEventListener("click", async () => {
      await apiFetch("/api/notifications/generate-alerts", { method: "POST" });
      notify("Alertes générées");
      loadNotifications();
    });
  }
  const btnAll = $("btnMarkAllRead");
  if (btnAll && !btnAll._bound) {
    btnAll._bound = true;
    btnAll.addEventListener("click", async () => {
      await apiFetch("/api/notifications/read-all", { method: "PUT" });
      loadNotifications();
    });
  }
  const form = $("notifForm");
  if (form && !form._bound) {
    form._bound = true;
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = formToObj(form);
      await apiFetch("/api/notifications", { method: "POST", body: JSON.stringify(data) });
      form.reset();
      notify("Notification envoyée");
      loadNotifications();
    });
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// MODULE 12 — Recrutement
// ═══════════════════════════════════════════════════════════════════════════

async function loadRecruitmentSection() {
  await Promise.all([loadJobOffers(), loadAllApplications(), populateJobDeptSelect()]);
  setupRecruitmentActions();
  // Load pipeline stats
  const apps = await apiFetch("/api/recruitment/applications") || [];
  const byStatus = apps.reduce((acc, a) => {
    const s = a.status || "Reçue";
    acc[s] = (acc[s] || 0) + 1;
    return acc;
  }, {});
  renderPipelineStats({ by_status: byStatus });
  // Pipeline refresh button
  const btnRefresh = $("btnRefreshPipeline");
  if (btnRefresh && !btnRefresh._bound) {
    btnRefresh._bound = true;
    btnRefresh.addEventListener("click", () => loadRecruitmentSection());
  }
}

async function populateJobDeptSelect() {
  const sel = $("jobDeptSelect");
  if (!sel) return;
  const depts = await apiFetch("/api/departments") || [];
  const first = sel.options[0];
  sel.innerHTML = "";
  sel.appendChild(first);
  depts.forEach(d => {
    const opt = document.createElement("option");
    opt.value = d.id;
    opt.textContent = d.name;
    sel.appendChild(opt);
  });
}

async function loadJobOffers() {
  const offers = await apiFetch("/api/recruitment/offers") || [];
  const wrap = $("jobOfferList");
  if (!wrap) return;
  if (!offers.length) { wrap.innerHTML = '<p class="text-muted">Aucune offre.</p>'; return; }
  const rows = offers.map(o => `<tr>
    <td>${o.title}</td>
    <td>${o.department_name || "—"}</td>
    <td><span class="pill pill-${o.status}">${o.status}</span></td>
    <td>${o.application_count}</td>
    <td>
      <button class="btn btn-danger btn-sm" onclick="deleteJobOffer(${o.id})"><i class="ri-delete-bin-line"></i></button>
    </td>
  </tr>`).join("");
  wrap.innerHTML = `<table class="data-table"><thead><tr><th>Poste</th><th>Département</th><th>Statut</th><th>Candidatures</th><th></th></tr></thead><tbody>${rows}</tbody></table>`;

  // Stats
  const statsWrap = $("recruitmentStats");
  if (statsWrap) {
    const stats = await apiFetch("/api/recruitment/stats") || {};
    statsWrap.innerHTML = `
      <div class="kpi-card"><div class="kpi-label">Offres ouvertes</div><div class="kpi-value">${stats.open_offers || 0}</div></div>
      <div class="kpi-card"><div class="kpi-label">Total candidatures</div><div class="kpi-value">${stats.total_applications || 0}</div></div>
    `;
  }
}

async function loadAllApplications() {
  const apps = await apiFetch("/api/recruitment/applications") || [];
  const wrap = $("applicationList");
  if (!wrap) return;
  if (!apps.length) { wrap.innerHTML = '<p class="text-muted">Aucune candidature.</p>'; return; }
  const rows = apps.slice(0, 20).map(a => `<tr>
    <td>${a.applicant_name}</td>
    <td>${a.applicant_email}</td>
    <td>${a.offer_title || "—"}</td>
    <td><span class="pill pill-${a.status}">${a.status}</span></td>
    <td>${a.interview_date ? new Date(a.interview_date).toLocaleDateString("fr") : "—"}</td>
    <td>
      <button class="btn btn-secondary btn-sm" onclick="updateApplicationStatus(${a.id}, 'retenu')"><i class="ri-check-line"></i></button>
      <button class="btn btn-danger btn-sm" onclick="updateApplicationStatus(${a.id}, 'refusé')"><i class="ri-close-line"></i></button>
    </td>
  </tr>`).join("");
  wrap.innerHTML = `<table class="data-table"><thead><tr><th>Candidat</th><th>Email</th><th>Offre</th><th>Statut</th><th>Entretien</th><th></th></tr></thead><tbody>${rows}</tbody></table>`;
}

async function deleteJobOffer(id) {
  if (!confirm("Supprimer cette offre ?")) return;
  await apiFetch(`/api/recruitment/offers/${id}`, { method: "DELETE" });
  loadJobOffers();
}

async function updateApplicationStatus(id, status) {
  await apiFetch(`/api/recruitment/applications/${id}`, { method: "PUT", body: JSON.stringify({ status }) });
  loadAllApplications();
}

function setupRecruitmentActions() {
  const form = $("jobOfferForm");
  if (form && !form._bound) {
    form._bound = true;
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = formToObj(form);
      if (!data.department_id) delete data.department_id;
      await apiFetch("/api/recruitment/offers", { method: "POST", body: JSON.stringify(data) });
      form.reset();
      notify("Offre publiée");
      loadJobOffers();
    });
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// MODULE 14 — Paramétrage système
// ═══════════════════════════════════════════════════════════════════════════

async function loadSettingsSection() {
  await Promise.all([loadSystemParameters(), loadHolidays()]);
  setupSettingsActions();
}

async function loadSystemParameters() {
  const params = await apiFetch("/api/settings/parameters") || [];
  const wrap = $("settingsParamList");
  if (!wrap) return;
  if (!params.length) {
    wrap.innerHTML = '<p class="text-muted">Aucun paramètre. Les paramètres par défaut seront créés au premier enregistrement.</p>';
    // Suggest default params
    const defaults = [
      { key: "company_name", value: "CNSS", description: "Nom de l'entreprise" },
      { key: "work_hours_per_day", value: "8", description: "Heures de travail par jour" },
      { key: "annual_leave_days", value: "24", description: "Jours de congé annuel" },
      { key: "overtime_rate", value: "1.5", description: "Taux heures supplémentaires" },
      { key: "currency", value: "FCFA", description: "Devise" },
    ];
    wrap.innerHTML = defaults.map(p => `
      <div class="settings-param-row">
        <label class="param-key" for="p_${p.key}">${p.description}</label>
        <input class="param-input" id="p_${p.key}" data-key="${p.key}" type="text" value="${p.value}" />
      </div>`).join("");
    return;
  }
  wrap.innerHTML = params.map(p => `
    <div class="settings-param-row">
      <label class="param-key" for="p_${p.key}">${p.description || p.key}</label>
      <input class="param-input" id="p_${p.key}" data-key="${p.key}" type="text" value="${p.value || ""}" />
    </div>`).join("");
}

async function loadHolidays() {
  const holidays = await apiFetch("/api/settings/holidays") || [];
  const wrap = $("holidayList");
  if (!wrap) return;
  if (!holidays.length) { wrap.innerHTML = '<p class="text-muted">Aucun jour férié.</p>'; return; }
  const rows = holidays.map(h => `<tr>
    <td>${h.name}</td>
    <td>${h.date || "—"}</td>
    <td>${h.is_recurring ? "Récurrent" : "Unique"}</td>
    <td>
      <button class="btn btn-danger btn-sm" onclick="deleteHoliday(${h.id})"><i class="ri-delete-bin-line"></i></button>
    </td>
  </tr>`).join("");
  wrap.innerHTML = `<table class="data-table"><thead><tr><th>Nom</th><th>Date</th><th>Type</th><th></th></tr></thead><tbody>${rows}</tbody></table>`;
}

async function deleteHoliday(id) {
  if (!confirm("Supprimer ce jour férié ?")) return;
  await apiFetch(`/api/settings/holidays/${id}`, { method: "DELETE" });
  loadHolidays();
}

function setupSettingsActions() {
  const btnSave = $("btnSaveParams");
  if (btnSave && !btnSave._bound) {
    btnSave._bound = true;
    btnSave.addEventListener("click", async () => {
      const inputs = document.querySelectorAll("#settingsParamList [data-key]");
      const parameters = Array.from(inputs).map(inp => ({ key: inp.dataset.key, value: inp.value }));
      await apiFetch("/api/settings/parameters/bulk", { method: "POST", body: JSON.stringify({ parameters }) });
      notify("Paramètres sauvegardés");
    });
  }
  const holidayForm = $("holidayForm");
  if (holidayForm && !holidayForm._bound) {
    holidayForm._bound = true;
    holidayForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = formToObj(holidayForm);
      await apiFetch("/api/settings/holidays", { method: "POST", body: JSON.stringify(data) });
      holidayForm.reset();
      notify("Jour férié ajouté");
      loadHolidays();
    });
  }
  const refreshHol = $("btnRefreshHolidays");
  if (refreshHol && !refreshHol._bound) {
    refreshHol._bound = true;
    refreshHol.addEventListener("click", () => loadHolidays());
  }
}

// ── Helper: convert form to plain object ──────────────────────────────────
function formToObj(form) {
  const fd = new FormData(form);
  const obj = {};
  fd.forEach((v, k) => { obj[k] = v === "" ? null : v; });
  return obj;
}

function init() {
  setReportsContent("Ouvre cette section pour charger le reporting.");
  setAccountingContent("Ouvre cette section pour charger la comptabilité.");
  renderOwnerAccountInfo();
  initThemeToggle();
  bindNavigation();
  bindForms();
  bindPasswordModal();
  setupAuthFlow();
  setupActions();
  setupBiometricActions();
  setupTeamActions();
  setupAttendanceSummaryDrawer();
  ensureSectionAccess();
  applyFormPermissions();
  setMustChangePassword(appState.mustChangePassword);
  // Poll notification badge every 60s when logged in
  setTimeout(() => { if (appState.token) updateNotifBadge(); }, 3000);
}

init();

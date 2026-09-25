/**
 * Client bridge ZK-9500 — parle au service Windows local (port 5002).
 * Si le bridge est arrêté, déclenche sgrhbridge:// (installeur) puis attend le démarrage.
 */
(function (global) {
  const DEFAULT_URL = "http://127.0.0.1:5002";
  const STORAGE_KEY = "sgrh_biometric_bridge_key";
  const PROTOCOL = "sgrhbridge://start";

  function bridgeUrl() {
    const meta = document.querySelector('meta[name="biometric-bridge-url"]');
    return (meta?.content || DEFAULT_URL).replace(/\/$/, "");
  }

  function configuredKey() {
    const meta = document.querySelector('meta[name="biometric-bridge-key"]');
    return (meta?.content || "local-secret-key").trim();
  }

  function storedKey() {
    try {
      return sessionStorage.getItem(STORAGE_KEY) || "";
    } catch {
      return "";
    }
  }

  function saveKey(key) {
    try {
      if (key) sessionStorage.setItem(STORAGE_KEY, key);
    } catch {
      /* ignore */
    }
  }

  function candidateKeys() {
    return [...new Set([storedKey(), configuredKey(), "local-secret-key"].filter(Boolean))];
  }

  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  /** Lance le bridge installé via protocole custom (geste utilisateur requis). */
  function launchInstalledBridge() {
    try {
      const iframe = document.createElement("iframe");
      iframe.style.display = "none";
      iframe.src = PROTOCOL;
      document.body.appendChild(iframe);
      setTimeout(() => iframe.remove(), 4000);
    } catch {
      /* ignore */
    }
    try {
      const a = document.createElement("a");
      a.href = PROTOCOL;
      a.style.display = "none";
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch {
      try {
        window.location.href = PROTOCOL;
      } catch {
        /* ignore */
      }
    }
  }

  async function fetchJson(path, options = {}) {
    const ctrl = new AbortController();
    const timeout = options.timeoutMs || 8000;
    const timer = setTimeout(() => ctrl.abort(), timeout);
    try {
      const res = await fetch(`${bridgeUrl()}${path}`, {
        ...options,
        signal: options.signal || ctrl.signal,
        headers: {
          Accept: "application/json",
          ...(options.body ? { "Content-Type": "application/json" } : {}),
          ...(options.headers || {}),
        },
      });
      const text = await res.text();
      let data = {};
      try {
        data = text ? JSON.parse(text) : {};
      } catch {
        data = { raw: text };
      }
      return { res, data };
    } finally {
      clearTimeout(timer);
    }
  }

  async function status() {
    try {
      const { res, data } = await fetchJson("/status", { method: "GET", timeoutMs: 2500 });
      if (!res.ok) {
        return { ok: false, status: "error", message: "Bridge local inaccessible" };
      }
      return {
        ok: data.status === "ok" || res.ok,
        status: data.status || "ok",
        message: "Lecteur biométrique local connecté (port 5002)",
        connected: true,
      };
    } catch {
      return {
        ok: false,
        status: "offline",
        connected: false,
        message:
          "Bridge non détecté — installation SGRH Fingerprint Bridge requise sur ce PC.",
      };
    }
  }

  /**
   * Vérifie le bridge ; s'il est offline, lance l'installeur via sgrhbridge:// et attend.
   */
  async function ensureRunning(options = {}) {
    const waitMs = options.waitMs || 20000;
    const onProgress = typeof options.onProgress === "function" ? options.onProgress : null;

    let st = await status();
    if (st.ok) return st;

    if (onProgress) onProgress("Démarrage du bridge biométrique…");
    launchInstalledBridge();

    const started = Date.now();
    while (Date.now() - started < waitMs) {
      await sleep(700);
      st = await status();
      if (st.ok) {
        if (onProgress) onProgress("Bridge prêt");
        return st;
      }
    }

    throw new Error(
      "Impossible de démarrer le bridge. Installez SGRH Fingerprint Bridge (INSTALLER.bat) sur ce PC Windows, branchez le ZK-9500, puis réessayez."
    );
  }

  async function pair() {
    const { res, data } = await fetchJson("/pair", {
      method: "POST",
      body: JSON.stringify({ appName: "SGRH Pro CNSS" }),
      timeoutMs: 120000,
    });
    if (!res.ok) {
      throw new Error(data.error || data.detail || "Appariement bridge refusé");
    }
    if (data.apiKey) saveKey(data.apiKey);
    return data.apiKey;
  }

  async function withApiKey(requestFn) {
    let lastErr = null;
    for (const key of candidateKeys()) {
      try {
        const result = await requestFn(key);
        if (result.unauthorized) {
          lastErr = new Error("Clé API bridge invalide");
          continue;
        }
        if (key) saveKey(key);
        return result.data;
      } catch (e) {
        lastErr = e;
      }
    }

    try {
      const paired = await pair();
      if (paired) {
        const result = await requestFn(paired);
        if (!result.unauthorized) return result.data;
      }
    } catch (e) {
      lastErr = e;
    }

    throw lastErr || new Error("Impossible d'authentifier le bridge local");
  }

  async function scan(options = {}) {
    await ensureRunning(options);
    return withApiKey(async (key) => {
      const { res, data } = await fetchJson("/scan", {
        method: "POST",
        headers: { "X-API-KEY": key },
        body: "{}",
        timeoutMs: 35000,
      });
      if (res.status === 401 || res.status === 403) {
        return { unauthorized: true };
      }
      if (!res.ok) {
        throw new Error(data.error || data.detail || data.title || `Échec scan (HTTP ${res.status})`);
      }
      if (!data.template) {
        throw new Error("Aucun gabarit reçu du lecteur");
      }
      return { data };
    });
  }

  /**
   * @param {string} probeTemplate
   * @param {Array<{id:number, template_b64:string}>} gallery
   */
  async function match(probeTemplate, gallery) {
    await ensureRunning();
    return withApiKey(async (key) => {
      const { res, data } = await fetchJson("/match", {
        method: "POST",
        headers: { "X-API-KEY": key },
        body: JSON.stringify({
          probe_template: probeTemplate,
          gallery: gallery || [],
        }),
        timeoutMs: 35000,
      });
      if (res.status === 401 || res.status === 403) {
        return { unauthorized: true };
      }
      if (res.status === 404) {
        throw new Error(
          "Ce bridge ne gère pas /match — réinstallez Fingerprint Bridge (INSTALLER.bat)."
        );
      }
      if (!res.ok) {
        throw new Error(data.error || data.detail || data.title || `Échec match (HTTP ${res.status})`);
      }
      return { data };
    });
  }

  global.LocalBiometricBridge = {
    bridgeUrl,
    status,
    ensureRunning,
    launchInstalledBridge,
    scan,
    match,
    pair,
    PROTOCOL,
  };
})(window);

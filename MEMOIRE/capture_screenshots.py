# -*- coding: utf-8 -*-
"""
Captures d'écran SGRH Pro pour le chapitre IV du mémoire.
Prérequis : php artisan serve sur http://127.0.0.1:8000
"""
from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"
OUT_DIR = Path(r"b:\LARIS\KEVANA\FINAL\bong\MEMOIRE\images\chapitre4")
VIEWPORT = {"width": 1440, "height": 900}


def wait_ms(ms: int) -> None:
    time.sleep(ms / 1000)


def clear_session(page) -> None:
    try:
        page.evaluate(
            """() => {
              localStorage.removeItem('ems_token');
              localStorage.removeItem('ems_username');
              localStorage.removeItem('ems_role');
              localStorage.removeItem('ems_permissions');
              localStorage.removeItem('ems_must_change_password');
            }"""
        )
    except Exception:
        pass


def login(page, username: str, password: str) -> None:
    clear_session(page)
    page.goto(BASE_URL, wait_until="networkidle")
    wait_ms(800)

    if page.locator("#appShell:not(.hidden)").count():
        page.click("#logoutBtn")
        page.wait_for_selector("#loginScreen:not(.hidden)", timeout=10000)
        wait_ms(500)

    page.fill("#username", username)
    page.fill("#password", password)
    page.click("#loginSubmitBtn")
    page.wait_for_selector("#appShell:not(.hidden)", timeout=20000)
    wait_ms(2500)


def navigate(page, section: str) -> None:
    page.evaluate(f"navigate('{section}')")
    page.wait_for_selector(f"#section-{section}.active", timeout=15000)
    wait_ms(2800)


def shot_login(page, path: Path) -> None:
    page.goto(BASE_URL, wait_until="networkidle")
    clear_session(page)
    page.reload(wait_until="networkidle")
    page.wait_for_selector("#loginScreen", timeout=10000)
    wait_ms(1200)
    page.locator(".login-screen").screenshot(path=str(path))


def shot_app(page, path: Path) -> None:
    page.locator("#appShell").screenshot(path=str(path))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    shots = {
        "fig_iv1_login.png": None,
        "fig_iv2_dashboard.png": ("adminrh", "adminrh123", "overview"),
        "fig_iv3_pointage.png": ("adminrh", "adminrh123", "punch"),
        "fig_iv4_mon_espace.png": ("agent", "Agent@123", "myspace"),
        "fig_iv5_enrolement.png": ("adminrh", "adminrh123", "biometric"),
        "fig_iv6_conges.png": ("adminrh", "adminrh123", "leaves"),
        "fig_iv7_employes.png": ("adminrh", "adminrh123", "employees"),
        "fig_iv8_rapports.png": ("adminrh", "adminrh123", "reports"),
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport=VIEWPORT, device_scale_factor=1.25)
        page = context.new_page()

        print("Capture login…")
        shot_login(page, OUT_DIR / "fig_iv1_login.png")

        current_user = None
        for filename, cfg in shots.items():
            if cfg is None:
                continue
            user, pwd, section = cfg
            if user != current_user:
                print(f"Connexion {user}…")
                login(page, user, pwd)
                current_user = user
            print(f"  -> {section} -> {filename}")
            navigate(page, section)
            if section == "overview":
                page.evaluate("window.scrollTo(0, 0)")
                wait_ms(500)
            if section == "reports":
                page.evaluate(
                    """async () => {
                      if (typeof loadReportsSection === 'function') await loadReportsSection();
                    }"""
                )
                wait_ms(2000)
            shot_app(page, OUT_DIR / filename)

        browser.close()

    print(f"\nCaptures enregistrées dans {OUT_DIR}")
    for f in sorted(OUT_DIR.glob("fig_iv*.png")):
        print(f"  - {f.name} ({f.stat().st_size // 1024} Ko)")


if __name__ == "__main__":
    main()

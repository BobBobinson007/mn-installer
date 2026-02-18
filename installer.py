#!/usr/bin/env python3
"""
MacroNotes Installer
Klont das GitHub-Repo nach ~/MacroNotes und generiert die config.json interaktiv.
"""

import os
import sys
import json
import subprocess
import importlib.util
import re

# ─── Farben ───────────────────────────────────────────────────────────────────
GREEN  = "\033[32m"
WHITE  = "\033[37m"
YELLOW = "\033[33m"
RED    = "\033[31m"
CYAN   = "\033[36m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
DIM    = "\033[2m"

# ─── Konfiguration ────────────────────────────────────────────────────────────
REPO_URL    = "https://github.com/BobBobinson007/Macro-Notes.git"
INSTALL_DIR = os.path.join(os.path.expanduser("~"), "MacroNotes")  # z.B. /tom/MacroNotes
CONFIG_FILE = "config.json"

SCHEMES = [
    {"name": "Standard", "color_name": "White",   "color_code": "\u001b[37m", "highlight_code": "\u001b[1m"},
    {"name": "Alice",    "color_name": "Magenta",  "color_code": "\u001b[35m", "highlight_code": "\u001b[1m"},
    {"name": "Charlie",  "color_name": "Green",    "color_code": "\u001b[32m", "highlight_code": "\u001b[1m"},
    {"name": "Daisy",    "color_name": "Yellow",   "color_code": "\u001b[33m", "highlight_code": "\u001b[1m"},
    {"name": "Eddie",    "color_name": "Blue",     "color_code": "\u001b[34m", "highlight_code": "\u001b[1m"},
    {"name": "Fiona",    "color_name": "Red",      "color_code": "\u001b[31m", "highlight_code": "\u001b[1m"},
]

REQUIRED_PACKAGES = {
    "readchar": "readchar",
}

BOX_W = 60

# ─── UI Helpers ───────────────────────────────────────────────────────────────

def clr():
    print("\033[H\033[J", end="")

def visible_len(s):
    return len(re.sub(r'\x1b\[[0-9;]*m', '', s))

def pad_to(s, width):
    return s + " " * max(0, width - visible_len(s))

def box_top(fc, title=""):
    if title:
        t      = f" {title} "
        dashes = BOX_W - len(t)
        l, r   = dashes // 2, dashes - dashes // 2
        print(f"  {fc}╭{'─'*l}{t}{'─'*r}╮{RESET}")
    else:
        print(f"  {fc}╭{'─'*BOX_W}╮{RESET}")

def box_sep(fc):
    print(f"  {fc}├{'─'*BOX_W}┤{RESET}")

def box_bot(fc):
    print(f"  {fc}╰{'─'*BOX_W}╯{RESET}")

def box_row(fc, content=""):
    inner_w = BOX_W - 2
    padded  = pad_to(content, inner_w)
    print(f"  {fc}│{RESET} {padded} {fc}│{RESET}")

def box_empty(fc):
    box_row(fc, "")

def draw_header(fc=WHITE):
    print(f"\n{fc}       ╭────────────────────────────────────────────────────────────╮")
    print(r"       │   \  |                           \ |          |               │")
    print(r"       │  |\/ |   _` |   _|   _| _ \     .  |   _ \   _|   -_) (_-<  │")
    print(r"       │ _|  _| \__,_| \__| _| \___/    _|\_| \___/ \__| \___| ___/ │")
    print(f"       ╰────────────────────────────── INSTALLER ─────────────────────╯{RESET}")
    print()

def status_line(fc, icon, label, value="", vc=WHITE):
    content = f"{icon} {label:<28} {vc}{value}{RESET}"
    box_row(fc, content)

def pause(msg="  Enter drücken..."):
    input(f"\n{DIM}{msg}{RESET}")

def confirm(prompt):
    return input(f"  {prompt} {DIM}[j/N]{RESET}: ").strip().lower() == "j"

# ─── Schritt 1: Git prüfen ────────────────────────────────────────────────────

def check_git(fc):
    result = subprocess.run(["git", "--version"], capture_output=True, text=True)
    if result.returncode != 0:
        clr(); draw_header(fc)
        box_top(fc, "FEHLER – GIT NICHT GEFUNDEN")
        box_empty(fc)
        box_row(fc, f"{RED}Git ist nicht installiert!{RESET}")
        box_empty(fc)
        box_row(fc, "Bitte installiere Git und starte den Installer erneut:")
        box_empty(fc)
        box_row(fc, f"  {CYAN}https://git-scm.com/downloads{RESET}")
        box_empty(fc)
        box_bot(fc)
        pause("Enter zum Beenden...")
        sys.exit(1)
    return result.stdout.strip()

# ─── Schritt 2: Python-Pakete prüfen & installieren ──────────────────────────

def check_packages(fc):
    clr(); draw_header(fc)
    box_top(fc, "SCHRITT 1 – BIBLIOTHEKEN")
    box_empty(fc)
    box_row(fc, f"{BOLD}Prüfe benötigte Python-Pakete...{RESET}")
    box_sep(fc)
    box_empty(fc)

    missing = []
    for module, package in REQUIRED_PACKAGES.items():
        if importlib.util.find_spec(module) is not None:
            status_line(fc, f"{GREEN}✓{RESET}", module, "installiert", GREEN)
        else:
            status_line(fc, f"{RED}✗{RESET}", module, "fehlt", RED)
            missing.append(package)

    box_empty(fc)
    box_bot(fc)

    if missing:
        print(f"\n  {YELLOW}Installiere fehlende Pakete...{RESET}\n")
        for pkg in missing:
            print(f"  {CYAN}pip install {pkg}{RESET}")
            res = subprocess.run(
                [sys.executable, "-m", "pip", "install", pkg],
                capture_output=True, text=True
            )
            if res.returncode == 0:
                print(f"  {GREEN}✓ {pkg} installiert.{RESET}")
            else:
                print(f"  {RED}✗ Fehler:{RESET}")
                print(f"  {DIM}{res.stderr.strip()[:200]}{RESET}")
                print(f"\n  {YELLOW}Manuell ausführen: pip install {pkg}{RESET}")
                pause("Enter zum Beenden...")
                sys.exit(1)
    else:
        print(f"\n  {GREEN}Alle Pakete vorhanden!{RESET}")

    pause()

# ─── Schritt 3: Name konfigurieren ───────────────────────────────────────────

def configure_name(fc):
    clr(); draw_header(fc)
    box_top(fc, "SCHRITT 2 – DEIN NAME")
    box_empty(fc)
    box_row(fc, "Wie soll MacroNotes dich nennen?")
    box_empty(fc)
    box_row(fc, f"{DIM}Erscheint in der Abschiedsnachricht beim Beenden.{RESET}")
    box_empty(fc)
    box_bot(fc)
    print()
    raw = input(f"  {WHITE}Name{RESET} {DIM}[Standard: User]{RESET}: ").strip()
    return raw if raw else "User"

# ─── Schritt 4: Farbschema wählen ────────────────────────────────────────────

COLOR_PREVIEW = {
    "White":   "\033[37m",
    "Magenta": "\033[35m",
    "Green":   "\033[32m",
    "Yellow":  "\033[33m",
    "Blue":    "\033[34m",
    "Red":     "\033[31m",
}

def configure_design(fc):
    try:
        import readchar as rc
        sel = 0
        while True:
            clr(); draw_header(fc)
            box_top(fc, "SCHRITT 3 – FARBSCHEMA")
            box_empty(fc)
            box_row(fc, "Wähle dein Farbschema:")
            box_sep(fc)
            box_empty(fc)
            for i, s in enumerate(SCHEMES):
                cc = COLOR_PREVIEW.get(s["color_name"], WHITE)
                if i == sel:
                    marker = f"{GREEN}●{RESET}"
                    label  = f"{cc}{BOLD}  {s['name']:<12} ({s['color_name']}){RESET}"
                else:
                    marker = f"{DIM}○{RESET}"
                    label  = f"{DIM}  {s['name']:<12} ({s['color_name']}){RESET}"
                box_row(fc, f"{marker} {label}")
            box_empty(fc)
            box_row(fc, f"{DIM}↑ ↓ Navigieren    Enter Bestätigen{RESET}")
            box_empty(fc)
            box_bot(fc)

            key = rc.readkey()
            if key == rc.key.UP:
                sel = (sel - 1) % len(SCHEMES)
            elif key == rc.key.DOWN:
                sel = (sel + 1) % len(SCHEMES)
            elif key == rc.key.ENTER:
                return SCHEMES[sel]

    except Exception:
        # Fallback ohne readchar (z.B. vor der Installation)
        clr(); draw_header(fc)
        box_top(fc, "SCHRITT 3 – FARBSCHEMA")
        box_empty(fc)
        for i, s in enumerate(SCHEMES):
            cc = COLOR_PREVIEW.get(s["color_name"], WHITE)
            box_row(fc, f"  {WHITE}[{i+1}]{RESET}  {cc}{s['name']:<12}{RESET} ({s['color_name']})")
        box_empty(fc)
        box_bot(fc)
        print()
        while True:
            raw = input(f"  Auswahl {DIM}[1–{len(SCHEMES)}]{RESET}: ").strip()
            try:
                idx = int(raw) - 1
                if 0 <= idx < len(SCHEMES):
                    return SCHEMES[idx]
            except ValueError:
                pass
            print(f"  {RED}Ungültige Eingabe.{RESET}")

# ─── Schritt 5: API-Port festlegen ───────────────────────────────────────────

def configure_port(fc):
    clr(); draw_header(fc)
    box_top(fc, "SCHRITT 4 – API-PORT")
    box_empty(fc)
    box_row(fc, "Auf welchem Port soll der API-Server laufen?")
    box_empty(fc)
    box_row(fc, f"{DIM}Standard: 8080    Bereich: 1024 – 65535{RESET}")
    box_empty(fc)
    box_row(fc, f"{DIM}Später änderbar: Settings → Developer → Port ändern{RESET}")
    box_empty(fc)
    box_bot(fc)
    print()
    while True:
        raw = input(f"  {WHITE}Port{RESET} {DIM}[Standard: 8080]{RESET}: ").strip()
        if raw == "":
            return 8080
        try:
            p = int(raw)
            if 1024 <= p <= 65535:
                return p
            print(f"  {RED}Muss zwischen 1024 und 65535 liegen.{RESET}")
        except ValueError:
            print(f"  {RED}Bitte eine Zahl eingeben.{RESET}")

# ─── Schritt 6: git clone ────────────────────────────────────────────────────

def clone_repo(fc):
    clr(); draw_header(fc)
    box_top(fc, "SCHRITT 5 – GIT CLONE")
    box_empty(fc)
    box_row(fc, "Klone Repository von GitHub...")
    box_empty(fc)
    box_row(fc, f"{DIM}{REPO_URL}{RESET}")
    box_empty(fc)
    box_row(fc, f"Ziel: {CYAN}{INSTALL_DIR}{RESET}")
    box_empty(fc)
    box_bot(fc)
    print()

    # Prüfe ob Ordner schon existiert
    if os.path.exists(INSTALL_DIR):
        print(f"  {YELLOW}! Ordner existiert bereits:{RESET}")
        print(f"  {CYAN}{INSTALL_DIR}{RESET}\n")
        if confirm("Vorhandenen Ordner löschen und neu klonen?"):
            import shutil
            shutil.rmtree(INSTALL_DIR)
            print(f"  {GREEN}✓ Alter Ordner entfernt.{RESET}\n")
        else:
            print(f"\n  {YELLOW}Vorhandenen Ordner wird verwendet.{RESET}")
            pause()
            return

    print(f"  {CYAN}$ git clone {REPO_URL}{RESET}\n")

    result = subprocess.run(
        ["git", "clone", REPO_URL, INSTALL_DIR],
        text=True
    )

    if result.returncode == 0:
        print(f"\n  {GREEN}✓ Repository erfolgreich geklont!{RESET}")

        # Zeige geklonte Dateien
        print(f"\n  {DIM}Inhalt von {INSTALL_DIR}:{RESET}")
        try:
            files = os.listdir(INSTALL_DIR)
            for f in sorted(files):
                if not f.startswith("."):
                    print(f"    {DIM}•{RESET} {f}")
        except Exception:
            pass
    else:
        print(f"\n  {RED}✗ git clone fehlgeschlagen.{RESET}")
        print(f"  {YELLOW}Prüfe Internetverbindung und Repo-URL.{RESET}")
        pause("Enter zum Beenden...")
        sys.exit(1)

    pause()

# ─── Schritt 7: config.json schreiben ────────────────────────────────────────

def write_config(name, design, port, fc):
    config = {
        "name": name,
        "design": design,
        "api_port": port
    }
    config_path = os.path.join(INSTALL_DIR, CONFIG_FILE)

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    clr(); draw_header(fc)
    box_top(fc, "SCHRITT 6 – KONFIGURATION")
    box_empty(fc)
    box_row(fc, f"{GREEN}{BOLD}config.json erfolgreich erstellt!{RESET}")
    box_sep(fc)
    box_empty(fc)
    status_line(fc, f"{GREEN}✓{RESET}", "Name",        name,                 WHITE)
    status_line(fc, f"{GREEN}✓{RESET}", "Farbschema",  design["name"],       WHITE)
    status_line(fc, f"{GREEN}✓{RESET}", "Farbe",       design["color_name"], WHITE)
    status_line(fc, f"{GREEN}✓{RESET}", "API-Port",    str(port),            WHITE)
    box_empty(fc)
    box_sep(fc)
    box_empty(fc)
    box_row(fc, f"{DIM}Gespeichert unter:{RESET}")
    box_row(fc, f"  {CYAN}{config_path}{RESET}")
    box_empty(fc)
    box_bot(fc)
    pause()

# ─── Abschluss ────────────────────────────────────────────────────────────────

def show_finish(fc, name):
    clr(); draw_header(fc)
    box_top(fc, "INSTALLATION ABGESCHLOSSEN")
    box_empty(fc)
    box_row(fc, f"{GREEN}{BOLD}MacroNotes ist startklar, {name}!{RESET}")
    box_empty(fc)
    box_sep(fc)
    box_empty(fc)
    box_row(fc, f"{BOLD}So startest du MacroNotes:{RESET}")
    box_empty(fc)
    box_row(fc, f"  {CYAN}cd {INSTALL_DIR}{RESET}")
    box_row(fc, f"  {CYAN}python main.py{RESET}")
    box_empty(fc)
    box_sep(fc)
    box_empty(fc)
    box_row(fc, f"{DIM}Installationsordner:{RESET}")
    box_row(fc, f"  {INSTALL_DIR}")
    box_empty(fc)
    box_bot(fc)
    print(f"\n  {GREEN}Viel Spaß mit MacroNotes!{RESET}\n")

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    fc = WHITE  # Startfarbe vor Nutzerwahl

    clr(); draw_header(fc)
    box_top(fc, "WILLKOMMEN")
    box_empty(fc)
    box_row(fc, f"{BOLD}MacroNotes Setup-Assistent{RESET}")
    box_empty(fc)
    box_row(fc, "Der Installer wird:")
    box_empty(fc)
    box_row(fc, f"  {GREEN}1.{RESET}  Python-Pakete prüfen & installieren")
    box_row(fc, f"  {GREEN}2.{RESET}  Deinen Namen konfigurieren")
    box_row(fc, f"  {GREEN}3.{RESET}  Ein Farbschema auswählen")
    box_row(fc, f"  {GREEN}4.{RESET}  Den API-Port festlegen")
    box_row(fc, f"  {GREEN}5.{RESET}  Repo klonen nach:")
    box_row(fc, f"        {CYAN}{INSTALL_DIR}{RESET}")
    box_row(fc, f"  {GREEN}6.{RESET}  config.json generieren")
    box_empty(fc)
    box_bot(fc)
    print()

    if not confirm(f"{WHITE}Installation starten?{RESET}"):
        print(f"\n  {YELLOW}Installation abgebrochen.{RESET}\n")
        sys.exit(0)

    # Git prüfen (sofort, bevor wir weitermachen)
    git_ver = check_git(fc)
    print(f"\n  {GREEN}✓ {git_ver}{RESET}")
    import time; time.sleep(0.8)

    # Schritte durchlaufen
    check_packages(fc)
    name   = configure_name(fc)
    design = configure_design(fc)
    fc     = design["color_code"]   # Ab hier: gewählte Farbe
    port   = configure_port(fc)
    clone_repo(fc)
    write_config(name, design, port, fc)
    show_finish(fc, name)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}Installation durch Benutzer abgebrochen.{RESET}\n")
        sys.exit(0)

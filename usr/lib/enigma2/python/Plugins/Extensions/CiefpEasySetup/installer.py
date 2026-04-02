# -*- coding: utf-8 -*-
import os
import json
import subprocess
import time
from enigma import eTimer
import logging

logging.basicConfig(filename="/tmp/ciefpeasysetup.log", level=logging.DEBUG, 
                   format="%(asctime)s - %(levelname)s - %(message)s")

STATUS_FILE = "/etc/enigma2/ciefpeasysetup_status.json"

def load_status():
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {
        "phase1_done": False,
        "phase2_done": False,
        "phase3_done": False,
        "plugins": {}
    }

def save_status(data):
    try:
        with open(STATUS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logging.error(f"Ne mogu da sačuvam status: {e}")

def run_command(cmd, skip_reboot=False):
    env = os.environ.copy()
    if skip_reboot:
        env["SKIP_REBOOT"] = "1"
    
    try:
        logging.info(f"Pokrećem: {cmd[:100]}... (SKIP_REBOOT={skip_reboot})")
        result = subprocess.run(cmd, shell=True, env=env, timeout=240, capture_output=True, text=True)
        success = result.returncode == 0
        if not success:
            logging.warning(f"Neuspeh (code {result.returncode}): {result.stderr[:300]}")
        return success
    except Exception as e:
        logging.error(f"Greška pri izvršavanju komande: {e}")
        return False


def check_system_for_plugins(plugins_db):
    installed_names = []

    # 1. Folderi ekstenzija
    ext_path = "/usr/lib/enigma2/python/Plugins/Extensions/"
    present_folders = os.listdir(ext_path) if os.path.exists(ext_path) else []

    # 2. OPKG paketi
    try:
        all_opkg = subprocess.check_output("opkg list_installed | cut -d' ' -f1", shell=True, text=True)
    except:
        all_opkg = ""

    # 3. Lista svih .conf fajlova u opkg folderu (za secret-feed)
    opkg_conf_path = "/etc/opkg/"
    present_confs = os.listdir(opkg_conf_path) if os.path.exists(opkg_conf_path) else []

    for p in plugins_db:
        name = p.get("name")
        cmd = p.get("command", "")

        # --- PROVERA ZA FEED (PO NAZIVU FAJLA) ---
        if "secret-feed" in name.lower() or "secret-feed" in cmd:
            if "cortexa15hf-neon-vfpv4-3rdparty-secret-feed.conf" in present_confs:
                installed_names.append(name)
                continue

        # --- PROVERA ZA OPKG ---
        if "opkg install" in cmd:
            package_name = cmd.split("install ")[-1].strip()
            if package_name in all_opkg:
                installed_names.append(name)
                continue

        # --- PROVERA FOLDERA (Sa podrškom za OpenPLi nazive) ---
        folder_guess = name.replace(" ", "")

        # Mapiranje imena plugina na moguće nazive foldera
        # Za Abertis proveravamo oba potencijalna foldera
        remap = {
            "AjPanel": "AJPan",
            "Vavoo": "vavoo",
            "CiefpSettingsT2miAbertis": ["CiefpSettingsT2miAbertis", "CiefpSettingsT2miAbertisOpenPLi"]
        }

        target = remap.get(name, folder_guess)

        if isinstance(target, list):
            # Ako je lista, proveri da li bilo koji od ponuđenih foldera postoji
            if any(f in present_folders for f in target):
                installed_names.append(name)
        else:
            # Standardna provera jednog foldera
            if target in present_folders:
                installed_names.append(name)

    return installed_names

# -*- coding: utf-8 -*-
import os
import json
import subprocess
import time
import logging
from enigma import eTimer

# Konfiguracija logovanja
logging.basicConfig(filename="/tmp/ciefpeasysetup.log", level=logging.DEBUG, 
                   format="%(asctime)s - %(levelname)s - %(message)s")

STATUS_FILE = "/etc/enigma2/ciefpeasysetup_status.json"

# --- NOVE POMOĆNE FUNKCIJE ---

def get_image_name():
    """Detektuje koji se imidž koristi (openatv, pure2, itd.)"""
    try:
        # Provera preko /etc/image-version (OpenATV, Pure2...)
        if os.path.exists("/etc/image-version"):
            with open("/etc/image-version", "r") as f:
                content = f.read().lower()
                if "openatv" in content: return "openatv"
                if "pure2" in content: return "pure2"
        
        # Provera preko /etc/issue (OpenPLi i ostali)
        if os.path.exists("/etc/issue"):
            with open("/etc/issue", "r") as f:
                content = f.read().lower()
                if "openatv" in content: return "openatv"
                if "pure2" in content: return "pure2"
                if "openpli" in content: return "openpli"
    except Exception as e:
        logging.error(f"Greška pri detekciji imidža: {e}")
    return "unknown"

def check_system_for_plugins(plugins_db):
    """Proverava šta je već instalirano na sistemu"""
    installed_names = []
    
    # Putanje za foldere (Extensions + SystemPlugins)
    ext_path = "/usr/lib/enigma2/python/Plugins/Extensions/"
    sys_path = "/usr/lib/enigma2/python/Plugins/SystemPlugins/"
    
    present_folders = []
    if os.path.exists(ext_path):
        present_folders.extend(os.listdir(ext_path))
    if os.path.exists(sys_path):
        present_folders.extend(os.listdir(sys_path))

    # Lista instaliranih OPKG paketa
    try:
        all_opkg = subprocess.check_output("opkg list_installed | cut -d' ' -f1", shell=True, text=True)
    except:
        all_opkg = ""

    # OPKG konfiguracije (za feed)
    opkg_conf_path = "/etc/opkg/"
    present_confs = os.listdir(opkg_conf_path) if os.path.exists(opkg_conf_path) else []

    for p in plugins_db:
        name = p.get("name")
        cmd = p.get("command", "")

        # 1. Provera za OSCam (Binarni fajlovi)
        if "oscam" in name.lower():
            if any(os.path.exists(path) for path in ["/usr/bin/oscam", "/usr/bin/oscam-emu", "/usr/bin/oscam_emu"]):
                installed_names.append(name)
                continue

        # 2. Provera za FEED
        if "secret-feed" in name.lower() or "secret-feed" in cmd:
            if "cortexa15hf-neon-vfpv4-3rdparty-secret-feed.conf" in present_confs:
                installed_names.append(name)
                continue

        # 3. Provera za OPKG
        if "opkg install" in cmd:
            package_name = cmd.split("install ")[-1].strip()
            if package_name in all_opkg:
                installed_names.append(name)
                continue

        # 4. Provera foldera (NewVirtualKeyBoard i ostali)
        folder_guess = name.replace(" ", "")
        remap = {
            "AjPanel": "AJPan",
            "Vavoo": "vavoo",
            "CiefpSettingsT2miAbertis": ["CiefpSettingsT2miAbertis", "CiefpSettingsT2miAbertisOpenPLi"],
            "NewVirtualKeyBoard": "NewVirtualKeyBoard"
        }
        target = remap.get(name, folder_guess)

        if isinstance(target, list):
            if any(f in present_folders for f in target):
                installed_names.append(name)
        else:
            if target in present_folders:
                installed_names.append(name)

    return installed_names

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

def run_installation(plugins_to_install, callback=None):
    current_image = get_image_name()
    status = load_status()
    total = len(plugins_to_install)

    for i, p in enumerate(plugins_to_install):
        name = p.get("name", "")
        
        # Filtriranje po imidžu
        if "secret-feed" in name.lower() and current_image != "openatv":
            continue
        if "subssupport" in name.lower() and current_image == "pure2":
            continue

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

    # 1. Priprema putanja za foldere (Ekstenzije + Sistemski plugini)
    ext_path = "/usr/lib/enigma2/python/Plugins/Extensions/"
    sys_path = "/usr/lib/enigma2/python/Plugins/SystemPlugins/"

    present_folders = []
    if os.path.exists(ext_path):
        present_folders.extend(os.listdir(ext_path))
    if os.path.exists(sys_path):
        present_folders.extend(os.listdir(sys_path))

    # 2. Dobavljanje liste instaliranih OPKG paketa
    try:
        # Uzimamo samo prvu kolonu (ime paketa) radi lakšeg poređenja
        all_opkg = subprocess.check_output("opkg list_installed | cut -d' ' -f1", shell=True, text=True)
    except:
        all_opkg = ""

    # 3. Provera konfiguracija za feed-ove
    opkg_conf_path = "/etc/opkg/"
    present_confs = os.listdir(opkg_conf_path) if os.path.exists(opkg_conf_path) else []

    for p in plugins_db:
        name = p.get("name")
        cmd = p.get("command", "")

        # --- A. PROVERA ZA OSCAM (Binarni fajlovi) ---
        if "oscam" in name.lower():
            oscam_paths = ["/usr/bin/oscam", "/usr/bin/oscam-emu", "/usr/bin/oscam_emu"]
            if any(os.path.exists(path) for path in oscam_paths):
                installed_names.append(name)
                continue

        # --- B. PROVERA ZA FEED (Po .conf fajlu) ---
        if "secret-feed" in name.lower() or "secret-feed" in cmd:
            if "cortexa15hf-neon-vfpv4-3rdparty-secret-feed.conf" in present_confs:
                installed_names.append(name)
                continue

        # --- C. PROVERA ZA OPKG PAKETE ---
        if "opkg install" in cmd:
            package_name = cmd.split("install ")[-1].strip()
            if package_name in all_opkg:
                installed_names.append(name)
                continue

        # --- D. PROVERA FOLDERA (Extensions & SystemPlugins) ---
        folder_guess = name.replace(" ", "")

        # Mapiranje za specifične slučajeve gde ime u DB nije isto kao folder
        remap = {
            "AjPanel": "AJPan",
            "Vavoo": "vavoo",
            "CiefpSettingsT2miAbertis": ["CiefpSettingsT2miAbertis", "CiefpSettingsT2miAbertisOpenPLi"],
            "NewVirtualKeyBoard": "NewVirtualKeyBoard"  # Sada se proverava i u SystemPlugins
        }

        target = remap.get(name, folder_guess)

        if isinstance(target, list):
            if any(f in present_folders for f in target):
                installed_names.append(name)
        else:
            if target in present_folders:
                installed_names.append(name)

    return installed_names

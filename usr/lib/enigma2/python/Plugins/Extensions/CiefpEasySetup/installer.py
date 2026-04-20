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

def get_image_name():
    """Detektuje koji se imidž koristi (openatv, pure2, itd.)"""
    try:
        if os.path.exists("/etc/image-version"):
            with open("/etc/image-version", "r") as f:
                content = f.read().lower()
                if "openatv" in content: return "openatv"
                if "pure2" in content: return "pure2"
        
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
    ext_path = "/usr/lib/enigma2/python/Plugins/Extensions/"
    sys_path = "/usr/lib/enigma2/python/Plugins/SystemPlugins/"
    
    present_folders = []
    if os.path.exists(ext_path):
        present_folders.extend(os.listdir(ext_path))
    if os.path.exists(sys_path):
        present_folders.extend(os.listdir(sys_path))

    try:
        all_opkg = subprocess.check_output("opkg list_installed | cut -d' ' -f1", shell=True, text=True)
    except:
        all_opkg = ""

    opkg_conf_path = "/etc/opkg/"
    present_confs = os.listdir(opkg_conf_path) if os.path.exists(opkg_conf_path) else []

    for p in plugins_db:
        name = p.get("name")
        cmd = p.get("command", "")

        if "oscam" in name.lower():
            if any(os.path.exists(path) for path in ["/usr/bin/oscam", "/usr/bin/oscam-emu", "/usr/bin/oscam_emu"]):
                installed_names.append(name)
                continue

        if "secret-feed" in name.lower() or "secret-feed" in cmd:
            if "cortexa15hf-neon-vfpv4-3rdparty-secret-feed.conf" in present_confs:
                installed_names.append(name)
                continue

        if "opkg install" in cmd:
            package_name = cmd.split("install ")[-1].strip()
            if package_name in all_opkg:
                installed_names.append(name)
                continue

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

class CiefpInstaller:
    def __init__(self, selected_plugins, callback=None):
        self.selected_plugins = selected_plugins
        self.callback = callback
        self.current_image = get_image_name()

    def run_phase(self, phase_number):
        """Izvršava instalaciju za konkretnu fazu"""
        logging.info(f"--- POKREĆEM FAZU {phase_number} ---")
        
        # Filtriramo samo selektovane plugine za ovu fazu
        to_install = [p for p in self.selected_plugins if p.get("phase") == phase_number]
        
        for plugin in to_install:
            name = plugin.get("name", "")
            cmd = plugin.get("command", "")
            
            # Filtriranje specifično za imidže
            if "secret-feed" in name.lower() and self.current_image != "openatv":
                continue
            if "subssupport" in name.lower() and self.current_image == "pure2":
                continue

            # Logika za lokalne skripte i SKIP_REBOOT
            if "/usr/lib/enigma2/python/Plugins/Extensions/CiefpEasySetup/" in cmd:
                # Automatski chmod 755
                parts = cmd.split(" ")
                script_path = next((p for p in parts if "/" in p and p.endswith(".sh")), None)
                if script_path and os.path.exists(script_path):
                    os.chmod(script_path, 0o755)
                
                # Dodajemo environment varijablu skripti
                cmd = "SKIP_REBOOT=1 " + cmd

            logging.info(f"Instalacija: {name}")
            try:
                # subprocess.call čeka da se proces završi pre nego što krene dalje
                subprocess.call(cmd, shell=True)
            except Exception as e:
                logging.error(f"Greška kod {name}: {e}")

    def start_full_process(self):
        """Glavna funkcija koja spaja sve faze u jedan niz"""
        faze = [1, 2, 3, 99]
        
        for f in faze:
            self.run_phase(f)
            # Mala pauza između faza radi stabilnosti sistema
            time.sleep(1)
        
        logging.info("SVE FAZE ZAVRŠENE. Sistem je spreman za restart.")
        self.final_reboot()

    def final_reboot(self):
        """Finalni restart GUI-ja na samom kraju"""
        if self.callback:
            self.callback()
        else:
            logging.info("Finalni reboot: killall -9 enigma2")
            os.system("killall -9 enigma2")

# Pomoćne funkcije za status (van klase)
def load_status():
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"phase1_done": False, "phase2_done": False, "phase3_done": False, "plugins": {}}

def save_status(data):
    try:
        with open(STATUS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logging.error(f"Ne mogu da sačuvam status: {e}")

def run_command(cmd, skip_reboot=False):
    """Izvršava shell komandu i vraća True/False"""
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
    except subprocess.TimeoutExpired:
        logging.error(f"Komanda je trajala predugo: {cmd[:100]}")
        return False
    except Exception as e:
        logging.error(f"Greška pri izvršavanju komande: {e}")
        return False
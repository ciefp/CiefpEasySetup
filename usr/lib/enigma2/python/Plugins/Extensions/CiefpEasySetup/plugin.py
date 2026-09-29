# -*- coding: utf-8 -*-
from .installer import CiefpInstaller, check_system_for_plugins
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
from Components.Label import Label
from enigma import eTimer
import os
import sys

CURRENT_LANG = "sr"
PLUGIN_VERSION = "3.0"
PLUGIN_NAME = "CiefpEasySetup"

# Nazivi faza za separatore
PHASE_TITLES = {
    0: "═══ FAZA 0 - Priprema (update + feed + oscam) ═══",
    1: "═══ FAZA 1 - System ═══",
    2: "═══ FAZA 2 - Ciefp Plugins ═══",
    3: "═══ FAZA 3 - Feed Plugins ═══",
    4: "═══ FAZA 4 - Third Party ═══",
    5: "═══ FAZA 5 - Secure ═══",
    6: "═══ FAZA 6 - Reserve ═══",
    100: "═══ FAZA 100 - Experimental ═══",
}


def _(txt):
    translations = {
        "English": {"en": "English", "sr": "Engleski"},
        "Start Installation": {"en": "Start Installation", "sr": "Pokreni instalaciju"},
        "Check Status": {"en": "Check Status", "sr": "Provera instalacije"},
        "Reboot Options": {"en": "Reboot Options", "sr": "Reboot opcije"},
        "Select Language": {"en": "Select Language", "sr": "Izaberi jezik"},
        "Settings": {"en": "Settings", "sr": "Podešavanja"},
        "Installation in progress...": {"en": "Installation in progress...", "sr": "Instalacija u toku..."},
        "Time: ": {"en": "Time: ", "sr": "Vreme: "},
        "Exit": {"en": "Exit", "sr": "Izlaz"},
        "Import error!": {"en": "Import error!", "sr": "Import greška!"},
        "Select installation option": {"en": "Select installation option", "sr": "Izaberite opciju instalacije"},
        "Install ALL": {"en": "Install ALL", "sr": "Instaliraj SVE"},
        "Only Phase 1 (System)": {"en": "Only Phase 1 (System)", "sr": "Samo Faza 1 (System)"},
        "Only Phase 2 (Ciefp plugins)": {"en": "Only Phase 2 (Ciefp plugins)", "sr": "Samo Faza 2 (Moji plugini)"},
        "Only Phase 3 (Others)": {"en": "Only Phase 3 (Others)", "sr": "Samo Faza 3 (Ostali)"},
        "Phase 1 + Phase 2": {"en": "Phase 1 + Phase 2", "sr": "Faza 1 + Faza 2"},
        "Select manually": {"en": "Select manually", "sr": "Selektuj ručno"},
        "ERROR: File import problem": {"en": "ERROR: File import problem", "sr": "GREŠKA: Problem sa importom fajlova"},
        "Reboot Box": {"en": "Reboot Box", "sr": "Restartuj risiver"},
        "Restart Enigma2 (GUI)": {"en": "Restart Enigma2 (GUI)", "sr": "Restartuj Enigma2 (GUI)"},
        "Cancel": {"en": "Cancel", "sr": "Odustani"},
        "Select action:": {"en": "Select action:", "sr": "Izaberite akciju:"},
        "Current Status": {"en": "Current Status", "sr": "Trenutni status"},
        "DONE": {"en": "DONE", "sr": "ZAVRŠENO"},
        "Not done": {"en": "Not done", "sr": "Nije završeno"},
        "Phase": {"en": "Phase", "sr": "Faza"},
        "System is successfully synchronized with the list.": {
            "en": "System is successfully synchronized with the list.",
            "sr": "Sistem je uspešno sinhronizovan sa listom."
        },
        "Installation finished!": {"en": "Installation finished!", "sr": "Instalacija završena!"},
        "✓ Successful": {"en": "✓ Successful", "sr": "✓ Uspešno"},
        "✗ Failed": {"en": "✗ Failed", "sr": "✗ Neuspešno"},
        "Failed plugins": {"en": "Failed plugins", "sr": "Neuspešni plugini"},
        "Do you want to retry failed ones?": {"en": "Do you want to retry failed ones?", "sr": "Želite li da ponovite neuspele?"},
        "All plugins installed successfully!": {"en": "All plugins installed successfully!", "sr": "Svi plugini su uspešno instalirani!"},
        "No plugins selected!": {"en": "No plugins selected!", "sr": "Niste izabrali nijedan plugin!"},
        "Manual Selection": {"en": "Manual Selection", "sr": "Ručni izbor"},
        "All selected plugins are already installed!": {"en": "All selected plugins are already installed!", "sr": "Svi izabrani plugini su već instalirani!"},
        "About": {"en": "About", "sr": "O aplikaciji"},
        "Installation Time Estimates": {"en": "Installation Time Estimates", "sr": "Procena trajanja instalacije"},
        "Note: Speed depends on receiver CPU": {"en": "Note: Speed depends on receiver CPU", "sr": "Napomena: Brzina zavisi od procesora risivera"},
        "and internet/media speed (Flash/USB).": {"en": "and internet/media speed (Flash/USB).", "sr": "i brzine interneta/medija (Flash/USB)."},
        "Special thanks to the community.": {"en": "Special thanks to the community.", "sr": "Posebno hvala zajednici na testiranju."},
        "Special thanks to Gemini A.I. for support.": {"en": "Special thanks to Gemini A.I. for support.", "sr": "Posebna zahvala Gemini A.I. za podršku."},
        "Update plugin": {"en": "Update plugin", "sr": "Ažuriraj plugin"},
        "Do you want to update CiefpEasySetup plugin?": {"en": "Do you want to update CiefpEasySetup plugin?", "sr": "Da li želite da ažurirate CiefpEasySetup plugin?"},
        "The plugin will be updated to the latest version.": {"en": "The plugin will be updated to the latest version.", "sr": "Plugin će biti ažuriran na najnoviju verziju."},
        "Updating plugin...": {"en": "Updating plugin...", "sr": "Ažuriranje plugina..."},
        "CiefpEasySetup update in progress": {"en": "CiefpEasySetup update in progress", "sr": "CiefpEasySetup ažuriranje u toku"},
        "Plugin updated successfully!": {"en": "Plugin updated successfully!", "sr": "Plugin je uspešno ažuriran!"},
        "Please restart Enigma2 for changes to take effect.": {"en": "Please restart Enigma2 for changes to take effect.", "sr": "Molimo restartujte Enigma2 da bi promene stupile na snagu."},
        "Update failed!": {"en": "Update failed!", "sr": "Ažuriranje neuspešno!"},
        "Please check your internet connection and try again.": {"en": "Please check your internet connection and try again.", "sr": "Molimo proverite internet konekciju i pokušajte ponovo."},
        "Fallback install...": {"en": "Fallback install...", "sr": "Fallback instalacija..."},
        "Priprema sistema...": {"en": "Preparing system...", "sr": "Priprema sistema..."},
        "Osvežavanje feed-ova (bez merenja vremena)": {"en": "Refreshing feeds (no time measurement)", "sr": "Osvežavanje feed-ova (bez merenja vremena)"},
        "Priprema završena": {"en": "Preparation finished", "sr": "Priprema završena"},
        "Pokretanje instalacije...": {"en": "Starting installation...", "sr": "Pokretanje instalacije..."},
        "Restart skipped (batch installation)": {"en": "Restart skipped (batch installation)", "sr": "Restart preskočen (batch instalacija)"},
        "Phase 0 finished.": {"en": "Phase 0 finished.", "sr": "Faza 0 završena."},
        "Manual installation...": {"en": "Manual installation...", "sr": "Ručna instalacija..."},
    }
    if txt in translations:
        return translations[txt].get(CURRENT_LANG, txt)
    return txt


# === KRITIČNI IMPORTI ===
sys.path.insert(0, "/usr/lib/enigma2/python/Plugins/Extensions/CiefpEasySetup")
try:
    from installer import load_status, save_status, run_command
    from plugins_list import PLUGINS_DB
    IMPORT_OK = True
except Exception as e:
    print("[CiefpEasySetup] GREŠKA IMPORTA:", str(e))
    IMPORT_OK = False
    PLUGINS_DB = []
    load_status = lambda: {}
    save_status = lambda x: None


def is_openpli():
    try:
        if os.path.exists("/etc/issue"):
            with open("/etc/issue", "r") as f:
                content = f.read().lower()
                if "openpli" in content:
                    return True
    except:
        pass
    return False


def is_openatv_only():
    """Proverava da li je OpenATV (samo OpenATV, ne OpenBH ili drugi OEA)."""
    try:
        if os.path.exists("/etc/issue"):
            with open("/etc/issue", "r") as f:
                content = f.read().lower()
                if "openatv" in content:
                    return True
    except:
        pass
    return False


def is_oea_image():
    """OpenATV, OpenBH, OpenSPA, Pure2, OpenVision - svi OEA imidži"""
    try:
        if os.path.exists("/etc/issue"):
            with open("/etc/issue", "r") as f:
                content = f.read().lower()
                if any(x in content for x in [
                    "openatv", "openbh", "openspa", "pure2",
                    "openvision", "openhdf", "opendroid", "egami"
                ]):
                    return True
    except:
        pass
    return False


def is_vuplus():
    try:
        if os.path.exists("/proc/stb/info/boxtype"):
            with open("/proc/stb/info/boxtype", "r") as f:
                content = f.read().lower()
                if "vu" in content:
                    return True
    except:
        pass
    return False


class CiefpInstallProgress(Screen):
    skin = """
    <screen name="CiefpInstallProgress" position="center,50" size="1200,120" title="Instalacija" backgroundColor="#1a1a1a" flags="wfNoBorder">
        <eLabel position="0,0" size="1200,120" backgroundColor="#1a1a1a" zPosition="-1" />
        <widget name="status" position="20,15" size="1160,40" font="Regular;30" halign="center" valign="center" foregroundColor="#f0ca00" transparent="1" />
        <widget name="detail" position="20,65" size="1160,35" font="Regular;24" halign="center" valign="center" foregroundColor="#ffffff" transparent="1" />
        <widget name="timer_label" position="950,15" size="230,40" font="Regular;28" halign="right" valign="center" transparent="1" foregroundColor="#ffffff" />
    </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self["timer_label"] = Label(_("Time: 00:00"))
        self["status"] = Label("Inicijalizacija...")
        self["detail"] = Label("Molimo sačekajte...")
        self["actions"] = ActionMap(["ColorActions", "OkCancelActions"], {
            "red": self.close,
            "cancel": self.close,
        }, -1)
        self.elapsed_time = 0
        self.stopwatch_timer = eTimer()
        self.stopwatch_timer.callback.append(self.update_stopwatch)
        self.timer_active = False

    def update_stopwatch(self):
        self.elapsed_time += 1
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        time_str = _("Time: ") + "%02d:%02d" % (minutes, seconds)
        self["timer_label"].setText(time_str)

    def start_timer(self):
        self.elapsed_time = 0
        self["timer_label"].setText(_("Time: 00:00"))
        self.stopwatch_timer.start(1000)
        self.timer_active = True

    def stop_timer(self):
        self.stopwatch_timer.stop()
        self.timer_active = False

    def update_info(self, status, detail):
        self["status"].setText(status)
        self["detail"].setText(detail)


class CiefpEasySetup(Screen):
    skin = """
    <screen name="CiefpEasySetup" position="center,center" size="1920,1080"  backgroundColor="#1a1a1a">
        <widget name="plugin_title" position="0,10" size="1920,50" font="Bold;34" halign="center" backgroundColor="#012e01" foregroundColor="#00FF00" text="..:: CiefpEasySetup Multi-Image One-Click Installer (Version{version}) ::.." />
        <widget name="list" position="40,80" size="880,810" scrollbarMode="showOnDemand" itemHeight="45" font="Regular;30" transparent="1" />
        <widget name="background" position="980,80" size="880,840" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CiefpEasySetup/background.png" zPosition="1" alphatest="on" />
        <widget name="status" position="40,930" size="880,60" font="Regular;26" halign="center" valign="center" transparent="1" foregroundColor="#00FF00" />
        <widget name="key_red"    position="40,1000" size="280,50" font="Regular;28" halign="center" backgroundColor="#9F1313" foregroundColor="#FFFFFF" />
        <widget name="key_green"  position="340,1000" size="280,50" font="Regular;28" halign="center" backgroundColor="#1F771F" foregroundColor="#FFFFFF" />
        <widget name="key_yellow" position="640,1000" size="280,50" font="Regular;28" halign="center" backgroundColor="#9F9F13" foregroundColor="#000000" />
        <widget name="key_blue"   position="940,1000" size="280,50" font="Regular;28" halign="center" backgroundColor="#13389F" foregroundColor="#FFFFFF" />
        <widget name="key_cyan"   position="1240,1000" size="280,50" font="Regular;28" halign="center" backgroundColor="#00FFFF" foregroundColor="#000000" />
        <widget name="key_menu"   position="1540,950" size="340,50" font="Regular;28" halign="center" backgroundColor="#333333" foregroundColor="#FFFFFF" />
    </screen>
    """.format(version=PLUGIN_VERSION)

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        self.IMPORT_OK = IMPORT_OK
        self["plugin_title"] = Label(f"..:: CiefpEasySetup Multi-Image One-Click Installer ::..  (Version {PLUGIN_VERSION})")
        self["list"] = MenuList([])
        self["background"] = Pixmap()
        self["status"] = Label("Učitavam stanje...")
        self["key_red"] = Label(_("Exit"))
        self["key_green"] = Label(_("Start Installation"))
        self["key_yellow"] = Label(_("Check Status"))
        self["key_blue"] = Label(_("Reboot Options"))
        self["key_cyan"] = Label(_("Menu:Language"))

        self.status_data = load_status() if IMPORT_OK else {}
        self.sync_with_system()
        global CURRENT_LANG
        CURRENT_LANG = self.status_data.get("settings_lang", "sr")
        self.success_plugins = []
        self.failed_plugins = []
        self.plugins_to_install = []
        self.current_plugin_index = 0
        self.update_success = False
        self.message_timer = None
        self.mini_screen = None
        self.phase0_plugins = []
        self.phase0_callback = None
        self.build_list()
        self.update_status_text()
        self._move_to_first_plugin()

        self["actions"] = ActionMap(
            ["ColorActions", "OkCancelActions", "MenuActions", "DirectionActions"],
            {
                "red": self.exit,
                "green": self.show_install_menu,
                "yellow": self.check_status,
                "blue": self.show_reboot_menu,
                "menu": self.show_config_menu,
                "ok": self.ok,
                "cancel": self.exit,
                "up": self.up,
                "down": self.down,
            }, -1)

    # ==================== NAVIGACIJA ====================
    def _is_separator(self, idx):
        curr = self["list"].list
        if 0 <= idx < len(curr):
            return curr[idx][1].get("separator", False)
        return False

    def _move_to_first_plugin(self):
        curr = self["list"].list
        for i, item in enumerate(curr):
            if not item[1].get("separator", False):
                self["list"].moveToIndex(i)
                return

    def up(self):
        curr_idx = self["list"].getSelectionIndex()
        if curr_idx <= 0:
            return
        new_idx = curr_idx - 1
        while new_idx >= 0 and self._is_separator(new_idx):
            new_idx -= 1
        if new_idx >= 0:
            self["list"].moveToIndex(new_idx)

    def down(self):
        curr_idx = self["list"].getSelectionIndex()
        curr = self["list"].list
        if curr_idx >= len(curr) - 1:
            return
        new_idx = curr_idx + 1
        while new_idx < len(curr) and self._is_separator(new_idx):
            new_idx += 1
        if new_idx < len(curr):
            self["list"].moveToIndex(new_idx)

    # ==================== MINI SCREEN HELPER ====================
    def ensure_mini_screen(self, start_timer=True):
        """Osigurava da je mini screen otvoren. Opciono pokreće timer."""
        self.hide()
        if not self.mini_screen:
            self.mini_screen = self.session.open(CiefpInstallProgress)
        if start_timer:
            self.mini_screen.start_timer()
        return self.mini_screen

    def close_mini_screen(self):
        """Zatvara mini screen ako postoji."""
        if self.mini_screen:
            try:
                self.mini_screen.stop_timer()
            except:
                pass
            try:
                self.mini_screen.close()
            except:
                pass
            self.mini_screen = None

    # ==================== SYNC ====================
    def sync_with_system(self):
        if not IMPORT_OK: return
        from installer import check_system_for_plugins
        installed_on_disk = check_system_for_plugins(PLUGINS_DB)

        current_plugins = self.status_data.get("plugins", {})
        for p in PLUGINS_DB:
            name = p.get("name")
            phase = p.get("phase")
            if phase == 0:
                continue
            if name in installed_on_disk:
                current_plugins[name] = {"success": True, "phase": phase}
            else:
                if name in current_plugins and current_plugins[name].get("success"):
                    current_plugins[name]["success"] = False

        self.status_data["plugins"] = current_plugins

        for phase in [1, 2, 3, 4, 5, 6]:
            phase_plugins = [p for p in PLUGINS_DB if p.get("phase") == phase]
            self.status_data[f"phase{phase}_done"] = all(
                current_plugins.get(pp["name"], {}).get("success") for pp in phase_plugins
            )
        save_status(self.status_data)

    def show_config_menu(self):
        options = [
            (_("Select Language"), "lang"),
            (_("Update plugin"), "update"),
            (_("About"), "about")
        ]
        self.session.openWithCallback(self.config_menu_callback, ChoiceBox, title=_("Settings"), list=options)

    def config_menu_callback(self, choice):
        if choice:
            if choice[1] == "lang":
                langs = [("English", "en"), ("Srpski", "sr")]
                self.session.openWithCallback(self.set_language, ChoiceBox, title=_("Select Language"), list=langs)
            elif choice[1] == "update":
                self.update_plugin()
            elif choice[1] == "about":
                self.show_about_info()

    def show_about_info(self):
        about_text = f"CiefpEasySetup v{PLUGIN_VERSION}\n"
        about_text += "Multi-Image One-Click Installer (PY3)\n\n"
        about_text += "--- " + _("Installation Time Estimates") + " ---\n"
        about_text += "• OpenATV, Pure2, OpenSPA: ~10-15 min eMMC,~35-40 min OMB\n"
        about_text += "• OpenPLi (Scarthgap): ~10-15 min eMMC,~50-60 min OMB\n\n"
        about_text += _("Note: Speed depends on receiver CPU") + "\n"
        about_text += _("and internet/media speed (Flash/USB).") + "\n\n"
        about_text += "Author: ciefp\n"
        about_text += _("Special thanks to the community.") + "\n"
        about_text += _("Special thanks to Gemini A.I. for support.")
        self.session.open(MessageBox, about_text, MessageBox.TYPE_INFO)

    def set_language(self, lang):
        if lang:
            global CURRENT_LANG
            CURRENT_LANG = lang[1]
            self.status_data["settings_lang"] = CURRENT_LANG
            save_status(self.status_data)
            self["key_red"].setText(_("Exit"))
            self["key_green"].setText(_("Start Installation"))
            self["key_yellow"].setText(_("Check Status"))
            self["key_blue"].setText(_("Reboot Options"))
            self.setTitle("CiefpEasySetup - " + _("Settings"))
            self.session.open(MessageBox, _("Language changed."), MessageBox.TYPE_INFO, timeout=3)

    # ==================== BUILD LIST ====================
    def build_list(self):
        if not self.IMPORT_OK:
            self["list"].setList([])
            return

        all_plugins = PLUGINS_DB
        plugins_status = self.status_data.get("plugins", {})
        list_data = []

        if not hasattr(self, "temp_selection"):
            self.temp_selection = {}

        phases = {}
        for p in all_plugins:
            ph = p.get("phase", 0)
            phases.setdefault(ph, []).append(p)

        try:
            old_idx = self["list"].getSelectionIndex()
            old_name = None
            if 0 <= old_idx < len(self["list"].list):
                old_name = self["list"].list[old_idx][1].get("name")
        except:
            old_name = None

        for ph in sorted(phases.keys()):
            title = PHASE_TITLES.get(ph, f"═══ FAZA {ph} ═══")
            list_data.append((title, {"separator": True, "name": f"__sep_{ph}__"}))

            for p in phases[ph]:
                name = p.get("name", "Unknown")
                status = plugins_status.get(name, {})
                is_installed = status.get("success", False)
                plugin_info = p.copy()
                plugin_info["separator"] = False

                if ph == 0:
                    display_name = f"  [  ] {name}"
                    plugin_info["selected"] = False
                elif is_installed:
                    display_name = f"  ✓ {name}"
                    plugin_info["selected"] = False
                else:
                    was_selected = self.temp_selection.get(name, False)
                    prefix = "  [X] " if was_selected else "  [  ] "
                    display_name = f"{prefix}{name}"
                    plugin_info["selected"] = was_selected

                list_data.append((display_name, plugin_info))

        self["list"].setList(list_data)

        if old_name:
            for i, item in enumerate(list_data):
                if item[1].get("name") == old_name:
                    self["list"].moveToIndex(i)
                    break
            else:
                self._move_to_first_plugin()
        else:
            self._move_to_first_plugin()

    def update_plugin(self):
        msg = _("Do you want to update CiefpEasySetup plugin?") + "\n\n" + _("The plugin will be updated to the latest version.")
        self.session.openWithCallback(self.confirm_update, MessageBox, msg, MessageBox.TYPE_YESNO)

    def confirm_update(self, answer):
        if answer:
            self.ensure_mini_screen(start_timer=True)
            self.mini_screen.update_info(_("Updating plugin..."), _("CiefpEasySetup update in progress"))
            self.update_timer = eTimer()
            self.update_timer.callback.append(self.run_update_command)
            self.update_timer.start(500, True)

    def run_update_command(self):
        update_cmd = "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpEasySetup/main/installer.sh -O - | /bin/sh"
        success = run_command(update_cmd, skip_reboot=True)
        self.close_mini_screen()
        self.update_success = success
        self.show()
        self.message_timer = eTimer()
        self.message_timer.callback.append(self.show_update_result)
        self.message_timer.start(500, True)

    def show_update_result(self):
        if self.update_success:
            msg = _("Plugin updated successfully!") + "\n\n" + _("Please restart Enigma2 for changes to take effect.")
            self.session.openWithCallback(self.restart_enigma2_after_update, MessageBox, msg, MessageBox.TYPE_YESNO)
        else:
            msg = _("Update failed!") + "\n\n" + _("Please check your internet connection and try again.")
            self.session.open(MessageBox, msg, MessageBox.TYPE_ERROR)

    def restart_enigma2_after_update(self, answer):
        if answer:
            os.system("killall -9 enigma2")

    def update_status_text(self):
        self.status_data = load_status()
        if not self.IMPORT_OK:
            self["status"].setText(_("ERROR: File import problem"))
            return

        def get_phase_status(phase_num):
            key = f"phase{phase_num}_done"
            if self.status_data.get(key, False):
                return _("DONE")
            return _("Not done")

        txt = f"P1:{get_phase_status(1)} P2:{get_phase_status(2)} P3:{get_phase_status(3)} "
        txt += f"P4:{get_phase_status(4)} P5:{get_phase_status(5)} P6:{get_phase_status(6)}"
        self["status"].setText(txt)

    # ==================== FAZA 0 ====================
    def run_phase_zero(self, callback):
        """Izvrši fazu 0 (opkg update + secret-feed + oscam) pre glavne instalacije.
        callback - funkcija koja se poziva kada faza 0 završi."""
        phase0_plugins = [p for p in PLUGINS_DB if p.get("phase") == 0]

        if not phase0_plugins:
            callback()
            return

        self.phase0_plugins = phase0_plugins
        self.phase0_callback = callback

        # Otvori mini screen ali NE pokreći timer
        self.hide()
        if not self.mini_screen:
            self.mini_screen = self.session.open(CiefpInstallProgress)

        self.mini_screen.update_info(
            _("Priprema sistema..."),
            _("Osvežavanje feed-ova (bez merenja vremena)")
        )

        self.phase0_timer = eTimer()
        self.phase0_timer.callback.append(lambda: self._run_phase0_step(0))
        self.phase0_timer.start(500, True)

    def _run_phase0_step(self, idx):
        if idx >= len(self.phase0_plugins):
            if self.mini_screen:
                self.mini_screen.update_info(
                    _("Priprema završena"),
                    _("Pokretanje instalacije...")
                )
            cb = getattr(self, "phase0_callback", None)
            if cb:
                self.phase0_callback()
            return

        plugin = self.phase0_plugins[idx]
        name = plugin.get("name", "Unknown")

        if self.mini_screen:
            self.mini_screen.update_info(
                _("Priprema sistema..."),
                f"[{idx + 1}/{len(self.phase0_plugins)}] {name}"
            )

        run_command(plugin.get("command"), skip_reboot=True)

        self.phase0_timer = eTimer()
        self.phase0_timer.callback.append(lambda: self._run_phase0_step(idx + 1))
        self.phase0_timer.start(500, True)

    # ==================== INSTALACIONI MENI ====================
    def show_install_menu(self):
        manual_selection = [item[1] for item in self["list"].list
                            if not item[1].get("separator", False) and item[1].get("selected", False)]

        if manual_selection:
            self.session.openWithCallback(self.start_manual_confirmed, MessageBox,
                                          _("Do you want to install selected plugins?"), MessageBox.TYPE_YESNO)
        else:
            atv_only = is_openatv_only()
            all_label = _("Install ALL (Phase 0-5)") if atv_only else _("Install ALL (Phase 1-5)")

            options = [
                (all_label, "all"),
                (_("Only Phase 0 (Prepare)"), 0),
                (_("Only Phase 1 (System)"), 1),
                (_("Only Phase 2 (Ciefp plugins)"), 2),
                (_("Only Phase 3 (Others)"), 3),
                (_("Only Phase 4 (Third Party)"), 4),
                (_("Only Phase 5 (Secure)"), 5),
                (_("Only Phase 6 (Reserve)"), 6),
                (_("Only Phase 100 (Experimental)"), 100),
                (_("Phase 1 + Phase 2"), "1+2")
            ]
            self.session.openWithCallback(self.start_selected_install, ChoiceBox,
                                          title=_("Select installation option"), list=options)

    def start_manual_confirmed(self, answer):
        if answer:
            self.start_selected_install("manual")

    def start_selected_install(self, choice):
        if not choice:
            return
        if isinstance(choice, tuple):
            choice = choice[1]

        all_plugins = PLUGINS_DB
        atv_only = is_openatv_only()

        self.phase3_names = set(p["name"] for p in all_plugins if p.get("phase") == 3)
        self.phase4_names = set(p["name"] for p in all_plugins if p.get("phase") == 4)
        self.duplicate_plugins = self.phase3_names.intersection(self.phase4_names)

        plugins_status = self.status_data.get("plugins", {})
        selected_list = []

        if choice == "manual":
            selected_list = [item[1] for item in self["list"].list
                             if not item[1].get("separator", False) and item[1].get("selected", False)]
            self.current_phase_label = _("Manual Selection")

        elif choice == "all":
            selected_list = []
            for p in all_plugins:
                name = p.get("name")
                phase = p.get("phase")

                # 🔥 Faza 0 - samo na OpenATV
                if phase == 0 and not atv_only:
                    continue

                if phase == 100:
                    continue
                if phase == 6:
                    continue
                if phase == 4 and name in self.duplicate_plugins:
                    continue
                selected_list.append(p)
            self.current_phase_label = _("Install ALL (Phase 0-5)") if atv_only else _("Install ALL (Phase 1-5)")

        elif isinstance(choice, int):
            selected_list = [p for p in all_plugins if p.get("phase") == choice]
            self.current_phase_label = f"{_('Phase')} {choice}"

        elif choice == "1+2":
            selected_list = [p for p in all_plugins if p.get("phase") in [1, 2]]
            self.current_phase_label = f"{_('Phase')} 1 + 2"

        if not selected_list:
            self.session.open(MessageBox, _("No plugins selected!"), MessageBox.TYPE_INFO)
            return

        pli_detected = is_openpli()
        oea_detected = is_oea_image()
        vu_detected = is_vuplus()
        self.plugins_to_install = []
        self.only_phase0 = False

        # Ako je izabrana samo faza 0
        if choice == 0:
            self.only_phase0 = True
            self.plugins_to_install = [p for p in selected_list if p.get("phase") == 0]
            # 🔥 Prikaži mini screen za fazu 0
            self.ensure_mini_screen(start_timer=False)
            self.run_phase_zero(self.after_phase_zero_only)
            return

        for p in selected_list:
            name = p.get("name")
            phase = p.get("phase")

            # Preskoči OEA-specifične plugine na ne-OEA imidžima
            if name == "secret-feed" and not oea_detected:
                continue
            if name in ["StreamlinkWrapper", "ytdlpwrapper", "OAWeather", "WebkitHbbTV"] and not oea_detected:
                continue
            if name == "chromium" and not vu_detected:
                continue

            if name == "CiefpSettingsT2miAbertis":
                if pli_detected:
                    p["command"] = "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsT2miAbertisOpenPLi/main/installer.sh -O - | /bin/sh"
                else:
                    p["command"] = "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsT2miAbertis/main/installer.sh -O - | /bin/sh"

            # Faza 0 - uvek dodaj (bez provere statusa)
            if phase == 0:
                self.plugins_to_install.append(p)
                continue

            status = plugins_status.get(name)
            if not status or not status.get("success", False):
                self.plugins_to_install.append(p)

        if not self.plugins_to_install:
            self.session.open(MessageBox, _("All selected plugins are already installed!"), MessageBox.TYPE_INFO)
            return

        # Odvoji fazu 0 od ostalih
        phase0 = [p for p in self.plugins_to_install if p.get("phase") == 0]
        others = [p for p in self.plugins_to_install if p.get("phase") != 0]

        self.success_plugins = []
        self.failed_plugins = []
        self.temp_selection = {}
        self.current_plugin_index = 0

        # 🔥 Uvek prikaži mini screen pre bilo čega
        self.ensure_mini_screen(start_timer=False)

        # Definiši callback koji se poziva posle faze 0
        def after_phase0():
            # Pokreni fazu 1-5
            self.plugins_to_install = sorted(others, key=lambda x: x.get("phase", 0))
            if not self.plugins_to_install:
                self.close_mini_screen()
                self.show()
                self.session.open(MessageBox, _("All selected plugins are already installed!"), MessageBox.TYPE_INFO)
                return
            self.current_plugin_index = 0
            if self.mini_screen:
                self.mini_screen.start_timer()
            self.start_actual_installation()

        # Ako postoji faza 0 → pokreni je, pa onda ostale
        if phase0:
            self.run_phase_zero(after_phase0)
        else:
            # Nema faze 0 - odmah pokreni fazu 1-5 sa timerom
            self.plugins_to_install = sorted(others, key=lambda x: x.get("phase", 0))
            if self.mini_screen:
                self.mini_screen.start_timer()
            self.start_actual_installation()

    def after_phase_zero_only(self):
        """Callback kada se završi samo Faza 0."""
        self.close_mini_screen()
        self.show()
        self.build_list()
        self.update_status_text()
        self.session.open(MessageBox, _("Phase 0 finished."), MessageBox.TYPE_INFO, timeout=5)

    def start_actual_installation(self):
        self.plugin_timer = eTimer()
        self.plugin_timer.callback.append(self.install_next_plugin)
        self.plugin_timer.start(500, True)

    def install_next_plugin(self):
        if self.current_plugin_index >= len(self.plugins_to_install):
            return self.finish_installation()

        plugin = self.plugins_to_install[self.current_plugin_index]
        name = plugin.get("name", "Unknown")

        if self.mini_screen:
            status = f"{_('Installation in progress...')}"
            details = f"[{self.current_plugin_index + 1}/{len(self.plugins_to_install)}] {name}"
            self.mini_screen.update_info(status, details)

        success = run_command(plugin.get("command"), skip_reboot=True)

        name = plugin.get("name")
        phase = plugin.get("phase")

        # Fallback za duplikate (faza 3 → faza 4)
        if not success and phase == 3 and name in getattr(self, "duplicate_plugins", set()):
            fallback = next((p for p in PLUGINS_DB if p.get("name") == name and p.get("phase") == 4), None)
            if fallback:
                if self.mini_screen:
                    self.mini_screen.update_info(_("Fallback install..."), name)
                success = run_command(fallback.get("command"), skip_reboot=True)

        if success:
            self.success_plugins.append(name)
        else:
            self.failed_plugins.append(name)

        # Faza 0 se ne čuva u JSON
        if phase != 0:
            self.status_data.setdefault("plugins", {})[name] = {"success": success, "phase": phase}
            save_status(self.status_data)

        self.current_plugin_index += 1
        self.plugin_timer.start(500, True)

    def finish_installation(self):
        self.close_mini_screen()
        self.show()
        self.summary_timer = eTimer()
        self.summary_timer.callback.append(self.show_install_summary)
        self.summary_timer.start(100, True)

    def show_install_summary(self):
        total = len(self.success_plugins) + len(self.failed_plugins)
        all_plugins = PLUGINS_DB
        self.status_data = load_status()
        plugins_status = self.status_data.get("plugins", {})

        def is_phase_done(phase_num):
            phase_plugins = [p for p in all_plugins if p.get("phase") == phase_num]
            for p in phase_plugins:
                name = p.get("name")
                status = plugins_status.get(name)
                if not status or not status.get("success", False):
                    return False
            return True

        # Faze 1-6 (bez faze 0)
        for phase in [1, 2, 3, 4, 5, 6]:
            self.status_data[f"phase{phase}_done"] = is_phase_done(phase)
        save_status(self.status_data)

        msg = f"{_('Installation finished!')}\n\n"
        msg += f"{_('✓ Successful')}: {len(self.success_plugins)} / {total}\n"
        msg += f"{_('✗ Failed')}: {len(self.failed_plugins)}\n\n"

        if self.failed_plugins:
            msg += f"{_('Failed plugins')}:\n"
            msg += "\n".join([f"• {p}" for p in sorted(self.failed_plugins)[:12]])
            msg += f"\n\n{_('Do you want to retry failed ones?')}"
            self.session.openWithCallback(self.retry_failed, MessageBox, msg, MessageBox.TYPE_YESNO, default=False)
        else:
            msg += _("All plugins installed successfully!")
            self.session.open(MessageBox, msg, MessageBox.TYPE_INFO, timeout=15)

        self.build_list()
        self.update_status_text()

    def retry_failed(self, answer):
        if answer and self.failed_plugins:
            retry_list = [p for p in PLUGINS_DB if p.get("name") in self.failed_plugins and p.get("phase") != 0]
            self.plugins_to_install = sorted(retry_list, key=lambda x: x.get("phase", 0))
            self.current_plugin_index = 0
            self.success_plugins = []
            self.failed_plugins = []
            # 🔥 Prikaži mini screen
            self.ensure_mini_screen(start_timer=True)
            self.start_actual_installation()
        else:
            self.build_list()
            self.update_status_text()

    # ====================== ŽUTA - PROVERA ======================
    def check_status(self):
        self["status"].setText("Skeniram sistem, molimo sačekajte...")
        from installer import check_system_for_plugins
        installed_list = check_system_for_plugins(PLUGINS_DB)

        new_plugins_status = {}
        for p in PLUGINS_DB:
            p_name = p.get("name")
            phase = p.get("phase")
            if phase == 0:
                continue
            if p_name in installed_list:
                new_plugins_status[p_name] = {"success": True, "phase": phase}
            else:
                old_status = self.status_data.get("plugins", {}).get(p_name, {})
                if old_status.get("success") is False:
                    new_plugins_status[p_name] = old_status

        self.status_data["plugins"] = new_plugins_status

        for phase in [1, 2, 3, 4, 5, 6]:
            phase_plugins = [p for p in PLUGINS_DB if p.get("phase") == phase]
            is_done = True
            for pp in phase_plugins:
                if pp.get("name") not in installed_list:
                    is_done = False
                    break
            self.status_data[f"phase{phase}_done"] = is_done

        save_status(self.status_data)
        self.build_list()
        self.update_status_text()

        msg = f"=== {_('Current Status')} ===\n\n"
        def get_done_text(val):
            return _("DONE") if val else _("Not done")

        msg += f"{_('Phase')} 1: {get_done_text(self.status_data.get('phase1_done'))}\n"
        msg += f"{_('Phase')} 2: {get_done_text(self.status_data.get('phase2_done'))}\n"
        msg += f"{_('Phase')} 3: {get_done_text(self.status_data.get('phase3_done'))}\n"
        msg += f"{_('Phase')} 4: {get_done_text(self.status_data.get('phase4_done'))}\n"
        msg += f"{_('Phase')} 5: {get_done_text(self.status_data.get('phase5_done'))}\n"
        msg += f"{_('Phase')} 6: {get_done_text(self.status_data.get('phase6_done'))}\n\n"
        msg += _("System is successfully synchronized with the list.")
        self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)

    # ====================== PLAVA - REBOOT ======================
    def show_reboot_menu(self):
        options = [
            (_("Reboot Box"), "reboot"),
            (_("Restart Enigma2 (GUI)"), "restart"),
            (_("Cancel"), "cancel")
        ]
        self.session.openWithCallback(self.do_reboot, ChoiceBox, title=_("Select action:"), list=options)

    def do_reboot(self, choice):
        if choice:
            action = choice[1]
            if action == "reboot":
                os.system("reboot")
            elif action == "restart":
                os.system("killall -9 enigma2")

    # ====================== OK ======================
    def ok(self):
        idx = self["list"].getSelectionIndex()
        if idx < 0:
            return
        curr_list = self["list"].list
        display_name, plugin_data = curr_list[idx]
        if plugin_data.get("separator", False):
            return
        name = plugin_data.get("name")
        if "✓" in display_name:
            return

        if hasattr(self, "temp_selection"):
            is_selected = not plugin_data.get("selected", False)
            plugin_data["selected"] = is_selected
            self.temp_selection[name] = is_selected
            if is_selected:
                new_display = f"  [X] {name}"
            else:
                new_display = f"  [  ] {name}"
            curr_list[idx] = (new_display, plugin_data)
            self["list"].setList(curr_list)
            self["list"].moveToIndex(idx)
        else:
            self.session.openWithCallback(self.install_single_plugin_confirmed, MessageBox,
                                          f"Instalirati {name}?", MessageBox.TYPE_YESNO)

    def install_single_plugin_confirmed(self, answer):
        if answer:
            idx = self["list"].getCurrentIndex()
            plugin = self["list"].list[idx][1]
            if plugin.get("separator", False):
                return

            # 🔥 Prikaži mini screen
            self.ensure_mini_screen(start_timer=True)
            self.mini_screen.update_info(_("Manual installation..."), plugin.get("name"))

            success = run_command(plugin.get("command"), skip_reboot=False)

            phase = plugin.get("phase")
            if phase != 0:
                self.status_data.setdefault("plugins", {})[plugin.get("name")] = {
                    "success": success, "phase": phase
                }
                save_status(self.status_data)

            self.close_mini_screen()
            self.show()
            self.build_list()
            self.update_status_text()

    def exit(self):
        self.close()


def Plugins(**kwargs):
    return [
        PluginDescriptor(
            name="{0} v{1}".format(PLUGIN_NAME, PLUGIN_VERSION),
            description="Multi-Image One-Click (PY3 Only: OpenATV, Pure2, OpenSPA, OpenPLi)",
            where=PluginDescriptor.WHERE_PLUGINMENU,
            icon="plugin.png",
            fnc=lambda session, **kwargs: session.open(CiefpEasySetup)
        )
    ]
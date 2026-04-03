# -*- coding: utf-8 -*-
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

# --- DODAJ OVO ISPOD ---
CURRENT_LANG = "sr" # Podrazumevani jezik

def _(txt):
    translations = {
        "English": {"en": "English", "sr": "Engleski"},
        "Main Screen": {"en": "Main Screen", "sr": "Glavni ekran"},
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
        "In progress": {"en": "In progress", "sr": "U toku"},
        "Installation: Phase": {"en": "Installation: Phase", "sr": "Instalacija: Faza"},
        "Installation finished!": {"en": "Installation finished!", "sr": "Instalacija završena!"},
        "✓ Successful": {"en": "✓ Successful", "sr": "✓ Uspešno"},
        "✗ Failed": {"en": "✗ Failed", "sr": "✗ Neuspešno"},
        "Failed plugins": {"en": "Failed plugins", "sr": "Neuspešni plugini"},
        "Do you want to retry failed ones?": {"en": "Do you want to retry failed ones?",
                                              "sr": "Želite li da ponovite neuspele?"},
        "All plugins installed successfully!": {"en": "All plugins installed successfully!",
                                                "sr": "Svi plugini su uspešno instalirani!"},
        "Retry logic will be added in the next version.": {"en": "Retry logic will be added in the next version.",
                                                           "sr": "Ponovni pokušaj neuspelih plugina biće dodato u sledećoj verziji."},
        "Failed plugins count": {"en": "Failed plugins", "sr": "Neuspešnih plugina"},
        "All recorded plugins are installed successfully.": {
            "en": "All recorded plugins are installed successfully.",
            "sr": "Svi zabeleženi plugini su uspešno instalirani."},
        "Select plugins to install": {"en": "Select plugins to install", "sr": "Izaberite plugine za instalaciju"},
        "No plugins selected!": {"en": "No plugins selected!", "sr": "Niste izabrali nijedan plugin!"},
        "Manual Selection": {"en": "Manual Selection", "sr": "Ručni izbor"},
        "Press OK to toggle, GREEN to start": {"en": "Press OK to toggle, GREEN to start",
                                               "sr": "OK za izbor, ZELENO za početak"},
        "All selected plugins are already installed!": {
            "en": "All selected plugins are already installed!",
            "sr": "Svi izabrani plugini su već instalirani!"},
        "About": {"en": "About", "sr": "O aplikaciji"},
        "Installation Time Estimates": {"en": "Installation Time Estimates", "sr": "Procena trajanja instalacije"},
        "Note: Speed depends on receiver CPU": {"en": "Note: Speed depends on receiver CPU", "sr": "Napomena: Brzina zavisi od procesora risivera"},
        "and internet/media speed (Flash/USB).": {"en": "and internet/media speed (Flash/USB).", "sr": "i brzine interneta/medija (Flash/USB)."},
        "Special thanks to the community.": {"en": "Special thanks to the community.", "sr": "Posebno hvala zajednici na testiranju."},
        "Special thanks to Gemini A.I. for support.": {"en": "Special thanks to Gemini A.I. for support.", "sr": "Posebna zahvala Gemini A.I. za podršku ."},
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

        self.start_time = 0
        self.elapsed_time = 0
        self.stopwatch_timer = eTimer()
        self.stopwatch_timer.callback.append(self.update_stopwatch)

    def update_stopwatch(self):
        self.elapsed_time += 1
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        # Formatiranje u 00:00 stil
        time_str = _("Time: ") + "%02d:%02d" % (minutes, seconds)
        self["timer_label"].setText(time_str)

    def start_timer(self):
        self.elapsed_time = 0
        self["timer_label"].setText(_("Time: 00:00"))
        self.stopwatch_timer.start(1000)  # Pokreće se na svakih 1000ms (1 sekunda)

    def stop_timer(self):
        self.stopwatch_timer.stop()

    def update_info(self, status, detail):
        self["status"].setText(status)
        self["detail"].setText(detail)

class CiefpEasySetup(Screen):
    skin = """
    <screen name="CiefpEasySetup" position="center,center" size="1600,800" title="CiefpEasySetup - Multi-Image PY3 One-Click Installer)">
        <widget name="list" position="20,20" size="780,680" scrollbarMode="showOnDemand" itemHeight="38" font="Regular;26" />
        <widget name="background" position="820,20" size="750,740" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CiefpEasySetup/background.png" zPosition="1" alphatest="on" />
        <widget name="status" position="20,720" size="780,50" font="Regular;22" halign="center" valign="center" />

        <widget name="key_red"    position="20,770"  size="240,40" font="Regular;24" halign="center" backgroundColor="#9F1313" foregroundColor="#FFFFFF" />
        <widget name="key_green"  position="280,770" size="240,40" font="Regular;24" halign="center" backgroundColor="#1F771F" foregroundColor="#FFFFFF" />
        <widget name="key_yellow" position="540,770" size="240,40" font="Regular;24" halign="center" backgroundColor="#9F9F13" foregroundColor="#000000" />
        <widget name="key_blue"   position="800,770" size="240,40" font="Regular;24" halign="center" backgroundColor="#13389F" foregroundColor="#FFFFFF" />
    </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        self.IMPORT_OK = IMPORT_OK

        self["list"] = MenuList([])
        self["background"] = Pixmap()
        self["status"] = Label("Učitavam stanje...")
        # ZAMENI STARE LINIJE OVIM:
        self["key_red"] = Label(_("Exit"))
        self["key_green"] = Label(_("Start Installation"))
        self["key_yellow"] = Label(_("Check Status"))
        self["key_blue"] = Label(_("Reboot Options"))

        self.status_data = load_status() if IMPORT_OK else {}
        self.sync_with_system()
        # DODAJ OVE LINIJE:
        global CURRENT_LANG
        CURRENT_LANG = self.status_data.get("settings_lang", "sr")  # Ako nema ništa u JSON, stavi 'sr'
        self.success_plugins = set()
        self.failed_plugins = set()
        self.current_phases = []
        self.current_phase_index = 0
        self.plugins_to_install = []
        self.current_plugin_index = 0

        self.build_list()
        self.update_status_text()
        self.mini_screen = None

        self["actions"] = ActionMap(["ColorActions", "OkCancelActions", "MenuActions", "DirectionActions"], {
            "red": self.exit,
            "green": self.show_install_menu,
            "yellow": self.check_status,
            "blue": self.show_reboot_menu,
            "menu": self.show_config_menu,
            "ok": self.ok,
            "cancel": self.exit,
        }, -1)

    def sync_with_system(self):
        """Tiha provera i ažuriranje JSON fajla prema stanju na disku."""
        if not IMPORT_OK: return

        from installer import check_system_for_plugins
        installed_on_disk = check_system_for_plugins(PLUGINS_DB)

        # Uzmi trenutne podatke iz JSON-a
        current_plugins = self.status_data.get("plugins", {})

        # Ažuriraj status za svaki plugin iz baze
        for p in PLUGINS_DB:
            name = p.get("name")
            if name in installed_on_disk:
                # Ako je nađen na disku, uvek označi kao uspeh
                current_plugins[name] = {"success": True, "phase": p.get("phase")}
            else:
                # Ako ga nema na disku, a u JSON-u piše da je instaliran, ispravi to
                if name in current_plugins and current_plugins[name].get("success"):
                    current_plugins[name]["success"] = False

        self.status_data["plugins"] = current_plugins

        # Osveži statuse faza (1, 2, 3)
        for phase in [1, 2, 3]:
            phase_plugins = [p for p in PLUGINS_DB if p.get("phase") == phase]
            self.status_data[f"phase{phase}_done"] = all(
                current_plugins.get(pp["name"], {}).get("success") for pp in phase_plugins
            )

        save_status(self.status_data)

    def show_config_menu(self):
        # Dodajemo "About" u listu koja se prikazuje korisniku
        options = [
            (_("Select Language"), "lang"),
            (_("About"), "about")  # Ovo je ključna reč koju šaljemo callback-u
        ]
        self.session.openWithCallback(self.config_menu_callback, ChoiceBox, title=_("Settings"), list=options)

    def config_menu_callback(self, choice):
        if choice:
            if choice[1] == "lang":
                # Tvoj postojeći kod za promenu jezika
                langs = [("English", "en"), ("Srpski", "sr")]
                self.session.openWithCallback(self.set_language, ChoiceBox, title=_("Select Language"), list=langs)

            elif choice[1] == "about":
                # Ako je korisnik kliknuo na About, pokreni funkciju koju smo gore dodali
                self.show_about_info()

    def show_about_info(self):
        # Naslov i osnovni info (PY3)
        about_text = "CiefpEasySetup v1.2\n"
        about_text += "Multi-Image One-Click Installer (PY3)\n\n"

        # Sekcija za vreme (Prevedena preko tvoje _(txt) funkcije)
        about_text += "--- " + _("Installation Time Estimates") + " ---\n"
        about_text += "• OpenATV, Pure2, OpenSPA: ~10-15 min eMMC,~35-40 min OMB\n"
        about_text += "• OpenPLi (Scarthgap): ~10-15 min eMMC,~50-60 min OMB\n\n"

        # Napomene
        about_text += _("Note: Speed depends on receiver CPU") + "\n"
        about_text += _("and internet/media speed (Flash/USB).") + "\n\n"

        about_text += "Author: ciefp\n"
        about_text += _("Special thanks to the community.") + "\n"
        about_text += _("Special thanks to Gemini A.I. for support.")

        # MessageBox prikazuje tekst na ekranu
        self.session.open(MessageBox, about_text, MessageBox.TYPE_INFO)

    def set_language(self, lang):
        if lang:
            global CURRENT_LANG
            CURRENT_LANG = lang[1]

            # Snimanje izbora u JSON da bi se pamtilo nakon restarta
            self.status_data["settings_lang"] = CURRENT_LANG
            save_status(self.status_data)

            # Osvežavanje UI elemenata
            self["key_red"].setText(_("Exit"))
            self["key_green"].setText(_("Start Installation"))
            self["key_yellow"].setText(_("Check Status"))
            self["key_blue"].setText(_("Reboot Options"))
            self.setTitle("CiefpEasySetup - " + _("Settings"))

            # Opciona potvrda
            self.session.open(MessageBox, _("Language changed."), MessageBox.TYPE_INFO, timeout=3)

    def build_list(self):
        if not self.IMPORT_OK:
            self["list"].setList([])
            return

        # Koristimo PLUGINS_DB koji je uvezen na vrhu fajla
        all_plugins = PLUGINS_DB
        plugins_status = self.status_data.get("plugins", {})
        list_data = []

        # Osiguravamo da temp_selection postoji
        if not hasattr(self, "temp_selection"):
            self.temp_selection = {}

        for p in all_plugins:
            name = p.get("name", "Unknown")
            status = plugins_status.get(name, {})
            is_installed = status.get("success", False)

            plugin_info = p.copy()

            if is_installed:
                display_name = f"✓ {name}"
                plugin_info["selected"] = False
            else:
                # Proveravamo da li je korisnik već označio ovaj plugin u ovoj sesiji
                was_selected = self.temp_selection.get(name, False)
                prefix = "[X] " if was_selected else "[  ] "
                display_name = f"{prefix}{name}"
                plugin_info["selected"] = was_selected

            list_data.append((display_name, plugin_info))

        self["list"].setList(list_data)

    def update_status_text(self):
        self.status_data = load_status()
        if not IMPORT_OK:
            self["status"].setText(_("ERROR: File import problem"))
            return

        # Funkcija za skraćivanje koda: proverava fazu i vraća prevod statusa
        def get_phase_status(phase_num):
            key = f"phase{phase_num}_done"
            if self.status_data.get(key, False):
                return _("DONE")
            return _("Not done")

        # Sastavljanje teksta koristeći prevode
        txt = f"{_('Phase')} 1: {get_phase_status(1)}  |  "
        txt += f"{_('Phase')} 2: {get_phase_status(2)}  |  "

        # Logika za Fazu 3: Ako je završena piše DONE, inače proveri da li se trenutno instalira
        if self.status_data.get('phase3_done', False):
            txt += f"{_('Phase')} 3: {_('DONE')}"
        else:
            # Ako je pokrenuta instalacija, ovde možeš ostaviti "U toku" ili "Nije"
            txt += f"{_('Phase')} 3: {_('Not done')}"

        self["status"].setText(txt)

    def install_single_plugin_confirmed(self, answer):
        if answer:
            idx = self["list"].getCurrentIndex()
            plugin = self["list"].list[idx][1]

            # Pokreni mini skin samo za ovaj jedan
            if not self.mini_screen:
                self.hide()
                self.mini_screen = self.session.open(CiefpInstallProgress)
                self.mini_screen.start_timer()

            self.mini_screen.update_info("Ručna instalacija...", plugin.get("name"))

            # Izvrši komandu (bez skip_reboot jer je ručno)
            success = run_command(plugin.get("command"), skip_reboot=False)

            # Sačuvaj status
            self.status_data.setdefault("plugins", {})[plugin.get("name")] = {"success": success}
            save_status(self.status_data)

            # Zatvori mini i osveži listu
            if self.mini_screen:
                self.mini_screen.close()
                self.mini_screen = None
            self.show()
            self.build_list()

    # ====================== ZELENA - INSTALACIJA ======================
    def show_install_menu(self):
        # Proveravamo šta je korisnik selektovao sa [X]
        manual_selection = [item[1] for item in self["list"].list if item[1].get("selected", False)]

        if manual_selection:
            # Ako ima [X] oznaka, odmah nudimo potvrdu za njih
            self.session.openWithCallback(
                self.start_manual_confirmed,
                MessageBox,
                _("Do you want to install selected plugins?"),
                MessageBox.TYPE_YESNO
            )
        else:
            # Ako nema [X], otvori standardni meni za faze
            options = [
                (_("Install ALL"), "all"),
                (_("Only Phase 1 (System)"), 1),
                (_("Only Phase 2 (Ciefp plugins)"), 2),
                (_("Only Phase 3 (Others)"), 3),
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

        # ChoiceBox vraća tuple ("tekst", value)
        if isinstance(choice, tuple):
            choice = choice[1]

        all_plugins = PLUGINS_DB
        plugins_status = self.status_data.get("plugins", {})
        selected_list = []

        # 1. Odabir osnovne liste na osnovu izbora korisnika
        if choice == "manual":
            selected_list = [item[1] for item in self["list"].list if item[1].get("selected", False)]
            self.current_phase_label = _("Manual Selection")
        elif choice == "all":
            selected_list = all_plugins
            self.current_phase_label = _("Install ALL")
        elif isinstance(choice, int):
            selected_list = [p for p in all_plugins if p.get("phase") == choice]
            self.current_phase_label = f"{_('Phase')} {choice}"
        elif choice == "1+2":
            selected_list = [p for p in all_plugins if p.get("phase") in [1, 2]]
            self.current_phase_label = f"{_('Phase')} 1 + 2"

        if not selected_list:
            self.session.open(MessageBox, _("No plugins selected!"), MessageBox.TYPE_INFO)
            return

        # 2. Detekcija imidža i filtriranje liste
        pli_detected = is_openpli()
        self.plugins_to_install = []

        for p in selected_list:
            name = p.get("name")

            # Dinamička promena komande za Abertis ako je detektovan OpenPLi
            if name == "CiefpSettingsT2miAbertis":
                if pli_detected:
                    p[
                        "command"] = "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsT2miAbertisOpenPLi/main/installer.sh -O - | /bin/sh"
                else:
                    p[
                        "command"] = "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsT2miAbertis/main/installer.sh -O - | /bin/sh"

            # Provera da li je već instaliran (da preskočimo nepotrebno)
            status = plugins_status.get(name)
            if not status or not status.get("success", False):
                self.plugins_to_install.append(p)

        if not self.plugins_to_install:
            self.session.open(MessageBox, _("All selected plugins are already installed!"), MessageBox.TYPE_INFO)
            return

        # 3. Reset stanja i pokretanje mini skina
        self.current_plugin_index = 0
        self.success_plugins = []
        self.failed_plugins = []
        self.temp_selection = {}

        self.hide()
        if not self.mini_screen:
            self.mini_screen = self.session.open(CiefpInstallProgress)

        # 🔥 POKRENI ŠTOPERICU PRE NEGO ŠTO POČNE INSTALACIJA
        self.mini_screen.start_timer()

        self.start_actual_installation()

    def start_actual_installation(self):
        # 🔥 POKRENI ŠTOPERICU AKO VEĆ NIJE POKRENUTA
        if self.mini_screen:
            self.mini_screen.start_timer()

        # Malo zakašnjenje da se UI osveži pre teškog posla
        self.plugin_timer = eTimer()
        self.plugin_timer.callback.append(self.install_next_plugin)
        self.plugin_timer.start(500, True)

    def on_install_finished(self, *args):
        # Ova funkcija vraća fokus na glavni prozor kada se progres završi
        self.show()
        self.build_list()
        self.update_status_text()

    def start_installation_process(self):
        # 🔥 POKRENI ŠTOPERICU NA MINI SKINU
        if self.mini_screen:
            self.mini_screen.start_timer()  # <-- DODAJ OVO

        if not self.plugins_to_install:
            self.show()
            return

        if not self.mini_screen:
            self.mini_screen = self.session.open(CiefpInstallProgress)
            self.mini_screen.start_timer()  # <-- I OVDE DODAJ

        self.mini_screen.update_info(_("Installation in progress..."), _("Preparing..."))

        self.plugin_timer = eTimer()
        self.plugin_timer.callback.append(self.install_next_plugin)
        self.plugin_timer.start(500, True)

    def install_next_plugin(self):
        # Da li smo završili listu?
        if self.current_plugin_index >= len(self.plugins_to_install):
            if self.mini_screen:
                self.mini_screen.stop_timer()
                self.mini_screen.close()
                self.mini_screen = None
            self.show()
            self.summary_timer = eTimer()
            self.summary_timer.callback.append(self.show_install_summary)
            self.summary_timer.start(100, True)
            return

        # Uzmi podatke o trenutnom pluginu
        plugin = self.plugins_to_install[self.current_plugin_index]
        name = plugin.get("name", "Unknown")

        # Javi progres baru
        if self.mini_screen:
            status = f"{_('Installation in progress...')}"
            details = f"[{self.current_plugin_index + 1}/{len(self.plugins_to_install)}] {name}"
            self.mini_screen.update_info(status, details)

        # IZVRŠI INSTALACIJU
        success = run_command(plugin.get("command"), skip_reboot=True)

        # Sačuvaj rezultat
        if success:
            self.success_plugins.append(name)
        else:
            self.failed_plugins.append(name)

        self.status_data.setdefault("plugins", {})[name] = {"success": success, "phase": plugin.get("phase")}
        save_status(self.status_data)

        # Sledeći!
        self.current_plugin_index += 1
        self.plugin_timer.start(500, True)

    def show_install_summary(self):
        total = len(self.success_plugins) + len(self.failed_plugins)

        # ================== ✅ UPDATE FAZA STATUS ==================
        all_plugins = PLUGINS_DB
        self.status_data = load_status()  # 🔥 KLJUČNO
        plugins_status = self.status_data.get("plugins", {})

        def is_phase_done(phase_num):
            phase_plugins = [p for p in all_plugins if p.get("phase") == phase_num]
            for p in phase_plugins:
                name = p.get("name")
                status = plugins_status.get(name)
                if not status or not status.get("success", False):
                    return False
            return True

        # Postavi status za sve faze (bitno!)
        for phase in [1, 2, 3]:
            self.status_data[f"phase{phase}_done"] = is_phase_done(phase)

        save_status(self.status_data)
        # ==========================================================

        # Sastavljanje poruke
        msg = f"{_('Installation finished!')}\n\n"
        msg += f"{_('✓ Successful')}: {len(self.success_plugins)} / {total}\n"
        msg += f"{_('✗ Failed')}: {len(self.failed_plugins)}\n\n"

        if self.failed_plugins:
            msg += f"{_('Failed plugins')}:\n"
            msg += "\n".join([f"• {p}" for p in sorted(self.failed_plugins)[:12]])
            msg += f"\n\n{_('Do you want to retry failed ones?')}"

            self.session.openWithCallback(
                self.retry_failed,
                MessageBox,
                msg,
                MessageBox.TYPE_YESNO,
                default=False
            )
        else:
            msg += _("All plugins installed successfully!")
            self.session.open(MessageBox, msg, MessageBox.TYPE_INFO, timeout=15)

        # ✅ Osveži UI u oba slučaja
        self.build_list()
        self.update_status_text()

    def retry_failed(self, answer):
        if answer:
            self.session.open(MessageBox, _("Retry logic will be added in the next version."), MessageBox.TYPE_INFO)
        self.build_list()
        self.update_status_text()

    # ====================== ŽUTA - PROVERA ======================
    def check_status(self):
        self["status"].setText("Skeniram sistem, molimo sačekajte...")
        
        # 1. Pozovi skeniranje iz installer.py
        from installer import check_system_for_plugins
        installed_list = check_system_for_plugins(PLUGINS_DB)
        
        # 2. Osveži status_data na osnovu pronađenog stanja
        new_plugins_status = {}
        for p in PLUGINS_DB:
            p_name = p.get("name")
            if p_name in installed_list:
                new_plugins_status[p_name] = {"success": True, "phase": p.get("phase")}
            else:
                # Zadrži stari neuspeh ako je postojao, ili ostavi prazno
                old_status = self.status_data.get("plugins", {}).get(p_name, {})
                if old_status.get("success") is False:
                    new_plugins_status[p_name] = old_status

        self.status_data["plugins"] = new_plugins_status
        
        # 3. Ponovo izračunaj da li su faze gotove
        for phase in [1, 2, 3]:
            phase_plugins = [p for p in PLUGINS_DB if p.get("phase") == phase]
            is_done = True
            for pp in phase_plugins:
                if pp.get("name") not in installed_list:
                    is_done = False
                    break
            self.status_data[f"phase{phase}_done"] = is_done

        # 4. Sačuvaj u JSON i osveži UI
        save_status(self.status_data)
        self.build_list()
        self.update_status_text()

        # 5. Prikaži MessageBox (tvoj postojeći kod za prikaz)
        msg = f"=== {_('Current Status')} ===\n\n"
        def get_done_text(val):
            return _("DONE") if val else _("Not done")

        msg += f"{_('Phase')} 1: {get_done_text(self.status_data.get('phase1_done'))}\n"
        msg += f"{_('Phase')} 2: {get_done_text(self.status_data.get('phase2_done'))}\n"
        msg += f"{_('Phase')} 3: {get_done_text(self.status_data.get('phase3_done'))}\n\n"
        
        msg += _("System is successfully synchronized with the list.")
        self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
    # ====================== PLAVA - REBOOT ======================
    def show_reboot_menu(self):
        from Screens.ChoiceBox import ChoiceBox
        # Koristimo _() za svaku opciju i naslov
        options = [
            (_("Reboot Box"), "reboot"),
            (_("Restart Enigma2 (GUI)"), "restart"),
            (_("Cancel"), "cancel")
        ]
        self.session.openWithCallback(self.do_reboot, ChoiceBox, title=_("Select action:"), list=options)

    def do_reboot(self, choice):
        if choice:
            action = choice[1] # ChoiceBox vraća tuple (ime, id)
            if action == "reboot":
                os.system("reboot")
            elif action == "restart":
                os.system("killall -9 enigma2")
                
    # ==========================================================
    def ok(self):
        # Umesto getCurrentIndex() koristimo getSelectionIndex()
        idx = self["list"].getSelectionIndex()

        if idx >= 0:
            # Uzimamo trenutnu listu stavki
            curr_list = self["list"].list
            item = curr_list[idx]

            # item je tuple: (prikazni_tekst, podaci_o_pluginu)
            display_name = item[0]
            plugin_data = item[1]
            name = plugin_data.get("name")

            # Ako je plugin već instaliran (ima kvačicu u imenu), ne radimo ništa
            if "✓" in display_name:
                return

            if not hasattr(self, "temp_selection"):
                self.temp_selection = {}

            # Toggle selekcije (True -> False / False -> True)
            is_selected = not plugin_data.get("selected", False)
            plugin_data["selected"] = is_selected
            self.temp_selection[name] = is_selected

            # Ažuriranje prikaza u listi
            # Ako je selektovan stavljamo [X], ako nije stavljamo [  ]
            prefix = "[X] " if is_selected else "[  ] "

            # Kreiramo novi tuple za tu poziciju
            new_item = (f"{prefix}{name}", plugin_data)

            # Zamenjujemo stari item novim u listi
            curr_list[idx] = new_item

            # Ponovo učitavamo listu u komponentu da se osveži ekran
            self["list"].setList(curr_list)
            self["list"].moveToIndex(idx) # Drži fokus na istoj liniji

    def exit(self):
        self.close()
        
def Plugins(**kwargs):
    return [
        PluginDescriptor(
            name="CiefpEasySetup v1.2",
            description="Multi-Image One-Click (PY3 Only: OpenATV, Pure2, OpenSPA, OpenPLi)",
            where=PluginDescriptor.WHERE_PLUGINMENU,
            icon="plugin.png",
            fnc=lambda session, **kwargs: session.open(CiefpEasySetup)
        )
    ]
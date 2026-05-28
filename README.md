
# CiefpEasySetup
 - Ultimate Enigma2 Automation & Plugin Installer

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Enigma2-orange.svg)](https://github.com/ciefp/CiefpEasySetup)
[![License](https://img.shields.io/badge/license-GPL--2.0-green.svg)](LICENSE)


### Preview

![Main Menu](https://i.postimg.cc/kMkJwSc7/ciefpeasysetup-1.jpg)
![Playlist](https://i.postimg.cc/Yq6H3s0h/ciefpeasysetup-2.jpg)
![WebCam](https://i.postimg.cc/7LcdD3bb/ciefpeasysetup-5.jpg)


**CiefpEasySetup** is the ultimate post-installation and system optimization tool for Enigma2 satellite receivers (Vu+, Dreambox, Zgemma, etc.). Designed for power users, developers, and enthusiasts, this plugin automates the tedious process of setting up a fresh Enigma2 image. 

Instead of manually downloading, FTP-ing, and installing dozens of components, **CiefpEasySetup** handles your entire ecosystem—installing up to 50+ essential plugins, softcams, system tools, and custom configuration files automatically in under 10 minutes.

---

## 🚀 Key Features

- **Blazing Fast Batch Installation:** Automatically installs your entire suite of custom plugins, dependencies, and extensions in one go.
- **Automated Dependency Resolution:** Checks for and installs required system packages (`python3-requests`, `curl`, `ffmpeg`, etc.) so your setup never breaks.
- **Smart Post-Install Control:** Includes smart execution flags like `SKIP_REBOOT` allowing you to perform continuous batch configurations without constant, time-consuming system restarts.
- **Custom Scripts Execution:** Seamlessly runs background shell scripts (`.sh`) tailored to optimize your local environment.
- **Multi-Image Compatibility:** Fully optimized and tested across major Enigma2 distributions including OpenATV (7.x+), OpenPLi, Pure2, and OpenViX.
- **Lightweight Architecture:** Written purely in Python and optimized to minimize memory overhead during deep background tasks.

---

## 🛠️ Quick Installation

You can get **CiefpEasySetup** up and running on your receiver with a single command via SSH/Telnet (using PuTTY or Terminal):

```bash
wget -O - [https://raw.githubusercontent.com/ciefp/CiefpEasySetup/main/installer.sh](https://raw.githubusercontent.com/ciefp/CiefpEasySetup/main/installer.sh) | bash
Manual Installation (Source Code)
Download or clone this repository.

FTP the CiefpEasySetup folder to your box under:
/usr/lib/enigma2/python/Plugins/Extensions/

Set folder and script permissions to 755.

Restart the Enigma2 GUI.
```

## ⚙️ How It Works & Configuration
The plugin relies on an optimized backend configuration system. It reads a centralized installer structure to pull required feeds, plugins, and dependencies safely.

The SKIP_REBOOT Flag
By default, standard installers force an Enigma2 GUI restart to apply changes. With CiefpEasySetup, you can toggle or pass a skip reboot trigger in your environment scripts. This allows you to chain multiple installation routines together and perform a single, clean reboot only when the entire environment is fully prepared.

## 🖥️ System Requirements & Dependencies
The plugin automatically tries to pull these, but ensuring they are available on your feed guarantees a flawless installation:


# Update package feed
opkg update

# Essential networking tools
opkg install curl wget python3-requests
Note: For older, legacy Python 2.7 images, make sure python-requests and basic core utilities are pre-installed.

# 🤝 Support & Contribution
Bug Reports & Requests: Please submit them via the GitHub Issues tracker.

# Disclaimer: 
This open-source utility is provided "as-is" for the Enigma2 community. Always back up your image/settings before running automated mass-installation scripts.

# Feedback: 
Join the discussion on major sat-forums or follow the project updates.

# Developer: 
Connected with the author on X (Twitter): @ciefp.

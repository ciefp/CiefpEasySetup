#!/bin/bash
##setup command=wget https://raw.githubusercontent.com/fairbird/NewVirtualKeyBoard/main/installer.sh -O - | /bin/sh

# Provera za SKIP_REBOOT - ako je postavljeno, ne radi restart na kraju
if [ "$SKIP_REBOOT" = "1" ]; then
    echo "SKIP_REBOOT je aktiviran - Enigma2 neće biti restartovan"
    DO_REBOOT=0
else
    DO_REBOOT=1
fi

###########
version="13.8"
description="
What is NEW :
- fixes some codes

ما هو الجديد :
- إصلاح بعض الاكواد
"

# remove old version
cp -r /usr/lib/enigma2/python/Plugins/SystemPlugins/NewVirtualKeyBoard/skins/kle /tmp/ >/dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Plugins/SystemPlugins/NewVirtualKeyboard >/dev/null 2>&1
#rm -f /usr/lib/enigma2/python/Screens/NewVirtualKeyBoard.py > /dev/null 2>&1
#rm -f /usr/lib/enigma2/python/Screens/NewVirtualKeyBoard.pyo > /dev/null 2>&1
#rm -f /usr/lib/enigma2/python/Screens/NewVirtualKeyBoard.pyc > /dev/null 2>&1
# Download and install plugin
echo " ** Download and install NewVirtualKeyBoard ** "
cd /tmp
set -e
rm -rf *main* >/dev/null 2>&1
rm -rf *NewVirtualKeyBoard* >/dev/null 2>&1
wget "https://github.com/fairbird/NewVirtualKeyBoard/archive/refs/heads/main.tar.gz"
tar -xzf main.tar.gz
cp -r NewVirtualKeyBoard-main/usr /
if [ -f '/tmp/kle' ]; then
	cp -f /tmp/kle/* /usr/lib/enigma2/python/Plugins/SystemPlugins/NewVirtualKeyBoard/skins/kle
fi
rm -rf /tmp/kle >/dev/null 2>&1
rm -rf *NewVirtualKeyBoard* >/dev/null 2>&1
rm -rf *main* >/dev/null 2>&1
echo
echo
set +e
cd ..

### Check if plugin installed correctly
if [ ! -d '/usr/lib/enigma2/python/Plugins/SystemPlugins/NewVirtualKeyBoard' ]; then
	echo "Some thing wrong .. Plugin not installed"
	exit 1
else
	if python --version 2>&1 | grep -q '^Python 3\.'; then
		echo ""
	else
		echo "You have Python2 image"
		echo "Send subtitles.py file"
		SubsSupport="/usr/lib/enigma2/python/Plugins/Extensions/SubsSupport"
		if [ -f "$SubsSupport/subtitles.py" ]; then
			wget -q -O "$SubsSupport/subtitles.py" "https://raw.githubusercontent.com/fairbird/NewVirtualKeyBoard/main/subtitles.py"
		fi
	fi
fi

sync
echo
echo
echo "###########################################################################"
echo "#                 NewVirtualKeyBoard INSTALLED SUCCESSFULLY               #"
echo "#                       mfaraj57 & RAED (fairbird)                        #"
echo "#                               support                                   #"
echo "#                         ttps://www.tunisia-sat.com                      #"
echo "#  restart enigma2 and select New virtual keyboard setup from menu-system #"
echo "###########################################################################"
echo

if [ "$DO_REBOOT" = "1" ]; then
    killall enigma2
else
    echo "###########################################################################"
    echo "#        INSTALLATION COMPLETE - SKIP_REBOOT=1                           #"
    echo "###########################################################################"
    echo "Molimo restartujte Enigma2 ručno kada budete spremni."
    echo "Zatim izaberite: menu -> system -> New virtual keyboard setup"
fi

exit 0
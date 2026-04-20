#!/bin/sh

# Provera za SKIP_REBOOT - ako je postavljeno, ne radi restart na kraju
if [ "$SKIP_REBOOT" = "1" ]; then
    echo "SKIP_REBOOT je aktiviran - Enigma2 neće biti restartovan"
    DO_REBOOT=0
else
    DO_REBOOT=1
fi

TMPDIR='/tmp'
PACKAGE='enigma2-plugin-extensions-xklass'
MY_URL='https://dreambox4u.com/emilnabil237/plugins/xklass'

PYTHON_VERSION=$(python -c "import platform; print(platform.python_version())")
MY_EM="============================================================================================================"

echo "***********************************************************************************************************************"

if python --version 2>&1 | grep -q '^Python 3\.'; then
    echo "You have Python3 image"
    PYTHON='PY3'
else
    echo "You have Python2 image"
    PYTHON='PY2'
fi

if [ -f /etc/opkg/opkg.conf ]; then
    STATUS='/var/lib/opkg/status'
    OSTYPE='Opensource'
    OPKGINSTAL='opkg install --force-overwrite'
    OPKGREMOV='opkg remove --force-depends'
elif [ -f /etc/apt/apt.conf ]; then
    STATUS='/var/lib/dpkg/status'
    OSTYPE='DreamOS'
    OPKGINSTAL='apt-get install -y'
    OPKGREMOV='apt-get purge --auto-remove -y'
    DPKINSTALL='dpkg -i --force-overwrite'
fi

rm -rf $TMPDIR/"${PACKAGE:?}"* > /dev/null 2>&1

if grep -qs "Package: $PACKAGE" $STATUS; then
    echo "   >>>>   Remove old version   <<<<"
    $OPKGREMOV $PACKAGE
    rm -rf /usr/lib/enigma2/python/Plugins/Extensions/XKlass
    sleep 1; clear
else
    echo "   >>>>   No Older Version Was Found   <<<<"
    sleep 1; clear
fi

echo "============================================================================================================================"
echo "   Install Plugin please wait "

if [ "$OSTYPE" = "Opensource" ]; then
    if [ "$PYTHON" = "PY3" ]; then
        opkg install python3-requests 
        opkg install python3-pillow
        opkg install p7zip
        opkg install curl
        opkg install enigma2-plugin-systemplugins-serviceapp
        opkg install ffmpeg
        opkg install exteplayer3
        opkg install gstplayer
        opkg update
        opkg install gstreamer1.0-plugins-good
        opkg install gstreamer1.0-plugins-ugly
    else
        opkg install python-requests
        opkg install python-multiprocessing
        opkg install python-image
        opkg install python-imaging
        opkg install enigma2-plugin-systemplugins-serviceapp
        opkg install ffmpeg
        opkg install exteplayer3
        opkg install gstplayer
        opkg update
        opkg install gstreamer1.0-plugins-good
        opkg install gstreamer1.0-plugins-ugly
        opkg install gstreamer1.0-plugins-base
        opkg install gstreamer1.0-plugins-bad
    fi

    echo "Installing XKlass plugin, please wait..."
    sleep 2
    cd /tmp
    curl -k -L -m 55532 -m 555104 "${MY_URL}/enigma2-plugin-extensions-xklass_all.ipk" > /tmp/enigma2-plugin-extensions-xklass_all.ipk
    sleep 1
    $OPKGINSTAL /tmp/enigma2-plugin-extensions-xklass_all.ipk
    echo ""
fi

if [ "$OSTYPE" = "DreamOS" ]; then
    if [ "$PYTHON" = "PY3" ]; then
        apt-get -y install python3-requests 
        apt-get -y install python3-multiprocessing
    else
        apt-get -y install python-requests
        apt-get -y install python-image
        apt-get -y install python-imaging
        apt-get -y install wget
    fi

    echo "Installing XKlass plugin, please wait..."
    sleep 2
    cd /tmp
    curl -k -L -m 55532 -m 555104 "${MY_URL}/enigma2-plugin-extensions-xklass_all.deb" > /tmp/enigma2-plugin-extensions-xklass_all.deb
    sleep 1
    $DPKINSTALL /tmp/enigma2-plugin-extensions-xklass_all.deb
    echo ""
fi

echo "DOWNLOAD Playlists By Emil_Nabil"
sleep 3
wget -O /etc/enigma2/xklass/playlists.txt "${MY_URL}/playlists.txt"
echo ""

echo "$MY_EM"
rm -rf $TMPDIR/"${PACKAGE:?}"*

sleep 1; clear
echo ""
echo "****************************************************************************************"
echo "$MY_EM"
echo "**                xklass **"
echo "****************************************************************************************"
echo ""

if [ "$DO_REBOOT" = "1" ]; then
    echo "Restartujem Enigma2 za 3 sekunde..."
    sleep 3
    killall -9 enigma2
else
    echo "Instalacija završena. SKIP_REBOOT=1 - restartujte Enigma2 ručno."
fi

exit 0
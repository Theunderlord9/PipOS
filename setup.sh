#!/bin/bash
set -e
# Sets Up The Pi After A Fresh Install (Requires Git But It Does The Rest)
# Usage: sudo ./setup.sh <username>
# Run As Sudo

if [ -z "$1" ]; then
    echo "Usage: sudo ./setup.sh <username>"
    exit 1
fi

USER=$1
HOME_DIR=/home/$USER

# Getting Apt Ready
apt update
apt upgrade
apt install -y python3 clang xorg xterm

# Pull Drivers
rm -rf LCD-show
git clone https://github.com/goodtft/LCD-show.git

# Copy Drivers
cp LCD-show/usr/mhs35ips-overlay.dtb /boot/overlays/
cp LCD-show/usr/mhs35ips-overlay.dtb /boot/overlays/mhs35ips.dtbo

# Back Up And Write Boot Config
cp /boot/config.txt /boot/configbackup.txt
cat >> /boot/config.txt <<EOF
hdmi_force_hotplug=1
dtparam=i2c_arm=on
dtparam=spi=on
enable_uart=1
dtoverlay=mhs35ips:rotate=90
hdmi_group=2
hdmi_mode=87
hdmi_cvt 480 320 60 6 0 0 0
hdmi_drive=2
EOF

# Xorg Config
cat > /etc/X11/xorg.conf <<EOF
Section "Device"
    Identifier "mhs35ips"
    Driver "fbdev"
    Option "fbdev" "/dev/fb1"
EndSection

Section "Screen"
    Identifier "Screen0"
    Device "mhs35ips"
EndSection
EOF

# Xinitrc
cat > $HOME_DIR/.xinitrc <<EOF
openbox &
xterm
EOF
chown $USER:$USER $HOME_DIR/.xinitrc

# Systemd Service
cat > /etc/systemd/system/xorg.service <<EOF
[Unit]
Description=Start Xorg At Boot
After=systemd-user-sessions.service

[Service]
ExecStart=/usr/bin/startx -- :0 -nocursor vt1
Restart=on-failure
User=$USER
Environment=HOME=$HOME_DIR
WorkingDirectory=$HOME_DIR

[Install]
WantedBy=multi-user.target
EOF

systemctl enable xorg.service

# Cleanup
rm -rf LCD-show

echo "Done. Reboot To Start Or Run startx To Boot Xorg"

#!/bin/sh

content=$(cat <<EOF
# udev rules for TiePie engineering USB devices
# see: www.tiepie.com/linux

SUBSYSTEM!="usb_device", ACTION!="add", GOTO="tiepie_rules_end"

# Add all TiePie engineering USB devices to the plugdev group
ATTR{idVendor}=="0e36", MODE="660", GROUP="plugdev"

LABEL="tiepie_rules_end"
EOF
)

# Specify the filename where you want to write this text
filename="/etc/udev/rules.d/45-tiepie-usb.rules"

# Install udev rules:
echo "Install udev rules"
echo "$content" > $filename

# Reload udev rules
echo "Reloading udev rules"
udevadm control --reload-rules
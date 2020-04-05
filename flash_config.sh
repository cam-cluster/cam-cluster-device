#!/bin/bash
#
# Interactively flash a RPi image for a device
#
# Prerequisites:
# - Install hypriot flash: https://github.com/hypriot/flash#installation
#

hypriotos_version="v1.12.0"
hypriotos_url="https://github.com/hypriot/image-builder-rpi/releases/download/${hypriotos_version}/hypriotos-rpi-${hypriotos_version}.img.zip"

# Check input parameters
if [ -z "$1" ]
then
  echo
  echo " Usage: $0 <userdata file>"
  echo
  exit -1
fi

echo "                                _           _            ";
echo "  ___ __ _ _ __ ___         ___| |_   _ ___| |_ ___ _ __ ";
echo " / __/ _\` | '_ \` _ \ _____ / __| | | | / __| __/ _ \ '__|";
echo "| (_| (_| | | | | | |_____| (__| | |_| \__ \ ||  __/ |   ";
echo " \___\__,_|_| |_| |_|      \___|_|\__,_|___/\__\___|_|   ";
echo "-- device flash configurator --"
echo

userdata_file_path="$1"
if [[ ! -f "$userdata_file_path" ]]; then
  echo "Error: Cannot find file \"${userdata_file_path}\""
  echo
  exit -2
fi

userdata="$(<$userdata_file_path)"

echo "Using hypriot os version ${hypriotos_version} with \"${userdata_file_path}\""

# Find all <placeholder> tags
placeholders=()
for text in ${userdata}; do
  if [[ "$text" =~ \<(.+)\> ]]; then
    placeholders+=(${BASH_REMATCH[1]})
  fi
done

# Get values for each <placeholder>
placeholder_values=()
for placeholder in ${placeholders[@]}; do
  read -p "${placeholder}: " value
  placeholder_values+=("$value")
done

## Replace each <placeholder> with its value
for i in "${!placeholders[@]}"; do 
  userdata=${userdata//"<${placeholders[i]}>"/"${placeholder_values[i]}"}
done

echo "$userdata"

# Save updated userdata to temp file for flash operation
tmpfile="$(mktemp)"
echo "$userdata" > "$tmpfile"
sleep 1

# Do the flash operation with all the info we've gathered
flash --userdata $tmpfile $hypriotos_url
#rm $tmpfile
echo $tmpfile

echo
echo "All done!"

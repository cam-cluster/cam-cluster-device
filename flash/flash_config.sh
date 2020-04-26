#!/bin/bash
#
# Interactively flash a RPi image for a device
#
# Prerequisites:
# - Install hypriot flash: https://github.com/hypriot/flash#installation
#

# Constants
hypriot_flash_version="2.7.0"
hypriot_flash_args=""
tempfile_rm_command="rm "

# Set common dir
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi

# Includes
. "$DIR/scripts/check_file.sh"
. "$DIR/scripts/parse_placeholders.sh"
. "$DIR/scripts/parse_yaml.sh"

function usage {
  echo
  echo " Usage: $0 <configmap.yaml file>"
  echo
}

function banner {
  echo "                                _           _            ";
  echo "  ___ __ _ _ __ ___         ___| |_   _ ___| |_ ___ _ __ ";
  echo " / __/ _\` | '_ \` _ \ _____ / __| | | | / __| __/ _ \ '__|";
  echo "| (_| (_| | | | | | |_____| (__| | |_| \__ \ ||  __/ |   ";
  echo " \___\__,_|_| |_| |_|      \___|_|\__,_|___/\__\___|_|   ";
  echo "-- device flash configurator --"
  echo
}

function parse_configmap {
  local file_path=$1

  configmap_dir=$(dirname $file_path)

  if ! check_file $file_path; then
    exit -2
  fi

  eval $(parse_yaml $file_path)
}

function parse_config {
  local config_name=$1
  local argument_tag=$2
  local config_file=$3

  local file_path="$configmap_dir/$config_file"
  if ! check_file $file_path; then
    exit -2
  fi
  echo "Adding $config_name: $file_path"

  local parsed_text=$(parse_placeholders $file_path)
  local tmpfile="$(mktemp)"
  echo "$parsed_text" > "$tmpfile"

  hypriot_flash_args="$hypriot_flash_args --$argument_tag $tmpfile"
  tempfile_rm_command="$tempfile_rm_command $tmpfile"
  echo
}

function flash_config {
  banner

  parse_configmap $configmap_yaml_file_path

  if [ ! -z $cloudinit_userdata ]; then
    echo "Using hypriot os version: $hypriotos_version"
    hypriotos_url="https://github.com/hypriot/image-builder-rpi/releases/download/${hypriotos_version}/hypriotos-rpi-${hypriotos_version}.img.zip"
    echo
  else
    echo "Must specify hypriot os version"
    exit -2
  fi

  if [ ! -z $raspberrypi_config ]; then
    parse_config "raspberry pi config" "bootconf" $raspberrypi_config
  fi

  if [ ! -z $cloudinit_userdata ]; then
    parse_config "cloud-init userdata" "userdata" $cloudinit_userdata
  fi

  echo "Preparing to flash sd card..."
  sleep 1

  hypriot_flash_script="$DIR/scripts/hypriot_flash_$hypriot_flash_version.sh"
  hypriot_flash_command="bash $hypriot_flash_script $hypriot_flash_args $hypriotos_url"

  echo "command: $hypriot_flash_command"

  eval $hypriot_flash_command
  eval $tempfile_rm_command

  echo
  echo "All done!"
  exit 0
}

# Check input parameters
if [ -z "$1" ]; then
  usage
  exit -1
fi

# Arguments
configmap_yaml_file_path="$1"

flash_config

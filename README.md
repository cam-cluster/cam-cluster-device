# cam-cluster-device
Camera Device for cam-cluster

## Instructions

The installer uses the [Hypriot Flash](https://github.com/hypriot/flash) utility,
so you'll need to follow the instructions there to install it.

Install the desired SD card for the Raspberry PI and then run:
  chmod a+x flash_config.sh
  ./flash_config.sh user-data.yml

This will prompt you for some settings such as hostname, wifi ssid and psk.
For the WiFi PSK, you can either enter a plain-text psk as such: "PASSWORD"
or you can use `wpa_passphrase SSID PASSWORD` first to encrypt the PSK
password, in which case make sure to exclude the quotes

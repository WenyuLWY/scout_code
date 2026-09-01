#!/bin/bash

# enable kernel module: gs_usb
sudo insmod gs_usb.ko


# bring up can interface
sudo ip link set can2 up type can bitrate 1000000
sudo ip link set can1 up type can bitrate 500000
# install can utils
sudo apt install -y can-utils

#!/bin/bash

#sudo insmod gs_usb.ko

# bring up can interface
sudo ip link set can2 up type can bitrate 500000

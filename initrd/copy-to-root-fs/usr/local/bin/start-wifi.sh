#!/bin/sh

modprobe wcn36xx
ifconfig wlan0 down
/etc/init.d/wpa_supplicant stop

ip link set wlan0 up
iwconfig wlan0 essid abyss
wpa_supplicant -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf &
sleep 5
udhcpc -i wlan0


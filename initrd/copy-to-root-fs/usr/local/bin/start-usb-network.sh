#!/bin/sh

# Every bit of this was extracted from the postmarketOS initrd
# https://gitlab.com/postmarketOS/pmaports/blob/master/main/postmarketos-mkinitfs/init_functions.sh

mount -t configfs configfs /config

modprobe usb_f_rndis
modprobe usb_f_ecm_subset
modprobe g_ether

sleep 1

CONFIGFS=/config/usb_gadget
mkdir $CONFIGFS/g1
printf "%s" "0x18D1" >"$CONFIGFS/g1/idVendor"
printf "%s" "0xD001" >"$CONFIGFS/g1/idProduct"
mkdir $CONFIGFS/g1/strings/0x409
mkdir $CONFIGFS/g1/functions/rndis.usb0
mkdir $CONFIGFS/g1/configs/c.1
mkdir $CONFIGFS/g1/configs/c.1/strings/0x409
printf "%s" "rndis" > $CONFIGFS/g1/configs/c.1/strings/0x409/configuration
ln -s $CONFIGFS/g1/functions/rndis.usb0 $CONFIGFS/g1/configs/c.1
echo "$(ls /sys/class/udc)" > $CONFIGFS/g1/UDC

IP=172.16.42.1
INTERFACE=usb0

ifconfig "$INTERFACE" "$IP"

# Create /etc/udhcpd.conf
{
	echo "start 172.16.42.2"
	echo "end 172.16.42.2"
	echo "auto_time 0"
	echo "decline_time 0"
	echo "conflict_time 0"
	echo "lease_file /var/udhcpd.leases"
	echo "interface $INTERFACE"
	echo "option subnet 255.255.255.0"
} >/etc/udhcpd.conf

echo "Start the dhcpcd daemon (forks into background)"
udhcpd

echo "Execute the following commands on the host to route traffic to the internet:"
echo ""
echo "    iptables -F -t filter"
echo "    iptables -X -t filter"
echo "    iptables -F -t nat"
echo "    iptables -X -t nat"
echo "    echo 1 | tee /proc/sys/net/ipv4/ip_forward > /dev/null"
echo "    iptables -P FORWARD ACCEPT"
echo "    iptables -A POSTROUTING -t nat -j MASQUERADE -s 172.16.42.0/24"
echo ""

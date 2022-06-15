uci delete network.lan
uci set network.lan=interface
uci set network.lan.ifname='eth0'
uci set network.lan.proto='dhcp'
uci commit
/etc/init.d/network restart
rm /etc/rc.d/S19dnsmasq
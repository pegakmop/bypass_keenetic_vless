#!/bin/sh
[ "$1" != "start" ] && exit 0
ipset create unblocksh hash:net -exist
ipset create unblockvless hash:net -exist
# ipset create unblockvpn hash:net -exist

if ls -d /opt/etc/unblock/vpn-*.txt >/dev/null 2>&1; then
for vpn_file_names in /opt/etc/unblock/vpn-*; do
vpn_file_name=$(echo "$vpn_file_names" | awk -F '/' '{print $5}' | sed 's/.txt//')
unblockvpn=$(echo unblock"$vpn_file_name")
ipset create "$unblockvpn" hash:net -exist
done
fi

exit 0
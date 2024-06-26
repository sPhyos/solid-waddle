#!/bin/bash

echo "Scanning for IP addresses on the network with netdiscover..."

sudo netdiscover -r 192.168.0.1/24 -P -N | grep ".*" | awk '{print $1}' >ip_list.txt

echo "Scanning for SSH port (22) on the found IP addresses..."

while read ip; do
    echo "Scanning IP: $ip"
    nmap_output=$(nmap -p 22 -A $ip)

    if echo "$nmap_output" | grep -q "22/tcp open"; then
        echo "SSH is open on IP: $ip"
        echo "Detailed information for IP: $ip"
        echo "$nmap_output"
        echo "--------------------------------------------------------"
    else
        echo "SSH is not open on IP: $ip"
    fi
done <ip_list.txt

rm ip_list.txt

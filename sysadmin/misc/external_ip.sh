#!/bin/bash
IP=$( wget -qO - http://cfaj.freeshell.org/ipaddr.cgi )
echo "Your external IP Address is: $IP"
exit 0

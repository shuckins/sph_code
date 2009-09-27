#!/bin/bash
###################################
#
# Written by Samuel Huckins
#
# March 2007
#
# Be sure to set the right network
# INTERFACE, as well as who will be
# mailed the message (RECIPIENT).
# Everything else should be fine on
# most any *nix box.
#
###################################
#
# Various config items, e.g. date,
# network interface, where to mail
# to, as well as definitions:
#
NOW=`date +'%H:%M%p on %A, %m/%e/%Y'`
DAY=`date +'%m/%e/%Y'`
# Let this be set as a command line parameter:
#INTERFACE="eth1"
# Make this smarter, to account for
# different locations of the command
# and columns
#IP=`ifconfig $INTERFACE | grep Mask | grep -v grep | awk '{sub(/addr:/, "IP: ", $2)} {print $2}'`
#MASK=`ifconfig $INTERFACE | grep Mask | grep -v grep | awk '{sub(/Mask:/, "Mask: ", $4)} {print $4}'`
# Make this smarter, may be days
# and not hrs minutes, diff cols, etc:
UPTIME=`uptime | awk '{sub(/,/,"",$3)} {sub(/:/," hours, ", $3)} {sub(/$/, " minutes", $3)} {print $3}'`
# This too:
LOADAVG=`uptime | awk '{print $10 " " $11 " " $11}'`
SUBJECT="Status report for $HOSTNAME on $DAY"
RECIPIENT="wormwood_3@yahoo.com"
# Where the data is placed before
# mailing:
TEMPFILE="/tmp/testscriptresults"
touch $TEMPFILE;
#
# Write the server data and disk usage
# report to the tmpfile:
#
echo "Server: $HOSTNAME" > $TEMPFILE;
echo "Type: $MACHTYPE" >> $TEMPFILE;
echo "OS: `cat /etc/issue`" >> $TEMPFILE;
#echo $IP >> $TEMPFILE;
#echo $MASK >> $TEMPFILE;
echo "Uptime and load averages: `uptime`" >> $TEMPFILE;
echo "" >> $TEMPFILE;
echo "Disk usage report for $NOW:" >> $TEMPFILE;
df -hlT >> $TEMPFILE;
echo "" >> $TEMPFILE;
# Show who logged in this week, if
# the script is run as root:
if [ `whoami` = "root" ]; then
    echo "User(s) logged in within last 7 days: " >> $TEMPFILE;
    lastlog -t 7 >> $TEMPFILE
else
    echo "Run this script as root to see more info!" >> $TEMPFILE;
fi
#
# Display for testing only:
#
#echo $SUBJECT;
#echo "Going to $RECIPIENT";
#cat $TEMPFILE;
#rm -f $TEMPFILE
#
# When not testing, comment above 4 lines,
# and uncomment next 2 lines:
cat $TEMPFILE | mail -s "$SUBJECT" "$RECIPIENT"
rm -f $TEMPFILE
#
# END SCRIPT
exit 0

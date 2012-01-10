#!/bin/bash

DBUSER=root
DBPASS=
WAIT_SECONDS=.25
LOGF="poor-mans-query.log"

# Main loop
while true 
    do
    #mysqladmin -u$DBUSER -p$DBPASS processlist 
    #egrep -vw 'Sleep|processlist|Binlog Dump' |
    #awk -F'|' '{print $6, $7, $8, $9}'
    # First line of vmstat is historical, so take the second
    #vmstat 1 2 | tail -1
    # Sleep for a while
    #sleep $WAIT_SECONDS

    mysql -u$DBUSER -p$DBPASS -e "show full processlist;" | cut -f1,8 | tee -a $LOGF
    sleep $WAIT_SECONDS
done 

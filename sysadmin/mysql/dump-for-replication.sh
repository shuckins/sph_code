#!/bin/bash
######################################################################
#
# AUTHOR:   Samuel Huckins (www.samuelhuckins.com)
#
# STARTED:  December 2008
#
# PURPOSE:  This dumps a MySQL DB in a way suitable for importing 
# into a slave in a replication setup. It compresses and sends the 
# dump through SSH, stops the slave, imports the dump, starts the 
# slave, prints status on both.
#
# Should be run from the master server. 
#
# SECURITY: All transfer are over SSH, all dump files are
# removed after use, and all messages are only to local console. 
# mysqldump hides the password passed from things like ps, so that
# should be safe.
#
# NOTES:
# * This assumes SSH key connections are working between master and
#   slave.
# * This assumes you have binary logging on and configured on the 
#   master.
# * This assumes you have have the slave configured to replicate the
#   master (creds, DB, etc).
# * You must set the user, password, and other variables below before 
#   running.
# * This script will lock the tables in the master DB while dumping, 
#   so be aware when using against production boxes. Time of lock
#   depends on DB size.
#
######################################################################
#
# SET THESE FIRST!
DATABASE_TO_REPLICATE="test"
MASTER_SERVER_USER="root"
MASTER_SERVER_PASSWORD=""
SLAVE_SERVER=""
SLAVE_SERVER_USER="root"
SLAVE_SERVER_PASSWORD=""
SLAVE_SERVER_SOCKET="/var/lib/mysql/mysql.sock"
#
echo " * Creating dump file and transferring..."
mysqldump -u $MASTER_SERVER_USER -p$MASTER_SERVER_PASSWORD --master-data=1 $DATABASE_TO_REPLICATE | gzip -c | ssh $SLAVE_SERVER "gunzip -c > $DATABASE_TO_REPLICATE-dump.sql" &&
echo " * Dump file created and transferred."
rm -f $DATABASE_TO_REPLICATE-dump.sql &&
echo " * Dump file local copy deleted."
echo " * Creating database $DATABASE_TO_REPLICATE on $SLAVE_SERVER..."
ssh $SLAVE_SERVER "mysql -u $SLAVE_SERVER_USER -S $SLAVE_SERVER_SOCKET -p$SLAVE_SERVER_PASSWORD -e 'drop database if exists $DATABASE_TO_REPLICATE ; create database $DATABASE_TO_REPLICATE ;'" &&
echo " * $DATABASE_TO_REPLICATE created on $SLAVE_SERVER."
echo " * Stopping slave..."
ssh $SLAVE_SERVER "mysql -u $SLAVE_SERVER_USER -S $SLAVE_SERVER_SOCKET -p$SLAVE_SERVER_PASSWORD -e 'SLAVE STOP;'" &&
echo " * Slave stopped."
echo " * Importing dump file..."
ssh $SLAVE_SERVER "mysql -u $SLAVE_SERVER_USER -S $SLAVE_SERVER_SOCKET -p$SLAVE_SERVER_PASSWORD $DATABASE_TO_REPLICATE < $DATABASE_TO_REPLICATE-dump.sql" &&
echo " * Dump file imported into slave."
rm -f $DATABASE_TO_REPLICATE-dump.sql &&
echo " * Dump file remote copy deleted."
echo " * Starting slave..."
ssh $SLAVE_SERVER "mysql -u $SLAVE_SERVER_USER -S $SLAVE_SERVER_SOCKET -p$SLAVE_SERVER_PASSWORD -e 'SLAVE START;'" &&
echo " * Slave started."
echo " * Master status:"
mysql -u $MASTER_SERVER_USER -p$MASTER_SERVER_PASSWORD -e 'SHOW MASTER STATUS;'
echo ""
echo " * Slave status:"
ssh $SLAVE_SERVER "mysql -u $SLAVE_SERVER_USER -S $SLAVE_SERVER_SOCKET -p$SLAVE_SERVER_PASSWORD -e 'SHOW SLAVE STATUS\G;'" | grep "IO\|Host\|User\|Master_Log_File\|Pos\|Last_Error\|Replicate_Do_DB" &&
echo ""
echo "All done."
exit

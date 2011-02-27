#!/bin/bash
#===============================================================================
#          FILE:  mysql-backup.sh
# 
#         USAGE:  ./mysql-backup.sh 
# 
#        AUTHOR:  Samuel Huckins, wormwood_3@yahoo.com
#       STARTED:  12/28/2009 08:07:16 PM EST
# 
#   DESCRIPTION:  MySQL backup script. Provides instructions for prerequisite
#   setup. 
#   Dumps are made locally to ensure a copy, then rsynced to a remote server. 
#   After the remote transfer the local copy is removed.
#
#   Type of backup taken:
#       * Text, SQL dumps: Uses mysqldump. Human-readable format, easy to read.
#         Info: http://dev.mysql.com/doc/refman/5.0/en/mysqldump.html
#
#   Restoration:
#   To restore from the text dumps, a variant of the following should suffice:
#   mysql -u root -p [password] [database_to_restore] < [database_dump.sql]
#
#===============================================================================

# ============== [ Config ] ==============
# Credentials for DB user that will create dumps
USER="backup"
PASSWORD="MaSXyByRaa8GJXTujWsE"
# Socket file for DB instance to be backed up
SOCKET="/var/run/mysqld/mysqld.sock"
    
# User that should run this script
LOCAL_USER="admin"
# Location where dumps are stored on DB server;
# make sure this exists, as well as "dumps" therein
LOCAL_BACKUP_DIR="/home/$LOCAL_USER/mysql-backups"
# Log of all steps. Make sure LOCAL_USER can write to this.
LOG="/var/log/mysql-backup.log"

# Remote server that dumps are rsynced to
RSYNC_SERV="catapult-creative.com"
# Should be setup with SSH key access by LOCAL_USER
RSYNC_USER="rembackup"
# Location where dumps are stored on remote server
REMOTE_BACKUP_DIR="/home/rembackup/htt_backups"
# Port on which SSH is running on remote server
REMOTE_PORT="5446"

# ============== [ Setup ] ==============
# Ensure that USER defined above is allowed:
#  * DB SELECT, SHOW VIEW, RELOAD, and LOCK privs
# To set this, run:
# GRANT SELECT, SHOW VIEW, LOCK TABLES, RELOAD ON *.* TO 'BACKUP_USER'@'localhost' IDENTIFIED BY 'PASSWORD';
# FLUSH PRIVILEGES;
#
# Replacing BACKUP_USER and PASSWORD with their correct values.

# DO NOT MODIFY BELOW UNLESS YE KNOW WHAT YE DO -------------------------------

echo "`date '+%Y-%m-%d_%H-%M-%S'` - ----- MARK -----" >> $LOG
# ============== [ Verifications ] ==============
# Check that we're running as the right user
if [ `/usr/bin/whoami` != $LOCAL_USER ]; then
    echo "Sorry, this needs to be run as $LOCAL_USER. Exiting." 
    exit
fi

echo "`date '+%Y-%m-%d_%H-%M-%S'` - Confirmed running as $LOCAL_USER. Local dumps will be in $LOCAL_BACKUP_DIR." >> $LOG

# ============== [ Dumps ] ==============
DBS=`/usr/bin/mysql --socket=$SOCKET --user=$USER --password="$PASSWORD" --batch --silent --execute="show databases;"`
for DB in $DBS
do
    # We don't ever need to back this up:
    if [ "$DB" == "information_schema" ]; then
        continue
    fi

    # Text dump (schema, data):
    echo "`date '+%Y-%m-%d_%H-%M-%S'`- Starting text dump of $DB... " >> $LOG
    /usr/bin/mysqldump --socket=$SOCKET --user=$USER --password=$PASSWORD --force --complete-insert --routines $DB > $LOCAL_BACKUP_DIR/dumps/$DB-dump.sql &&
    echo "`date '+%Y-%m-%d_%H-%M-%S'`- Done!" >> $LOG
done

echo "`date '+%Y-%m-%d_%H-%M-%S'`- Local dumps complete." >> $LOG

# ============== [ rsync ] ==============
echo "`date '+%Y-%m-%d_%H-%M-%S'`- rsyncing dumps to $RSYNC_SERV..." >> $LOG
/usr/bin/rsync --archive --recursive --compress --port=$REMOTE_PORT -e "ssh -p $REMOTE_PORT" $LOCAL_BACKUP_DIR $RSYNC_USER@$RSYNC_SERV:$REMOTE_BACKUP_DIR >> $LOG 2>&1 &&
echo "`date '+%Y-%m-%d_%H-%M-%S'`- Done!" >> $LOG

# ============== [ Remove temp files ] ==============
echo "`date '+%Y-%m-%d_%H-%M-%S'`- Removing local dump files..." >> $LOG
/bin/rm -rf $LOCAL_BACKUP_DIR/dumps/* &&
echo "`date '+%Y-%m-%d_%H-%M-%S'`- Done!" >> $LOG

#------------------------------------------------------------------------------
echo "`date '+%Y-%m-%d_%H-%M-%S'`- Backup operations complete." >> $LOG
exit

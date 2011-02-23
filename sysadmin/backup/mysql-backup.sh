#!/bin/bash
#===============================================================================
#          FILE:  mysql-backup.sh
# 
#         USAGE:  sudo ./mysql-backup.sh 
# 
#   DESCRIPTION:  MySQL backup script. Provides instructions for prerequisite
#   setup as well as optional commented approaches for varying circumstances. 
#   Dumps are made locally to ensure a copy, then rsynced to a remote server. 
#   N.B.: Script must be run with sudo or by user with filesystem read access 
#   to MySQL's data files.
#
#   Two types of backups are taken:
#       * Text, SQL dumps: Uses mysqldump. Human-readable format, easy to read.
#         Info: http://dev.mysql.com/doc/refman/5.0/en/mysqldump.html
#       * Binary, hotcopies: Uses mysqlhotcopy. Faster to backup, faster
#         to restore and more reliable for live DBs. Info: 
#         http://dev.mysql.com/doc/refman/5.0/en/mysqlhotcopy.html
#
#   Restoration:
#   To restore from the binary dumps (recommended) you simply need to copy all
#   the datafiles per DB under LOCAL_BACKUP_DIR/hotcopies to the appropriate
#   data directory for the MySQL instance. If you then start MySQL the DB should
#   be in the exact state as when the dump was taken.
#
#   To restore from the text dumps, a variant of the following should suffice:
#   mysql -u root -p [password] [database_to_restore] < [database_dump.sql]
# 
#        AUTHOR:  Samuel Huckins, wormwood_3@yahoo.com
#       STARTED:  12/28/2009 08:07:16 PM EST
#===============================================================================

# ============== [ Config ] ==============
# Credentials for DB user that will create dumps
USER="root"
PASSWORD=""
# Socket file for DB instance to be backed up
SOCKET="/var/run/mysqld/mysqld.sock"
    
# Location where dumps are stored on DB server;
# make sure this exists, as well as directories "dumps"
# and "hotcopies" therein
LOCAL_BACKUP_DIR="/backups/mysql"
# Log of all steps
LOG="/var/log/mysql-backup.log"

# Remote server that dumps are rsynced to
RSYNC_SERV=""
# Should be setup with SSH key access
RSYNC_USER=""
# Location where dumps are stored on remote server
REMOTE_BACKUP_DIR=""

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

# ============== [ Dumps ] ==============
# To avoid using the password option with no value
PASS_STRING=""
if [ "$PASSWORD" != "" ]; then
    PASS_STRING="--password=\"$PASSWORD\""
fi

DBS=`/usr/bin/mysql --socket=$SOCKET --user=$USER $PASS_STRING --batch --silent --execute="show databases;"`
for DB in $DBS
do
    # We don't need to back this up, and mysqlhotcopy will complain if we try:
    if [ "$DB" == "information_schema" ]; then
        continue
    fi

    # Text dump (schema, data):
    echo "`date '+%Y-%m-%d_%H-%M-%S'`- Starting text dump of $DB... " >> $LOG
    /usr/bin/mysqldump --socket=$SOCKET --user=$USER $PASS_STRING --force --complete-insert --routines $DB > $LOCAL_BACKUP_DIR/dumps/$DB-dump.sql &&
    echo "`date '+%Y-%m-%d_%H-%M-%S'`- Done!" >> $LOG

    # Binary dump:
    echo "`date '+%Y-%m-%d_%H-%M-%S'`- Starting binary dump of $DB... " >> $LOG
    # mysqlhotcopy will complain about using locks with log tables if these
    # aren't ignored:
    if [ "$DB" == "mysql" ]; then
        DB="mysql./~.+_log$/"
    fi
    /usr/bin/mysqlhotcopy --quiet --user=$USER --socket=$SOCKET $PASS_STRING $DB $LOCAL_BACKUP_DIR/hotcopies >> $LOG 2>&1 &&
    echo "`date '+%Y-%m-%d_%H-%M-%S'`- Done!" >> $LOG
done

echo "`date '+%Y-%m-%d_%H-%M-%S'`- Dumps complete." >> $LOG

# ============== [ rsync ] ==============
echo "`date '+%Y-%m-%d_%H-%M-%S'`- rsyncing dumps to $RSYNC_SERV..." >> $LOG
/usr/bin/rsync --archive --recursive --compress -e ssh $LOCAL_BACKUP_DIR $RSYNC_USER@$RSYNC_SERV:$REMOTE_BACKUP_DIR >> $LOG 2>&1 &&
echo "`date '+%Y-%m-%d_%H-%M-%S'`- Done!" >> $LOG

# ============== [ Remove temp files ] ==============
echo "`date '+%Y-%m-%d_%H-%M-%S'`- Removing local dump files..." >> $LOG
/bin/rm -rf $LOCAL_BACKUP_DIR/dumps/* &&
/bin/rm -rf $LOCAL_BACKUP_DIR/hotcopies/* &&
echo "`date '+%Y-%m-%d_%H-%M-%S'`- Done!" >> $LOG

#------------------------------------------------------------------------------
echo "`date '+%Y-%m-%d_%H-%M-%S'`- Backup operations complete." >> $LOG
exit

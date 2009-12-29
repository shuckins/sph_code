#!/bin/bash
#===============================================================================
#          FILE:  mysql-backup.sh
# 
#         USAGE:  ./mysql-backup.sh 
# 
#   DESCRIPTION:  MySQL backup script. Provides instructions for prerequisite
#   setup as well as optional commented approaches for varying circumstances. 
#   Assumes dumps will be rsynced to a remote server. 
#
#   Two types of backups are taken:
#       * Text, SQL dumps: Uses mysqldump. Human-readable format, easy to read.
#       * Binary, hotcopies: Uses mysqlhotcopy. Faster to backup, faster
#         to restore and more reliable for live DBs.
# 
#        AUTHOR:  Samuel Huckins, wormwood_3@yahoo.com
#       CREATED:  12/28/2009 08:07:16 PM EST
#===============================================================================

# ============== [ Config ] ==============


# ============== [ Setup ] ==============


# ============== [ Dumps ] ==============
# Text: Dump all databases (table structure, data, functions):
echo "`date '+%Y-%m-%d_%H-%M-%S'`- Starting structure and data dump... "
/usr/bin/mysqldump --socket=/var/lib/mysql/mysql.sock --user=$USER --password=$PASS --force --complete-insert --routines --all-databases > $BACKUP_DIR/dumps/mysqldump.sql &&
echo "`date '+%Y-%m-%d_%H-%M-%S'`- Done!"
# Binary: Dump the data files:
echo "`date '+%Y-%m-%d_%H-%M-%S'`- Starting hotcopy... "
mysqlhotcopy --quiet --user=$USER --socket=/var/lib/mysql/mysql.sock --password=$PASS --regexp='' $BACKUP_DIR/hotcopy
echo "`date '+%Y-%m-%d_%H-%M-%S'`- Done!"

# ============== [ rsync ] ==============

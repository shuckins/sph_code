#!/bin/bash
#===============================================================================
#          FILE:  backup-slice.sh
# 
#         USAGE:  ./backup-slice.sh 
# 
#   DESCRIPTION:  Pulls down backups of important directories on my SliceHost
#                 server.
# 
#        AUTHOR:  Samuel Huckins, wormwood_3@yahoo.com
#       CREATED:  01/03/2010 10:29:55 AM EST
#===============================================================================

# ============== [ Config ] ==============
# Remote server settings
r_server="174.143.211.116"
r_user="root"
ssh_comm="ssh $r_user@$r_server"
#r_dirs="/etc /var/lib/mysql /var/www"
r_dirs="/etc"

# Local server settings
# N.B.: If this directory exists when this is first run rdiff-backup will complain
# and not run. If it doesn't exist, rdiff-backup will create it.
local_dir="/home/shuckins/Backups/samuelhuckins.com_server/regular-backups"

# Log related
NOW="date +%Y-%m-%d_%H-%M-%S"
LOG="/tmp/backup-slice.log"
# Use this for each log entry:
# echo "`$NOW` - MSG." >> $LOG

RB="/usr/bin/rdiff-backup"

# ============== [ Sanity checks ] ==============
# Make sure local dir exists
# if [ ! -w $local_dir ]; then
    # echo "`$NOW` - $local_dir on localhost isn't writable." >> $LOG; 
    # exit
# fi
# echo "`$NOW` - Confirmed local backup dir is writable." >> $LOG


# ============== [ Backup ] ==============
echo "`$NOW` - ----- MARK -----" >> $LOG
# Pull backup
for DIR in $r_dirs; do
    echo "`$NOW` - Backing up $DIR..." >> $LOG
    $RB --print-statistics --include-symbolic-links --exclude-special-files $r_user@$r_server::$DIR $local_dir >> $LOG 2>&1 &&
    echo "`$NOW` - Done." >> $LOG
done

echo "`$NOW` - Backups complete." >> $LOG

# Verify
echo "`$NOW` - Verifying..." >> $LOG
local_dirs=`ls $local_dir`
for DIR in $local_dirs; do
    $RB --verify $local_dir/$DIR >> $LOG 2>&1
done
echo "`$NOW` - Verification complete." >> $LOG

# DONE
echo "`$NOW` - All operations complete." >> $LOG
exit

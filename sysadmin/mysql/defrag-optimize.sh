#!/bin/bash
#===============================================================================
#          FILE:  defrag-optimize.sh
# 
#         USAGE:  ./defrag-optimize.sh 
# 
#   DESCRIPTION:  
# 
#       OPTIONS:  ---
#          BUGS:  ---
#        AUTHOR:  Samuel Huckins, wormwood_3@yahoo.com
#       CREATED:  03/11/2010 10:48:26 PM EST
#===============================================================================

#TODO Add prompt for creds. Show fragmented tables and total fragmentation. Provide
# prompt to continue or quit. Then defrag. Show results after.

# Get a list of all fragmented tables
# FRAGMENTED_TABLES="$( mysql -e 'use information_schema; SELECT TABLE_SCHEMA,TABLE_NAME \
# FROM TABLES WHERE TABLE_SCHEMA NOT IN ("information_schema","mysql") AND \
# Data_free > 0' | grep -v "^+" | sed "s,\t,.," )"
 # 
# for fragment in $FRAGMENTED_TABLES; do
  # database="$( echo $fragment | cut -d. -f1 )"
  # table="$( echo $fragment | cut -d. -f2 )"
  # [ $fragment != "TABLE_SCHEMA.TABLE_NAME" ] && mysql -e "USE $database;\
  # OPTIMIZE TABLE $table;" > /dev/null 2>&1
# done
# 

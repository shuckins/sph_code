#
#===============================================================================
#          FILE:  defrag-optimize.sh
# 
#         USAGE:  ./defrag-optimize.sh 
# 
#   DESCRIPTION:  Script to check for MySQL table fragmentation and repair it.
#   First presents fragmented tables, then prompts before optimization begins.
#   NOTE: Optimization locks affected tables and can take a while!
# 
#        AUTHOR:  Samuel Huckins, wormwood_3@yahoo.com
#       CREATED:  03/11/2010 10:48:26 PM EST
#===============================================================================

read -p "MySQL username: " MYSQL_USER
stty -echo
read -p "MySQL username: " -e MYSQL_PASS; echo
stty echo

if [ "$MYSQL_PASS" ]; then
    $MYSQL_PASS = "-p$MYSQL_PASS"
fi

echo -e "\nGathering table information...\n"

# Get a list of all fragmented tables; ignores special system DBs
FRAGMENTED_TABLES="$( mysql -u $MYSQL_USER $MYSQL_PASS -e ' 
    use information_schema; 
    SELECT TABLE_SCHEMA,TABLE_NAME 
        FROM TABLES 
        WHERE TABLE_SCHEMA NOT IN ("information_schema","mysql") 
            AND Data_free > 0' | grep -v "^+" | sed "s,\t,.," )"

echo $FRAGMENTED_TABLES

if [ -n $FRAGMENTED_TABLES ]; then
    echo -e "Fragmented tables found: \n"
else 
    echo -e "\nNo fragmented tables!\n"
    exit
fi

# Show fragmented tables and total fragmentation. 
mysql -u $MYSQL_USER $MYSQL_PASS -e ' 
    use information_schema; 
    SELECT TABLE_SCHEMA,TABLE_NAME 
        FROM TABLES 
        WHERE TABLE_SCHEMA NOT IN ("information_schema","mysql") 
            AND Data_free > 0'

# Provide prompt to continue or quit. Then defrag. 

# for fragment in $FRAGMENTED_TABLES; do
  # database="$( echo $fragment | cut -d. -f1 )"
  # table="$( echo $fragment | cut -d. -f2 )"
  # [ $fragment != "TABLE_SCHEMA.TABLE_NAME" ] && mysql -e "USE $database;\
  # OPTIMIZE TABLE $table;" > /dev/null 2>&1
# done

# Show results after. 

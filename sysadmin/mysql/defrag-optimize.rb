#!/usr/bin/env ruby
# 
#   DESCRIPTION:  Script to check for MySQL table fragmentation and repair it.
#   First presents fragmented tables, then prompts before optimization begins.
#   NOTE: Optimization locks affected tables and can take a while!
# 
#        AUTHOR:  Samuel Huckins, wormwood_3@yahoo.com
#       CREATED:  03/11/2010 10:48:26 PM EST
#===============================================================================

print "MySQL username: " 
mysql_user = gets.chomp!
print "MySQL password: " 
mysql_pass = gets.chomp!

unless mysql_pass == ""
  mysql_pass = "-p#{mysql_pass}"
end

puts "\nGathering table information...\n\n"

# Get a list of all fragmented tables; ignores special system DBs
mysql_query = "SELECT TABLE_SCHEMA, TABLE_NAME 
        FROM information_schema.TABLES 
        WHERE TABLE_SCHEMA NOT IN ('information_schema','mysql') 
        AND Data_free > 0;"

fragmented_tables = %x{mysql -u #{mysql_user} #{mysql_pass} -e "#{mysql_query}" | grep -v '^+' | sed 's,\t,.,'}

if fragmented_tables
    puts "Fragmented tables found (Database.Table): \n"
    fragmented_tables = fragmented_tables.split
    fragmented_tables.delete(fragmented_tables[0])
else 
    puts "\nNo fragmented tables!\n"
    exit
end

# Show fragmented tables and total fragmentation. 

fragmented_tables.each {|dbtb| puts dbtb}

def defrag(fragmented_tables)
  for ft in fragmented_tables do
    db = ft.split(".")[0]
    tab = ft.split(".")[1]
    # mysql -e "USE $database;\
    # OPTIMIZE TABLE $table;" > /dev/null 2>&1
  end
end

# Provide prompt to continue or quit. Then defrag. 
print "\nDo you want to proceed with optimization for fragmented tables? "
if gets.chomp! == "y"
  defrag fragmented_tables
else
  puts "Ok then, exiting."
end

# TODO Show results

exit

#!/usr/bin/env ruby
# 
#   DESCRIPTION:  Script to check for MySQL table fragmentation and repair it.
#   First presents fragmented tables, then prompts before optimization begins.
#   NOTE: Optimization locks affected tables and can take a while on large 
#   datasets!
# 
#        AUTHOR:  Samuel Huckins, wormwood_3@yahoo.com
#       CREATED:  03/11/2010 10:48:26 PM EST
#===============================================================================

class Maintenance

  @mysql_user = "root"
  @mysql_pass = ""

  @fragmented_tables = []
  
  def setup
    print "MySQL username: " 
    @mysql_user = gets.chomp!
    print "MySQL password: " 
    @mysql_pass = gets.chomp!

    unless @mysql_pass == ""
      @mysql_pass = "-p#{@mysql_pass}"
    end

  end


  def scan
    # Get a list of all fragmented tables; ignores special system DBs
    mysql_query = "SELECT TABLE_SCHEMA, TABLE_NAME 
            FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA NOT IN ('information_schema','mysql') 
            AND Data_free > 0;"

    fragmented_tables = %x{mysql -u #{@mysql_user} #{@mysql_pass} -e "#{mysql_query}" | grep -v '^+' | sed 's,\t,.,'}
    if fragmented_tables
        @fragmented_tables = fragmented_tables.split
        @fragmented_tables.delete(@fragmented_tables[0])
    end

    return @fragmented_tables

  end


  def defrag
    @fragmented_tables.each do |ft|
      db = ft.split(".")[0]
      tab = ft.split(".")[1]
      # mysql -e "USE $database;\
      # OPTIMIZE TABLE $table;" > /dev/null 2>&1
    end
  end

end

#------------------------------------------------------------------------------

# main 
m = Maintenance.new
m.setup
puts "\nGathering table information...\n\n"
fragmented_tables = m.scan

if fragmented_tables
    puts "Fragmented tables found (Database.Table): \n"
    fragmented_tables.each {|dbtb| puts dbtb}
else 
    puts "\nNo fragmented tables!\n"
    exit
end

print "\nDo you want to proceed with optimization for fragmented tables (y/n)? "
if gets.chomp! == "y"
  m.defrag
else
  puts "Ok then, exiting."
  exit
end

# Show fragmented tables and total fragmentation. 

puts "All done. Exiting"

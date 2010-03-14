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

  def initialize
    @mysql_user = "root"
    @mysql_pass = ""
    @fragmented_tables = []
  end
  
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

    # Fragmented tables:
    ft = %x{mysql -u #{@mysql_user} #{@mysql_pass} -e "#{mysql_query}" | grep -v '^+' | sed 's,\t,.,'}
    if ft
        ft = ft.split
        ft.delete(ft[0])
        # Associate pairs of DB and table names
        ft.map { |dbtb| @fragmented_tables << [dbtb.split(".")[0], dbtb.split(".")[1]] }
    end

    return @fragmented_tables

  end


  def defrag
    @fragmented_tables.each do |ft|
      db = ft[0]
      tab = ft[1]
      puts "Optimizing #{tab} in #{db}..."
      query = "OPTIMIZE TABLE #{tab};" 
      cmd = %x{mysql -u #{@mysql_user} #{@mysql_pass} -D #{db} -e "#{query}"}
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
    puts "Fragmented tables found (Database | Table): \n"
    fragmented_tables.each {|db, tb| puts "#{db} | #{tb}"}
    # TODO Show total fragmentation, per table?
else 
    puts "\nNo fragmented tables!\n"
    exit
end

print "\nDo you want to proceed with optimization for fragmented tables (y/n)? "
if gets.chomp! == "y"
  puts
  m.defrag
else
  puts "Ok then, exiting."
  exit
end

# TODO Confirm tables are defragmented

puts "\n\nAll done. Exiting."

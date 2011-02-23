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
    @defragment_manually = []
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
    mysql_query = "SELECT TABLE_SCHEMA, TABLE_NAME, ENGINE
            FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA NOT IN ('information_schema','mysql') 
            AND Data_free > 0;"

    # Fragmented tables:
    ft = %x{mysql -u #{@mysql_user} #{@mysql_pass} -e "#{mysql_query}" | grep -v '^+' | sed 's,\t,.,g'}
    if ft
        ft = ft.split
        ft.delete(ft[0])
        # Associate pairs of DB and table names; store incompatible table types separately
        ft.map { |dbtb|    if ["MyISAM", "ARCHIVE", "InnoDB"].include? dbtb.split(".")[2]
                             @fragmented_tables << [dbtb.split(".")[0], dbtb.split(".")[1], dbtb.split(".")[2]]
                           else
                             @defragment_manually << [dbtb.split(".")[0], dbtb.split(".")[1], dbtb.split(".")[2]]
                           end
               }
    end

    if @defragment_manually.length > 0
      puts "The following tables cannot be automatically defragmented (DB | TABLE | ENGINE):"
      @defragment_manually.each {|db, tab, eng| puts "#{db} | #{tab} | #{eng}"}
    end

    return @fragmented_tables

  end


  def defrag
    @fragmented_tables.each do |ft|
      db = ft[0]
      tab = ft[1]
      eng = ft[2]
      puts "Optimizing #{tab} in #{db}..."

      if eng == "InnoDB"
        query = "ALTER TABLE #{tab} ENGINE=INNODB;"
      else
        query = "OPTIMIZE TABLE #{tab};" 
      end

      query = query + " FLUSH TABLE #{tab};"

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

if fragmented_tables.length > 0
    puts "\nFragmented tables found (Database | Table): \n"
    fragmented_tables.each {|db, tb| puts "#{db} | #{tb}"}
    # TODO Show total fragmentation, per table?
else 
    puts "\nNo fragmented tables found that can be automatically defragmented.\n"
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

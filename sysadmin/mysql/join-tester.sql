select "COMMA" as "Using version";

# Comma join version
explain extended 
select * from world.City ci, world.Country co
where co.code = ci.countrycode
and GNP < 1000000.0;

select "";
show warnings;

#------------------------------------------------------------------------------
select "----------------------------------" as "";

select "JOIN" as "Using version";

# JOIN syntax version
explain extended
select * from world.City ci
join world.Country co on (co.code = ci.countrycode)
where GNP < 1000000.0;

select "";
show warnings;

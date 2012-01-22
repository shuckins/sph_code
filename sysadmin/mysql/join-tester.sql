select "Using version: COMMA" as "";

# Comma join version
explain extended 
select * from world.City ci, world.Country co
where co.code = ci.countrycode
and GNP < 1000000.0;

select "Warnings: " as "";
show warnings;

#------------------------------------------------------------------------------
select "----------------------------------" as "";

select "Using version: JOIN" as "";

# JOIN syntax version
explain extended
select * from world.City ci
join world.Country co on (co.code = ci.countrycode)
where GNP < 1000000.0;

select "Warnings: " as "";
show warnings;

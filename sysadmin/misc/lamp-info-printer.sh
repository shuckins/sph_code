#!/bin/bash
###################################
#
# Written by Samuel Huckins
#
# July 2007
#
# Prints out version info for 
# things in the LAMP stack.
#
###################################
#
echo -e "\e[1;34mThis machine's LAMP stack:\e[0m"
echo ""
# Linux:
LINUX=`cat /etc/issue`
echo -e -n " * \e[31mL\e[1;33minux: \e[0m"
echo "$LINUX"
# Apache:
echo -e -n " * \e[31mA\e[1;33mpache: \e[0m"
if [ -e /usr/sbin/httpd ]
then
    echo "`/usr/sbin/httpd -v| head -n 1 | awk '{print $3}'`"
elif [ -e /usr/sbin/apache2 ]
then
    echo "`/usr/sbin/apache2 -v| head -n 1 | awk '{print $3}'`"
else
    echo -e "\e[37mNot present\e[0m"
fi
# MySQL:
echo -e -n " * \e[31mM\e[1;33mySQL: \e[0m"
if [ -e /usr/bin/mysql ]
then
    echo "`/usr/bin/mysql --version | awk '/Ver/ {print $2, $3, $4, $5}' | sed 's/,//'`"
else
    echo -e "\e[37mNot present\e[0m"
fi
# PHP:
echo -e -n " * \e[31mP\e[1;33mHP: \e[0m"
if [ -e /usr/bin/php ]
then 
    echo "`php -v`"
else
    echo -e "\e[37mNot present\e[0m"
fi
# Perl:
echo -e -n " * \e[31mP\e[1;33merl: \e[0m"
if [ -e /usr/bin/perl ]
then 
    echo "`perl -v | awk '/This is perl/ {print $4}' | sed 's/v//'`"
else
    echo -e "\e[37mNot present\e[0m"
fi
# Python:
echo -e -n " * \e[31mP\e[1;33mython: \e[0m"
if [ -e /usr/bin/python ]
then 
    echo "`/usr/bin/env python -V 2>&1 | awk '/Python/ {print $2}'`"
else
    echo -e "\e[37mNot present\e[0m"
fi

# PostgreSQL
echo -e -n " * \e[31mP\e[1;33mostgreSQL: \e[0m"
if [ -e /usr/bin/psql ]
then 
    echo "`psql --version | head -n 1 | cut -d" " -f 3`"
else
    echo -e "\e[37mNot present\e[0m"
fi

# Ruby:
echo -e -n " * \e[31mR\e[1;33muby: \e[0m"
if [ -e /usr/bin/ruby ]
then 
    echo "`ruby --version | cut -f 2 -d' '`"
else
    echo -e "\e[37mNot present\e[0m"
fi
# done
echo ""

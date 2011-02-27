#!/bin/bash
# A command to provide lots of 
# info about a file at glance!
FILE=`file $1`
echo "$FILE has `wc -l $1 | cut -d" " -f1` lines." &&
echo -e "\e[1;34mOwned by: \e[0m`ls -l $1 | cut -d" " -f3` | \e[1;34mGroup: \e[0m`ls -l $1 | cut -d" " -f4`" &&
echo -e "\e[1;34mSize: \e[0m`ls -lh $1 | cut -d" " -f5` | \e[1;34mLast updated: \e[0m`ls -lh $1 | cut -d" " -f6`" &&
echo "**********************************"
echo -e "\e[1;34mTop bits: \n \e[0m" &&
head -n 5 $1 | nl -b a &&
echo "" &&
echo -e "\e[1;34mBottom bits: \n \e[0m" &&
nl -b a $1 | tail -n 5
exit 0

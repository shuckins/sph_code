#!/bin/bash
###################################
# Created on July 2, 2007 by Samuel Huckins
# Adopted from the basic script floating 
# around the internet.
#
# Generates random password. Of length equal to number given after
# command, otherwise 10.
#
# Uses /dev/urandom and not /dev/random since the latter
# can block without enough hardware entropy.
###################################
#
# Checks to see if user entered something after invocation. 
# If so, use that to generate right amount of random bytes,
# and display that number.
# Only works up to 25 characters, not sure why yet.
if [ -n "$1" ] ; then
	let "RANDOMTOGRAB=$1+20"
	echo `head -c $RANDOMTOGRAB /dev/urandom |uuencode -m - |tail -n 2 |head -c $1`
# If they entered nothing, give them a 10 character random string.
elif [ -z "$1" ] ; then
	echo `head -c 20 /dev/urandom |uuencode -m - |tail -n 2|head -c 10`
exit 0
fi

#!/bin/bash
#===============================================================================
#          FILE:  setup_for_backup.sh
# 
#         USAGE:  ./setup_for_backup.sh 
# 
#   DESCRIPTION:  This script prepares a server we want to add to our backup 
#                 process. 
#                 NOTE: This may not be needed anymore since the packages below
#                 are in most repos.
#
#        AUTHOR:  Samuel Huckins, wormwood_3@yahoo.com
#       CREATED:  01/03/2010 12:09:53 PM EST
#===============================================================================

# ============== [ OS checks ] ==============
DEB_OS=`egrep -i 'Ubuntu|Debian' /etc/issue`
RH_OS=`egrep -i 'CentOS|Red Hat' /etc/issue`
if [[ ${#DEB_OS} -gt 0 ]] ; then
    CUR_OS="debian"
    echo "Looks like we're on a $CUR_OS-type system."
elif [[ ${#RH_OS} -gt 0 ]] ; then
    CUR_OS="redhat"
    echo "Looks like we're on a $CUR_OS-type system."
else
    CUR_OS="unknown"
    echo "OS type unknown. Exiting."
    exit
fi


# ============== [ Pre-requisites ] ==============
echo "Installing pre-requisites..."
if [ "$CUR_OS" == "redhat" ]; then
    sudo yum install python-devel &&
    sudo yum install gcc gcc-c++ &&
else;
    sudo apt-get install python-devel &&
    sudo apt-get install gcc gcc-c++ &&
fi

echo "Pre-requisites complete."


# ============== [ librsync ] ==============
echo " * Setting up librsync..."
# For emergencies
# cd /tmp &&
# curl -s -L -o librsync-0.9.7.tar.gz http://downloads.sourceforge.net/librsync/librsync-0.9.7.tar.gz?modtime=1097439809
# cd /usr/local/src &&
# sudo tar -xzf /tmp/librsync-0.9.7.tar.gz &&
# cd librsync-0.9.7/ 
# sudo ./configure &&
# On 64 bit RHEL systems, you might need to run "sudo make AM_CFLAGS=-fPIC". 
# See http://wiki.rdiff-backup.org/wiki/index.php/Installations
# sudo make &&
# sudo make install &&
# sudo /sbin/ldconfig &&

if [ "$CUR_OS" == "redhat" ]; then
    sudo yum install librsync &&
else;
    sudo apt-get install librsync &&
fi

echo " * librsync setup." 


# ============== [ rdiff-backup ] ==============
echo " * Setting up rdiff-backup..."
# For emergencies
# echo &&
# cd /tmp &&
# curl -s -L -o rdiff-backup-1.2.8.tar.gz http://savannah.nongnu.org/download/rdiff-backup/rdiff-backup-1.2.8.tar.gz
# tar -zvxf rdiff-backup-1.2.8.tar.gz &&
# cd rdiff-backup-1.2.8 &&
# sudo python setup.py --librsync-dir=/usr/local/lib build &&
# sudo python setup.py install &&
# rdiff-backup --version &&
if [ "$CUR_OS" == "redhat" ]; then
    sudo yum install rdiff-backup &&
else;
    sudo apt-get install rdiff-backup &&
fi

echo "rdiff-backup setup." 

#!/bin/bash
#===============================================================================
#          FILE:  update-ubuntu.sh
# 
#         USAGE:  ./update-ubuntu.sh 
# 
#   DESCRIPTION:  For Ubuntu boxes. Updates package lists, performs safe 
#                 upgrade, cleans out cached packages.
# 
#        AUTHOR:  Samuel Huckins, wormwood_3@yahoo.com
#       CREATED:  12/31/2009 09:56:57 AM EST
#===============================================================================
# Downloads latest package lists
echo "Starting package list update..."
sudo /usr/bin/aptitude update && 
echo "Complete."
# Downloads and installs all upgraded packages
echo "Starting safe-upgrade..."
sudo /usr/bin/aptitude safe-upgrade && 
echo "Complete."
# Clears out download temp packages from /var/cache/apt
echo "Clearing out cached packages..."
sudo /usr/bin/aptitude autoclean &&

echo "All update steps complete."

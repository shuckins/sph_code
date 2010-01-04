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
echo -e "\n --- Starting package list update..."
sudo /usr/bin/aptitude update && 
echo "Complete."
# Downloads and installs all upgraded packages
echo -e "\n --- Starting safe-upgrade..."
sudo /usr/bin/aptitude safe-upgrade && 
echo "Complete."
# Clears out download temp packages from /var/cache/apt
echo -e "\n --- Clearing out cached packages..."
sudo /usr/bin/aptitude autoclean &&

# To update to the next distro version:
# sudo apt-get install update-manager-core
# sudo do-release-upgrade
#
# For more info see: http://www.ubuntu.com/getubuntu/upgrading

echo -e "\n\nAll update steps complete."

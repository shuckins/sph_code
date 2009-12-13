#!/bin/bash
#===============================================================================
#          FILE:  set-up-rails.sh
# 
#         USAGE:  ./set-up-rails.sh 
# 
#   DESCRIPTION:  Attempts to setup Ruby on Rails and deps on Ubuntu.
# 
#        AUTHOR:  Samuel Huckins, wormwood_3@yahoo.com
#       CREATED:  12/13/2009 12:15:40 PM EST
#===============================================================================
echo -ne "\nThis script will attempt to set up Rails and necessary deps on an Ubuntu system. Continue? (y/n) "
read -e CONT
if [ "$CONT" == "y" ]; then
    echo -e "\nAlright, here we go!"
else
    echo "Exiting."
    exit
fi

# OS check
# Make sure we have egrep
EGREP_VER=`egrep --version | head -n 1`
if [[ "${EGREP_VER:0:8}" != "GNU grep" ]] ; then
    echo "egrep isn't installed, sorry."
    exit
fi
# Make sure we have /etc/issue
if [[ ! -r '/etc/issue' ]] ; then
    echo "/etc/issue isn't readable."
    exit
fi
# Run checks
DEB_OS=`egrep -i 'Ubuntu|Debian' /etc/issue`
RH_OS=`egrep -i 'CentOS|Red Hat' /etc/issue`
if [[ ${#DEB_OS} -gt 0 ]] ; then
    echo -e "\n---- Suitable OS confirmed."
elif [[ ${#RH_OS} -gt 0 ]] ; then
    CUR_OS="redhat"
    echo "Not able to install on this OS."
    exit
else
    CUR_OS="unknown"
    echo "Not able to install on this OS."
    exit
fi


# Ruby and friends
echo -e "\n---- Installing Ruby and friends...\n"
sudo apt-get install ruby rdoc irb build-essential &&
echo "Installed ruby (`ruby --version`), rdoc (`rdoc --version`), irb (`irb --version`), build-essential."

# Rubygems
echo -e "\n---- Installing rubygems...\n"
cd /tmp
# Check here to see if this is the latest:
# http://rubyforge.org/frs/?group_id=126
wget http://rubyforge.org/frs/download.php/60718/rubygems-1.3.5.tgz &&
tar xzvf rubygems-1.3.5.tgz &&
cd rubygems-1.3.5/
sudo ruby setup.rb
# Without this 'gem' will either not work or will be something else:
sudo ln -s /usr/bin/gem1.8 /usr/bin/gem
echo -e "\n ---- Installed gem `gem --version`.\n"

# Rails
echo -e "\n---- Installing rails...\n"
sudo gem install rails &&
echo -e "\n---- Installed rails `rails --version`.\n"

# To get sqlite setup (default Rails DB backend):
echo -e "---- Installing sqlite...\n"
sudo apt-get install sqlite3 &&
sudo apt-get install libsqlite3-dev &&
sudo gem install sqlite3-ruby
echo -e "\n---- Installed sqlite.\n"
#------------------------------------------------------------------------------

echo "Setup complete! You should now be able to use 'rails APPNAME'."
exit

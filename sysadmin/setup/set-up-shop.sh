#!/bin/bash
#-----------------------------------------------------------------------------
# Name:        set-up-shop
# Purpose:     This script checks prereqs, downloads my SVN code and config, 
#              installs things, creates symlinks. It assumes you can login to 
#              the SVN server by key, so run this on the box in question after 
#              key is established.
#
# Author:      Samuel Huckins
# Started:     2008-09-25
# Copyright:   (c) 2008 Samuel Huckins
#-----------------------------------------------------------------------------
# Where SVN command is:
SVNLOC="/usr/bin/svn"
# Where the SVN server is:
SVNSERVER="svn+ssh://samuelhuckins.com/var/lib/svn"
# Code checkout command:
SVNCODECHECKOUT="$SVNLOC co $SVNSERVER/code code_homerepo"
# Config checkout command:
SVNCONFIGCHECKOUT="$SVNLOC co $SVNSERVER/configuration conf_homerepo"
# Check for user
read -p "What user should we use? " FINDOUTMORE
USER=$FINDOUTMORE
# Intended key location
KEYFILE="/home/$USER/.ssh/id_rsa"
# OSes we want to run this on
declare -a TRUSTEDOSES[0]="*Ubuntu*" TRUSTEDOSES[1]="*Red Hat*" TRUSTEDOSES[2]="*CentOS*" TRUSTEDOSES[3]="*Debian*"
# What to check for internet connectivity
INTERNETCHECK="ping -c 1 www.google.com"
#-----------------------------------------------------------------------------
echo ""
echo "~~~ Time to configure this server for your use! ~~~"
sleep 1
# Check OS. I can only vouch for using these
# scripts and config on RHEL, CentOS, Debian,
# and Ubuntu.
echo " * Checking OS..."
CURRENTOS=`cat /etc/issue`
for os in $TRUSTEDOSES
do
    if `echo ${CURRENTOS} | grep "${OS}" 1>/dev/null 2>&1` ; then
        echo "You are on a valid OS ($CURRENTOS). Good!"
    else
        echo "I don't trust running this on '$CURRENTOS'. Exiting."
        exit 0
    fi
done
# Check that this isn't being run as root
echo " * Checking user..."
if [ `id -u` = 0 ] ; then
    echo "Don't run this as root. Run it as a normal user."
    exit 0
else
    echo "Non-root user confirmed."
fi
# Check for a key
echo " * Checking for key..."
if [[ ! -f $KEYFILE ]] ; then
    echo "Doesn't look you have a key in place. Exiting."
    exit 0
else
    echo "Keyfile ($KEYFILE) confirmed!"
fi
# Check for internet access
echo " * Checking for internet access..."
if [ "`$INTERNETCHECK | grep 'bytes from'`" ] ; then
    echo "Internet connection seems to be up. Good."
else
    echo "No internet available. Check the tubes."
    exit 0
fi
# Check for subversion. Every few times, this will throw a
# "svn: Write error: Broken pipe". It's an SVN issue, doesn't
# hurt anything as far as I can tell.
echo " * Checking for subversion..."
if [ ! -x "$SVNLOC" ] ; then
    echo "Looks like you don't have svn installed, or it's not in $SVNLOC. Exiting."
    exit 0
else
    echo "`$SVNLOC --version | head -n 1` installed!"
fi
#
echo ""
echo "~~~ Prerequisites confirmed! ~~~"
sleep 1
# Now for the real work
# Checkout SVN code
echo " * Checking out SVN (code)..."
mkdir /home/$USER/code
cd /home/$USER/code
$SVNCODECHECKOUT &&
echo "Code checkout complete."
# Checkout SVN config
echo " * Checking out SVN (config)..."
cd /home/$USER
$SVNCONFIGCHECKOUT &&
echo "Config checkout complete."
# Create symlinks
echo " * Creating symlinks..."
echo "Replacing .vimrc..."
rm -f /home/$USER/.vimrc
ln -s /home/$USER/conf_homerepo/g_vim/.vimrc
echo "Replacing .gvimrc..."
rm -f /home/$USER/.gvimrc
ln -s /home/$USER/conf_homerepo/g_vim/.gvimrc
echo "Adding .vim folder..."
ln -s /home/$USER/conf_homerepo/g_vim/.vim
echo "Replacing .irbrc..."
rm -f /home/$USER/.irbrc
ln -s /home/$USER/conf_homerepo/ruby/.irbrc
echo "Replacing .toprc..."
rm -f /home/$USER/.toprc
ln -s /home/$USER/conf_homerepo/top/.toprc
echo "Replacing .bashrc..."
rm -f /home/$USER/.bashrc
ln -s /home/$USER/conf_homerepo/bash/.bashrc
echo "Linking SVN updater script..."
ln -s /home/$USER/conf_homerepo/misc/update-home-svn.sh
echo "Linking Python startup config..."
ln -s /home/$USER/conf_homerepo/python/.pythonstartup
echo "Linking MySQL client conf..."
ln -s /home/$USER/conf_homerepo/mysql/client-my.cnf .my.cnf
echo "Linking toggle-caps-and-esc script..."
ln -s /home/$USER/conf_homerepo/misc/toggle-caps-and-esc.sh
echo "Linking SVN ignore patterns file..."
ln -s /home/$USER/conf_homerepo/misc/.svnignore
echo "Linking git and gitk config files..."
ln -s /home/$USER/conf_homerepo/git/.gitconfig
ln -s /home/$USER/conf_homerepo/git/.gitk

echo "Symlinking finished!"
echo "Done!"
sleep 1
# Install needed things
echo ""
echo "~~~ Installing needed programs ~~~"
for os in $TRUSTEDOSES
do
    if `echo ${CURRENTOS} | grep "*Debian*" \| "*Ubuntu*" 1>/dev/null 2>&1` ; then
        sudo apt-get -y -q install dmidecode ack-grep build-essential cowsay curl dmidecode dnsutils exuberant-ctags fping htop imagemagick iptraf irb iotop netcat fortune nast nethogs nmap pyflakes pylint python-dev python-setuptools rdoc ruby ruby-dev screen sharutils shtool tcpdump tidy traceroute unrar unzip vim-full vim-python whois &&
        echo "Package installation complete."
    else
        echo "Desired software package installation not complete for this OS."
    fi
done
# Can't seem to get this reloading automatically:
echo ""
echo "You'll need to reload your .bashrc file (. ~/.bashrc) to have most changes take effect."
# More info on this server
echo "To find out more about this system, type 'system' once this you reload .bashrc."
echo "If you are on a desktop, you should find and run set-up-desktop.py to get desktop related apps."
echo "Also you'll need to symlink conky's config."
# DONE
echo "All done! Enjoy."
echo ""
exit 0

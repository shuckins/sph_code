#!/bin/bash
# From: http://ariejan.net/2007/06/12/bash-your-svn-and-trac-installation/
#
# Sets up an SVN repo and a Trac installation. Configures 
# permissions and users.
#
# It takes one argument, the name of the project you want to 
# create. E.g if you wanted to create a SVN repository and trac 
# installation for “My Project” you would run the following 
# command:
# $ ./create_dev_env my_project
#
################################################################
echo "Creating Subversion and Trac installation for $1"
 
# Subversion
echo "Creating SVN Repository..."
mkdir -p /home/svn/repositories/$1
svnadmin create /home/svn/repositories/$1
sed s/EXAMPLE/$1/g /usr/share/trac/contrib/post-commit > /home/svn/repositories/$1/hooks/post-commit
chmod +x /home/svn/repositories/$1/hooks/post-commit
chown -R www-data:www-data /home/svn/repositories/$1
 
# Trac
echo "Creating Trac install..."
cd /var/svn/trac
mkdir -p /var/svn/trac/$1
 
echo "Creating files..."
trac-admin /var/svn/trac/$1 initenv $1 sqlite:db/trac.db svn \
/var/svn/trac/$1 /usr/share/trac/templates
 
echo "Removing anonymous permissions..."
trac-admin /var/svn/trac/$1 permission remove anonymous  BROWSER_VIEW
trac-admin /var/svn/trac/$1 permission remove anonymous  CHANGESET_VIEW
trac-admin /var/svn/trac/$1 permission remove anonymous  FILE_VIEW
trac-admin /var/svn/trac/$1 permission remove anonymous  LOG_VIEW
trac-admin /var/svn/trac/$1 permission remove anonymous  MILESTONE_VIEW
trac-admin /var/svn/trac/$1 permission remove anonymous  REPORT_SQL_VIEW
trac-admin /var/svn/trac/$1 permission remove anonymous  REPORT_VIEW
trac-admin /var/svn/trac/$1 permission remove anonymous  ROADMAP_VIEW
trac-admin /var/svn/trac/$1 permission remove anonymous  SEARCH_VIEW
trac-admin /var/svn/trac/$1 permission remove anonymous  TICKET_CREATE
trac-admin /var/svn/trac/$1 permission remove anonymous  TICKET_MODIFY
trac-admin /var/svn/trac/$1 permission remove anonymous  TICKET_VIEW
trac-admin /var/svn/trac/$1 permission remove anonymous  TIMELINE_VIEW
trac-admin /var/svn/trac/$1 permission remove anonymous  WIKI_CREATE
trac-admin /var/svn/trac/$1 permission remove anonymous  WIKI_MODIFY
trac-admin /var/svn/trac/$1 permission remove anonymous  WIKI_VIEW
 
echo "Creating Trac admins..."
trac-admin /var/svn/trac/$1 permission add ariejan TRAC_ADMIN
chown -R www-data:www-data /var/svn/trac/$1
echo "Done."

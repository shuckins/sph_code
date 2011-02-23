#!/usr/bin/bash
# Setting up Django on a Linux server.
#
echo "~~ PRE-REQs ~~"
echo "Installing packages..."
sudo apt-get apache2 postgresql-8.1 python-psycopg2 python-egenix-mxdatetime libapache2-mod-python subversion
#
echo "~~ DB ~~"
echo "Setting up DB..."
echo "Setting up DB user..."
echo "Setting up DB user perms..."
#
echo "~~ DJANGO ~~"
echo "Checking out latest Django..."
echo "Creating symlink..."
echo "Adding Djang admin to path..."
echo "Creating Django project folder..."
django-admin startproject $PROJNAME
echo "Creating first Django project..."
manage.py startapp $APPNAME
#
echo "~~ CONFIG ~~"
echo "Turning on debug mode..."
echo "Setting DB settings..."
echo "Adding to installed apps..."
#
echo "~~ APP ~~"
echo "Creating first app..."
#
echo "Done."
exit 0

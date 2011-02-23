#!/usr/bin/env python
"""
This script installs a number of desktop applications I like.

Only tested on Ubuntu desktop.

Author: Samuel Huckins
Started on: 2009-05-13
"""
import sys
import subprocess

# All the apps we want to install: 
apps_to_install = ['avidemux', 'conky', 'dia', 'flashplugin-nonfree', 
                   'gcolor2', 'gscrot', 'guake', 'inkscape', 
                   'launchy', 'mozilla-mplayer', 'screenlets', 
                   'synergy', 'ttf-droid', 'wireshark', 'xresprobe', 
                   'zenmap']

for app in apps_to_install:
    command = "sudo apt-get install %s --assume-yes" % app
    print "Installing %s..." % app
    subp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    (stdout, stderr) = subp.communicate()
    print stdout

print "All apps installed except for Java stuff."
print "Run 'sudo apt-get install sun-java6-jre sun-java6-plugin'."
print "Also install the following manually (not in repo): xmind, Adobe Air, twhirl, skype."
sys.exit(0)

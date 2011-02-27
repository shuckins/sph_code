#!/usr/bin/env python
"""
File: nat-geo_background-setter.py
Author: Samuel Huckins
Date: 2011-02-18 18:03:05 CST

Description: A script to pull the latest National Geographic Picture of the
Day and set it as your desktop background. Won't run if you are low on
space, easily configurable below.

NOTE: Only works on Linux! (Written on Ubuntu)
"""

import os
import re
import sys
import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
from BeautifulSoup import BeautifulSoup, Tag
from HTMLParser import HTMLParser, HTMLParseError

picture_dir = os.path.expanduser("~/Pictures/NatGeoPics")
free_space_minimum = 25
base_url = "http://photography.nationalgeographic.com/photography/photo-of-the-day"

#------------------------------------------------------------------------------

def free_space(dir):
    """
    Returns percentage of free space.
    """
    try:
        fs = os.statvfs(dir)
    except OSError:
        return False
    gb_total = float(float(fs.f_bsize * fs.f_blocks) / 1024 / 1024 / 1024)
    gb_free = float(float(fs.f_bsize * fs.f_bavail) / 1024 / 1024 / 1024)
    percen_free = (gb_total - gb_free) / gb_total * 100
    return int(round(percen_free))

def get_wallpaper_details(base_url):
    """
    Finds the URL to download the wallpaper version of the image as well as the
    title shown on the page.
    """
    try:
        html = urllib2.urlopen(base_url).read()
    # Their server isn't responding, or in time, or the page is unavailable:
    except (urllib2.URLError, urllib2.HTTPError), e:
        return False
    new_html = []
    for line in html.split("\n"):
        # Their pages write some script tags through document.write, which was
        # causing BeautifulSoup to choke
        if line.find("document.write") != -1:
            continue
        else:
            new_html.append(line)
    html = "\n".join(new_html)
    try:
        soup = BeautifulSoup(html)
    except HTMLParseError, e:
        print e
        sys.exit(0)

    # Find wallpaper image URL
    urls = []
    for i in soup.findAll("div", {"class": "download_link"}):
        for link in i.findAll("a"): 
            urls.append(link['href'])
    # No download link
    if not urls:
        return False
    url = urls[0]

    # Get main title
    for i in soup.findAll("h1"):
        title = re.sub('[\W]+', '-', i.contents[0]).lower()

    return [url, title]

def download_wallpaper(url, picture_dir, filename):
    """
    Downloads URL passed, saves in specified location, cleans filename.
    """
    filename = filename + "." + url.split(".")[-1]
    image = urllib2.urlopen(url)
    outpath = os.path.join(picture_dir, filename)
    req = Request(url)
    try:
        f = urlopen(req)
        print "Now downloading " + url
        # Open our local file for writing
        local_file = open(outpath, "wb")
        #Write to our local file
        local_file.write(f.read())
        local_file.close()
    #handle errors
    except HTTPError, e:
        print "HTTP Error:",e.code , url
    except URLError, e:
        print "URL Error:",e.reason , url

    return outpath

def set_wallpaper(filename):
    """
    Sets the passed file as wallpaper.
    """
    os.system("gconftool-2 -t str --set /desktop/gnome/background/picture_filename " + filename)
    print "BG set!"

#------------------------------------------------------------------------------
fs = free_space(picture_dir)
if not fs:
    print "%s does not exist, please create." % picture_dir
    sys.exit(0)
if fs <= free_space_minimum:
    print "Not enough free space in %s! (%s%% free)" % (picture_dir, fs)
    sys.exit(0)

ut = get_wallpaper_details(base_url)
if not ut:
    print "No wallpaper URL found."
    sys.exit(0)
url, title = ut[0], ut[1]

# Verify pictures_dir exists
if not os.path.isdir(picture_dir):
    print "Hey! This no exist " + picture_dir
    os.mkdir(picture_dir)
    print "Created dir."

filename = download_wallpaper(url, picture_dir, title)
set_wallpaper(filename)

sys.exit(0)

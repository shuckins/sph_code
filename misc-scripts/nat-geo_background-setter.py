#!/usr/bin/env python
"""
File: nat-geo_background-setter.py
Author: Samuel Huckins
Date: 2011-02-18 18:03:05 CST

Description: A script to pull the latest National Geographic Picture of the
Day and set it as your desktop background. Won't run if you are low on
space, easily configurable below.

NOTE: Only works on Linux or Windows! (Written on Ubuntu)
"""

import os
import re
import sys
import platform
import urllib2
import ctypes
from urllib2 import Request, urlopen, URLError, HTTPError
from BeautifulSoup import BeautifulSoup, Tag
from HTMLParser import HTMLParser, HTMLParseError

picture_dir = os.path.expanduser("~/Pictures/NatGeoPics")
free_space_minimum = 25
base_url = "http://photography.nationalgeographic.com/photography/photo-of-the-day"

#------------------------------------------------------------------------------

def _get_free_bytes(folder):
	"""
	Return folder/drive free space and total space (in bytes)
	"""
	if platform.system() == 'Windows':
		free_bytes = ctypes.c_ulonglong()
		p_free_bytes = ctypes.pointer(free_bytes)
		total_bytes = ctypes.c_ulonglong()
		p_total_bytes = ctypes.pointer(total_bytes)
		GetDiskFreeSpaceEx = ctypes.windll.kernel32.GetDiskFreeSpaceExW
		res = GetDiskFreeSpaceEx(unicode(folder), None, p_total_bytes, p_free_bytes)
		if not res:
			raise WindowsError("GetDiskFreeSpace failed")
		free_bytes = free_bytes.value
		total_bytes = total_bytes.value
	else:
		stat = os.statvfs(folder)
		free_bytes = stat.f_bsize * stat.f_bfree
		total_bytes = stat.f_bsize * stat.f_blocks
	return free_bytes, total_bytes

def free_space(dir):
	"""
	Returns percentage of free space.
	"""
	try:
		free, total = _get_free_bytes(dir)
	except OSError:
		return False
	percen_free = float(free) / total * 100
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
	for i in soup.findAll("div", {"class": "download_link"}):
		urls = []
		for link in i.findAll("a"): 
			urls.append(link['href'])
	if len(urls) != 1:
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

def _set_wallpaper_linux2(filename):
	"""
	Sets the passed file as wallpaper.
	"""
	os.system("gconftool-2 -t str --set /desktop/gnome/background/picture_filename " + filename)
	print "BG set!"

def _set_wallpaper_win32(filename):
	SPI_SETDESKWALLPAPER = 0x14
	SPIF_UPDATEINIFILE = 0x1
	SPIF_SENDWININICHANGE = 0x2
	SystemParametersInfo = ctypes.windll.user32.SystemParametersInfoW
	SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, filename,
		SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)

set_wallpaper = globals()['_set_wallpaper_' + sys.platform]

#------------------------------------------------------------------------------
fs = free_space(picture_dir)
if not fs:
	print "%s does not exist, please create." % picture_dir
	sys.exit(0)
if fs <= free_space_minimum:
	print "Not enough free space in %s! (%s%% free)" % (picture_dir, fs)
	sys.exit(0)

ut = get_wallpaper_details(base_url)
url, title = ut[0], ut[1]
if not url:
	print "No wallpaper URL found."
	sys.exit(0)

# Verify pictures_dir exists
if not os.path.isdir(picture_dir):
	print "Hey! This no exist " + picture_dir
	os.mkdir(picture_dir)
	print "Created dir."

filename = download_wallpaper(url, picture_dir, title)
set_wallpaper(filename)

sys.exit(0)

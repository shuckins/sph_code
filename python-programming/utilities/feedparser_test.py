#!/usr/bin/env python

import feedparser

testurl = "http://feeds.feedburner.com/dancingpenguinsoflight?format=xml"

print "Trying to parse", testurl
f = feedparser.parse(testurl)
fitems = f.entries

for item in fitems:
    print "Title:", item.title
    print "Link:", item.link

print "Done."

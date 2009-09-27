#!/usr/bin/env python
#-----------------------------------------------------------------------------
"""
Uses the Flickr API to return the URL of the latest photo having a particular
tag.

Author: Samuel Huckins
Date started: 2009-04-20
"""
#-----------------------------------------------------------------------------
# For exiting:
import sys
# Flickr API module:
try:
    import flickrapi
except ImportError:
    print "You need to install the flickrapi module. Check PyPI."
    sys.exit(-1)
# For logging:
import logging
script_name = __file__.split("/")[-1]
# Setup logging
logger = logging.getLogger(script_name)
logger.setLevel(logging.DEBUG)
# Use file for standard logging
#logfilename = "/var/log/%s.log" % script_name
#filelog = logging.FileHandler(logfilename, 'a')
#filelog.setLevel(logging.INFO)
# Use console for debugging
conlog = logging.StreamHandler()
conlog.setLevel(logging.DEBUG)
# Setup log formatter, add to console log
formatter = logging.Formatter("%(asctime)s - \
%(name)s - %(lineno)s - %(levelname)s - %(message)s")
conlog.setFormatter(formatter)
#filelog.setFormatter(formatter)
# Add console log to logger
logger.addHandler(conlog)
#logger.addHandler(filelog)
# For parsing options passed:
from optparse import OptionParser
# For internet connection checking
from httplib import HTTP 
from urlparse import urlparse
#-----------------------------------------------------------------------------

def latest_image(tag):
    """
    Returns the latest image from Flickr matching the tag passed.
    """
    api_key = "00dee01a7d0e3914b80245023597a6a5"
    my_user_id = '25402951@N00'
    flickr = flickrapi.FlickrAPI(api_key)
    import pdb; pdb.set_trace()

#-----------------------------------------------------------------------------
def main():
    """
    Provides main flow control.
    """
    logger.debug("Starting %s." % script_name)
    # Flickr goodness:
    latest_image("colorful")
    # Done:
    logger.debug("Exiting.")
    sys.exit(0)
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()

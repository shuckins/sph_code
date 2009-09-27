#!/usr/bin/env python
"""
Tries to determine the current operating system, via several methods.

Author: Samuel Huckins
Date started: 2009-05-23
"""
import sys

def find_os(detailed=False):
    """
    Returns the current OS platform, one of:
        * Windows
        * Linux
        * ?

    Returns False if platform cannot be determined.

    If detailed is passed, will return a tuple of the platform and the
    particular OS information, such as Windows version or Linux distribution.
    """
    # Imported here to ensure inclusion. Move to the appropriate place in your
    # script if possible:
    import platform
    import sys
    import re
    # The modules we need are standard for Python 2.3 and above:
    try:
        python_version = sys.version.split(' ')[0]
        if python_version < 2.3:
            return False
    except:
        print "Can't determine Python version, unable to continue."
        return False

    # Get the general platform first:
    general_platform = platform.system()
    # Set the particular OS to False in case we can't determine it:
    os_detail = False
    # Windows:
    if general_platform == "Windows":
        os_detail = " ".join(platform.win32_ver())
    # Darwin:
    # BSDs:
    # Solaris:
    # Unix:
    # Linux:
    if general_platform == "Linux":
        os_detail = " ".join(platform.dist())

    if detailed:
        return (general_platform, os_detail)
    else:
        return general_platform

#---------------------------------------------------------------

if __name__ == '__main__':
    os_info = find_os(detailed=True)
    if os_info:
        print "Platform: %s" %  os_info[0]
        print "Operating system: %s" %  os_info[1]
        sys.exit(0)
    else:
        print "Unable to determine OS."
        sys.exit(-1)

#!/usr/bin/env python
"""Creates python file in current directory of the name passed, adds shebang
line, makes executable, opens in preferred editor.

Should work on Linux, Mac, and Windows.

Author: Samuel Huckins
Date: 2009-07
"""
import sys
import os
import subprocess
args = sys.argv

# Contents to be added to file:
content = """#!/usr/bin/env python"""

# Make sure a filename is passed, and only one:
if args:
    if len(args) > 2:
        print "Unable to process multiple names, please pass one."
        sys.exit(1)
    else:
        filename = args[-1]
else:
    print "Please pass a filename!"
    sys.exit(1)
# Add the extension if it's not present:
if filename[-3:] != ".py":
    filename += ".py"
# See if the file exists already:
if os.path.exists(filename):
    skip_exists = raw_input("%s already exists. Overwrite? (y/n) " % filename)
    skip_exists = skip_exists.lower()
    if skip_exists != "y":
        if skip_exists != "n":
            print "Didn't understand your decision, exiting."
            sys.exit(1)
        else:
            sys.exit(0)
# Create the file, pass in contents:
FILE = open(filename, "w")
FILE.write(content)
FILE.close()
# Make it executable:
full_path = os.getcwd() + "/" + filename
os.chmod(full_path, 0744)
# Open it with preferred application:
if os.name == 'mac':
    subprocess.call(["open", full_path])
elif os.name == 'nt':
    subprocess.call(["start", full_path])
else:
    subprocess.call(["xdg-open", full_path])

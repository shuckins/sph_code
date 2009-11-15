#!/usr/bin/env python
#-----------------------------------------------------------------------------
"""
Dumps the create statement for MySQL VIEW_NAME in DATABASE, performs
some text replacement to make it more readable, writes to a
file VIEW_NAME.sql in current directory.

USAGE: ./mysqldump_view.py DATABASE VIEW_NAME

Author: Samuel Huckins
Date started: 2009-11-15
"""

import commands
import os
import re
import sys

#------------------------------------------------------------------------------

def get_clean_view(db, view):
    """
    Grabs create statement for view in db passed. Performs text replacements
    to make more human-readable, returns resulting string.
    """
    default_user = "root"
    query = """SELECT VIEW_DEFINITION FROM information_schema.VIEWS where \
TABLE_NAME = "%s" and TABLE_SCHEMA = "%s" """ % (view, db)
    mysql_command = "mysql -u %s -p --skip-column-names -e '%s'" % (default_user, query)

    print("Using user %s, trying to connect..." % default_user)
    # Get create statement from DB
    output = commands.getstatusoutput(mysql_command)
    # There was some error running the command
    if output[0] != 0:
        err = output[1]
        print("Problem running command:\n%s" % err)
        sys.exit(1)
    else:
        view_syntax = output[1]
    # Text replacement patterns
    find_replace = {"`,`":      "`,\n`",
                    " from ":   "\nfrom ",
                    " join ":   "\n\tjoin ",
                    " where ":  "\nwhere ",
                    " and ":    "\n\tand ",
                    " limit ":  "\nlimit ",
                    " order ":  "\norder "}
    for (f, r) in find_replace.items():
        view_syntax = view_syntax.replace(f, r)
    return view_syntax

def write_view(view, output_file):
    out = open(output_file, "w")
    out.write(view)
    out.close()

def main():
    """
    Provides main flow control.
    """
    args = sys.argv
    if len(args) != 3:
        print("Need to pass database and viewname.")
        print(__doc__)
        sys.exit(1)
    else:
        db = args[1]
        view = args[2]

    output_file = "%s.sql" % view
    if os.path.exists(output_file):
        print("Default dump file (%s) exists!" % output_file)
        cont = raw_input("Continue anyway (y/n)? ").lower()
        if cont != "y":
            sys.exit(0)

    clean_view = get_clean_view(db, view)
    write_view(clean_view, output_file)
    print("Done. View syntax now in %s." % output_file)
    sys.exit(0)
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()

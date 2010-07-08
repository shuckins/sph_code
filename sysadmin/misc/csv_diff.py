#!/usr/bin/env python
#-----------------------------------------------------------------------------
"""
Finds differences between matching columns within two passed CSV files.
Can output the intersection, difference, symmetric difference, union, and
either complement.

It's not well-optimized for large files yet. For more information, including an
explanatory diagram, see this post: 

Author: Samuel Huckins
Date started: 2009-08-06
"""
#-----------------------------------------------------------------------------
import sys
import os
import csv
import linecache
from optparse import OptionParser
# For logging:
import logging
script_name = __file__.split("/")[-1]
# Setup logging
logger = logging.getLogger(script_name)
logger.setLevel(logging.DEBUG)
# Use console for debugging
conlog = logging.StreamHandler()
conlog.setLevel(logging.DEBUG)
# Setup log formatter, add to console log
formatter = logging.Formatter("%(asctime)s - \
%(name)s - %(lineno)s - %(levelname)s - %(message)s")
conlog.setFormatter(formatter)
# Add console log to logger
logger.addHandler(conlog)
#-----------------------------------------------------------------------------

def check_output_file(option, opt, value, parse):
    """Checks to see if output file already exists, prompts for overwrite."""
    if os.path.exists(value):
        cont = raw_input("%s exists. Overwrite (y/n)?: " % value).lower()
        if cont == "n":
            sys.exit(0)
        elif cont == "y":
            parse.values.outputfile = value
        else:
            print "Response not recognized, exiting."
            sys.exit(0)
 
def check_slice_type(option, opt, value, parse):
    """Verifies slice type is among those accepted."""
    allowed = ["diff", "symdiff", "intersection", "union", "file1comp", "file2comp"]
    if value not in allowed:
        print "%s not a valid slice type." % value
        print "Please select from the following: ", ", ".join(allowed)
        sys.exit(1)
    parse.values.slicetype = value

def check_col1(option, opt, value, parse):
    """Checks that the column for file 1 has been specified."""
    if not parse.values.col1:
        print "Must pass -c if passing -C."
        sys.exit(1)
    parse.values.col2 = value

def process_args():
    """
    Process options passed at the command line. Return arguments and
    options.
    """
    usage = __doc__
    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--output-file", dest="outputfile",
                      action="callback", callback=check_output_file,
                      type="string",
                      help="File to send results to instead of stdout.")
    parser.add_option("-c", "--column", dest="col1", type="int",
                      help="""The column to compare (starts at one). Unless -C is
specified, this column will be used for both files.""")
    parser.add_option("-C", "--column2", dest="col2", type="int",
                      action="callback", callback=check_col1,
                      help="""The column to compare (starts at one) in file two.
-c must be specified if this option is selected.""")
    parser.add_option("-s", "--slice-type", dest="slicetype", action="callback",
                      callback=check_slice_type, type="string", default="diff",
                      help="""The slice of records you want to see. Options:
"diff" for the records only existing in file1 not file2; "symdiff" for records only in file1 or file2 but not both; "intersection" for records existing in both file1 and file2; "union" for all records in file1 combined with all of file2; "file1comp" Records only in file2; "file2comp" records only in file1.""")
    return parser

def check_args(args):
    """Verifies two files are passed and that they are present and readable."""
    if len(args) != 2:
        print "Incorrect number of file arguments passed. Please specify two files."
        sys.exit(1)
    else:
        if not os.path.isfile(args[0]):
            print "%s not present or not a file." % args[0]
            sys.exit(1)
        if not os.path.isfile(args[1]):
            print "%s not present or not a file." % args[1]
            sys.exit(1)

def check_opts(opts):
    """Verifies required options are passed."""
    if not opts.col1:
        print "Must pass the column index to be used (-c)."
        sys.exit(1)

#-----------------------------------------------------------------------------

def extract_column(file, col):
    """Creates set from members of col in file."""
    try:
        csvfile = open(file)
    except IOError:
        print "Unable to read %s." % file
        sys.exit(1)
    rows = [row for row in csv.DictReader(csvfile)]
    csvfile.close()
    # We need the column header name to extract the column contents:
    headers = linecache.getline(file, 1)
    headers = headers.strip('\n')
    headers = headers.split(",")
    colhead = headers[col - 1]
    # Check for integrity
    row_len = None
    for row in rows:
        if not row_len:
            row_len = len(row.keys())
        if row_len != len(row.keys()):
            print "Not all rows in %s have equal column numbers." % file
            sys.exit(1)
    # Pull out desired column as set
    column = set([row[colhead] for row in rows])
    return column

def create_slice(column1, column2, slicetype):
    """Pulls desired slicetype using the columns passed."""
    if slicetype == "diff":
        slice = column1.difference(column2)
    if slicetype == "symdiff":
        slice = column1.symmetric_difference(column2)
    elif slicetype == "union":
        slice = column1.union(column2)
    elif slicetype == "intersection":
        slice = column1.intersection(column2)
    elif slicetype == "file1comp":
        slice = column2.difference(column1)
    elif slicetype == "file2comp":
        slice = column1.difference(column2)

    return slice

def output(slice, outputfile=None):
    """Outputs slice to stdout or to output file if specified."""
    if outputfile:
        logger.info("%s results. Writing..." % len(slice))
        output = csv.writer(open(outputfile, "w"))
        for rec in slice:
            output.writerows([rec])
        logger.info("Results written to %s" % outputfile)
    else:
        logger.info("%s results:" % len(slice))

#-----------------------------------------------------------------------------
def main():
    """
    Provides main flow control.
    """
    # Parse and check opts and args passed:
    parser = process_args()
    opts_args = parser.parse_args()
    opts = opts_args[0]
    arguments = opts_args[1]
    check_args(arguments)
    check_opts(opts)
    logger.debug("Starting %s." % script_name)

    col1 = extract_column(arguments[0], opts.col1)
    if opts.col2:
        col2 = extract_column(arguments[1], opts.col2)
    else:
        col2 = extract_column(arguments[1], opts.col1)

    slice = create_slice(col1, col2, opts.slicetype)
    if opts.outputfile:
        output(slice, opts.outputfile)
    else:
        output(slice)

    logger.debug("Exiting.")
    sys.exit(0)
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()

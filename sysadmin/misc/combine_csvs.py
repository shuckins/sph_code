#!/usr/bin/env python
#-----------------------------------------------------------------------------
"""
This can be run from the command line, passing in one or more csv files, as 
well as a location for an output file. The input files are checked and 
combined into a single output csv file, whose specified location is checked
before the run.

This script can detect differences in delimiters between the files, and will
throw an error in these cases.

As a module, this provides a function to combine csv files passed into a 
single file. When using it thusly, be sure to add the checks performed in the
optparse callbacks and generally in the run finction, as these are assumed by 
the concat_csv_files function itself.
"""
author = "Samuel Huckins"
date_started = "2009-01-30"
#-----------------------------------------------------------------------------
# For grabbing arguments passed:
import sys
from optparse import OptionParser
# Working with files and paths:
import os
# For reading csv files
import csv
# For timings
import time
# ActiveState Recipe 52560: Remove duplicates from a sequence
sys.path.append('/home/shuckins/code/code_homerepo/python-programming/utilities')
import uniqueify
# Setup logging
import logging
logger = logging.getLogger("combine-csvs")
logger.setLevel(logging.DEBUG)
# Use console for debugging
conlog = logging.StreamHandler()
conlog.setLevel(logging.DEBUG)
# Setup log formatter, add to console log
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - \
    %(message)s")
conlog.setFormatter(formatter)
# Add console log to logger
logger.addHandler(conlog)
#-----------------------------------------------------------------------------
def concat_csv_files(**kwargs):
    """
    Combines passed csv file(s) into single passed output file, using the
    delimiter passed. Dedupes and removes headers if passed.

    The dedupe_on is what deduping occurs against, if dedupe is true. With
    the default, row, two entire rows must match for one to be eliminated as a
    duplicate.
    """
    # For easier access:
    csv_files = kwargs['csv_files']
    output_file = kwargs['output_file']
    delimiter = kwargs['delimiter']
    dedupe = kwargs['dedupe']
    dedupe_on = kwargs['dedupe_on']
    remove_headers = kwargs['remove_headers']
    #
    logger.debug("CSV files to combine: %s" % ', '.join(csv_files))
    logger.info("Performing concatenation...")
    start_time = time.time()
    combined = []
    # Add the lines of each file to list:
    for f in csv_files:
        # Get number of lines:
        csv_file = open(f)
        csv_file_len = len(csv_file.readlines())
        csv_file.close()
        csv_file = open(f)
        # Read in the lines
        file_reader = csv.reader(csv_file, delimiter=delimiter)
        logger.info("Reading file: %s (%s lines)" % (f, csv_file_len))
        # Add the lines to output
        # Start on second row if we are removing headers:
        if remove_headers == True:
            first = 0
            for row in file_reader:
                if first == 0:
                    first = 1
                else:
                    combined.append(row)
        else:
            for row in file_reader:
                combined.append(row)
    logger.debug("Files' contents collected.")
    # Open for writing, erasing contents:
    output = open(output_file, 'w')
    # If we are deduping, make list of unique members:
    if dedupe == True:
        # If we are deduping aginst rows:
        if dedupe_on == "row":
            logger.debug("Deduping on entire row.")
            # Write the combined list to output file
            output_writer = csv.writer(output)
            # Remove dupes of entirely matching rows:
            unique_by_row = uniqueify.unique(combined)
            for row in unique_by_row:
                output_writer.writerow(row)
        # If not on row, we are deduping against
        # a particular cell:
        else:
            logger.debug("Deduping on column %s." % dedupe_on)
            # Remove dupes of entirely matching rows:
            unique_by_row = uniqueify.unique(combined)
            # Remove dupes in the column specified:
            entries = []
            unique_on_column = []
            # Keep a count of dupes
            dupes = 0
            for row in unique_by_row:
                try:
                    # Decrement the index passed by 1 so that user can
                    # pass the column counting from 1:
                    filter_cell = row[(int(dedupe_on) - 1)]
                    if filter_cell not in entries:
                        entries.append(filter_cell)
                        unique_on_column.append(row)
                    else:
                        dupes += 1
                except IndexError:
                    logger.critical("It appears that the dedupe field (%s) \
                        is outside the current columns." % dedupe_on)
            logger.debug("%s duplicates removed." % dupes)
            # Write the combined list to output file
            output_writer = csv.writer(output)
            # Write results:
            for row in unique_on_column:
                output_writer.writerow(row)
    # Otherwise just write the list:
    else:
        output_writer = csv.writer(output)
        for row in combined:
            output_writer.writerow(row)
    output.close()
    # Get the number of lines:
    output = open(output_file)
    output_file_len = len(output.readlines())
    output.close()
    duration = time.time() - start_time
    logger.info("Done: %s combined into %s (%s lines)" % \
        (', '.join(csv_files), output_file, output_file_len))
    logger.debug("Operation took %s seconds." % duration)

def get_csv_information(csvfile, prop="ALL"):
    """
    Finds various properties of the csv file passed. Will return the one
    specified by prop, or all of them by default).
    """
    # Get the information:
    csv_file = open(csvfile)
    dialect = csv.Sniffer().sniff(csv_file.read())
    all_props = {}
    all_props["delimiter"] = dialect.delimiter
    all_props["escapechar"] = dialect.escapechar
    all_props["lineterminator"] = dialect.lineterminator
    all_props["quotechar"] = dialect.quotechar
    csv_file.close()
    csv_file = open(csvfile)
    all_props["headerness"] = csv.Sniffer().has_header(csv_file.read(1024))
    csv_file.close()
    # Return what was asked for:
    if prop == "ALL":
        return all_props
    else:
        return all_props[prop]
#-----------------------------------------------------------------------------
def input_file_handler(option, opt_str, value, parser):
    """
    Makes the group of files passed into a list of filenames. It also 
    performs checks on the files to make sure we can use them.
    """
    value_list = value.split(',')
    # Make the comma-separated files into a list:
    setattr(parser.values, option.dest, value_list)
    for f in value_list:
        # Make sure each of the files exist:
        if os.path.isfile(f):
            # Make sure they can be opened:
            if os.access(f, 4):
                # Make sure they have content:
                if os.path.getsize(f) > 0:
                    continue
                else:
                    logger.critical("It seems %s is empty!" % f)
                    sys.exit(-1)
            else:
                logger.critical("It seems %s can't be read!" % f)
                sys.exit(-1)
        else:
            logger.critical("It seems %s doesn't exist or isn't a file!" % f)
            sys.exit(-1)

def output_file_checker(output_file):
    """
    This function checks to see if the output_file exists, providing the
    ability to stop the script from running if so.
    """
    if os.path.isfile(output_file):
        if os.access(output_file, 6):
            if os.path.getsize(output_file) > 0:
                logger.warning("%s exists and contains content." % output_file)
                cont = raw_input("Shall we continue anyway? (y/n) ")
                if cont.lower() == "n" or cont.lower() == "no":
                    logger.debug("Exiting based on user input.")
                    sys.exit(0)
            else:
                logger.debug("%s exists and is writeable, but is empty." % \
                    output_file)
        else:
            logger.critical("%s is a file, but cannot be read. Exiting." % \
                output_file)
            sys.exit(-1)

def check_delimiter_type(csv_files):
    """
    Finds the delimiter used in the first of the csv files passed.
    If the delimiter of subsequent files differs, exit with error.

    If all are consistent, return that delimiter.
    """
    for f in csv_files:
        try:
            delimiter
        except NameError:
            # If it's the first one, set delimiter:
            delimiter = get_csv_information(f, prop="delimiter")
            continue
        cur_delimiter = get_csv_information(f, prop="delimiter")
        # Compare first to current:
        if cur_delimiter != delimiter:
            logger.critical("""Initial file used delimiter %s, \
but %s uses %s!""" % (repr(delimiter), f, repr(cur_delimiter)))
            sys.exit(-1)
    return delimiter
#-----------------------------------------------------------------------------
def run():
    """
    Controls main program flow.
    """
    logger.debug("--MARK--")
    # Deal with parameters
    usage = "usage: %prog [options] -f INPUT_FILE(S) -o OUTPUT_FILE"
    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--files", action="callback", \
        callback=input_file_handler, type="string", \
        help="Comma-separated list of csv file locations to combine. Can be \
specified as full path, or just filenames if in current dir.", \
        dest="csv_files")
    parser.add_option("-o", "--output-file", dest="output_file", \
        help="Output file.")
    parser.add_option("-d", "--dedupe", dest="dedupe", action="store_true", \
        default=False, help="Pass this to dedupe all rows across files.")
    parser.add_option("-c", "--dedupe-on", dest="dedupe_on", help="The number \
of the cell to dedupe across files on, starting from 1.", default="row")
    parser.add_option("-r", "--remove-headers", dest="remove_headers", \
        action="store_true", default=False, help="Pass this to ignore the \
first row of each input file (headers).")
    (options, args) = parser.parse_args()
    # Exit if lacking parameters:
    if not options.output_file or not options.csv_files:
        logger.critical("You need to pass the csv file list and the output \
file name!")
        sys.exit(-1)
    # Shorter forms to access parameters:
    output_file = options.output_file
    output_file_checker(output_file)
    csv_files = options.csv_files
    # Create dict of options:
    concat_options = options.__dict__.copy()
    # Make sure there are no headers if they aren't to be removed:
    if options.remove_headers == False:
        for f in csv_files:
            if get_csv_information(f, prop="headerness"):
                logger.warning("%s appears to have headers." % f)
                cont = raw_input("Do you still want to continue (not recommended!)? ")
                print cont
                if cont.lower() != "y":
                    logger.debug("Exiting based on user input.")
                    sys.exit(0)
    # Check delimiter of files and add:
    delimiter = check_delimiter_type(csv_files)
    concat_options['delimiter'] = delimiter
    # Combine the files:
    concat_csv_files(**concat_options)
    # Done
    sys.exit(0)
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    run()

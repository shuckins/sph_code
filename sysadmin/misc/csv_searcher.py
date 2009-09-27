#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Name:        csv-searcher
# Purpose:     Checks a csv file, pulls out dates, counts up rows per date,
#              displays this, can filter on DoW.
#
# Author:      Samuel Huckins
#
# Started:     12/13/2008
# Copyright:   (c) 2008 Samuel Huckins
#-----------------------------------------------------------------------------
#
# For grabbing arguments passed:
import sys 
from optparse import OptionParser
# For reading csv files
import csv
# For checking files
import os
# For finding day of week:
import datetime
# For graphing:
try:
    from pylab import *
except:
    graphing = False
#-----------------------------------------------------------------------------
def checkFile(csv_file):
    """
    Make sure file exists and can be opened.
    """
    if os.path.exists(csv_file) and os.path.isfile(csv_file):
        try:
            open(csv_file, 'r')
            return 1
        except:
            return None
    else:
        return None
    
def readFile(csv_file_to_read):
    """
    Reads the csv file, returns a list of rows.
    """
    file = open(csv_file_to_read, 'r')
    rows = []
    try:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    finally:
        file.close()
        if len(rows) == 0:
            return None
        else:
            del rows[0]
            return rows

def dedupeFile(file_to_dedupe, field='email'):
    """
    Removes duplicates of field in file.
    """
    file_contents = readFile(file_to_dedupe)
    return deduped_file

def filterContents(csv_contents, filter_file, field='email'):
    """
    After deduping, remove matching field values from csv_contents 
    that are in options.filter_file.
    """
    deduped_filter_file = dedupeFile(filter_file)
    filtered_contents = []
    return filtered_contents

def parseContents(csv_contents):
    """
    Looks through each row, sums entries per date.
    """
    counts_per_date = {}
    for row in csv_contents:
        date = row[2][:10]
        if counts_per_date.has_key(date):
            counts_per_date[date] += 1
        else:
            counts_per_date[date] = 1
    return counts_per_date

def addDayOfWeek(undayed_results):
    """
    Takes list of lists of things including a date, add day of week for date.
    """
    for x in undayed_results:
        ugly_date = x[0]
        year = int(ugly_date[6:10])
        month = int(ugly_date[0:2])
        day = int(ugly_date[3:5])
        date = datetime.date(year, month, day)
        x.insert(1, date.strftime("%A"))
    return undayed_results
        
def graphData(days, counts, filter_day):
    """
    Creates graph image of data.
    """
    # Changes dates into ints in datetime format
    dated_days = []
    for day in days:
        year = int(day[6:10])
        month = int(day[0:2])
        day = int(day[3:5])
        date = datetime.date(year, month, day)
        dated_days.append(date)
    # Set labels
    x = xlabel('Date')
    setp(x, fontweight='bold')
    y = ylabel('Subscriptions')
    setp(y, fontweight='bold')
    # Subplot to handle date positioning
    ax = subplot(111)
    labels = ax.get_xticklabels()
    setp(labels, fontweight='bold', rotation=30, fontsize=10)
    # Plot as dates 
    plotted = plot_date(dated_days, counts, '--')
    setp(plotted, marker='s')
    title('Total subscriptions per %s' % filter_day)
    grid(True)
    savefig('%s_results.png' % filter_day, dpi=100)
#-----------------------------------------------------------------------------
def run():
    """
    Calls all other functions, provides main flow. 
    """
    # Define usage and options
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file", dest="csv_file", help="The csv file to parse")
    parser.add_option("-d", "--day", dest="day_of_week", help="The day of the week to filter")
    parser.add_option("-r", "--filter-file", dest="filter_file", help="File with entries to be removed from results")
    (options, args) = parser.parse_args()
    csv_file = options.csv_file
    # Check day passed:
    if options.day_of_week:
        days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
        if options.day_of_week not in days:
            print "Sorry, that day of week isn't recognized."
            sys.exit(-1)
    # Check for input file existence, perms, size:
    if csv_file is None:
        print "You need to pass a filename."
        sys.exit(-1)
    if checkFile(csv_file) != 1:
        print "Can't find and/or open your file."
        sys.exit(-1)
    csv_contents = readFile(csv_file)
    if csv_contents is None:
        print "Your %s is empty!" % csv_contents
        sys.exit(-1)
    # Define filter file
    if options.filter_file:
        # Remove duplicate email addresses
        csv_contents = filterContents(csv_contents, options.filter_file)
    # Parses dates, creates totals per date:
    results = parseContents(csv_contents)
    datatable = []
    # Sort by date:
    for key in results.keys():
        datatable.append([key, results[key]])
    datatable.sort()
    # Add day of week for each date:
    datatable = addDayOfWeek(datatable)
    # Define filter day
    filter_day = "Saturday"
    if options.day_of_week:
        filter_day = options.day_of_week
    # Define output csv
    results_csv_file = "%s_results.csv" % filter_day
    # Define and add header
    header = ["Date", "Day", "Count"]
    datatable.insert(0, header)
    # Define total of all:
    sum_total = 0
    days_returned = 0
    filtered_results = []
    # Print results, headers first:
    print datatable[0]
    for row in datatable[1:]:
        if row[1] == filter_day:
            sum_total += row[2]
            days_returned += 1
            filtered_results.append(row)
    for each_result in filtered_results:
        print each_result
    stats = "Total: %s | Average: %s" % (sum_total, (sum_total / days_returned))
    print
    print " * " + stats
    result_csv = csv.writer(open(results_csv_file, 'wb'))
    result_csv.writerow(datatable[0])
    result_csv.writerows([row for row in filtered_results])
    print  " * " + "Results table written as csv to: %s" % results_csv_file
    if graphing:
        dates = [x[0] for x in filtered_results]
        counts = [x[2] for x in filtered_results]
        graphData(dates, counts, filter_day)
        print  " * " + "Results graph created as: %s" % ('%s_results.png' % filter_day)
        sys.exit(0)
    else:   
        print  " * " + "Can't create graph, install pylab."
        sys.exit(0)
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    run()


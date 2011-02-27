#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Name:        mysql-table-size
# Purpose:    
# This script is designed to print out the top five largest MySQL tables on 
# the box.
#
# Author:      Samuel Huckins
#
# Started:     11/14/2008
# Copyright:   (c) 2008 Samuel Huckins
#-----------------------------------------------------------------------------
#
# For grabbing arguments passed:
import sys
from optparse import OptionParser
# For connecting to MySQL
import MySQLdb
# For pretty printing
import operator
import cStringIO
import math
#
def indent(rows, hasHeader=True, headerChar='-', delim=' | ', justify='left',
           separateRows=False, prefix='|', postfix='|', wrapfunc=lambda x:x):
    """
    Utility function to print pretty tables.
    """
    # closure for breaking logical rows to physical, using wrapfunc
    def rowWrapper(row, width=40):
        newRows = [wrapfunc(item).split('\n') for item in row]
        return [[substr or '' for substr in item] for item in \
                map(None,*newRows)]
    # break each logical row into one or more physical ones
    logicalRows = [rowWrapper(row) for row in rows]
    # columns of physical rows
    columns = map(None,*reduce(operator.add,logicalRows))
    # get the maximum of each column by the string length of its items
    maxWidths = [max([len(str(item)) for item in column]) for column in \
        columns]
    rowSeparator = headerChar * (len(prefix) + len(postfix) + sum(maxWidths) \
                                + len(delim)*(len(maxWidths)-1))
    # select the appropriate justify method
    justify = {'center':str.center, 'right':str.rjust, \
        'left':str.ljust}[justify.lower()]
    output=cStringIO.StringIO()
    if separateRows: print >> output, rowSeparator
    for physicalRows in logicalRows:
        for row in physicalRows:
            print >> output, \
                prefix \
                + delim.join([justify(str(item),width) for (item,width) in \
                zip(row,maxWidths)]) \
                + postfix
        if separateRows or hasHeader: print >> output, rowSeparator; \
            hasHeader=False
    return output.getvalue()

def runMySQL(user, passwd):
    """
    """
    db = MySQLdb.connect("localhost", user, passwd, "information_schema")
    cursor = db.cursor()
    sql = "SELECT concat(table_schema,'.',table_name) table_name, concat(round(data_length/(1024*1024),2),'M') data_length FROM TABLES ORDER BY data_length DESC LIMIT 5;"
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    return data

def run():
    """
    """
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-u", "--user", dest="user", help="The MySQL user", default="root")
    parser.add_option("-p", "--password", dest="passwd", help="The MySQL password")
    (options, args) = parser.parse_args()
    if options.passwd is None:
        print "Please enter a password!"
        sys.exit(-1)
    data = runMySQL(options.user, options.passwd)
    headertoadd = ("Table Name", "Size")
    datatable = (headertoadd,) + data
    print indent(datatable)

#-----------------------------------------------------------------------------
if __name__ == "__main__":
    run()

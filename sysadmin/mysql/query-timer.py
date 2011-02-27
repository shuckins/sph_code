#! /usr/bin/env python
#-----------------------------------------------------------------------------
# Name:        query-timer
# Purpose:     Runs a requested query, or a set of pre-specified queries,
#              against a MySQL instance, reports time taken.                
#
# Author:      Samuel Huckins
#
# Started:     12/19/2008
# Copyright:   (c) 2008 Samuel Huckins
#-----------------------------------------------------------------------------
# For exiting app
import sys
# For checking files
import os
# For logging
import logging
# For getting the password without echo
import getpass
# For reading conf files
import ConfigParser
# For timing
import time
# For MySQL DB access
try:
    import MySQLdb
except ImportError:
    print "You need to install the MySQLdb module. Check",
    print "http://sourceforge.net/projects/mysql-python for details."
    sys.exit(-1)

# Setup logging
logger = logging.getLogger("query-timer")
logger.setLevel(logging.INFO)
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
def runQuery(db='', user = 'root', password = '', socket = '/var/lib/mysql/mysql.sock', port = 3306, query='show databases;'):
    """
    Runs the requested query with passed params. If no query, uses short, simple default.
    """
    try:
        logger.debug("Attempting to connect...")
        db = MySQLdb.connect(host='localhost', unix_socket=socket, port=int(port), user=user, passwd=password, db=db)
        logger.debug("Connected to '%s' as '%s'." % (socket, user))
        cursor = db.cursor()
        logger.debug("Running query...")
        cursor.execute(query)
        mysql_results = cursor.fetchall()
        logger.debug("Query complete.")
        cursor.close()
        db.close()
        return mysql_results
    except MySQLdb.Error, e:
        logger.error("Error %d: %s" % (e.args[0], e.args[1]))
        sys.exit(-1)

def runAndTime(configs):
    """
    Wraps query run in timer, returns the time taken.
    """
    try:
        del configs['instance']
    except:
        pass
    start_time = time.time()
    results = runQuery(**configs)
    time_taken = time.time() - start_time
    if len(results) > 0:
        logger.debug("Query returned results.")
    else:
        logger.debug("Query returned no results.")
    return time_taken

def readConfiguration(conf_file):
    """
    Reads in the conf file passed, returns dictionary of options.
    """
    configs = []
    config = ConfigParser.ConfigParser()
    config.read(conf_file)
    for section in config.sections():
        section_configs = {}
        for item in config.items(section):
            section_configs[item[0]] = item[1]
        section_configs['instance'] = section
        configs.append(section_configs)
    return configs

def run():
    """
    Calls the various functions in order and exits.
    """
    conf_file = raw_input("Conf file: ")
    times_to_run = int(raw_input("Times to run the query: "))
    if os.path.exists(conf_file) and os.path.isfile(conf_file):
        if os.path.getsize(conf_file) > 0:
            configs = readConfiguration(conf_file)
            times_recorded = {}
            for section in configs:
                time_name = section['instance']
                temp_time = 0
                for x in range(times_to_run):
                    temp_time += runAndTime(section)
                avg_time = temp_time / times_to_run
                times_recorded[time_name] = avg_time
        else:
            logger.critical("%s appears to be empty." % conf_file)
            sys.exit(-1)
    else:
        logger.critical("Sorry, doesn't look like %s exists." % conf_file)
        sys.exit(-1)
    # Format and print results
    logger.info("Average times recorded:")
    for each_time in times_recorded:
        print " * %s: %s seconds" % (each_time, times_recorded[each_time])
    sys.exit(0)
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    run()

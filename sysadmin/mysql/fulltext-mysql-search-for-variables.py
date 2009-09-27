#!/usr/bin/env python
#-----------------------------------------------------------------------------
"""This script allows you to obtain a list of search terms, then find matches
in a specified column, using MySQL fulltext searching. This is needed because
there is no way to pass a variable to the against() function in MySQL, only
plain strings. Lame.
"""
author = "Samuel Huckins"
date_started = "2009-02-05"
#-----------------------------------------------------------------------------
conf_file='fulltext-search.yaml'
# For grabbing arguments passed:
import sys
from optparse import OptionParser
# For connecting to MySQL
import MySQLdb
# For config file reading
import yaml
#-----------------------------------------------------------------------------
def run_mysql(**kwargs):
    """
    Runs query passed with connection info passed, returns results.
    """
    query = kwargs['query']
    try:
        db = MySQLdb.connect(user=kwargs['user'], passwd=kwargs['password'], \
            db=kwargs['database'], unix_socket=kwargs['socket'], host=kwargs['host'])
    except MySQLdb.Error, e:
        print "Error connecting to DB!"
        raise e
    cursor = db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return data

def get_search_terms(mysql_options):
    """
    Runs the query passed to form and return a list of search terms.
    """
    search_terms = run_mysql(mysql_options)
    if len(search_terms) > 0:
        return search_terms
    else:
        return None
#-----------------------------------------------------------------------------
def run():
    """
    Controls main program flow.
    """
    # All conf needs to be in this file:
    config_file = open(conf_file, 'r')
    options_from_file = yaml.load(config_file)
    config_file.close()
    options = options_from_file['original']
    # Get list of terms to search on
    # Perform search
    # Done
    print "Done."
    sys.exit(0)
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    run()

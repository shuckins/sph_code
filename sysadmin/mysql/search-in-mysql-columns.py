#! /usr/bin/env python
#-----------------------------------------------------------------------------
# Name:        search-in-mysql-columns
# Author:      Samuel Huckins
# Started:     12/03/2008
#-----------------------------------------------------------------------------
"""
Searches through all columns in all tables of the DB specified for the string 
specified, prints the results.

NOTE! This is no longer necessary if you are running MySQL version 5 or 
higher. With the current versions information_schema 
(http://dev.mysql.com/doc/refman/5.0/en/information-schema.html) 
is provided as a way to search for column names:

    select column_name from information_schema
    where table_schema = "MYDB"
    and column_name like "%foo%";

"""
# For exiting app
import sys
# For logging
import logging
# For getting the password without echo
import getpass
# For MySQL DB access
try:
    import MySQLdb
except ImportError:
    print "You need to install the MySQLdb module. Check",
    print "http://sourceforge.net/projects/mysql-python for details."
    sys.exit(-1)
# Setup logging
logger = logging.getLogger("search-in-mysql-columns")
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

def searchForStringInColumns(searchterm, DB, mysql_user, mysql_password, mysql_socket):
    """
    Look for fieldnames containing searchterm in all tables in DB.
    """
    mysql_table_query = """SELECT TABLE_NAME, COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE column_name LIKE '%s'
and TABLE_SCHEMA like '%s';""" % ("%" + searchterm + "%", DB)
    try:
        db = MySQLdb.connect(host = "localhost", user=mysql_user, passwd=mysql_password, db=DB, unix_socket=mysql_socket)
        logger.debug("Connected to '%s' as '%s'." % (DB, mysql_user))
    except MySQLdb.Error, e:
        logger.error("Error %d: %s" % (e.args[0], e.args[1]))
        raise e
    cursor= db.cursor()
    logger.debug("Searching for '%s' in '%s'..." % (searchterm, DB))
    cursor.execute(mysql_table_query)
    mysql_results = cursor.fetchall()
    db.close()
    return mysql_results

def find_all_databases(mysql_user, mysql_password, mysql_socket):
    """
    Find all databases in the instance passed.
    """
    mysql_db_query = "show databases;"
    try:
        db = MySQLdb.connect(host = "localhost", user=mysql_user, passwd=mysql_password, unix_socket=mysql_socket)
        logger.debug("Connected to as '%s'." % mysql_user)
    except MySQLdb.Error, e:
        logger.error("Error %d: %s" % (e.args[0], e.args[1]))
        raise e
    cursor= db.cursor()
    logger.debug("Performing search for databases...")
    cursor.execute(mysql_db_query)
    mysql_results = cursor.fetchall()
    db.close()
    return mysql_results


def formatAndPrintResults(search_results):
    """
    Creates a more readable display of the results.
    """
    for each_result in search_results:
        print " * Table: %s, Column(s): %s" % (each_result[0], each_result[1])

def run():
    """
    Calls the various functions in order and exits.
    """
    # Collect the connection settings to use:
    print "~~Connection settings~~"
    db_passed = raw_input("MySQL DB (or 'ALL'): ")
    mysql_user_passed = raw_input("MySQL user (root): ")
    if len(mysql_user_passed) == 0:
        mysql_user_passed = "root"
    mysql_password_passed = getpass.getpass()
    mysql_socket_passed = raw_input("MySQL socket (/var/run/mysqld/mysqld.sock): ")
    if len(mysql_socket_passed) == 0:
        mysql_socket_passed = "/var/run/mysqld/mysqld.sock"
    search_again = 1
    # Follow this loop for the first time and until user enters that
    # they don't want to continue:
    while search_again == 1:
        print ""
        searchterm = raw_input("Searchterm: ")
        if len(searchterm) == 0:
            logger.error("Please enter a real searchterm!")
            sys.exit(-1)
        # If they want to search in all databases, find them all:
        if db_passed == "ALL":
            dbs = find_all_databases(mysql_user_passed, mysql_password_passed, mysql_socket_passed)
            for db in dbs:
                search_results = searchForStringInColumns(searchterm, db[0], mysql_user_passed, mysql_password_passed, mysql_socket_passed)
                # Format and print results
                if len(search_results) > 0:
                    logger.debug("Matches found!")
                    print "Matches on '%s' in '%s' database columns: " % (searchterm, db[0])
                    formatted_results = formatAndPrintResults(search_results)
                else:
                    logger.debug("No matches found.")
                    print "No matches on '%s' in '%s' database columns." % (searchterm, db[0])
        else:
            search_results = searchForStringInColumns(searchterm, db_passed, mysql_user_passed, mysql_password_passed, mysql_socket_passed)
            # Format and print results
            if len(search_results) > 0:
                logger.debug("Matches found!")
                print "Matches on '%s' in '%s': " % (searchterm, db_passed)
                formatted_results = formatAndPrintResults(search_results)
            else:
                logger.debug("No matches found.")
                print "No matches on '%s' in '%s'." % (searchterm, db_passed)
        run_again = raw_input("Perform another search? (y/n) ")
        if run_again.lower() == "y":
            search_again = 1
        else:
            # Done
            logger.debug("Exiting.")
            sys.exit(0)
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    run()

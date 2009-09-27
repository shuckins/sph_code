#!/usr/bin/env python
#-----------------------------------------------------------------------------
"""
This program retrieves create table statements for all tables in a DB, creates
equivalent Federated table create statements, prints these to file. You can 
then import this file.

All config is placed in federated_converter.yaml.
"""
author = "Samuel Huckins"
date_started = "2009-01-12"
version = "0.1"
#-----------------------------------------------------------------------------
conf_file='/home/shuckins/federated_converter.yaml'
# For grabbing arguments passed:
import sys
from optparse import OptionParser
# Regex magic
import re
# For logging
import logging
# For connecting to MySQL
import MySQLdb
# For config file reading
import yaml
# Setup logging
logger = logging.getLogger("create-federated-equivalent")
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
def run_mysql(**kwargs):
    """
    Runs query passed with connection info passed, returns results.
    """
    query = kwargs['query']
    try:
        db = MySQLdb.connect(user=kwargs['user'], passwd=kwargs['password'], \
            db=kwargs['database'], unix_socket=kwargs['socket'], host=kwargs['host'])
    except MySQLdb.Error, e:
        logger.critical("Error connecting to DB!")
        raise e
    cursor = db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return data

def get_create_table(options):
    """
    Finds create table statements for the DB passed. Returns these as list.
    """
    # Get tables for database passed:
    tables = []
    options['query'] = "show tables;"
    for table in run_mysql(**options):
        tables.append(table)
    # Get create table statements per table:
    create_table_statements = []
    for table in tables:
        options['query'] = "show create table %s;" % table
        create_table = run_mysql(**options)
        create_table_statements.append(create_table[0][1])
    return create_table_statements

def make_federated(regular_statements, fed_options):
    """
    Returns Federated version of each regular statement passed.
    This requires a change of the ENGINE as well as adding a 
    connection string.
    """
    # Create list of Federated versions
    federated_statements = []
    for statement in regular_statements:
        # Remove any FULLTEXT indexes; Federated will throw an error:
        # ALERT/TODO: You have to remove the comma and the end of the line before this,
        # otherwise you get an error.
        fulltext_result = re.search('.*(FULLTEXT KEY)(.*)', statement)
        if fulltext_result:
            statement = re.sub(".*(FULLTEXT KEY)(.*)", "/* FULLTEXT KEYs not allowed by Federated; \\2 */", statement)
        #  New engine
        engine = "ENGINE=FEDERATED"
        # Find the table name with regex to put in conn string
        re1='.*?'   # Non-greedy match on filler
        re2='(CREATE)' 
        re3='.*?'   # Non-greedy match on filler
        re4='(TABLE)'
        re5='.*?'   # Non-greedy match on filler
        re6='((?:[a-z][a-z0-9_]*))' # The table name
        rg = re.compile(re1+re2+re3+re4+re5+re6,re.IGNORECASE|re.DOTALL)
        results = rg.search(statement)
        table = results.group(3)
        # Define the middle stuff to keep
        re1='(\\))' # Any Single Character 1
        re2='.*?'   # Any Single Character 2
        re3='(ENGINE)'  # Word 1
        re4='(=)'   # Any Single Character 3
        re5='((?:[a-z][a-z0-9_]*))'  # Word 2
        re6='.*?'   # Any Single Character 3
        re7='(?P<MID>[a-z][a-z0-9_ =]*)$' # Variable Name 1
        rg = re.compile(re1+re2+re3+re4+re5+re6+re7,re.IGNORECASE|re.DOTALL)
        m = rg.search(statement)
        middle = m.group('MID')
        # Form the connection string
        connection = "CONNECTION='mysql://%s:%s@%s:%s/%s/%s';" % (fed_options['user'], fed_options['password'], fed_options['host'], fed_options['port'], fed_options['database'], table)
        # Remove unneeded last line:
        statement_list = statement.split('\n')
        statement_sans_last = statement_list[0:(len(statement_list) - 1)]
        statement = '\n'.join(statement_sans_last)
        # Put it all together
        last_line = "\n" + ") " + "\t" + engine + "\n" + "\t" + middle + "\n" + "\t" + connection + "\n"
        fed_statement = statement + last_line
        federated_statements.append(fed_statement)
    # Add necessary create database to output:
    federated_statements.insert(0, 'CREATE DATABASE /*!32312 IF NOT EXISTS*/ `%s` /*!40100 DEFAULT CHARACTER SET latin1 */; \nUSE `%s`;\n' % (fed_options['database'], fed_options['database']))
    return federated_statements

def run():
    """
    Controls main program flow.
    """
    # All conf needs to be in this file:
    config_file = open(conf_file, 'r')
    options_from_file = yaml.load(config_file)
    config_file.close()
    options = options_from_file['original']
    fed_options = options_from_file['federated']
    # Get create table statements for the DB desired:
    regular_statements = get_create_table(options)
    # Make Federated versions of those statements:
    federated_statements = make_federated(regular_statements, fed_options)
    # Print Federated versions to file:
    filename = "federated_tables_from_%s.sql" % options['database']
    results_file = open(filename, 'w')
    results_file.write('\n'.join(federated_statements))
    results_file.close()
    # Done
    logger.info("""All done! %s created with Federated versions of the tables 
in the DB passed (%s).""" % (filename, options['database']))
    sys.exit(0)
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    run()

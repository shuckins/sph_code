#!/usr/bin/env python
#-----------------------------------------------------------------------------
"""
This program queries the user for information and, based on that, creates a
skeleton script file.  The goal is to create a clean script with some of the
repetitive setup already done for you, ready for additions pertinent to the
task at hand.

It takes no parameters, simply run it as a normal user and buckle up. It tries
to provide sensible default values and options, helpful comments, and follow
PEP8. It also incorporates what I have found to be optimal setups for common
actions.

Author: Samuel Huckins
Date started: 2008-11-25
"""
#-----------------------------------------------------------------------------
# For exiting:
import sys
# For determining date:
import datetime
# For checking file states:
import os
#-----------------------------------------------------------------------------
def check_filename(filename):
    """
    Checks if the passed filename exists in the current directory. If it
    doesn't, return the filename. If it does, alert the user, see if they
    want to quit or continue. If they want to continue, ask for another
    filename.
    """
    while os.path.exists(filename):
        print "DANGER! %s already exists!" % filename
        if raw_input("Do you want to continue anyway (YES/no)? ").lower() \
            == "no":
            sys.exit(0)
        return filename
    return filename

def get_params():
    """
    Get needed params for script generation.
    """
    params = {}
    # Get script file name
    script_filename = raw_input(" * What would you like the script filename \
to be? ")
    if len(script_filename) == 0:
        print "You have to enter a filename!"
        sys.exit(-1)
    else:
        if script_filename.split('.')[-1] != 'py':
            script_filename += '.py'
        check_filename(script_filename)
        params['filename'] = script_filename

    print "\nFirst I'll need information on what you want your script to do.\n"
    # Get author name
    default_author = os.getenv('USER')
    author = raw_input(" * What is your name? (%s) " % default_author)
    if len(author) > 0:
        params['author'] = author
    else:
        params['author'] = default_author
    # Get purpose
    user_input = []
    entry = raw_input(" * What is the purpose of the script? ('done' on its \
own line to quit) \n")
    while entry != "done":
        user_input.append(entry)
        entry = raw_input("")
    # Joining with newline preserves user breaks and paragraphs.
    purpose = '\n'.join(user_input)
    params['purpose'] = purpose
    # Notify of defaults:
    print "\nConsole logging will be added by default. A file logging example",
    print "will be included, commented.\n"
    # Ask about optional functionality:
    print "Would you like your script to also include:"
    # Option parsing?
    option_parsing = raw_input(" * Option parsing? (YES/no): ")
    params['option_parsing'] = True
    if option_parsing.lower() == "no":
        params['option_parsing'] = False
    # Send email?
    email = raw_input(" * Sending email? (YES/no): ")
    params['email'] = True
    if email.lower() == "no":
        params['email'] = False
    # Access MySQL DB?
    mysql_access = raw_input(" * MySQL DB access? (YES/no): ")
    params['mysql_access'] = True
    if mysql_access.lower() == "no":
        params['mysql_access'] = False
    # Use config file?
    config_file = raw_input(" * Config file parsing? (YES/no): ")
    params['config_file'] = True
    if config_file.lower() == "no":
        params['config_file'] = False
    # Check for internet access?
    internet_check = raw_input(" * Checking for internet access? (YES/no): ")
    params['internet_check'] = True
    if internet_check.lower() == "no":
        params['internet_check'] = False
    # Timing of operation?
    timing = raw_input(" * Timing of the script's run? (YES/no): ")
    params['timing'] = True
    if timing.lower() == "no":
        params['timing'] = False
    # Send back the options determined:
    return params

def create_header(author, purpose):
    """
    Creates top matter based on params passed.
    """
    date_started = datetime.date.today().isoformat()
    header = """#!/usr/bin/env python
#-----------------------------------------------------------------------------
\"\"\"
%s

Author: %s
Date started: %s
\"\"\"
#-----------------------------------------------------------------------------""" % (purpose, author, date_started)
    return header

def create_body(params):
    """
    Creates the main body of the script, returns it.
    """
    imports = ["# For exiting:\nimport sys"]
    add_to_main = []
    body_things = []
    # Setup logging:
    imports.append("""# For logging:
import logging
script_name = __file__.split("/")[-1]
# Setup logging
logger = logging.getLogger(script_name)
logger.setLevel(logging.INFO)
# Use file for standard logging
#logfilename = "/var/log/%s.log" % script_name
#filelog = logging.FileHandler(logfilename, 'a')
#filelog.setLevel(logging.INFO)
# Use console for debugging
conlog = logging.StreamHandler()
conlog.setLevel(logging.DEBUG)
# Setup log formatter, add to console log
formatter = logging.Formatter("%(asctime)s - \\
%(name)s - %(lineno)s - %(levelname)s - %(message)s")
conlog.setFormatter(formatter)
#filelog.setFormatter(formatter)
# Add console log to logger
logger.addHandler(conlog)
#logger.addHandler(filelog)""")
    # Setup option parsing:
    if params['option_parsing']:
        imports.append('# For parsing options passed:\nfrom optparse import OptionParser')
        body_things.append("""def process_args():
    \"\"\"
    Process options passed at the command line. Return arguments and
    options.
    \"\"\"
    usage = __doc__
    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--option1", action="store", dest="option1",
        help="An example option which announces that it was passed.")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose_logging",
        default=False,
        help="If passed, default logging level is changed to DEBUG.")
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet",
        default=False,
        help="If passed, default logging level is raised to ERROR (and above).")
    return parser.parse_args()
""")
        add_to_main.insert(0, """    # Parsing options passed:
    (opts, args) = process_args()
    if opts.verbose_logging:
        logger.setLevel(logging.DEBUG)
    elif opts.quiet:
        logger.setLevel(logging.ERROR)""")
        add_to_main.append("""    if opts.option1 is not None:
        logger.debug("Looks like you passed '%s' as option1. Good job." % opts.option1)""")
    # Setup for sending email:
    if params['email']:
        imports.append('# For sending email:\nimport smtplib')
        body_things.append("""def send_mail(send_from, send_to, subject,
        body_text = "", server="localhost"):
    \"\"\"
    Sends out mail via SMTP. Assumes mail server is on local box.
    \"\"\"
    headers = "From: %s\\r\\nTo: %s\\r\\nSubject: %s\\r\\n\\r\\n" % \\
        (send_from, send_to, subject)
    message = headers + body_text
    mail_server = smtplib.SMTP(server)
    logger.debug("Sending email...")
    mail_server.sendmail(send_from, send_to, message)
    mail_server.quit()
    logger.debug("Sent.")
""")
        add_to_main.append("""
    # Here is an example of sending mail:
    #logger.debug("Sending mail...")
    #send_mail(subject="I am the subject", \\
        #send_from="local_user@test.com", send_to="other_user@example.com", \\
        #body_text="I am totally a message! Wooo!")
    #logger.debug("Mail sent.")""")
    # Setup MySQL access:
    if params['mysql_access']:
        imports.append("""# For MySQL DB access
try:
    import MySQLdb
except ImportError:
    print \"\"\"You need to install the MySQLdb module. Check \\
http://sourceforge.net/projects/mysql-python for details.\"\"\"
    sys.exit(1)""")
        body_things.append("""def run_mysql(db_params):
    \"\"\"
    Run MySQL queries passed using passed connection information.
    \"\"\"
    # If you want to see params for each connection attempt:
    #logger.debug("Trying to connect with: %s" % db_params)
    try:
        db = MySQLdb.connect(use_unicode=True, user=db_params['user'], \\
            passwd=db_params['password'], db=db_params['database'], \\
            unix_socket=db_params['socket'], host=db_params['host'], \\
            port=db_params['port'])
    except MySQLdb.Error, e:
        logger.critical("Error in connecting %d: %s" % (e.args[0], \\
            e.args[1]))
        sys.exit(1)
    cursor = db.cursor()
    try:
        cursor.execute(db_params['query'])
        data = cursor.fetchall()
        rows_returned = cursor.rowcount
    except MySQLdb.Error, e:
        raise e
        cursor.close()
        db.close()
    cursor.close()
    db.close()
    return data, rows_returned
""")
    # Setup config file parsing:
    if params['config_file']:
        # A sensible config file name:
        config_file = './%s_conf.yaml' % params['filename'][0:-3]
        imports.append("""# For reading config files:
try:
    import yaml
except ImportError:
    print "You need to install the yaml module. See http://pyyaml.org/."
    sys.exit(1)
config_file='%s'""" % config_file)
        add_to_main.append("""    # Read in config file:
    conf_file = open(config_file, 'r')
    conf_options = yaml.load(conf_file)
    conf_file.close()
    # Now you can access options via: 
    #option_name = conf_options['option_name']""")
    # Setup internet access check:
    if params['internet_check']:
        imports.append("""# For internet connection checking
from httplib import HTTP
from urlparse import urlparse""")
        body_things.append("""def check_internet():
    \"\"\"
    For checking this box's internet connection.
    \"\"\"
    # Multiple generally reliable sites to verify connection:
    verify_list = ['http://www.google.com/', 'http://www.yahoo.com', \\
        'http://www.w3c.org/']
    for u in verify_list:
        try:
            p = urlparse(u)
            h = HTTP(p[1])
            h.putrequest('HEAD', p[2])
            h.endheaders()
            if h.getreply()[0] != 200:
                logger.critical("Internet connection seems to be down. Exiting.")
                sys.exit(1)
        except:
            logger.critical("There is a problem with the network interface.")
            sys.exit(1)
    logger.info("Internet connection appears to be up.")""")
        add_to_main.append("""    # Checking internet access:\n    check_internet()""")

    # Setup script timing
    if params["timing"]:
        imports.append("# For timing:\nimport time")
        add_to_main.insert(0, """# Start time:
    start_time = time.time()""")
        add_to_main.append("""    # Duration:
    duration = time.time() - start_time
    logger.debug("Script operations took %.4f seconds." % duration)""")

    imports.append("#-----------------------------------------------------------------------------")

    # If there's nothing to be added to main, say hello:
    if len(add_to_main) == 0:
        add_to_main.append(1, "    logger.info(\"Hello world!\")")
    else:
        add_to_main.insert(1, "    logger.debug(\"Starting %s.\" % script_name)")
        add_to_main.append("    logger.debug(\"Exiting.\")")
    # Form the body from parts collected:
    body = """
%s

%s
#-----------------------------------------------------------------------------
def main():
    \"""
    Provides main flow control.
    \"""
    %s
    sys.exit(0)""" % ((('\n').join(imports)), (('\n').join(body_things)), \
        (('\n').join(add_to_main)))
    return body

def create_footer():
    """
    Returns a defined footer structure."""
    footer = """
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()"""
    return footer

def output_script(script, filename):
    """
    Print the produced script to filename passed.
    """
    try:
        print "\nMaking your script, checking it twice..."
        script_file = open(filename, "w")
        script_file.write(script)
        script_file.close()
    except Exception:
        return Exception
#-----------------------------------------------------------------------------
def main():
    """
    Control main program flow.
    """
    # Get params:
    params = get_params()
    # Create top matter:
    author = params['author']
    if params.has_key('purpose'):
        if len(params['purpose']) == 0:
            purpose = "Something useful."
        else:
            purpose = params['purpose']
    header = create_header(author, purpose)
    body = create_body(params)
    footer = create_footer()
    # Create config file if needed:
    if params['config_file']:
        # A sensible config file name:
        config_file = '%s_conf.yaml' % params['filename'][0:-3]
        # Create a file of that name:
        check_filename(config_file)
        openfile = open(os.path.join(config_file), 'w')
        openfile.close()
    # Collect script and write it to file:
    script = header + body + footer
    output_script(script, params['filename'])
    # Make script executable:
    os.chmod(os.path.join(os.path.abspath(os.path.curdir), \
        params['filename']), 0755)
    # Done
    print "\nAll done. Your script (%s) is waiting." % params['filename'],
    if params['config_file']:
        print "A blank config file (%s) was also created." % config_file,
    print "Get coding!"
    sys.exit(0)
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()

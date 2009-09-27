#!/usr/bin/env python
#-----------------------------------------------------------------------------
"""
This script is designed to collect cronjob related information on Linux
systems. It looks in all user's crontab files as well as all cron.d files. It
provides command line options to specify what is collected and how it is
presented. The output consists of cronjobs ordered by their time of their
location.

This file can also be imported as a module, to provide access to the cronjob
collection and parsing classes, for use in other programs.

Author: Samuel Huckins
Date started: 2009-05-23
"""
#-----------------------------------------------------------------------------
# For exiting:
import sys
# OS information:
import os
# For logging:
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
formatter = logging.Formatter("%(asctime)s - \
%(name)s - %(lineno)s - %(levelname)s - %(message)s")
conlog.setFormatter(formatter)
#filelog.setFormatter(formatter)
# Add console log to logger
logger.addHandler(conlog)
#logger.addHandler(filelog)
# For parsing options passed:
from optparse import OptionParser
# For sending email:
import smtplib
#-----------------------------------------------------------------------------

def check_system():
    """
    Checks the local operating system to verify script can complete.
    """
    uname = os.uname()
    print uname
    # Verify system is Linux or Darwin:
    # Verify crontab files can be found:
    # Verify cron.d files can be found:
    pass

class CronGatherer(object):
    """
    Collects crontab and cron.d contents based on OS information passed.
    """

    def __init__(self):
        """
        """
        pass

class Outputter(object):
    """
    Formats and prints output based on options passed.
    """

    def __init__(self):
        """
        """
        pass

    def mail_output(self):
        #logger.debug("Sending mail...")
        #send_mail(subject="I am the subject", \
            #send_from="local_user@test.com", send_to="other_user@example.com", \
            #body_text="I am totally a message! Wooo!")
        #logger.debug("Mail sent.")
        pass

    def send_mail(self, send_from, send_to, subject,
            body_text = "", server="localhost"):
        """
        Sends out mail via SMTP. Assumes mail server is on local box.
        """
        headers = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % \
            (send_from, send_to, subject)
        message = headers + body_text
        mail_server = smtplib.SMTP(server)
        logger.debug("Sending email...")
        mail_server.sendmail(send_from, send_to, message)
        mail_server.quit()
        logger.debug("Sent.")

#-----------------------------------------------------------------------------

def process_args():
    """
    Process options passed at the command line. Return arguments and
    options.
    """
    usage = __doc__
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose_logging",
        default=False,
        help="If passed, default logging level is changed to DEBUG.")
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet",
        default=False,
        help="If passed, default logging level is raised to ERROR (and above).")
    return parser.parse_args()


def main():
    """
    Provides main flow control.
    """
    # Parsing options passed:
    (opts, args) = process_args()
    if opts.verbose_logging:
        logger.setLevel(logging.DEBUG)
    elif opts.quiet:
        logger.setLevel(logging.ERROR)
    logger.debug("Starting %s." % script_name)
    # Verify system meets requirements:
    check = check_system()
    if not check:
        logger.error("System does not meet requirements.")
        sys.exit(-1)
    # Gather cronjob information:
    cronjobs = CronGatherer()
    # Output results:
    Outputter(cronjobs)
    # Done:
    logger.debug("Exiting.")
    sys.exit(0)
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()

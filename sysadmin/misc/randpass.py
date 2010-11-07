#!/usr/bin/env python
"""
Generates random passwords.

With no options it will return one 10 character password, alphanumeric with
varying cases. You can specify a different length, number of passwords, and
whether special characters (punctuation, etc) should be included.

If you want to learn more about password generation or want a *really* secure
password, check out this site: https://www.grc.com/passwords.htm

Examples:
    * Single 10 character alphanumeric case-varying password:
        randpass.py
    * Two 20 character alphanumeric case-varying passwords with special
      characters:
        randpass.py --count=2 --length=20 --specialc

Author: Samuel Huckins
Date started: 2010-11-06
Email: wormwood_3@yahoo.com
Homepage: http://samuelhuckins.com/
"""

from optparse import OptionParser
import random
import sys
#-----------------------------------------------------------------------------

def gen_pass(pwlen, specialc):
    """
    """
    alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
    alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    special_chars= "!?$?%^&*()_-+={[}]:;@~#|\<,>.?/"

    chars = alphabet_lower + alphabet_upper + numbers
    if specialc:
        chars += special_chars

    pw = "".join(random.sample(chars, pwlen))
    return pw


def process_args():
    """
    Process options passed at the command line. Return arguments and
    options.
    """
    usage = __doc__
    parser = OptionParser(usage=usage)
    parser.add_option("-l", "--length", action="store", dest="pwlen",
        help="The length of each password, defaults to 10 characters.")
    parser.add_option("-s", "--specialc", action="store_true", dest="specialc",
        help="If passed, passwords will include non alphanumeric characters (default off).")
    parser.add_option("-c", "--count", action="store", dest="pwcount",
        help="Number of passwords to generate (default is one).")

    return parser.parse_args()

#-----------------------------------------------------------------------------
def main():
    """
    Provides main flow control.
    """
    (opts, args) = process_args()
    # Set defaults
    pwlen = int(opts.pwlen) if opts.pwlen else 10
    pwcount = int(opts.pwcount) if opts.pwcount else 1
    specialc = opts.specialc if opts.specialc else False

    for p in range(0, pwcount):
        pw = gen_pass(pwlen, specialc)
        print pw

    sys.exit(0)
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()

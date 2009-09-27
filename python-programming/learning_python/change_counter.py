#!/usr/bin/env python
# by Samuel Huckins

import sys

def change_counter():
    """
    This program provides a total of the change indicated.
    """
    print "Welcome to the change counter."
    quarters = raw_input("How many quarters? ")
    dimes = raw_input("How many dimes? ")
    nickels = raw_input("How many nickels? ")
    pennies = raw_input("How many pennies? ")
    print "Calculating total..."
    print ""
    total = (float(quarters) * .25) + (float(dimes) * .10) + (float(nickels) * .05) \
        + (float(pennies) * .01)
    print "The total is: $%0.02f" % total
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

if __name__ == '__main__':
    change_counter()

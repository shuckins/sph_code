#!/usr/bin/env python
import sys
    
def main():
    """
    Formulates and prints a username based on full name entered and a given
    pattern.
    """
    print "This will formulate your username."
    first = raw_input("What is your first name? ")
    last = raw_input("What is your last name? ")
    username = first[0] + last
    print "The username for", first, last, "is", "%s." % username.lower()
    if raw_input("Press RETURN to exit."):
        sys.exit(0)
    
if __name__ == '__main__':
    main()

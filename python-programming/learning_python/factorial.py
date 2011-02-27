#!/usr/bin/env python
# by Samuel Huckins

""" Calculates factorial of the number entered.
"""

def main():
    """
    Requests a number, returns its factorial.
    """
    num = int(raw_input("What is the number? "))
    fact = 1
    for factor in range(num, 1, -1):
        fact = fact * factor
    print "The factorial of %s is %s." % (num, fact)

if __name__ == '__main__':
    main()
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

#!/usr/bin/env python
import sys
    
def main():
    """
    Asks for a month number, prints the corresponding short month name.
    """
    months = "JanFebMarAprMayJunJulAugSepOctNovDec"
    sel = int(raw_input("What month's short name would you like? "))
    position = (sel - 1) * 3
    result = months[position:position + 3]
    print "The short name of month", sel, "is %s." % result
    if raw_input("Press RETURN to exit."):
        sys.exit(0)
    
if __name__ == '__main__':
    main()

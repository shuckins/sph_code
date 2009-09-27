#!/usr/bin/env python
    
def main():
    """
    Takes a short formatted date and outputs a longer format.
    """
    import sys
    import string
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December", ]
    short = raw_input("Please enter the date (mm/dd/yyyy): ")
    month_s, day_s, year_s = string.split(short, "/")
    month = int(month_s)
    month_l = months[month - 1]
    print "The date is: %s %s, %s." % (month_l, day_s, year_s)
    if raw_input("Press RETURN to exit."):
        sys.exit(0)
    
if __name__ == '__main__':
    main()

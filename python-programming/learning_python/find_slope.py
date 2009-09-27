#!/usr/bin/env python
# by Samuel Huckins

def find_slope(pos1, pos2):
    """
    Finds the slope of the line between two points specified.
    
    pos1 -- X and Y coordinates of first point.
    pos2 -- X and Y coordinates of second point.
    """
    try:
        slope = (pos2[1] - pos1[1]) / (pos2[0] - pos1[0])
        return slope
    except ZeroDivisionError:
        return False

def main():
    """
    Provides main program flow.
    """
    first_point = input("Coordinates of first point (x, y): ")
    second_point = input("Coordinates of second point (x, y): ")
    slope = find_slope(first_point, second_point)
    if slope is False:
        print "Sorry, vertical points don't have a slope!"
    else:
        print "The slope between %s and %s is %s." % (first_point, second_point, \
                slope)

if __name__ == '__main__':
    main()
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

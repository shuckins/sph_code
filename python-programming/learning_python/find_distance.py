#!/usr/bin/env python
# by Samuel Huckins

import math

def find_distance(point1, point2):
    """
    Find the distance between the points passed.
    
    point1 -- X and Y coordinates of the first point.
    point2 -- X and Y coordinates of the second point.
    """
    distance = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) **2)
    return distance

def main():
    """
    Provides main flow control.
    """
    point1 = input("Coordinates for point 1 (x, y): ")
    point2 = input("Coordinates for point 2 (x, y): ")
    dist = find_distance(point1, point2)
    print "The distance between %s and %s is %0.2f." % (point1, point2, dist)

if __name__ == '__main__':
    main()
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

#!/usr/bin/env python
# by Samuel Huckins

import math

def find_area_of_triangle(side1, side2, side3):
    """
    Finds the area of a triangle based on sides passed.
    
    side1 -- Length of side 1
    side2 -- Length of side 2
    side3 -- Length of side 3
    """
    s = (side1 + side2 + side3) / 2.0
    area = math.sqrt(s * (s - side1) * (s - side2) * (s - side3))
    return area

def main():
    """
    Provides main control flow.
    """
    import sys
    side1, side2, side3 = input("Length of sides: ")
    area = find_area_of_triangle(side1, side2, side3)
    print "The area of a triangle having sides of length %s, %s, and %s is %0.4f."\
        % (side1, side2, side3, area)
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

if __name__ == '__main__':
    main()

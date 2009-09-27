#!/usr/bin/env python
# by Samuel Huckins

import math

def area_of_circle(diameter):
    """ Calculates the value per unit area of a circle.
    """
    radius = diameter / 2
    area = 4 * math.pi * (radius * radius)
    return area

def main():
    """
    Controls main program flow.
    """
    diameter = input("What is the circle's diameter? ")
    cost = input("What is the circle's cost? ")
    area = area_of_circle(diameter)
    cost_area = cost / area
    print "The circle is worth", cost_area, "per unit area."
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

if __name__ == "__main__":
    main()

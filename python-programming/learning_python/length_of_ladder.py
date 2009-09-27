#!/usr/bin/env python
# by Samuel Huckins

import math

def find_ladder_length(angle, height):
    """
    Calculates the length of a ladder needed to reach a passed height at a
    passed angle.
    
    angle -- Angle at which ladder is inclined.
    height -- Height ladder must reach.
    """
    rad_angle = (math.pi / 180) * angle
    length = height / (math.sin(rad_angle))
    return length

def main():
    """
    Provides main control flow.
    """
    angle = input("At what angle (degrees) should the ladder be inclined? ")
    height = input("What height must the ladder reach? ")
    length = find_ladder_length(angle, height)
    print """For a ladder to reach %s, inclined at %s degress, it must be %s long""" % (height, angle, length)

if __name__ == '__main__':
    main()
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

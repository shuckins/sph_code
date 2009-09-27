#!/usr/bin/env python
# by Samuel Huckins

def main():
    """ Approximates pi through summing terms supplied, according to the Taylor
    series."""
    import sys
    import math
    # Number of terms to add:
    to_add = int(raw_input("How many terms to use? "))
    # For alternating the sign of terms in the seies:
    cur_sign = 1
    approx = 0.0
    # Iterating through the term selected, add the approximation to the current
    # sign multiplied by 4, dividing by the current iteration:
    for i in range(1, 2 * to_add, 2):
        approx = approx + cur_sign * 4.0 / i
        cur_sign = -cur_sign  
    print "Using %s terms resulted in the approximation: %s." % (to_add, approx)
    # Compare to module-provided value.
    inacc = abs((math.pi - approx) / math.pi) * 100
    print "The standard value is %s, an inaccuracy of %s%%." % \
        (math.pi, inacc)
    # Prompt to exit:
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

if __name__ == '__main__':
    main()

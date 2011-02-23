#!/usr/bin/env python
# by Samuel Huckins

def main():
    """
    Calculates and returns values of quadratic formula based on
    list of coefficients passed. If the resulting discriminant is
    negative, it returns the discrinimant, in order to show in the error.

    An example set of coefficients resulting in real roots: 1, 6, 7.

    An example set of coefficients resulting in double roots: 1, 2, 1.

    An example set of coefficients resulting in imaginary roots: 1, 2, 3.
    """
    import math
    import sys

    # Get the digits:
    vars = raw_input("Please enter values for a, b, c (comma-sep): ")
    var_list = vars.split(",")
    # In case they didn't listen:
    if len(var_list) != 3:
        print "You need to enter a comma-separated set of numbers (e.g. 1, 2, \
3)."
        sys.exit(-1)
    try:
        var_list = [float(v) for v in var_list]
    except ValueError, e:
        print "You need to enter a comma-separated set of numbers (e.g. 1, 2, \
3)."
        sys.exit(-1)

    discriminant = (var_list[1] * var_list[1]) - (4 * var_list[0] * var_list[2])
    print
    print "Coefficients:", vars
    print
    # Check for negative numbers:
    if discriminant < 0:
        print "The discriminant (%s) of those coefficients produces \
imaginary roots. Exiting." % discriminant
        sys.exit(0)
    # Otherwise solve:
    sr = math.sqrt(discriminant)
    x_1 = (-var_list[1] + sr) / (2 * var_list[0])
    x_2 = (-var_list[1] - sr) / (2 * var_list[0])
    solution = (x_1, x_2)
    # Warn if double root, as that's strange:
    if solution[0] == solution[1]:
        print "Double solution at", solution
        sys.exit(0)
    # Normal cases:
    answer = "Real solutions found: %s, %s" % (solution[0], solution[1])
    print answer
    print

if __name__ == '__main__':
    main()

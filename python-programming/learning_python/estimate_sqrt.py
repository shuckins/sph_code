#!/usr/bin/env python
# by Samuel Huckins
import math

def estimate_sqrt(num, iterations):
    """Attempts to guess the square root of num, using Newton's method.
    Continues guessing until iterations.
    """
    guess = num / 2.0
    for i in range(iterations):
        guess = (guess + (num / guess)) / 2
    return guess

def main():
    """
    Provides main control flow.
    """
    import sys
    num = int(raw_input("What is the number to guess its square root? "))
    iterations = int(raw_input("How many times should we improve our guess? "))
    guess = estimate_sqrt(num, iterations)
    print "Estimated square root for %s using %s iterations is %s." % (num, \
       iterations, guess)
    print "This is %s%% off from that supplied by math.sqrt()." % \
        ((math.sqrt(num) - guess) * 100)
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

if __name__ == '__main__':
    main()

#!/usr/bin/env python

import math

def main():
    """
    Asks for height and weight, returns BMI and meaning.
    """
    height = raw_input("What is your height (FEET INCHES)? ")
    height = int(height.split(" ")[0]) * 12 + int(height.split(" ")[1])
    weight = int(raw_input("What is your weight (lbs)? "))

    w_part = weight * 720
    h_part = math.sqrt(height)

    bmi = w_part / h_part

    print "Being %s inches tall and weighing %s pounds, your BMI is: %s" % \
        (height, weight, bmi)
    if bmi in range(19, 26):
        print "This is considered healthy."
    else:
        print "This is considered unhealthy."

main()

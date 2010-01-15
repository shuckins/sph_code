#!/usr/bin/env python

def main():
    sum = 0.0
    count = 0
    msg = "Enter a number (<Enter> to quit) >> "
    x = raw_input(msg)
    while x != "":
        x = eval(x)
        sum = sum + x
        count = count + 1
        x = raw_input(msg)
    print "\nThe average of the numbers is", sum / count
    
main()

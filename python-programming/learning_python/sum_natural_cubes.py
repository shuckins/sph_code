#!/usr/bin/env python
# by Samuel Huckins

def sum_natural_cubes(terminator):
    """
    Sums the first natural number cubes until number passed.
    
    terminator -- Number of natural number to count to.
    """
    sum = 0
    for i in range(0, terminator + 1):
        sum += i ** 3
    return sum

def main():
    """
    Provides main flow control.
    """
    terminator = input("Sum natural cubes to: ")
    sum = sum_natural_cubes(terminator)
    print "The sum of the natural cubes to %s is %s." % (terminator, sum)

if __name__ == '__main__':
    main()
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

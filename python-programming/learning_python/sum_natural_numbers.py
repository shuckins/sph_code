#!/usr/bin/env python
# by Samuel Huckins

def sum_natural_numbers(terminator):
    """
    Sums the first natural numbers until number passed.
    
    terminator -- Number of natural number to count to.
    """
    sum = 0
    for i in range(0, terminator + 1):
        sum += i
    return sum

def main():
    """
    Provides main flow control.
    """
    terminator = int(raw_input("Sum natural numbers to: "))
    sum = sum_natural_numbers(terminator)
    print "The sum of the natural numbers to %s is %s." % (terminator, sum)

if __name__ == '__main__':
    main()
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

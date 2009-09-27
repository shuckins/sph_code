#!/usr/bin/env python
# by Samuel Huckins

def average(numbers):
    """ Averages the numbers passed.
    """
    sum = 0.0
    for i in numbers:
        sum += i
    average = (sum / len(numbers))
    return average

def main():
    """
    Provides main control flow.
    """
    import sys
    to_add = int(raw_input("How many numbers will be averaged? "))
    numbers= []
    for i in range(1, (to_add + 1)):
        numbers.append(int(raw_input("Enter number #%s: " % i)))
    avg = average(numbers)
    print "The average of %s is %0.2f." % (numbers, avg)
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

if __name__ == '__main__':
    main()

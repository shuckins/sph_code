#!/usr/bin/env python
# by Samuel Huckins

def sum(numbers):
    """Sums the numbers passed.
    """
    sum = 0
    for i in numbers:
        sum += i
    return sum

def main():
    """
    Provides main control flow.
    """
    import sys
    to_add = int(raw_input("How many numbers will be summed? "))
    numbers= []
    for i in range(1, (to_add + 1)):
        numbers.append(int(raw_input("Enter number #%s: " % i)))
    total = sum(numbers)
    print "The sum of %s is %s." % (numbers, total)
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

if __name__ == '__main__':
    main()

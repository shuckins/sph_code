#!/usr/bin/env python
# by Samuel Huckins

def find_fibonacci(n):
    """ Calculate and display the Fibonacci sequence, beginning from 1 and
    proceeding to the number passed.
    """
    a = 1
    b = 1
    results = [a, b]
    for i in range(n):
        results.append(a + b)
        b, a = a + b, b
    return results

def main():
    """
    Provides main control flow.
    """
    import sys
    n = int(raw_input("To what term would you like the Fibonacci sequence to \
be shown? "))
    results = find_fibonacci(n)
    print "Fibonacci to %s: %s" % (n, results)
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

if __name__ == '__main__':
    main()

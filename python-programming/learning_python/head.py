#!/usr/bin/env python
# by Samuel Huckins 

def main():
    """
    Prints the first 10 lines of the file passed.
    """
    import sys
    fname = raw_input("What is the filename? ")
    f_open = open(fname)
    for i in range(10):
        l = f_open.readline()
        print l[:-1]
    f_open.close()
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

if __name__ == '__main__':
    main()

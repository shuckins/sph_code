#!/usr/bin/env python
# by Samuel Huckins

def main():
    """
    Print the plain text form of the ASCII codes passed.
    """
    import sys
    import string
    print "This program will compute the plain text equivalent of ASCII codes."
    ascii = raw_input("Enter the ASCII codes: ")
    print "Here is the plaintext version:"
    plain = ""
    for a in string.split(ascii):
        ascii_code = eval(a)
        plain = plain + chr(ascii_code)
    print ""
    print plain
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# by Samuel Huckins

def main():
    """
    Print the ASCII codes for the passed text.
    """
    import sys
    plain = raw_input("Please enter the plaintext string you want to encode: ")
    print "Here are the ASCII codes for that text, space-separated:"
    for e in plain:
        print ord(e),
    print
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

if __name__ == '__main__':
    main()

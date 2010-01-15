#!/usr/bin/env python

def main():
    file_name = raw_input("What file are the numbers in? ")
    in_file = open(file_name, 'r')
    sum = 0.0
    count = 0
    for line in in_file:
        sum = sum + eval(line)
        count = count + 1
    print "\nThe average of the numbers is", sum / count
    
if __name__ == '__main__':
    main()
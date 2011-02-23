#!/usr/bin/env python
#-----------------------------------------------------------------------------
"""This program finds the largest directory in current or passed 
directory, and does the same within that directory until it is in a 
directory with no directories. Allows for prompting to continue.
"""
author = "Samuel Huckins"
date_started = "2009-01-09"
#-----------------------------------------------------------------------------
# For making system calls
import os
# For getting params
import sys
# Option parsing
from optparse import OptionParser
# Dictionary sorting
from operator import itemgetter

def get_dir_size(dir):
    """ 
    Get the size of the directory passed.
    """
    dir_size = 0
    for (path, dirs, files) in os.walk(dir):
        for file in files:
            filename = os.path.join(path, file)
            if os.path.isfile(filename):
                try:
                    dir_size += os.path.getsize(filename)
                except OSError, e:
                    raise e
    return round((dir_size / (1024*1024.0)), 2)

def recursively_find_largest(target, prompt=False, level=1):
    """
    Looks in target for dirs, prints largest, prompting
    if passed.
    """
    dir_sizes = {}
    for eachitem in [os.path.join(target, x) for x in os.listdir(target)]:
        if os.path.isdir(eachitem):
            dir_sizes[eachitem] = get_dir_size(eachitem)
    if len(dir_sizes) == 0:
        return
    largest_dir = sorted(dir_sizes.iteritems(), key=itemgetter(1), \
        reverse=True)[0]
    separator = "-" * level
    print " |%s> %s: %s MB" % (separator, os.path.split(largest_dir[0])[1], largest_dir[1])
    level += 1
    if prompt == True:
        cont = raw_input("Continue? (y/n) ")
        if cont == "y":
            recursively_find_largest(largest_dir[0], prompt, level)
        else:
            return
    else:
        recursively_find_largest(largest_dir[0], prompt, level)

def main():
    """
    Control main program flow.
    """
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-t", "--target", dest="target_dir", help="The directory to start in")
    parser.add_option("-p", "--prompt", dest="prompt", action="store_true", \
        default=False, help="Prompt to continue in child dirs")    
    (options, args) = parser.parse_args()
    current_dir = os.getcwd()
    if options.target_dir:
        target = options.target_dir
    else:
        target = current_dir
    parent_size = get_dir_size(target)
    print "%s: %s MB (parent)" % (target, parent_size)
    recursively_find_largest(target, options.prompt)
    sys.exit(0)
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()

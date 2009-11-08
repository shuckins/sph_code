#!/usr/bin/env python

def mf(obj, term):
    """
    Searches through the methods defined for obj, looks for those containing the term passed.
    Returns all matches or a warning of none found.
    """
    meths = dir(obj)
    match_meths = []
    for meth in meths:
        if meth.rfind(term) != -1:
            match_meths.append(meth)
    if match_meths:
        print match_meths
    else:
        print "No matches!"

def minfo(item):
    """
    Print useful information about item.

    From http://www.ibm.com/developerworks/library/l-pyint.html
    """
    if hasattr(item, '__name__'):
        print "NAME:    ", item.__name__
    if hasattr(item, '__class__'):
        print "CLASS:   ", item.__class__.__name__
    print "ID:      ", id(item)
    print "TYPE:    ", type(item)
    print "VALUE:   ", repr(item)
    print "CALLABLE:",
    if callable(item):
        print "Yes"
    else:
        print "No"
    if hasattr(item, '__doc__'):
        doc = getattr(item, '__doc__')
    doc = doc.strip()   # Remove leading/trailing whitespace.
    firstline = doc.split('\n')[0]
    print "DOC:     ", firstline

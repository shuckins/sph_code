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

def obinfo(obj):
    """
    Print useful information about object.

    From http://www.ibm.com/developerworks/library/l-pyint.html
    """
    if hasattr(obj, '__name__'):
        print "NAME:    ", obj.__name__
    if hasattr(obj, '__class__'):
        print "CLASS:   ", obj.__class__.__name__
    print "ID:      ", id(obj)
    print "TYPE:    ", type(obj)
    print "VALUE:   ", repr(obj)
    print "CALLABLE:",
    if callable(obj):
        print "Yes"
    else:
        print "No"
    if hasattr(obj, '__doc__'):
        doc = getattr(obj, '__doc__')
        doc = doc.strip()
        topfive = doc.split('\n')[0:4]
        print "DOC:     ", "\n".join(topfive)
    else:
        print "No docstring. Yell at the author."

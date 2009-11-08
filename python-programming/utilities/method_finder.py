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

#!/usr/bin/env python
"""
Assorted utilities.
"""

def mf(obj, term):
    """
    Searches through the methods defined for obj, 
    looks for those containing the term passed. 
	Prints all matches or 'No matches' if none found.

    Initial version improved by Jason R. Coombs:
    https://svn.jaraco.com/jaraco/python/jaraco.util/jaraco/lang/python.py

    >>> mf(set, "diff")
    ['difference', 'difference_update', 'symmetric_difference', 'symmetric_difference_update']
    """
    methods = dir(obj)
    term = term.lower()
    result = [m for m in methods if term in m.lower()] or 'No matches'
    return result

def obinfo(obj):
    """
    Print useful information about object.

    From http://www.ibm.com/developerworks/library/l-pyint.html

    Initial version improved by Jason R. Coombs:
    https://svn.jaraco.com/jaraco/python/jaraco.util/jaraco/lang/python.py
    """
    if hasattr(obj, '__name__'):
        print "NAME:    ", obj.__name__
    if hasattr(obj, '__class__'):
        print "CLASS:   ", obj.__class__.__name__
    print("ID:      ", id(obj))
    print("TYPE:    ", type(obj))
    print("VALUE:   ", repr(obj))
    print("CALLABLE:", ['No', 'Yes'][callable(obj)])
    if hasattr(obj, '__doc__'):
        doc = getattr(obj, '__doc__')
        doc = doc.strip()
        topfive = doc.split('\n')[0:4]
        print "DOC:     ", "\n".join(topfive)
    else:
        print "No docstring. Yell at the author."

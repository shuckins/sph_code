#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Name:        function-timer
# Purpose:     Runs a function specified number of times, writes time to csv.
#              Taken from Bartosz Ptaszynski at http://yazzgoth.org/.
#
# Author:      Samuel Huckins
#
# Started:     12/20/2008
#-----------------------------------------------------------------------------
#
import timing
from datetime import datetime

def timeFunction(function):
    def wrapper(*args, **kw):
        timing.start()
        function(*args, **kw)
        timing.finish()
        f = open("timing.csv", "a")
        f.write("%s,%s,%d\n"%(datetime.now(), function.__name__, timing.micro())) 
        f.flush()
        f.close()
    return wrapper

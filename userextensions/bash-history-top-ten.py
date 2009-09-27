#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Name:        bash-history-top-ten
# Purpose:     Runs history command for user, finds top used commands, prints 
#              out with colors based on percentage.
#
# Author:      Samuel Huckins
#
# Started:     12/23/2008
#-----------------------------------------------------------------------------
#
from decimal import *
import commands
from operator import itemgetter

def readHistory():
    """
    Read in the running user's bash history. This will grab any preferences
    they have set in the profile, unlike reading the history file.
    """
    bash_history_contents = commands.getoutput('history')
    return bash_history_contents

def countAndSortHistory(history, number_desired):
    """
    Sort bash history passed, create count for each cmd, return this sorted.
    """
    import pdb; pdb.set_trace()
    history.sort()
    counted_cmds = {}
    for each_cmd in history:
        if counted_cmds.has_key(each_cmd):
            counted_cmds[each_cmd] += 1
        else:
            counted_cmds[each_cmd] = 1
    sorted_counted_cmds = sorted(counted_cmds.iteritems(), key=itemgetter(1))
    desired = sorted_counted_cmds[-number_desired:-1]
    return desired

def formatHistory(counted):
    """
    Put results into more readable form.
    """
    formatted = []
    for each_cmd in counted:
        formatted.append((each_cmd[0].replace("\n",""), each_cmd[1]))
    return formatted

def main():
    """
    Get everything moving.
    """
    cmds_to_show = 10
    history = readHistory()
    history_length = len(history)
    counted = countAndSortHistory(history, cmds_to_show)
    formatted = formatHistory(counted)
    print "Top ten most used commands (Count, Command, % of history):"
    for each_cmd in formatted:
        getcontext().prec = 4
        percent = Decimal(each_cmd[1]) / Decimal(history_length)
        print " * %s - %s - %s%%" % (each_cmd[1], each_cmd[0], percent)
    print "Total history: %s lines." % history_length


if __name__ == '__main__':
    main()

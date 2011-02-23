#!/usr/bin/env python
#-----------------------------------------------------------------------------
"""
This script accepts a file argument, assumed to be a log file in a particular 
format (for now, the one I use in logging). It then finds the difference 
between log steps, and prints the 10 log operations taking the most time by
default. A different number may also be passed as an option.

Examples:
    ./log_interval.py -h
        * Show help and options
    ./log_interval.py -f FILE
        * Show the top 10 (default) deltas in FILE
    ./log_interval.py -f FILE -n 15
        * Show the top 15 deltas in FILE
    ./log_interval.py -f FILE -N
        * Show all available deltas in FILE

This script is useful to determine where in a script's run you might want to 
try to optimize. It assumes the operations resulting in the log messages
occurred contiguously. Therefore it wouldn't be valuable in situations where the
logged operations have to wait for input, such as a user-interaction script, or
web server logs. So, YMMV, etc, this isn't a universal log parsing script!

Author: Samuel Huckins
Date started: 2009-03-31
"""
#-----------------------------------------------------------------------------
# For exiting:
import sys
# For datetime parsing:
from datetime import datetime
# For sorting dicts by value
from operator import itemgetter
# For parsing options passed:
from optparse import OptionParser
#-----------------------------------------------------------------------------
def parse_log(logfile):
    """Parses the logfile passed, returning a dictionary of line numbers and
    the datetime component of the line, as well as a dictionary of line numbers
    and the entire line.
    """
    log = open(logfile, 'r')
    # Make a list of dictionaries, each have the line number as the key, and
    # the value as the dictionary containing a dictionary of the datetime part 
    # as key and the message part as value. Phew.
    nums_and_lines = []
    line = 1
    for x in log.readlines():
        # The temp dict to hold the line number and the log line:
        num_and_line = {}
        # The temp dict to hold the datetime part and the message part:
        time_events = {}
        # Split the log line, pulling out datetime part and message part:
        x1 = '-'.join(x.split('-')[0:3]).strip()
        x2 = '-'.join(x.split('-')[3:]).strip()
        time_events[x1] = x2
        num_and_line[line] = time_events
        line += 1
        nums_and_lines.append(num_and_line)
    log.close()
    # Pull out all the times, with line numbers since there might be dupes:
    nums_and_times = {}
    for pair in nums_and_lines:
        for dt in pair.values()[0].keys():
            for i in pair.keys(): 
                nums_and_times[i] = dt
    return nums_and_times, nums_and_lines

def get_time_delta(time1, time2):
    """Given two datetimes as strings, return the diff between them.
    """
    # Turn time1 into a datetime obj:
    date_part1, time_part1 = time1.split(' ')
    year1, month1, day1 = date_part1.split('-')
    year1, month1, day1 = int(year1), int(month1), int(day1)
    hms_part1, ms1 = time_part1.split(',')
    ms1 = int(ms1)
    hour1, min1, sec1 = hms_part1.split(':')
    hour1, min1, sec1 = int(hour1), int(min1), int(sec1)
    micro1 = ms1 * 1000
    dt1 = datetime(year1, month1, day1, hour1, min1, sec1, micro1)
    # Turn time2 into a datetime obj:
    date_part2, time_part2 = time2.split(' ')
    year2, month2, day2 = date_part2.split('-')
    year2, month2, day2 = int(year2), int(month2), int(day2)
    hms_part2, ms2 = time_part2.split(',')
    ms2 = int(ms2)
    hour2, min2, sec2 = hms_part2.split(':')
    hour2, min2, sec2 = int(hour2), int(min2), int(sec2)
    micro2 = ms2 * 1000
    dt2 = datetime(year2, month2, day2, hour2, min2, sec2, micro2)
    # Find the diff
    delta = dt2 - dt1
    return delta

def parse_times(nums_and_times):
    """Given a dictionary of line numbers and datetime parts, returns a
    dictionary of the line numbers and the deltas between that line and the
    previous.
    """
    # Make sure we are going in order of the lines in the file:
    line_numbers = nums_and_times.keys()
    line_numbers.sort()
    # Line numbers and the delta between their line's time and that of the 
    # previous:
    nums_and_deltas = {}
    # Find diffs between all consecutive pairs of datetimes:
    for li in line_numbers:
        if li == line_numbers[-1]:
            pass
        else:
            time1 = nums_and_times[li]
            time2 = nums_and_times[li + 1]
            delta = get_time_delta(time1, time2)
            nums_and_deltas[li] = delta
    # Return the top number requested:
    return nums_and_deltas

def get_longest_events(nums_and_deltas, events=0, all=False):
    """Given a dictionary of line numbers and timedelta objects of that line and
    the previous, rank them and return the top_events number requested as a
    list of dictionaries, each being the rank corresponding to a dict of the
    line number to the timedelta.
    """
    sorted_by_delta = sorted(nums_and_deltas.items(), key=itemgetter(1), 
        reverse=True)
    ranks_nums_deltas = []
    rank = 1
    if all:
        print "Printing all %s deltas..." % len(sorted_by_delta)
        for e in sorted_by_delta:
            num_delta = {}
            rank_num_delta = {}
            num_delta[e[0]] = e[1]
            rank_num_delta[rank] = num_delta
            ranks_nums_deltas.append(rank_num_delta)
            rank += 1
    else:
        if events > len(sorted_by_delta):
            print "Can only print %s deltas instead of %s requested..." % \
                (len(sorted_by_delta), events)
            for e in sorted_by_delta:
                num_delta = {}
                rank_num_delta = {}
                num_delta[e[0]] = e[1]
                rank_num_delta[rank] = num_delta
                ranks_nums_deltas.append(rank_num_delta)
                rank += 1
        else:
            count = 1
            for e in sorted_by_delta:
                if count > events:
                    return ranks_nums_deltas
                else:
                    num_delta = {}
                    rank_num_delta = {}
                    num_delta[e[0]] = e[1]
                    rank_num_delta[rank] = num_delta
                    ranks_nums_deltas.append(rank_num_delta)
                    rank += 1
                    count += 1
    return ranks_nums_deltas

def print_events(ranks_nums_deltas, nums_and_lines):
    """Given a dictionary of the ranking of longest to a dictionary of 
    line numbers and the timedelta of the longest events, as well as a dictionary 
    of the line numbers and the line contents, print out the longest messages.
    """
    results = []
    for x in ranks_nums_deltas:
        # Pull out the ranking:
        rank = x.keys()[0]
        # Keep track of the longest rank for printing:
        cur_rank_len = len(str(rank))
        try:
            longest_rank
        except NameError:
            longest_rank = cur_rank_len
        if longest_rank < cur_rank_len:
            longest_rank = cur_rank_len
        # Pull out the line number:
        linenum = x[rank].keys()[0]
        # Keep track of the longest linenum for printing:
        cur_linenum_len = len(str(linenum))
        try:
            longest_linenum
        except NameError:
            longest_linenum = cur_linenum_len
        if longest_linenum < cur_linenum_len:
            longest_linenum = cur_linenum_len
        # Dictionary of the line number and the line contents:
        for foo in nums_and_lines:
            if foo.keys()[0] == linenum:                
                line_parts = foo
        # Split that dict into the line number and the contents:
        line = line_parts.values()[0].keys()[0] + ' - ' + line_parts.values()[0].values()[0]
        # Keep track of the longest line for printing:
        cur_line_len = len(str(line))
        try:
            longest_line
        except NameError:
            longest_line = cur_line_len
        if longest_line < cur_line_len:
            longest_line = cur_line_len
        # Pull out the time delta:
        delta = x[rank].values()[0]
        # Split it up for conversion:
        days, seconds, microseconds = delta.days, delta.seconds, delta.microseconds
        # Convert to more useful units:
        minutes = seconds / 60
        seconds = seconds % 60
        hours = minutes / 60
        minutes = minutes % 60
        milliseconds = microseconds / 1000
        microseconds = microseconds % 1000
        # Build up a list of non-zero time units:
        pretty_delta = []
        if days > 0:
            pretty_delta.append("%sd" % days)
        if hours > 0:
            pretty_delta.append("%sh" % hours)
        if minutes > 0:
            pretty_delta.append("%sm" % minutes)
        if seconds > 0:
            pretty_delta.append("%ss" % seconds)
        if milliseconds > 0:
            pretty_delta.append("%sms" % milliseconds)
        if microseconds > 0:
            pretty_delta.append("%smu" % microseconds)
        # Join the list together into a string for printing:
        pretty_delta = ', '.join(pretty_delta)
        # Keep track of the longest pretty_delta for printing:
        cur_pretty_delta_len = len(str(pretty_delta))
        try:
            longest_pretty_delta
        except NameError:
            longest_pretty_delta = cur_pretty_delta_len
        if longest_pretty_delta < cur_pretty_delta_len:
            longest_pretty_delta = cur_pretty_delta_len
    # Store the rank, delta and the line itself:
        results.append((rank, pretty_delta, linenum, line))

    # Print header info:
    header = 'The longest %s events (rank, delta, line number, message):' % len(ranks_nums_deltas)
    print header
    max_line_length = (longest_rank + longest_pretty_delta +
                       longest_linenum + longest_line) + 14
    print '-' * max_line_length
    # Check the length of each column against their max, pad with spaces as
    # needed:
    for res in results:
        # Rank column:
        rank = res[0]
        rank_pad = longest_rank - len(str(rank))
        rank = str(rank) + (' ' * rank_pad)
        # Delta column:
        delta = res[1]
        delta_len = len(str(delta))
        if delta_len == 0:
            delta = 'None detectable' 
            delta_pad = longest_pretty_delta - len(delta)
            delta = '(' + delta + '): ' + (' ' * delta_pad)
        else:
            delta_pad = longest_pretty_delta - delta_len
            delta = '(' + str(delta) + '): ' + (' ' * delta_pad)
        # Line number column:
        num = res[2]
        num_pad = longest_linenum - len(str(num))
        num = str(num) + (' ' * num_pad)
        # Message column:
        msg = res[3]
        msg_pad = longest_line - len(str(msg))
        msg = str(msg) + (' ' * msg_pad)
        # Print it!
        print '#%s - %s %s | %s |' % (rank, delta, num, msg)
    print '-' * max_line_length

def process_args():
    """Process options passed at the command line. Return arguments and
    options.
    """
    usage = __doc__
    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--file", action="store", dest="log_file",
        help="filename of the log to parse")
    parser.add_option("-n", "--num-events", action="store", dest="log_events",
        default=10, type="int",         
        help="the number of log events to show, starting with the longest")
    parser.add_option("-N", "--all-events", action="store_true", dest="show_all",
        help="show all available deltas and events", default=False)
    return parser.parse_args()

#-----------------------------------------------------------------------------
def main():
    """Provides main flow control.
    """
    # Parsing options passed:
    (opts, args) = process_args()
    if not opts.log_file:
        print 'You must enter a log file to parse.'
        sys.exit(-1)
    # Parse the log:
    nums_and_times, nums_and_lines =  parse_log(opts.log_file)
    # Parse the times, get line numbers and deltas:
    nums_and_deltas = parse_times(nums_and_times)
    # Rank the deltas, return request number:
    if opts.show_all:
        ranks_nums_deltas = get_longest_events(nums_and_deltas, 
            all=opts.show_all)
    else:
        ranks_nums_deltas = get_longest_events(nums_and_deltas, 
            events=opts.log_events)
    # Print results:
    print_events(ranks_nums_deltas, nums_and_lines)
    # Done:
    sys.exit(0)
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()

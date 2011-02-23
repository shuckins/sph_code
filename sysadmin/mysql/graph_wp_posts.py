#!/usr/bin/env python
try:
    from pylab import *
except:
    graphing = False
import pprint
import datetime

# Read in the file of titles and dates:
f = open('posts.csv')
flines = []
for line in f: flines.append(line.split('\t'))
# Create dict of year-month and counts therein:
date_counts = {}
for line in flines:
    if date_counts.has_key(line[0][0:7]):
        date_counts[line[0][0:7]] += 1
    else:
        date_counts[line[0][0:7]] = 1
# Make a list of the counts, dates and sort them:
counts = date_counts.items()
counts.sort()
# Turn the partial date strings into date objects for graphing:
dates = [key for key, value in counts]
dated_days = []
for day in dates:
    year = int(day[0:4])
    month = int(day[5:7])
    day = 1
    date = datetime.date(year, month, day)
    dated_days.append(date)
counts = [ value for key, value in counts]
# Set labels
x = xlabel('Date')
setp(x, fontweight='bold')
y = ylabel('Posts')
setp(y, fontweight='bold')
# Subplot to handle date positioning
ax = subplot(111)
labels = ax.get_xticklabels()
setp(labels, fontweight='bold', rotation=30, fontsize=10)
# Plot as dates 
plotted = plot(dated_days, counts, '--')
setp(plotted, marker='s')
title('Posts over time')
grid(True)
savefig('results.png', dpi=100)

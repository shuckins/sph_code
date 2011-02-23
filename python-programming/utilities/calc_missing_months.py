#!/usr/bin/env python
"""
Example script to find the months between two dates and calculate dates for
these. Works across years. Assumes dates will be given in ascending order.
"""
import datetime

# Example dates
dt = datetime.date(2006, 7, 22)
dt2 = datetime.date(2009, 9, 20)

# Find diffs
diff_month = dt2.month - dt.month
diff_year = 0
if dt.year != dt2.year:
    diff_month += 12 * (dt2.year - dt.year)
    diff_year = dt2.year - dt.year

# Form list of new months
new_months = []
# Day can be constant across all, we just care about month and year:
day = 1
# Year and month set to global so we can increment them conditionally from
# within the loop:
global year 
year = dt.year
global month 
month = dt.month
for m in range(1, diff_month):
    month += 1
    if month > 12:
        year += 1
        month = 1
    new_months.append(datetime.date(year, month, day))

# Print first date, added dates, and end date
print dt
for m in new_months:
    print m
print dt2

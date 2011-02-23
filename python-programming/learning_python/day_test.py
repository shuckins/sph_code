#!/usr/bin/env python
# by Samuel Huckins

def test_for_day(target_day):
    """
    This accepts a weekday and tests if today is that weekday.
    """
    import time
    # Get the date object of today's date:
    todays_date = time.localtime().tm_wday
    # Form a dictionary of the days of the week, starting on Monday
    # since this is the time module's assumption:
    date_dict = dict(enumerate('Monday Tuesday Wednesday Thursday Friday Saturday Sunday'.split()))
    # Find the weekday of today's date and compare to target:
    if date_dict[todays_date] == target_day:
        print "Today is the target (%s)." % target_day
    else:
        print "Today is %s, not %s." % (date_dict[todays_date], target_day)

if __name__ == "__main__":
    tarday = raw_input("What is the target day? ")
    test_for_day(tarday)
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

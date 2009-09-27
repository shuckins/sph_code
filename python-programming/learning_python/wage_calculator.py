#!/usr/bin/env python
from decimal import Decimal

def main():
    """
    Asks for hours worked and normal rate. Assumes normal working period is 40
    hours and that overtime rate is 1.5 times normal rate.
    """
    hours = int(raw_input("How many hours did you work last week? "))
    wage = Decimal(raw_input("What is your normal wage per hour? "))
    ot_wage = wage * Decimal("1.5")
    normal = 40
    if hours > normal:
        n_hours = normal
        o_hours = hours - normal
    elif hours == normal:
        n_hours = normal
        o_hours = 0
    else: # hours < normal
        n_hours = normal - hours
        o_hours = 0
    earnings = (n_hours * wage) + (o_hours * ot_wage)
    print
    print "Working %s normal hours and %s overtime hours, you earned: $%.2f." % \
        (n_hours, o_hours, earnings)

main()

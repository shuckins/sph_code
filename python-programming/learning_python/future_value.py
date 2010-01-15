#!/usr/bin/env python

def calc_values(principal, apr, years):
    """
    Given initial investment, annual interest rate and years to invest,
    calculates the change in principal per year.
    """
    values = {0:principal}
    for year in range(1, years + 1):
        principal = principal * (1 + apr)
        values[year] = principal
    return values

def graph_values(values):
    """
    """
    pass

def main():
    principal = 2000
    apr = float(.1)
    values = calc_values(principal, apr, 10)
    print values
    graph_values(values)

#------------------------------------------------------------------------------

if __name__ == '__main__':
    main()

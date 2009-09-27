#!/usr/bin/env python

def main():
    """
    Gets a score, returns a grade.
    """
    score = int(raw_input("What is your score? "))
    d_range = range(60, 70)
    c_range = range(70, 80)
    b_range = range(80, 90)

    if score < 60:
        grade = "F"
    elif score in d_range:
        grade = "D"
    elif score in c_range:
        grade = "C"
    elif score in b_range:
        grade = "B"
    else:
        grade = "A"
    
    print
    print "Your %s earns you a %s." % (score, grade)

main()

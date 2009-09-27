#!/usr/bin/env python

class Testerama(object):

    def __init__(self):
        pass
    def foo(self):
        print "in foo"
        quack = InnerTesterama()
        try:
            quack.baz()
        except ValueError, e:
            print "baz error:", e
        1/0

class InnerTesterama(object):

    def __init__(self):
        pass
    def baz(self):
        print "in baz"
        int("ssss")

def main():
    print "in main"
    bar = Testerama()
    try:
        print "in outer try"
        bar.foo()
    except ZeroDivisionError, e:
        print "in outer except"
        print "Outside:\n", e

main()

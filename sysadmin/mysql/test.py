#!/usr/bin/env python
import time

def list_times(method, run_times):
    df = "/usr/share/dict/words"
    dfile = open(df)
    times = []
    for i in range(run_times):
        if method == 1:
            start = time.time()
            result = ''.join([s for s in dfile])
            duration = time.time() - start
            times.append(duration)
        if method == 2:
            start = time.time()
            result = []
            for s in dfile:
                result.append(s)
            duration = time.time() - start
            times.append(duration)
    dfile.close()
    print "Method %s times: %s" % (method, times)
    print "Average: ", times /  len(times)

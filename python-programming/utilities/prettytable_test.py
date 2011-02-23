#!/usr/bin/env python
import PrettyTable

foo = PrettyTable.PrettyTable()
foo.set_field_names(["Num", "Sum", "Double", "Triple"])
sum = 0
for n in range(1, 6):
    sum += n
    dub = n * 2
    tri = n * 3
    foo.add_row([n, sum, dub, tri])
foo.printt()

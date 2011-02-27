#!/usr/bin/env python
""" NOT DONE OR GOOD YET
This will eventually be a utility script to find all unique HTML entities in a
text file and print them out, optionally along with common name, etc.
"""

import re

file = "char_entity_posts.csv"
pat = re.compile('&#..;')
uniq_matches = set()
#------------------------------------------------------------------------------
print "Starting...\n"

text = open(file)
for line in text:
    if pat.match(line):
        matches = pat.findall(line)
        for m in matches:
            if m == "&#58;":
                import pdb; pdb.set_trace()
            #uniq_matches.add(m)

print "\nDone"
import pdb; pdb.set_trace()

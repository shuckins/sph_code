#!/usr/bin/env python
# by Samuel Huckins

def hydrocarbon_weight(hydrogen, carbon, oxygen):
    """
    Calculates the weight of a hydrocarbon atom containing
    the passed number of atoms present per type.
    
    hydrogen -- Number of hydrogen atoms.
    carbon -- Number of carbon atoms.
    oxygen -- Number of oxygen atoms.
    """
    h_weight = 1.0079 * hydrogen
    c_weight = 12.011 * carbon
    o_weight = 15.9994 * oxygen
    mol_weight = h_weight + c_weight + o_weight
    return mol_weight

def main():
    """
    Controls main program flow.
    """
    h = int(raw_input("What is the number of hydrogen atoms? "))
    c = int(raw_input("What is the number of carbon atoms? "))
    o = int(raw_input("What is the number of oxygen atoms? "))
    mol_weight = hydrocarbon_weight(h, c, o)
    print "The hydrocarbon containing %s hydrogen atoms, %s carbon atoms, and \
%s oxygen atoms has a molecular weight of %s." % (h, c, o, mol_weight)            

if __name__ == '__main__':
    main()
    if raw_input("Press RETURN to exit."):
        sys.exit(0)

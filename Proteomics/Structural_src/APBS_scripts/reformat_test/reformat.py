import os, sys, re


def reformat():
    rootdir = os.getcwd()
    files = os.listdir(rootdir)
    f_list = []
    potential = open('potential.txt', 'w')
    potential_id = open('potential_id', 'w')

    for f in files:
        if '.dx' in f:
            f_list.append(f)

    for fn in f_list:
        name = fn.split('.', 1);
        name = name[0]
        pot_list = []
        f_file = open(fn).readlines()
        for pl in f_file:
            mObj = re.match('([e\d\.\+\-]+)\s+([e\d\.\+\-]+)\s+([e\d\.\+\-]+)\s+', pl)
            if mObj:
                pot_list.append(mObj.group(1))
                pot_list.append(mObj.group(2))
                pot_list.append(mObj.group(3))

        potential_id.write("%s\n" % name)
        print 'The number of points for %s is: %s' % (fn, len(pot_list))
        for i in pot_list:
            potential.write("%s " % i)
        potential.write("\n")


if __name__ == '__main__':
    if len(sys.argv) != 1:
        print "\nPlease give the correct multipdb filename. Example: \n> python cut_pdb.py multipdb \n"
    reformat()

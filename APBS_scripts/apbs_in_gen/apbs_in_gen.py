import os, sys, re

# Description: this script take in input all the file.pqr files present in the directory and create the files file.in
# that are input for APBS. The parameters have to be set in here (directly in the fout.write function).  


def file_gen():
    rootdir = os.getcwd()
    files = os.listdir(rootdir)
    f_list = []

    for f in files:
        if '.pqr' in f:
            f_list.append(f)

    for fn in f_list:
        name = fn.split('.', 1);
        name = name[0]
        in_name = '%s.in' % name
        fout = open(in_name, 'w')

        fout.write( \
            'read\n' \
            '  mol pqr %s/%s\nend\n' \
            'elec\n' \
            '  mg-auto\n' \
            '  dime 65 65 65\n' \
            '  cglen 40 40 40\n' \
            '  cgcent 36.596 82.612 56.883\n' \
            '  fglen 40 40 40\n' \
            '  fgcent 36.596 82.612 56.883\n' \
            '  mol 1\n' \
            '  lpbe\n' \
            '  bcfl sdh\n' \
            '  srfm smol\n' \
            '  chgm spl2\n' \
            '  ion 1 0.150 2.0\n' \
            '  ion -1 0.150 2.0\n' \
            '  pdie  1.0\n' \
            '  sdie  78.54\n' \
            '  sdens  10.0\n' \
            '  srad  1.4\n' \
            '  swin  0.3\n' \
            '  temp  298.15\n' \
            '  gamma  0.105\n' \
            '  calcenergy no\n' \
            '  calcforce no\n' \
            '  write pot dx %s\n' \
            'end\n' \
            'quit' \
            % (rootdir, fn, name))


if __name__ == '__main__':
    if len(sys.argv) != 1:
        print "\nPlease give the correct multipdb filename. Example: \n> python cut_pdb.py multipdb \n"
    file_gen()


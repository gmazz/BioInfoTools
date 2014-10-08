import os, sys, re
# Script to reformat all the pdb within the giving directory taking ONLY the ATOM field, and renumbering atoms and residues.
# Note: the PDB format is very old and totally un-optimized for parsing. This piece of code makes PDB refactoring easier.


rootdir = os.getcwd()
lst_files = os.listdir(rootdir)
list_pdb = []

def iterate():

    for f in lst_files:
        if '.pdb' in f:
            list_pdb.append(f)

    for pdb in list_pdb:
        reformat(pdb)

def field_3_check(f3):

    checker = False

    try:
        gotit = int(f3[0])
        checker = True
    except:
        pass

    return checker

def reformat(pdb):

    atom_c = 0
    res_c = 0
    tmp_res = ''

    ID = pdb.split('.pdb')[0]
    ID_out = '%s_rf.pdb' % ID
    file_handle = open(pdb, 'r')
    file_out = open(ID_out, 'w+')

    pdb_lines = file_handle.readlines()
    for pdb_line in pdb_lines:
        test = re.compile("(^ATOM)[\s]+([\d]+)[\s]+([\d\w]+)[\s]+([\w]+)[\s]+([\w]+)[\s]+([\d]+)[\s]+([\d\.]+)[\s]+([\d\.]+)[\s]+([\d\.]+)")
        yes = test.match(pdb_line)
        if yes:
            atom_c += 1
            if yes.group(3) == 'N':
                res_c += 1

            dynamic_spaces = "  "
            f3 = list(yes.group(3))
            checker = field_3_check(f3)
            if checker == True:
                dynamic_spaces = " "

            line_out = "%s%s%s%s%s%s%s%s%s%s\n" %(str(yes.group(1)), \
                                                    str(atom_c).rjust(7), \
                                                    dynamic_spaces, \
                                                    str(yes.group(3)).ljust(3), \
                                                    str(yes.group(4)).rjust(4), \
                                                    str(yes.group(5)).rjust(2), \
                                                    str(res_c).rjust(4), \
                                                    str(yes.group(7)).rjust(12), \
                                                    str(yes.group(8)).rjust(8), \
                                                    str(yes.group(9)).rjust(8))

            #print yes.groups()
            #print line_out

            file_out.write(line_out)
    file_out.write('END')

iterate()

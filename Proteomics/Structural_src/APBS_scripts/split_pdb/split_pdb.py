import os, sys, re, urllib
from Bio import SeqIO


def reader(multi_pdb_name):
    rootdir = os.getcwd()
    files = os.listdir(rootdir)
    split_pos_list = [0]
    file_name_list = []
    if multi_pdb_name in files:
        multipdb_tmp = open(multi_pdb_name).readlines()
        multipdb = [f.replace('\n', '') for f in multipdb_tmp]
        for pidx, pval in enumerate(multipdb):
            if 'SPDBVn' in pval:
                tag, ID = pval.split('    ')
                ID = ID.split('.B99990001')[0]
                file_name_list.append(ID)
                split_pos_list.append(pidx)
    else:
        print "Your multipdb file is not present!"
    return multipdb, split_pos_list, file_name_list


def split(multipdb, spl, fnl):
    for i in range(0, len(spl) - 1):
        tmp_file = multipdb[spl[i]:spl[i + 1]]
        filename = "%s.pdb" % (fnl[i])
        # print filename
        #print i,  spl[i], spl[i+1]
        target = open(filename, 'a')
        for j in tmp_file:
            target.write(j)
        target.write('END')
        target.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "\nPlease give the correct multipdb filename. Example: \n> python cut_pdb.py multipdb \n"
    multi_pdb_name = (sys.argv[1])

    multipdb, split_pos_list, file_name_list = reader(multi_pdb_name)
    split(multipdb, split_pos_list, file_name_list)
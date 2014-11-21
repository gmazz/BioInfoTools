import os, shutil, sys
from Bio import Entrez
from Bio import SeqIO

# Read two accession number lists and compare them
def read():

    hasp = open('HASP_list.txt', 'r')
    my = open('1203_model_list.txt', 'r')

    hasp_read = hasp.readlines()
    my_read = my.readlines()

    hasp_list = []
    my_list = []
    overlap = []
    not_included = []

    [hasp_list.append(i.split('\n')[0]) for i in hasp_read]
    [my_list.append(i.split('\n')[0]) for i in my_read]
    [overlap.append(i) for i in my_list if i in hasp_list]
    [not_included.append(i) for i in my_list if i not in hasp_list]

    #print 'HASP:\t%s' %len(hasp_list)
    print 'overlap:\t%s' %len(overlap)
    print 'not_included:\t%s' %len(not_included)
    print 'tot:\t%s' %(len(overlap) + len(not_included))
    #print '\n'.join(str(p) for p in included)

    return (hasp_list, my_list, overlap)

# To copy the elements of a list in the .overlap dir
def copy(my_list):
    root = os.getcwd()
    print root
    for filename in os.listdir('./HASP_structures'):
        fn_id = filename.split('_')[0]
        if fn_id in my_list:
            shutil.copy2('%s/HASP_structures/%s' % (root, filename), '%s/overlap/' % root)


# Gets GI from a given list of Genebank access IDs (AC)
def get_gi(accs):


    db = "nuccore"
    Entrez.email = "g.mazzocco@icm.edu.pl"
    file_out = open('hasplist_ac_gi.txt', 'w+')

    for i, acc in enumerate(accs):
        try:
            handle = Entrez.efetch(db=db, rettype="gb", id=acc)
            for record in SeqIO.parse(handle, "genbank"):
                gi = record.annotations['gi']
                file_out.write("%s\t%s\n" %(acc, gi))
        except:
            sys.stderr.write("Error! Cannot fetch: %s\n" % acc)


hasp_list, my_list, overlap = read()

# Write the AC and GI in external files
get_gi(hasp_list)
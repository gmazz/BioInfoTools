from prody import *
import numpy as np
from matplotlib.pylab import *
import operator
import sys, os


def protein_analysis(protein, protein_id):
    try:
        ubi = parsePDB(protein)
        calphas = ubi.select('calpha and chain A')
        gnm = GNM('model')
        gnm.buildKirchhoff(calphas, cutoff=10., gamma=1.)
        gnm.calcModes()
        mat_cov = gnm.getCovariance()
        diag_mat_cov = np.diag(mat_cov)
        c = 1
        dict_mobility = {}
        for i in diag_mat_cov:
            dict_mobility[c] = i
            #print ("%s\t%s\n" %(c, i))
            c = c+1
        #dict_mobility_sorted = dict_sorting(dict_mobility) #Function needed just to test
        return dict_mobility

    except:
        print "Problems with %s" %(protein)


def dict_sorting(dict):
    sorted_by_key = sorted(dict.items(), key=operator.itemgetter(0))
    sorted_by_val = sorted(dict.items(), key=operator.itemgetter(1))
    return sorted_by_val


def main(prot_list, str_path):
    mob_file = open('mob.csv', 'w+')
    stderr = open('stderr.txt', 'w+')
    for protein_id in prot_list:
        protein_path = '%s/%s' %(str_path, protein_id)
        dict_mobility = protein_analysis(protein_path, protein_id)
        if dict_mobility:
            mob_str_list = [str(i) for i in dict_mobility.values()]
            mob_file.write(("%s,%s\n") %(protein_id, ",".join(mob_str_list)))
        else:
            stderr.write("Problems with %s\n" %(protein_id))

def list_reader(pdb_path):
    prot_list = []
    for file in os.listdir(pdb_path):
        if file.endswith(".pdb"):
            prot_list.append(file)
    return prot_list


if __name__ == "__main__":
    data_path = sys.argv[1] # Please give the path to the PDBs
    prot_list = list_reader(data_path)
    main(prot_list, data_path)

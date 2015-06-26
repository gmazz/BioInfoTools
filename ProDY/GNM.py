from prody import *
import numpy as np
from matplotlib.pylab import *
import operator


def protein_analysis(protein):
    ubi = parsePDB(protein)
    calphas = ubi.select('calpha and chain A')
    gnm = GNM('protein_name')
    gnm.buildKirchhoff(calphas, cutoff=10., gamma=1.)
    gnm.calcModes()
    print(dir(gnm))
    mat_cov = gnm.getCovariance()
    diag_mat_cov = np.diag(mat_cov)
    c = 1
    dict_mobility = {}
    for i in diag_mat_cov:
        dict_mobility[c] = i
        #print ("%s\t%s\n" %(c, i))
        c = c+1
    dict_mobility_sorted = dict_sorting(dict_mobility)
    return dict_mobility


def dict_sorting(dict):
    sorted_by_key = sorted(dict.items(), key=operator.itemgetter(0))
    sorted_by_val = sorted(dict.items(), key=operator.itemgetter(1))
    return sorted_by_val

def main(prot_list):
    for protein in prot_list:
        dict_mobility = protein_analysis(protein)
        mob_string = ','.join(map(str, dict_mobility.values()))
        print ("%s,%s\n") %(protein, mob_string)

#prot_list = ['4bgx.pdb']

main(prot_list)


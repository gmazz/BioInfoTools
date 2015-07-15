from prody import *
import numpy as np
from matplotlib.pylab import *
import operator
import sys, os


def protein_analysis(protein):
    ubi = parsePDB(protein)
    print ubi
    calphas = ubi.select('calpha and chain A')
    gnm = GNM('protein_name')
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
    dict_mobility_sorted = dict_sorting(dict_mobility) #Function needed just to test
    return dict_mobility


def dict_sorting(dict):
    sorted_by_key = sorted(dict.items(), key=operator.itemgetter(0))
    sorted_by_val = sorted(dict.items(), key=operator.itemgetter(1))
    return sorted_by_val

def main(prot_list, str_path):
    for protein in prot_list:
        protein_path = '%s/%s' %(str_path, protein)
        dict_mobility = protein_analysis(protein_path)
        mob_string = ','.join(map(str, dict_mobility.values()))
        print ("%s,%s\n") %(protein, dict_mobility.keys())

def list_reader(pdb_path):
    prot_list = []
    for file in os.listdir(pdb_path):
        if file.endswith(".pdb"):
            prot_list.append(file)
    return prot_list

#str_path = "/Users/johnny/github_home/BioInfoTools/ProDY/data" #here insert the path where the pdb are located.
pdbs_path = "/Users/johnny/Desktop/CeNT/HA/PDB_models_crystals/crystals_chain_A"
#models_path = "/Users/johnny/Desktop/CeNT/HA/PDB_models_crystals/models"

prot_list = list_reader(pdbs_path)
main(prot_list, pdbs_path)


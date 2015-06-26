from prody import *
import numpy as np
from matplotlib.pylab import *


def protein_analysis(protein):
    ubi = parsePDB(protein)
    calphas = ubi.select('calpha and chain A')
    gnm = GNM('protein_name')
    gnm.buildKirchhoff(calphas, cutoff=10., gamma=1.)
    gnm.calcModes()
    print(dir(gnm))
    mat_cov = gnm.getCovariance()
    diag_mat_cov = np.diag(mat_cov)
    print (diag_mat_cov)
    #print (gnm.getVariances)
    #kirch_mat = gnm.getKirchhoff()
    #kirch_mat_inv = np.linalg.inv(kirch_mat)
    #kirch_diag_inv = np.diag(kirch_mat_inv)

def main(prot_list):
    for protein in prot_list:
        protein_analysis(protein)

#prot_list = ['1aar', '1p38']
prot_list = ['./4bgx.pdb']

main(prot_list)


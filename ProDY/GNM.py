from prody import *
from matplotlib.pylab import *


def protein_analysis(protein):
    ubi = parsePDB(protein)
    calphas = ubi.select('calpha and chain A')
    gnm = GNM('protein_name')
    gnm.buildKirchhoff(calphas)
    print(dir(gnm.getKirchhoff()))

def main(prot_list):
    for protein in prot_list:
        protein_analysis(protein)

prot_list = ['1aar', '1p38']
main(prot_list)


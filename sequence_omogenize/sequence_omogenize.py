import os, sys, re
import itertools
from Bio import SeqIO
from Bio import pairwise2
from Bio.SubsMat import MatrixInfo as matlist


def generate_dict(fasta_file):
    data_dict = {}
    records = list(SeqIO.parse(fasta_file, 'fasta'))
    for rec in records:
        data_dict[rec.id.lower()] = str(rec.seq)
        return data_dict


def select(fasta_c_dict, fasta_l_dict, parameters):
    for k in fasta_c_dict.keys():
        print '>%s_pdb\n%s' %(k, str(pairwise2.align.globalds(fasta_c_dict[k], fasta_l_dict[k], parameters['matrix'], parameters['gap_open'], parameters['gap_extended'])[0][0]))
        print '>%s_seq\n%s' %(k, str(pairwise2.align.globalds(fasta_c_dict[k], fasta_l_dict[k], parameters['matrix'], parameters['gap_open'], parameters['gap_extended'])[0][1]))


def main():
    parameters = {
                'matrix': matlist.blosum62,
                'gap_open': -10,
                'gap_extended': -0.5
                }

    fasta_c = 'crystals.fas'
    fasta_l = 'long_sequences_chA.fas'
    fasta_c_dict = generate_dict(fasta_c)
    fasta_l_dict = generate_dict(fasta_l)
    select(fasta_c_dict, fasta_l_dict, parameters)

main()
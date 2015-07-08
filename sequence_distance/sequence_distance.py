import os, sys, re
import itertools
from Bio import SeqIO
from Bio import pairwise2

#import subprocess
#from multiprocessing import Pool
#import affinity

# Script to calculate protein distances among all the sequences within a given MSA using the pairwise2 library from BioPython.

#def set_affinity():
#    affinity.set_process_affinity_mask(os.getpid(), 0xFFFFFFFF)


def generate_dict(fasta_file):
    data_dict = {}
    records = list(SeqIO.parse(fasta_file, 'fasta'))
    for rec in records:
        data_dict[rec.id] =  str(rec.seq)
    return data_dict


def iterate(data_dict):
    id_pairs = itertools.combinations(data_dict.keys(), 2)
    #pairs_number = len(list(itertools.combinations(data_dict.keys(), 2)))
    for i in id_pairs:
        seq_1 = data_dict[i[0]]
        seq_2 = data_dict[i[1]]


#TM_RMSD()
#print "Total pairs number: %s" %pairs_number

def main():
    fasta_file = 'crystals.fas'
    data_dict = generate_dict(fasta_file)
    iterate(data_dict)

main()
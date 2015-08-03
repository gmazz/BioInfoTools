import os, sys, re
import itertools
from Bio import SeqIO
from Bio import pairwise2
from Bio.SubsMat import MatrixInfo as matlist
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


def iterate(data_dict, parameters, fasta_file):
    out_file_name = "%s.csv" %(fasta_file.split('.fas')[0])
    out_file = open(out_file_name, "w")
    id_pairs = itertools.combinations(data_dict.keys(), 2)
    #pairs_number = len(list(itertools.combinations(data_dict.keys(), 2)))
    for i in id_pairs:
        try:
            seq_1 = data_dict[i[0]]
            seq_2 = data_dict[i[1]]
            message = "%s,%s,%s\n" %(i[0],i[1], str(pairwise2.align.globalds(seq_1, seq_2, parameters['matrix'], parameters['gap_open'], parameters['gap_extended'])[0][2]))
            out_file.write(message)
        except:
            print "\nI do have problems with the following sequence pair: %s\n" %(str(i))
        #print i, pairwise2.align.globaldx(seq_1, seq_2, matrix)


#TM_RMSD()
#print "Total pairs number: %s" %pairs_number

def main():
    fasta_file = 'test.fas'
    parameters = {
                    'matrix': matlist.blosum62,
                    'gap_open': -10,
                    'gap_extended': -0.5
                }
    data_dict = generate_dict(fasta_file)
    iterate(data_dict, parameters, fasta_file)

main()
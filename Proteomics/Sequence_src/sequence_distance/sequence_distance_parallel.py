import os, sys, re
import itertools
from Bio import SeqIO
from Bio import pairwise2
from Bio.SubsMat import MatrixInfo as matlist
import sys
from multiprocessing import Pool
import argparse

# Script to calculate protein distances among all the sequences within a given MSA using the pairwise2 library from BioPython.
# Please give the file_name as argument e.g. python sequence_distance.py fasta.fas


def generate_dict(fasta_file):

    try:
        data_dict = {}
        fasta_path = './fasta/' + fasta_file
        records = list(SeqIO.parse(fasta_path, 'fasta'))
        for rec in records:
            data_dict[rec.id] = str(rec.seq)
        return data_dict

    except IOError:
        print "Fasta file missing or having wrong format."

def pairwise_calc(seq_pair):
    parameters = {
        'matrix': matlist.blosum62,
        'gap_open': -11,
        'gap_extended': -1
    }
    try:
        return (seq_pair[2], pairwise2.align.globalds(seq_pair[0], seq_pair[1], parameters['matrix'], parameters['gap_open'], parameters['gap_extended'])[0][2])
    except:
        print "\nI do have problems with the following sequence pair: %s\n" % seq_pair[2]
        return {seq_pair[2]: ''}

def iterate(data_dict, fasta_file, proc_number):
    p = Pool(3)
    id_pairs = itertools.combinations(data_dict.keys(), 2)
    seq_pairs = ((data_dict[i[0]], data_dict[i[1]], i) for i in id_pairs)
    score_results = p.map(pairwise_calc, seq_pairs)


    # Print this in outer file

    out_file_name = "%s_bis.csv" %(fasta_file.split('.fas')[0])
    out_file = open(out_file_name, "w")
    for i in score_results:
        message = "%s,%s,%s\n" %(i[0][0], i[0][1], i[1])
        out_file.write(message)

def main(args):
    data_dict = generate_dict(args.i)
    iterate(data_dict, args.i, args.p)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parallel seq distance')
    parser.add_argument('-proc_n', '--p', help='define the number of processors on the machine')
    parser.add_argument('-in', '--i', help='input file')
    args = parser.parse_args()
    main(args)

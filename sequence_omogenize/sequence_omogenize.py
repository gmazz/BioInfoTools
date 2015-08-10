import os, sys, re
import itertools
from Bio import SeqIO
from Bio import pairwise2
from Bio.SubsMat import MatrixInfo as matlist
from operator import itemgetter
from itertools import groupby


def generate_dict(fasta_file):
    data_dict = {}
    records = list(SeqIO.parse(fasta_file, 'fasta'))
    for rec in records:
        data_dict[rec.id.lower()] = str(rec.seq)
    return data_dict


def iterate_selection(fasta_c_dict, fasta_l_dict, parameters):
    for k in fasta_c_dict.keys():
        #k = "4m5z"
        pdb = (pairwise2.align.globalds(fasta_c_dict[k], fasta_l_dict[k], parameters['matrix'], parameters['gap_open'], parameters['gap_extended'])[0][0])
        seq = (pairwise2.align.globalds(fasta_c_dict[k], fasta_l_dict[k], parameters['matrix'], parameters['gap_open'], parameters['gap_extended'])[0][1])
        selection = select(pdb, seq)
        print '>%s_pdb\n%s' %(k, pdb)
        print '>%s_seq\n%s' %(k, seq)
        print '>%s_sele\n%s' %(k, selection)


def gen(mylist):
    tmp = list()
    for i, e in enumerate(mylist):
        tmp.append(e)
        if all(p == '-' for p in tmp):
            yield i
        else:
            tmp = list()


def get_ranges(data):
    ranges = list()
    for k, g in groupby(enumerate(data), lambda (i,x):i-x):
        ranges.append(map(itemgetter(1), g))
    return ranges


def select(seq, pdb):
    dashes = gen(seq)
    ranges = get_ranges(list(dashes))
    to_remove = list()
    selection = list()
    for r in ranges:
        if 0 in r:
            to_remove += r
        elif (len(seq) - 1) in r:
            to_remove += r
    for i, e in enumerate(pdb):
        if i not in to_remove:
            selection.append(e)
    selection_str = ''.join(selection)
    return selection_str


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
    iterate_selection(fasta_c_dict, fasta_l_dict, parameters)


main()
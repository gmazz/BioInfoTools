from encode_HQI8 import *
import itertools
from Bio import SeqIO


def encode_seq(fasta_file):
    #out_name = fasta_file.split('.fas')[0] + '.csv'
    out_name = fasta_file.replace('.fas', '.csv')
    out_name = out_name.replace('/fasta/', '/results/')
    out_file = open(out_name, 'a+')
    records = list(SeqIO.parse(fasta_file, 'fasta'))
    for rec in records:
        aaindex_rec = encode_aaindex_features(rec.seq)
        res = separate_representation(aaindex_rec)
        out_file.write('%s%s\n' %(rec.id, res))


def separate_representation(aaindex_rec):
    tmp = ''
    for i in aaindex_rec:
        val_list = [str('{:.3f}'.format(x)) for x in list(i)]
        tmp = tmp + ';' + ','.join(val_list)
    return tmp


fasta_file = "../fasta/test.fas"
encode_seq(fasta_file)
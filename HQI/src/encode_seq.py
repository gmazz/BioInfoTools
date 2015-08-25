from encode_HQI8 import *
import itertools
from Bio import SeqIO

def encode_seq(fasta_file):
    records = list(SeqIO.parse(fasta_file, 'fasta'))
    for rec in records:
        aaindex_rec = encode_aaindex_features(rec.seq)
        res = list(itertools.chain(*aaindex_rec))
        print aaindex_rec, rec

    #seq = encode_aaindex_features(rec)
    #print seq

fasta_file = "../fasta/test.fas"
encode_seq(fasta_file)
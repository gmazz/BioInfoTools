from prody import *
#from Bio.PDB import *
from Bio import SeqIO

import sys, os
import pickle


def data_import(data_file):
    records = list(SeqIO.parse(data_file, 'fasta'))
    return records

def search_hit(record, cutoff):
    id = record.id.split('|')[3]
    seq = str(record.seq)
    return id

def iterate(data):
    results = [search_hit(record, data['cutoff']) for record in data['records']]
    print (list(results))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ("\n Please indicate the data.fas file. e.g.: $ pdb_template_fetch.py test.fas\n")

data = {}
data['data_file'] = sys.argv[1]
data['records'] = data_import(data['data_file'])
data['cutoff'] = 75
iterate(data)

#fasta_seq = 'ASFPVEILPFLYLGCAKDSTNLDVLEEFGIKYILNVTPNLPNLFENAGEFKYKQIPISDHWSQNLSQFFPEAISFIDEARGKNCGVLVHSLAGISRSVTVTVAYLMQKLNLSMNDAYDIVKMKKSNISPNFNFMGQLLDFERTL'
#cutoff = 80
#hits, best_hit = search_hits(fasta_seq, cutoff)
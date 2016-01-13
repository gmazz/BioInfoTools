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
    blast_record = blastPDB(seq)
    filename = 'mkp3_blast_record.pkl'
    pickle.dump(blast_record, open(filename, 'wb')) #writing pickle file

    with open(filename, 'rb') as f:
        blast_record = pickle.load(f, encoding='latin1')
    hits = blast_record.getHits(percent_identity=cutoff)
    best_hit = blast_record.getBest()
    #print (record, best_hit['pdb_id'], list(hits))
    return hits

def iterate(records, cutoff):
    results = [search_hit(record, cutoff) for record in records]
    print (list(results))

def get_pdb(fasta_id, best_hit):
    print(best_hit['pdb_id'], best_hit['percent_identity'])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ("\n Please indicate the data.fas file. e.g.: $ pdb_template_fetch_obsolete.py test.fas\n")

data_file = sys.argv[1]
records = data_import(data_file)
cutoff = 75
iterate(records, cutoff)

#fasta_seq = 'ASFPVEILPFLYLGCAKDSTNLDVLEEFGIKYILNVTPNLPNLFENAGEFKYKQIPISDHWSQNLSQFFPEAISFIDEARGKNCGVLVHSLAGISRSVTVTVAYLMQKLNLSMNDAYDIVKMKKSNISPNFNFMGQLLDFERTL'
#cutoff = 80
#hits, best_hit = search_hits(fasta_seq, cutoff)
from prody import *
from Bio import *
import pickle

def main(file):


def search_hits(fasta_seq, cutoff):
    blast_record = blastPDB(fasta_seq)
    filename = 'mkp3_blast_record.pkl'
    pickle.dump(blast_record, open(filename, 'wb')) #writing pickle file

    with open(filename, 'rb') as f:
        blast_record = pickle.load(f, encoding='latin1')
    hits = blast_record.getHits(percent_identity=cutoff)
    best_hit = blast_record.getBest()
    return hits, best_hit

def get_pdb(fasta_id, best_hit):


    #print(best_hit['pdb_id'], best_hit['percent_identity'])

fasta_seq = 'ASFPVEILPFLYLGCAKDSTNLDVLEEFGIKYILNVTPNLPNLFENAGEFKYKQIPISDHWSQNLSQFFPEAISFIDEARGKNCGVLVHSLAGISRSVTVTVAYLMQKLNLSMNDAYDIVKMKKSNISPNFNFMGQLLDFERTL'
cutoff = 80
hits, best_hit = search_hits(fasta_seq, cutoff)

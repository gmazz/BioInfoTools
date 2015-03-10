from prody import *
import pickle

def get_template(fasta_seq):
    blast_record = blastPDB(fasta_seq)
    filename = 'mkp3_blast_record.pkl'
    pickle.dump(blast_record, open(filename, 'wb')) #writing pickle file

    with open(filename, 'rb') as f:
        blast_record = pickle.load(f, encoding='latin1')


    best = blast_record.getBest()
    print(best['pdb_id'], best['percent_identity'])

    hits = blast_record.getHits(percent_identity=80)
    print (list(hits))


fasta_seq = 'ASFPVEILPFLYLGCAKDSTNLDVLEEFGIKYILNVTPNLPNLFENAGEFKYKQIPISDHWSQNLSQFFPEAISFIDEARGKNCGVLVHSLAGISRSVTVTVAYLMQKLNLSMNDAYDIVKMKKSNISPNFNFMGQLLDFERTL'
get_template(fasta_seq)

from prody import *
#from Bio.PDB import *
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Blast.Applications import NcbiblastpCommandline
import collections


import sys, os, re, io
import pickle


def data_import(data_file):
    records = list(SeqIO.parse(data_file, 'fasta'))
    return records

def search_hit(record, cutoff):
    cwd = os.getcwd()
    blast_cmd = '/usr/local/ncbi/blast/bin/blastp'
    blast_db = '%s/HA_db/HA_pdb' % cwd
    SeqIO.write(record, "blast_query.fas", "fasta")

    #blastp -query test.fas -db HA_pdb -out proteins_blastp_1e-40_table.txt -evalue 1e-40 -outfmt 10

    blast_output = NcbiblastpCommandline(cmd=blast_cmd, db=blast_db, evalue=cutoff, outfmt=6, query="blast_query.fas")()[0]#Blast command
    blast_list = blast_output.rstrip('\s').split('\n')
    blast_header = ["query id", "subject_id", "%_identity", "alignment_length", "mismatches", "gap_opens", "q_start", "q_end", "s_start", "s_end", "evalue", "bit score"]


    #X_dict = collections.OrderedDict(sorted(X_dict.items())) #ordered dictionary
    print(blast_list)

    return

def iterate(data):
    results = [search_hit(record, data['cutoff']) for record in data['records'][0:1]]

    #for record in data['records'][0:1]:
    #    record = ">%s\n%s" % (record.id, record.seq)
    #    print (record)
    #print (list(results))

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
from prody import *
#from Bio.PDB import *
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Blast.Applications import NcbiblastpCommandline
from Bio.Blast import NCBIXML

import sys, os, re, io
import pickle


def data_import(data_file):
    records = list(SeqIO.parse(data_file, 'fasta'))
    return records

def search_hit(record, cutoff):
    cwd = os.getcwd()
    blast_cmd = '/usr/local/ncbi/blast/bin/blastp'
    blast_db = '%s/HA_db/HA_pdb' %cwd
    #id = record.id.split('|')[3]
    #seq2 = SeqRecord(Seq("FQTWEEFSRAEKLYLADPMKVRVVLRYRHVDGNLCIKVTDDLICLVYRTDQAQDVKKIEKF")
    SeqIO.write(SeqRecord(record.seq), "blast_query", "fasta")
    #blastp -query test.fas -db HA_pdb -out proteins_blastp_1e-40_table.txt -evalue 1e-40 -outfmt 10

    blast_output = NcbiblastpCommandline(cmd=blast_cmd, db=blast_db, evalue=1e-40, outfmt=5, query="blast_query")() #Blast command
    #blast_result = NCBIXML.read(io.StringIO(blast_output))
    #fasta = io.StringIO(fasta)

    return id

def iterate(data):
    results = [search_hit(record, data['cutoff']) for record in data['records']]
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
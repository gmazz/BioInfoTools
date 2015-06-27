from Bio import SeqIO
import os, re, sys, io
from os import listdir
from os.path import isfile, join

def fasta2csv(fasta_file):
    name_fout = fasta_file.split('.fas')[0] + '.csv'
    file_out = open(name_fout, 'w+')
    records = list(SeqIO.parse(fasta_file, 'fasta'))
    for rec in records:
        rec_id = rec.id.split('_chA')[0]
        rec_seq = rec.seq
        entry = "%s,%s\n" %(rec_id, rec_seq)
        file_out.write(entry)
    file_out.close()

def main():
    cwd = os.getcwd()
    list_dir = "%s/lists" %cwd
    fasta_file = 'models_aln.fas'
    fasta_path = '%s/%s' % (cwd, fasta_file)
    fasta2csv(fasta_file)

main()

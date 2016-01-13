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

def main(multifasta):
    fasta_file = multifasta
    fasta2csv(fasta_file)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "\n Please indicate the multifasta file e.g.: $ fasta2csv.py multi.fasta\n"

    multifasta = sys.argv[1]
    main(multifasta)

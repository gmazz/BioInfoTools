from Bio import SeqIO
from Bio import Entrez
import os, re, sys, io


def data_write(id_list, fasta_file):
    records = list(SeqIO.parse(fasta_file, 'fasta'))
    file_handle = open(id_list, 'r')
    file_handle = file_handle.readlines()
    template_name = "%s.fas" %(file_handle[0].rstrip('\n').split('\t')[1])
    file_out = open(template_name, 'w+')

    id_list = [id.split('\t')[0] for id in file_handle]
    for id in id_list:
        for r in records:
            if id in r.id:
                entry = ">%s\n%s\n" %(r.id, r.seq)
                file_out.write(entry)
    file_out.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ("\n Please indicate the ID_list file. e.g.: $ select_fasta.py id_list.txt\n")

    id_list = sys.argv[1]
    cwd = os.getcwd()
    fasta_file = 'HA_sequences_2nd_modeling.fas'
    fasta_file = '%s/%s' % (cwd, fasta_file)
    data_write(id_list, fasta_file)



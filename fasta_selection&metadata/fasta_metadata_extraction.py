from Bio import SeqIO
from Bio import Entrez
import os, re, sys, io


def data_write(fasta_file):
    file_out = open('HA_new_models_classes.csv', 'w')

    records = list(SeqIO.parse(fasta_file, 'fasta'))
    for r in records:
        id = r.id.split('|')[3]
        sero_list = re.findall(r'[\(]([H][0-9]+)([N]?[0-9]+)?[\)]', r.description)
        #sero_list = re.findall(r'([\(][H][0-9]+[N][0-9]+[\)])', r.description)
        if sero_list:
            H = sero_list[0][0]
            N = sero_list[0][1]
            if not H:
                H = 'Hx'
            if not N:
                N = 'Nx'

            message = "%s,%s%s\n" %(id, H, N)
            file_out.write(message)
        else:
            message = "%s,NA\n" %id
            file_out.write(message)

    #id_list = [id.split('\t')[0] for id in file_handle]





cwd = os.getcwd()
fasta_file = 'HA_sequences_2nd_modeling.fas'
data_write(fasta_file)


    #fasta_file = '%s/%s' % (cwd, fasta_file)
    #data_write(id_list, fasta_file)



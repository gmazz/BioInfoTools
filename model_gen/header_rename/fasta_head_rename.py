from Bio import SeqIO
from Bio import Entrez
import os, re, sys, io
from os import listdir
from os.path import isfile, join

def rename(file):
    records = list(SeqIO.parse(file, 'fasta'))
    file_handle = open(id_list, 'r')
    file_handle = file_handle.readlines()
    template_name = "fasta_results/%s_target.fas" %(file_handle[0].rstrip('\n').split('\t')[1])
    file_out = open(template_name, 'w+')

    id_list = [id.split('\t')[0] for id in file_handle]
    for id in id_list:
        for r in records:
            if id in r.id:
                entry = ">%s\n%s\n" %(r.id, r.seq)
                file_out.write(entry)
    file_out.close()

def main():
    cwd = os.getcwd()
    list_dir = "%s/fasta_targets" % cwd
    file_list = [f for f in listdir(list_dir) if isfile(join(list_dir, f))]
    for file in file_list:
        rename(file)

main()
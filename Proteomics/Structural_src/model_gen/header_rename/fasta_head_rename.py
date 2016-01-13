from Bio import SeqIO
from Bio import Entrez
import os, re, sys, io
from os import listdir
from os.path import isfile, join
import contextlib


def rename(file, file_dir):
    new_file_name = "fasta_renamed/%s,my_alignment.fst" %(file.split('.')[0])
    file_out = open(new_file_name, 'w+')

    file_path = "%s/%s" %(file_dir, file)
    records = list(SeqIO.parse(file_path, 'fasta'))
    template = records[0]
    new_ref_id = records[0].id.replace("_ref", "")
    new_ref = ">%s\n%s\n" %(new_ref_id, records[0].seq)
    file_out.write(new_ref)

    for r in records[1:]:
        new_target_id = r.id.split('|')[3]
        new_target = ">%s\n%s\n" %(new_target_id, r.seq)
        file_out.write(new_target)


def main():
    cwd = os.getcwd()
    file_dir = "%s/fasta_targets" % cwd
    file_list = [f for f in listdir(file_dir) if isfile(join(file_dir, f))]
    for file in file_list:
        rename(file, file_dir)

main()
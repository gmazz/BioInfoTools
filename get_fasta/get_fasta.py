from Bio import SeqIO
import os, re, sys, io
import urllib.request
import contextlib


def get_id_list(id_file_list):
    handle = open(id_file_list, 'r+')
    ids = handle.readlines()
    id_list = [id.rstrip('\n').split('\t')[0] for id in ids]
    return id_list

def fasta_fetch(id_list):
    for id in id_list:
        with contextlib.closing(urllib.request.urlopen("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=" + id + "&rettype=fasta&retmode=text")) as url:
            fasta = url.read().decode('utf8')
            fasta = io.StringIO(fasta)
            records = list(SeqIO.parse(fasta, 'fasta'))
            print (records)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ("\n Please indicate the ID_list file. e.g.: $ get_fasta.py ID_list.txt\n")

    id_file_list = sys.argv[1]
    id_list = get_id_list(id_file_list)
    fasta_fetch(id_list[0:1])


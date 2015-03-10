from Bio import SeqIO
import os, re, sys, io
import urllib.request
import contextlib


def get_id_list(id_file_name):
    handle = open(id_file_name, 'r+')
    ids = handle.readlines()
    id_list = [id.rstrip('\n').split('\t')[0] for id in ids]
    return id_list

def fasta_fetch(id_list, id_file_name):
    multifasta_name = id_file_name.replace("_list.txt", "_multi.fas")
    multifasta_out = open(multifasta_name, 'w+')

    for id in id_list:
        try:
            with contextlib.closing(urllib.request.urlopen("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=" + id + "&rettype=fasta&retmode=text")) as url:
                fasta = url.read().decode('utf8')
                fasta = io.StringIO(fasta)
                records = list(SeqIO.parse(fasta, 'fasta'))
        except:
            print ('Not working for %s' %id)

        if records:
            if len(records) == 1:
                print (records[0].description)
                print (records[0].seq)
                multifasta_out.write(str('>' + records[0].description + '\n'))
                multifasta_out.write(str(records[0].seq + '\n'))

            else:
                sys.exit("%s has multiple entries, for chain A. Please check it out!" % id)
        else:
            print ("No data for %s" % id)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ("\n Please indicate the ID_list file. e.g.: $ get_fasta.py ID_list.txt\n")

    id_file_name = sys.argv[1]
    id_list = get_id_list(id_file_name)
    fasta_fetch(id_list, id_file_name)
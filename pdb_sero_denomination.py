# This file retrieve the taxonomical denomination of a give list of pdb files

import os, re, sys, io
from Bio import SeqIO
import urllib.request
import contextlib


def map_dict(map_file):
    d = {}
    f = open(map_file)
    strings = f.readlines()
    for s in strings:
        s = s.rstrip('\n')
        tmp_data = s.split('\t')
        pdb = tmp_data[0]
        uniprot = tmp_data[2]

        if pdb not in d.keys():
            d[pdb] = {uniprot}
        else:
            d[pdb].update({uniprot})

    return d

def access_uniprot (uniprot_dict):

    #pdb_sero_out = open('pdb_sero_out.txt', 'w+')
    missing_map_out = open('missing_map_out.txt', 'w+')

    checklist = []
    for k, vals in uniprot_dict.items():
        if k not in checklist:
            for v in vals:
                with contextlib.closing(urllib.request.urlopen("http://www.uniprot.org/uniprot/" + v + ".fasta")) as url:
                    fasta = url.read().decode('utf8')
                    fasta = io.StringIO(fasta)

                fasta_sequences = SeqIO.parse(fasta, 'fasta')
                for i in fasta_sequences:
                    tmp_desc = i.description
                    sero = re.findall(r'([H][0-9]+[N][0-9]+)', tmp_desc)
                    try:
                        #pdb_sero_out.write("%s %s\n" %(k, sero[0]))
                        print (k, sero[0])
                        checklist.append(k)
                    except:
                        missing_map_out.write("%s NAN\n" % k)
                        print ("I can't find the serotype for %s" % v)

def get_uniprot(in_file, d):

    uniprot_dict={}
    in_file_handle = open(in_file)
    pdbs = in_file_handle.readlines()
    pdbs = [pdb.rstrip('\n') for pdb in pdbs]

    for pdb in pdbs:
        try:
            uniprot_dict[pdb] = d[pdb]
        except:
            print ("I can't find mapping for %s" % pdb)

    return uniprot_dict

if __name__ == '__main__':
    if len(sys.argv) != 2:
        "Please, give the pdb file list as input"

    map_file = 'pdb_chain_uniprot.lst'
    d = map_dict(map_file)


    in_file = sys.argv[1]
    uniprot_dict = get_uniprot(in_file, d)
    access_uniprot(uniprot_dict)
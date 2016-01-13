# This script retrieve the PDB "description" of a list of Hemagglutinin(HA) PDBs given in input.
# The script uses the direct PDB annotation without mapping it to Uniprot.
# Usage e.g.: python pdb_direct_metadata.py pdb_list_crystals.txt

import os, re, sys, io
import urllib.request
import contextlib
from Bio.PDB import *

def fetch_annotation(pdb_dict):

    #raw_metadata = open('raw_metadata.txt', 'w+')
    checklist = []

    for k, v in pdb_dict.items():
        if k not in checklist:
            with contextlib.closing(urllib.request.urlopen("http://www.rcsb.org/pdb/files/" + k.upper() + ".pdb?headerOnly=YES")) as url:
                pdb_tmp = url.read().decode('utf8')
                pdb_tmp = io.StringIO(pdb_tmp)

                try:
                    tmp_desc = BioPDB_parser(k, pdb_tmp)
                    #print (k, tmp_desc)

                except:
                    print (k, "NULL")

            #print (str_tmp)
            #    fasta_sequences = SeqIO.parse(str_tmp, 'fasta')

            #for i in fasta_sequences:
            #    sero, tmp_desc, flag = filter(i)

            #    if flag == 1:
            #        print ("%s\t%s\t%s" % (k, sero, tmp_desc))
                    #raw_metadata.write("%s\t%s\t%s\n" % (k, sero, tmp_desc))
            #    elif flag == 2:
            #        print ("%s\t%s\t%s" % (k, sero, tmp_desc))
                    #raw_metadata.writels("%s\t%s\t%s\n" % (k, sero, tmp_desc))
            #    else:
            #        sys.exit("There is an exception to be corrected")

            checklist.append(k)
        else:
            print ("%s is already in cheklist" % k)


def BioPDB_parser(k, pdb_tmp):
    parser = PDBParser()
    structure = parser.get_structure(k, pdb_tmp)
    tmp_desc_strain = (structure.header['source']['1']['strain'])
    tmp_desc_os = (structure.header['source']['1']['organism_scientific'])
    print (k, tmp_desc_strain, tmp_desc_os)
    return tmp_desc

def pdb_annotation(in_file):

    pdb_dict = {}
    in_file_handle = open(in_file)
    pdbs = in_file_handle.readlines()
    pdbs = [pdb.rstrip('\n') for pdb in pdbs]

    for pdb in pdbs:
        pdb_dict[pdb] = ""

    return pdb_dict

if __name__ == '__main__':
    if len(sys.argv) != 2:
        "Please, give the pdb file list as input"

    in_file = sys.argv[1]
    pdb_dict = pdb_annotation(in_file)
    #pdb_dict = {'4wa1' : "", '4uo7' : "", '1jsi' : ""}
    fetch_annotation(pdb_dict)
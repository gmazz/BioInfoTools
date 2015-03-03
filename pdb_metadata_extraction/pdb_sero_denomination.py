# This script retrieve the fasta "description" of a list of Hemagglutinin(HA) PDBs given in input.
# The differences in the HA annotation, have been somehow mitigated, in order to make the information more consistent.
# Usage e.g.: python pdb_sero_denomination.py pdb_list_crystals.txt

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
        chain = tmp_data[1]
        uniprot = tmp_data[2]

        if pdb not in d.keys():
            d[pdb] = [{chain: uniprot}]
        else:
            d[pdb].append({chain: uniprot})

    return d

def uniprot_fasta_parse (uniprot_dict):

    missing_map_out = open('missing_map_out.txt', 'w+')
    raw_metadata = open('raw_metadata.txt', 'w+')

    checklist = []
    for k, v in uniprot_dict.items():
        if k not in checklist:
            with contextlib.closing(urllib.request.urlopen("http://www.uniprot.org/uniprot/" + v + ".fasta")) as url:
                fasta = url.read().decode('utf8')
                fasta = io.StringIO(fasta)
                fasta_sequences = SeqIO.parse(fasta, 'fasta')

            # Substitutions Ad Hoc
            for i in fasta_sequences:
                tmp_desc = i.description
                sero = re.findall(r'([H][0-9]+[N][0-9]+)', tmp_desc)
                tmp_desc = tmp_desc.replace("(Fragment)", "")
                tmp_desc = tmp_desc.replace("Influenza A virus", "Influenza_A_virus")
                tmp_desc = tmp_desc.replace("Hong Kong", "HongKong")
                tmp_desc = tmp_desc.split()

            # Matching cases
                if (len(tmp_desc)) == 6:
                    tmp_desc = tmp_desc[3]
                elif (len(tmp_desc)) == 7:
                    tmp_desc = tmp_desc[3]
                elif (len(tmp_desc)) == 8:
                    tmp_desc = tmp_desc[3] + tmp_desc[4]
                elif (len(tmp_desc)) == 9:
                    tmp_desc = tmp_desc[3] + tmp_desc[4] + "(" + tmp_desc[5] + ")"
                elif (len(tmp_desc)) == 10:
                    tmp_desc = tmp_desc[3] + tmp_desc[4] + tmp_desc[5] + "(" + tmp_desc[6] + ")"
                elif (len(tmp_desc)) == 11:
                    tmp_desc = tmp_desc[3] + tmp_desc[4] + "(" + tmp_desc[5] + "))"
                elif (len(tmp_desc)) == 12:
                    tmp_desc = tmp_desc[3] + tmp_desc[4] + tmp_desc[5] + "(" + tmp_desc[6] + "))"
                else:
                    sys.exit("The case for %s is missing. Please check it out!" % k)

                # Replace "StrainSomethingA" with A ()

                str_rep = re.search('([S,s]train[A-Z,a-z]+)', tmp_desc)

                if str_rep:
                    tmp_desc = tmp_desc.replace(str_rep.group(1), "A")

                if sero:
                    print ("%s\t%s\t%s" % (k, sero[0], tmp_desc))
                    raw_metadata.write("%s\t%s\t%s\n" % (k, sero[0], tmp_desc))

                else:
                    print ("%s\t--\t%s  " % (k, tmp_desc))
                    raw_metadata.write("%s\t--\t%s\n" % (k, tmp_desc))
                    missing_map_out.write("%s NAN\n" % k)
                    print ("I can't find the serotype for %s" % k)
            checklist.append(k)
        else:
            print ("%s is already in cheklist" % k)

def get_uniprot(in_file, d):

    uniprot_dict={}
    in_file_handle = open(in_file)
    pdbs = in_file_handle.readlines()
    pdbs = [pdb.rstrip('\n') for pdb in pdbs]

    for pdb in pdbs:
        try:
            for k, v in d[pdb][0].items():
                uniprot_dict[pdb] = v
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
    uniprot_fasta_parse(uniprot_dict)
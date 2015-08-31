import os, sys, re
from Bio import SeqIO
from Bio import pairwise2
from Bio.SubsMat import MatrixInfo as matlist


def generate_dict(fasta_file):
    data_dict = {}
    fasta_path = './fasta/' + fasta_file
    records = list(SeqIO.parse(fasta_path, 'fasta'))
    for rec in records:
        data_dict[rec.id] =  str(rec.seq)
    return data_dict


def iterate(data_dict, parameters, fasta_file):
    print data_dict
    out_file_name = "%s_auto.csv" %(fasta_file.split('.fas')[0])
    out_file = open(out_file_name, "w")
    for k, v in data_dict.items():
        try:
            message = "%s,%s,%s\n" %(k, k, str(pairwise2.align.globalds(v, v, parameters['matrix'], parameters['gap_open'], parameters['gap_extended'])[0][2]))
            out_file.write(message)
        except:
            print "\nI do have problems with the following sequence pair: %s\n" %(str(i))


def main():
    fasta_file = 'models.fas'
    parameters = {
                    'matrix': matlist.blosum62,
                    'gap_open': -11,
                    'gap_extended': -1
                }
    data_dict = generate_dict(fasta_file)
    iterate(data_dict, parameters, fasta_file)

main()

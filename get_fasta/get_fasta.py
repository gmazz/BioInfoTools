from Bio import SeqIO
from Bio import Entrez
import os, re, sys, io
import urllib.request
import contextlib
import itertools



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


def record_filter(records, id):
    GBFeatures = records[0]['GBSeq_feature-table']
    GBE = [gbf.get('GBFeature_quals') for gbf in GBFeatures]
    GBE = (list(itertools.chain(*GBE)))
    p_id =([d['GBQualifier_value'] for d in GBE if d['GBQualifier_name'] == 'protein_id'][0])
    print (id, p_id)

# This method converts ID from gene_AC to protein_ID
def geneAC_2_proteinID(id_list):

    for id in id_list:
        try:
            handle = Entrez.efetch(db='nuccore', id=id, retmode='xml')
            records = Entrez.parse(handle) # obj of dict
            records = [rec for rec in records]

            try:
                record_filter(records, id)

            except:
                print ("Problems with " + id + " parsing.")

        except:
            print ("Impossible to get info for %s" % id)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ("\n Please indicate the ID_list file. e.g.: $ get_fasta.py ID_list.txt\n")

    id_file_name = sys.argv[1]
    id_list = get_id_list(id_file_name)
    #fasta_fetch(id_list, id_file_name)
    #id_list = ['CY014497.1']
    geneAC_2_proteinID(id_list)
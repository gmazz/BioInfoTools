from prody import *
#from Bio.PDB import *
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Blast.Applications import NcbiblastpCommandline
from operator import itemgetter
import collections
import sys, os, re, io
import pickle


def data_import(data_file):
    records = list(SeqIO.parse(data_file, 'fasta'))
    return records


def type_set(bl):
    bl[0] = str(bl[0].split('|')[3])
    bl[1] = str(bl[1].split('|')[0])
    bl[2] = float(bl[2])
    bl[3] = int(bl[3])
    bl[4] = int(bl[4])
    bl[5] = int(bl[5])
    bl[6] = int(bl[6])
    bl[7] = int(bl[7])
    bl[8] = int(bl[8])
    bl[9] = int(bl[9])
    bl[10] = float(bl[10])
    bl[11] = float(bl[11])
    return bl


def search_hit(record, cutoff):
    cwd = os.getcwd()
    blast_cmd = '/usr/local/ncbi/blast/bin/blastp'
    blast_db = '%s/HA_db/HA_pdb' % cwd
    SeqIO.write(record, "blast_query.fas", "fasta")
    blast_output = NcbiblastpCommandline(cmd=blast_cmd, db=blast_db, evalue=cutoff, outfmt=6, query="blast_query.fas")()[0] #Blast command
    blast_list = blast_output.rstrip('\s').split('\n')[:-1]

    blast_header = [
                    'query_id',
                    'subject_id',
                    'identity',
                    'alignment_length',
                    'mismatches',
                    'gap_opens',
                    'q_start',
                    'q_end',
                    's_start',
                    's_end',
                    'evalue',
                    'bit score'
                    ]

    record_dict = {record.id : []}

    for tmp in blast_list:
        bl = tmp.split('\t')
        type_set(bl)
        bl_dict = dict(zip(blast_header, bl))
        record_dict[record.id].append(bl_dict)
    ordered_dict_list = sorted(record_dict[record.id], key=itemgetter('identity'), reverse=True)
    record_dict[record.id] = ordered_dict_list
    return record_dict


def read_results(results, bhn):
    for tmp in results:
        for k, v in tmp.items():
            subject_id = [i['subject_id'] for i in v[0:bhn]]
            evalue = [i['evalue'] for i in v[0:bhn]]
            alignment_length = [i['alignment_length'] for i in v[0:bhn]]
            message = list(zip(subject_id, evalue, alignment_length))
            print (k, message)


def iterate(data):
    results = [search_hit(record, data['cutoff']) for record in data['records']]
    return results


def main():
    if __name__ == '__main__':
        if len(sys.argv) != 2:
            print ("\n Please indicate the data.fas file. e.g.: $ pdb_template_fetch.py test.fas\n")
    data = {}
    data['data_file'] = sys.argv[1]
    data['records'] = data_import(data['data_file'])
    data['cutoff'] = 75
    best_hits_number = 10
    results = iterate(data)
    read_results(results, best_hits_number)

main()
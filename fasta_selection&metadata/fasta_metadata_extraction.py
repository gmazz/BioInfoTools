from Bio import SeqIO
from Bio import Entrez
import os, re, sys, io


def extract_data(rec):
        myset = ()
        description = rec.description
        #print description
        id = rec.id.split('|')[3]
        sero_list = re.findall(r'[\(]([H][0-9]+)([N]?[0-9]+)?[\)]', rec.description)
        raw_data = re.findall(r'[\(]([\w\W\d\w]+)[\)]', rec.description)[0].split('/')


        #print rec.description, sero_list
        if sero_list:
            H = sero_list[0][0]
            N = sero_list[0][1]
            if not H:
                H = 'Hx'
            if not N:
                N = 'Nx'

            message = "%s,%s%s\n" %(id, H, N)
            #file_out.write(message)
        else:
            message = "%s,NA\n" %id
            #file_out.write(message)

        return raw_data, id

def data_write(fasta_file):
    rec_dir = {'rec' : {}}
    #file_out = open('HA_new_models_classes.csv', 'w')
    my_set = set()
    records = list(SeqIO.parse(fasta_file, 'fasta'))
    for rec in records:
        raw_data, id = extract_data(rec)
        #print raw_data
        my_set.add(len(raw_data))
        if len(raw_data) == 5:
            rec_dir[id] = {'chain': raw_data[0], 'host': raw_data[1], 'location': raw_data[2], 'year': raw_data[4], 'line_length': 5}
        elif len(raw_data) == 4:
            rec_dir[id] = {'chain': raw_data[0], 'location': raw_data[1], 'year': raw_data[3], 'line_length': 4}
        elif len(raw_data) == 3:
            rec_dir[id] = {'chain': raw_data[0], 'location': raw_data[1], 'year': raw_data[2], 'line_length': 3}
        else:
            print "Missing case, please check %s" %rec

    #print my_set
    return rec_dir

    #id_list = [id.split('\t')[0] for id in file_handle]





cwd = os.getcwd()
fasta_file = 'HA_sequences_2nd_modeling.fas'
rec_dir = data_write(fasta_file)
print len(rec_dir)

#for k, v in rec_dir.items():
#    try:
#        print k, v['line_length']

#    except:
#        print k


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
    #rec_dir = {'rec' : {}}
    rec_dir = {}
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
            rec_dir[id] = {'chain': raw_data[0], 'host': '-', 'location': raw_data[1], 'year': raw_data[3], 'line_length': 4}
        elif len(raw_data) == 3:
            rec_dir[id] = {'chain': raw_data[0], 'host': '-', 'location': raw_data[1], 'year': raw_data[2], 'line_length': 3}
        else:
            print "Missing case, please check %s" %rec
    #print my_set
    return rec_dir

    #id_list = [id.split('\t')[0] for id in file_handle]


def data_filtering(rec_dir):
    host_renaming = {}
    host_renaming ['avian'] = ['murre', 'crane', 'grebe', 'bustard', 'coot', 'waterfowl', 'turtledove', 'chukkar', 'stint', 'anas', 'garganey', 'ostrich', 'pheasant', 'falcon', 'goose', 'chicken', 'turkey', 'duck', 'mallard', 'winged', 'sanderling', 'bird','quail','pelican', 'teal', 'shoveler', 'turnstone', 'knot', 'pintail', 'heron', 'gull', 'sandpiper']
    host_renaming ['swine'] = ['sw']
    for k, v in rec_dir.items():
        try:
            for k1, v1 in host_renaming.items():
                # Substitute host names
                m_streight = [k1 for s in v1 if v['host'].lower() in s.lower()]
                m_reverse = [k1 for s in v1 if s.lower() in v['host'].lower()]
                check = len(m_streight) + len(m_reverse)
                if check > 0:
                    rec_dir[k]['host'] = k1
        except:
            pass
        try:
            # Fetch correct year
            year = clear_year(v['year'])
            rec_dir[k]['year'] = year
        except:
            rec_dir[k]['year'] = '-'
            print "ALARM!", k, v
    return rec_dir

def clear_year(raw_year):
    year = raw_year.split('(')[0]
    year = year.rstrip(' ')
    if len(year) == 2:
        if int(year) <= 15:
            year = int(year) + 2000
        else:
            year = int(year) + 1900
    try:
        return int(year)
    except:
        return int(year)

cwd = os.getcwd()
#fasta_file = 'HA_sequences_2nd_modeling.fas'
fasta_file = 'unique.fas'
rec_dir = data_write(fasta_file)
rec_dir = data_filtering(rec_dir)

for k, v in rec_dir.items():
    if v:
        print "%s,%s,%s,%s,%s" %(k, v['chain'], v['host'], v['location'], v['year'])

from Bio import SeqIO
from Bio import Entrez
import os, re, sys, io


def extract_data(rec):
        id, subtype, description = rec.split('\t')
        subtype_list = re.findall(r'[\(]([H][0-9]+)([N][0-9]+)[\)]', description)
        if subtype_list:
                raw_data = re.findall(r'[\(]([\w\W\d\w]+)[\)]', description)[0].split('/')
                return (id, subtype, raw_data, description)

def clear_year(raw_year):
    year = raw_year.split('(')[0]
    if len(year) == 2:
        if int(year) <= 15:
            year = int(year) + 2000
        else:
            year = int(year) + 1900
    try:
        return int(year)
    except:
        return year

def data_write(data_file):
    rec_dir = {'rec' : {}}
    my_set = set()

    file_handle = open(data_file, 'r')
    records = file_handle.readlines()
    records = [r.rstrip('\n') for r in records]

    for rec in records:
        vals = extract_data(rec)
        if vals:
            id = vals[0]
            subtype = vals[1]
            raw_data = vals[2]
            description = vals[3]

            my_set.add(len(raw_data))
            if len(raw_data) == 5:
                year = clear_year(raw_data[4])
                rec_dir[id] = {'chain': raw_data[0], 'host': raw_data[1], 'location': raw_data[2], 'year': year, 'subtype': subtype, 'gvt': raw_data[3], 'desc': vals[3], 'line_length': 5}
            elif len(raw_data) == 4:
                year = clear_year(raw_data[3])
                rec_dir[id] = {'chain': raw_data[0], 'host': '', 'location': raw_data[1], 'year': year, 'subtype': subtype, 'gvt': raw_data[2],'desc': vals[3], 'line_length': 4}
            elif len(raw_data) == 3:
                year = clear_year(raw_data[2])
                rec_dir[id] = {'chain': raw_data[0], host: '', 'location': raw_data[1], 'year': year, 'subtype': subtype, 'gvt': raw_data[2],'desc': vals[3], 'line_length': 3}
            else:
                print "Missing case, please check %s" %rec
    return rec_dir


cwd = os.getcwd()
data_file = 'raw_metadata.txt'
rec_dir = data_write(data_file)

for k, v in rec_dir.items():
    if v:
       print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" %(k, v['chain'], v['subtype'], v['host'].lower(), v['location'].capitalize(), v['year'], v['gvt'], v['desc'])
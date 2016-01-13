# Description: this python script parse the 22k.fas multifasta headers to extract statistics about subtypes, year of infections, hosts, etc.
# A mapping dictionary for locations is needed as well as the enlargment of the dictionary for the various species.
# Although several parsing steps are implemented in order to deal with the non coherently formatted headers of the sequences, some
# sporadic cases are wrongly parsed, because there wasn't any way find general parsing rules for these cases.

from Bio import SeqIO
from Bio import Entrez
import os, re, sys, io


def extract_data(rec):
        myset = ()
        description = rec.description
        tmp = rec.id.split('__')
        if len(tmp) >= 3:
            subtype = tmp[3]
            id = tmp[0]
            data = tmp[2].split('/')
        else:
            print ('Fuck! %s' % tmp)
        return data, id, subtype


def data_write(fasta_file):
    rec_dir = {}
    records = list(SeqIO.parse(fasta_file, 'fasta'))
    for rec in records:
        data, id, subtype = extract_data(rec)
        if len(data) == 6:
            rec_dir[id] = {'chain': data[0], 'host': data[1], 'location': data[2], 'year': data[5], 'subtype': subtype, 'aln': rec.seq, 'line_length': 6}
        elif len(data) == 5: # Check control to operate on the last field (year__host__...)
            rec_dir[id] = {'chain': data[0], 'host': data[1], 'location': data[2], 'year': data[4], 'subtype': subtype, 'aln': rec.seq, 'line_length': 5}
        elif len(data) == 4:
            rec_dir[id] = {'chain': data[0], 'host': '-', 'location': data[1], 'year': data[3], 'subtype': subtype, 'aln': rec.seq, 'line_length': 4}
        elif len(data) == 3:
            rec_dir[id] = {'chain': data[0], 'host': '-', 'location': data[1], 'year': data[2], 'subtype': subtype, 'aln': rec.seq, 'line_length': 3}
        else:
            #raise ValueError('>>>>>>>>>>>>>>>>> Attention the following filed is not as the others:\n %s, %s' %(id, data))
            pass
    return rec_dir


def data_filtering(rec_dir):
    host_renaming = {}
    host_renaming ['avian'] = ['murre', 'crane', 'grebe', 'bustard', 'coot', 'waterfowl', 'turtledove', 'chukkar', 'stint', 'anas', 'garganey', 'ostrich', 'pheasant', 'falcon', 'goose', 'chicken', 'turkey', 'duck', 'mallard', 'winged', 'sanderling', 'bird','quail','pelican', 'teal', 'shoveler', 'turnstone', 'knot', 'pintail', 'heron', 'gull', 'sandpiper', 'eagle', 'owl', 'cormorant', 'pigeon', 'cygnus', 'crow', 'sparrow', 'peacock', 'goosander']
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
            tmp_year = rec_dir[k]['year']
            year = literal_digit_split(tmp_year)
            rec_dir[k]['year'] = year
    return rec_dir


def literal_digit_split(mess):
    fragments = re.split('(\d+)', mess)
    year = ''
    for f in fragments:
        if f.isdigit():
            if len(f) == 2 or len(f) == 4:
                year = clear_year(f)
    try:
        return year
    except:
        return '-'


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


def read(rec_dir):
    for k, v in rec_dir.items():
        if v:
            print "%s,%s,%s,%s,%s" %(k, v['chain'], v['host'], v['location'], v['year'])


def statistics(rec_dir):
    stats = {}
    stats['locations'] = {}
    stats['years'] = {}
    stats['subtypes'] = {}
    stats['hosts'] = {}
    for k, v in rec_dir.items():
        if v['location'] in stats['locations'].keys():
            stats['locations'][v['location']] = stats['locations'][v['location']] + 1
        else:
            stats['locations'][v['location']] = 1
        if v['host'] in stats['hosts'].keys():
            stats['hosts'][v['host']] = stats['hosts'][v['host']] + 1
        else:
            stats['hosts'][v['host']] = 1
        if v['year'] in stats['years'].keys():
            stats['years'][v['year']] = stats['years'][v['year']] + 1
        else:
            stats['years'][v['year']] = 1
        if v['subtype'] in stats['subtypes'].keys():
            stats['subtypes'][v['subtype']] = stats['subtypes'][v['subtype']] + 1
        else:
            stats['subtypes'][v['subtype']] = 1
    return stats


def print_stats(stats):
    for k1, data in stats.iteritems():
        print "####################### %s:" %(k1)
        for k2, v in data.iteritems():
            print "%s : %s" %(k2, v)
        print "\n"

def aln_year_subtype(rec_dir):
    for k, v in rec_dir.items():
        print "%s,%s,%s,%s" %(k, v['subtype'], v['year'], v['aln'])


def main():
    cwd = os.getcwd()
    #fasta_file = '22k.fas'
    fasta_file = '/Users/johnny/Desktop/CeNT/HA/HxNx_aligned_AA_FASTA/22k.fas'
    rec_dir = data_write(fasta_file)
    rec_dir = data_filtering(rec_dir)
    aln_year_subtype(rec_dir)
    #stats = statistics(rec_dir)
    #print_stats(stats)

main()

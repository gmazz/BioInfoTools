from prody import *
from Bio.PDB import *
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Blast.Applications import NcbiblastpCommandline
from operator import itemgetter
import collections
import contextlib
import urllib.request
import sys, os, re, io

################################################################# Performing BLAST agains the pdb database and getting data back ####################################


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


def print_results(results, bhn):
    for tmp in results:
        for k, v in tmp.items():
            subject_id = [i['subject_id'] for i in v[0:bhn]]
            evalue = [i['evalue'] for i in v[0:bhn]]
            alignment_length = [i['alignment_length'] for i in v[0:bhn]]
            message = list(zip(subject_id, evalue, alignment_length))
            #print ("%s\t%s\n" %(k, message))


def unique(list):
    unique_list = []
    chain_list = []
    chain_str = ''
    for i in list:
        pdb_id, chain = i.split(':')
        if pdb_id not in unique_list:
            if chain_str:
                pdb, chains = chain_str.split('\t')
                chains = chains.split(',')
                tmp_tuple = (pdb, chains)
                chain_list.append(tmp_tuple)
            unique_list.append(pdb_id)
            chain_str = "%s\t%s" %(pdb_id, chain)
        else:
            chain_str = "%s,%s" %(chain_str, chain)
    unique_list = [x.lower() for x in unique_list]
    return unique_list, chain_list


def iterate(data):
    results = [search_hit(record, data['cutoff']) for record in data['records']]
    return results


def get_pdb_list(results, bhn):
    data_dict = {}
    for tmp in results:
        for k, v in tmp.items():
            pdb_list = [i['subject_id'] for i in v[0:bhn]]
            unique_list, chain_list = unique(pdb_list)
            tmp_dict = {'unique_list': unique_list, 'chain_list': chain_list}
            data_dict[k.split('|')[3]] = tmp_dict
    return data_dict


#############################  Obtaining the PDBs and checking quality  ###################


    #GBFeatures = records[0]['GBSeq_feature-table']
    #GBE = [gbf.get('GBFeature_quals') for gbf in GBFeatures]
    ##GBE = (list(itertools.chain(*GBE)))
    #p_id = ([d['GBQualifier_value'] for d in GBE if d['GBQualifier_name'] == 'protein_id'][0])
    #return p_id


def PDB_text_parser(k, pdb_id, pdb_text):
    handle = pdb_text.split('\n')
    for s in handle:
        m = re.match(r'(REMARK)[\s]+([\d]+)[\s]+(FREE R VALUE)[\s\W]+([\:])[\s]+([\d\.]+)', s)
        if m:
            return m.groups()[4]


def BioPDB_parser(k, pdb_id, pdb_file, SRC):
    parser = PDBParser()
    structure = parser.get_structure(pdb_id, pdb_file)
    resolution = structure.header.get('resolution')
    chain_name = structure.header.get('compound')['1']['chain']
    return resolution, chain_names

def parser_manager(k, pdb_id, pdb_file, pdb_text, SRC):
    resolution, chains = BioPDB_parser(k, pdb_id, pdb_file, SRC)
    free_R = PDB_text_parser(k, pdb_id, pdb_text)
    print (k, pdb_id, free_R, resolution, chains)


def pdb_check(k, unique_list, SRC):
    checklist = []
    for pdb_id in unique_list:
        if pdb_id not in checklist:
            with contextlib.closing(urllib.request.urlopen("http://www.rcsb.org/pdb/files/" + pdb_id.upper() + ".pdb?headerOnly=YES")) as url:
                pdb_text = url.read().decode('utf8')
                pdb_file = io.StringIO(pdb_text)
                try:
                    parser_manager(k, pdb_id, pdb_file, pdb_text, SRC)
                        #print (k, tmp_desc)

                except:
                    print (pdb_id, "NULL")


def pdb_loop(data_dict, SRC):
    for k, v in data_dict.items():
        unique_list = v['unique_list']
        pdb_check(k, unique_list, SRC)



############################################### Main ####################################################


def main():
    if __name__ == '__main__':
        if len(sys.argv) != 2:
            print ("\n Please indicate the data.fas file. e.g.: $ pdb_template_fetch.py test.fas\n")
    data = {}
    data['data_file'] = sys.argv[1]
    data['records'] = data_import(data['data_file'])
    data['cutoff'] = 75
    best_hits_number = 20
    Structure_Resolution_Cutoff = 2.8

    results = iterate(data)
    #print_results(results, best_hits_number)
    data_dict = get_pdb_list(results, best_hits_number)
    pdb_loop(data_dict, Structure_Resolution_Cutoff)

main()
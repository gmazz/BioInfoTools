import pandas as pd
import sys, os


def file_path(data_name):
    os.chdir('../data')
    root = os.getcwd()
    data_path = root + '/' + data_name
    os.chdir('../src')
    return data_path


def get_data(mob_name, aln_name):
    mob_path = file_path(mob_name)
    aln_name = file_path(aln_name)
    aln = pd.read_csv(aln_name, index_col=None)
    mob = [m.rstrip().split(',') for m in open(mob_path, 'r+').readlines()]
    mob_dict = {}
    aln_dict = {}

    # Fill alignment dict
    for i, a in aln.iterrows():
        aln_dict[a['p_id']] = list(a['sequence'])

    # Fill mobility dict
    for m in mob:
        mob_dict[m[0].split('.')[0]] = m[1:]

    return mob_dict, aln_dict


def combine_data(mob_dict, aln_dict):
    data = {}
    for ak, av in aln_dict.iteritems():
        if ak in mob_dict.keys():
            tmp_data = []
            tmp_gaps = [indx for indx, v in enumerate(av) if v == '-']
            av = [x for x in av if x != '-']
            tmp_data = zip(av, mob_dict[ak])
            [tmp_data.insert(index, ('-', 'None')) for index in tmp_gaps]
            data[ak] = tmp_data
    return data


def mobility_stats(data):
    binding_positions = [131,132,133,134,135,154,156,186,187,191,194,195,226,227,228,229]
    proximity_positions = [128,129,130,136,137,138,151,152,153,156,157,158,183,184,185,189,196,197,198,223,224,225,230,231,232]
    

mob_name = 'crystals_mob.txt'
aln_name = 'crystals_aln.csv'
mob_dict, aln_dict = get_data(mob_name, aln_name)
data = combine_data(mob_dict, aln_dict)
mobility_stats(data)

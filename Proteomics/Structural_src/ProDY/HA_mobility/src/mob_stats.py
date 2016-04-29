import pandas as pd
import numpy as np
import sys, os
import matplotlib.pyplot as plt
import scipy.stats


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
    #proximity_positions = [128,129,130,136,137,138,151,152,153,156,157,158,183,184,185,189,196,197,198,223,224,225,230,231,232]
    binding_positions = range(1,30,1)

    binding_data = []
    proximity_data = []

    for k, v in data.iteritems():
        for b in binding_positions:
            binding_data.append(v[b][1])

    for k, v in data.iteritems():
        for b in proximity_positions:
            proximity_data.append(v[b][1])

    binding_data = [float(v) for v in binding_data if v != 'None']
    proximity_data = [float(v) for v in proximity_data if v != 'None']
    return binding_data, proximity_data


def plots(binding_data, proximity_data):
    fig = plt.figure(figsize=(15, 20), dpi=300)
    ax = fig.add_subplot(111)


    print np.max(proximity_data)
    print np.max(binding_data)

    n_bins = 150
    plt.hist(proximity_data, bins=n_bins, histtype='stepfilled', normed=True, color='b', label='Proximity')
    plt.hist(binding_data, bins=n_bins, histtype='stepfilled', normed=True, color='r', alpha=0.6, label='Binding_site')

    #Formatting
    plt.title("Proximity/Binding site Histogram\n(# bins = %s)" %n_bins, fontsize=30)
    plt.xlabel("Value", fontsize=20)
    plt.ylabel("Normalized frequency", fontsize=20)

    yticks = ax.yaxis.get_major_ticks()
    xticks = ax.xaxis.get_major_ticks()

    yticks[-8].set_visible(False)


    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.legend(fontsize=20)

    plt.savefig('/Users/johnny/Dropbox/Flu_project/3DFlu_paper_04_16/images/mobility/mobility_models.png', dpi=300, figsize=(20, 10))
    #plt.show()



def stats(binding_data, proximity_data):
    n_bins = 150
    hist_b, bins_b = np.histogram(binding_data, bins=np.linspace(np.min(binding_data), np.max(binding_data),n_bins))
    hist_p, bins_p = np.histogram(proximity_data, bins=np.linspace(np.min(binding_data), np.max(binding_data),n_bins))
    #print hist_b, hist_p
    print "Binding data> mean:%s, median:%s, std:%s" %(np.mean(binding_data), np.median(binding_data), np.std(binding_data))
    print "Proximity data> mean:%s, median:%s, std:%s" %(np.mean(proximity_data), np.median(proximity_data), np.std(proximity_data))
    print scipy.stats.spearmanr(hist_b, hist_p)



#mob_name = 'crystals_mob.txt'
#aln_name = 'crystals_aln.csv'
mob_name = 'models_mob.txt'
aln_name = 'models_aln.csv'


mob_dict, aln_dict = get_data(mob_name, aln_name)
data = combine_data(mob_dict, aln_dict)
binding_data, proximity_data = mobility_stats(data)
plots(binding_data, proximity_data)
#stats(binding_data, proximity_data)
import os, sys, re
import itertools
import subprocess
import numpy as np
import linecache

def read_two_lines(id_name, tmpline_1, tmpline_2):
    l1 = linecache.getline(id_name, tmpline_1)
    l2 = linecache.getline(id_name, tmpline_2)
    return l1, l2

def metric_1(l1, l2, id_tuple):
    if len(l1) == len(l2):
        l1 = np.array(l1)
        l2 = np.array(l2)
        data = np.array([l1, l2])
        corr_coeff = np.corrcoef(data)
        return corr_coeff[0][1]

    else:
        print ">Attention, different potential lenghts:\n>%s:%s\t%s:%s" %(id_tuple[0], len(l1), id_tuple[1], len(l2))

def euclidean_dist(l1, l2, id_tuple):
    if len(l1) == len(l2):
        l1 = np.array(l1)
        l2 = np.array(l2)
        euc_dist = np.linalg.norm(l1-l2)
        return euc_dist

    else:
        print ">Attention, different potential lenghts:\n>%s:%s\t%s:%s" %(id_tuple[0], len(l1), id_tuple[1], len(l2))

def main():
    #dir_name = 'global_ESP_trimmed_100'
    dir_name = 'fake_test'
    id_name = './%s/potential_id' %dir_name
    pot_name = './%s/potential.dat' %dir_name
    id_handle = open(id_name, 'r')
    id_lines = id_handle.readlines()
    id_lines = [l.split('\n', 1)[0] for l in id_lines]
    id_len = len(id_lines)
    pdb_pairs = itertools.combinations(range(id_len), 2)

    for i in pdb_pairs:
        id_tuple = (id_lines[i[0]], id_lines[i[1]])
        ln1, ln2 = read_two_lines(pot_name, i[0]+1, i[1]+1)
        l1 = ln1.split('\n')[0].split(' ')
        l2 = ln2.split('\n')[0].split(' ')
        del l1[-1] # removing last element of the list (empty)
        del l2[-1]
        l1 = [float(i) for i in l1]
        l2 = [float(i) for i in l2]
        euc_dist = euclidean_dist(l1, l2, id_tuple)

        print "%s\t%s\t%s" % (id_tuple[0], id_tuple[1], euc_dist)

main()

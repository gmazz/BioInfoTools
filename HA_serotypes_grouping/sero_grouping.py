import numpy as np
import pandas as pd
import itertools

"""
The NesteDict iterator class generates a nested dictionary to be easily filled and accessed.
Usage:

    >> To generate nested dicts and store values
    >> Note '...' is used in the example to represent an arbitrary number of level, is not a command symbol:

    nd = NestedDict()
    nd['level_1']['level_2'] ... ['level_n'] = 'value'

    >> To store a specific value:

    value =  nd['level_1']['level_2'] ... ['level_n']
"""
class NestedDict(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

"""
    The following method import both serotype and distance data and generate a sero dict and nested distance dict
    respectively. The nested distance dict is built to be accessed fast (avoiding inconvenient slow loops on lists)
"""
def import_data(par):

    #Istantiate
    pairs_distance = NestedDict()

    #Generate serogroups
    cl = pd.read_csv(par['data'], index_col=par['index_c'])
    cl_groups = cl.groupby('sero').groups

    #Generate  containing protein_pair:distance
    df = pd.read_csv(par['distance_data'], index_col=None)
    for index, row in df.iterrows():
        pairs_distance[row['p_id']][row['p_id2']] = row['distance']

    return cl_groups, pairs_distance

"""
This function compute the average distance within each serotype group.
All the permutation of the elements of each 'sero' dict entry are initially computed.
Permutations are used instead of combination because we don't know if we have:
'a,b,distance' or '(b,a,distance)' for a given pair.
Hence both options are considered. Anyway if one option is found, the inverted one is discarded
(as the results are equal)
"""
def merge(sero, pair_distance):
    done = []
    tmp_distance_list = []
    sero_main_values = dict()
    #for k, p_list in sero.items():
    #    print k, p_list
    tmp_permutations = itertools.permutations(sero['H10N7'], 2)

   # print '4cyw,4cz0,' + str(pair_distance['4cyw']['4cz0'])
   # print '4cz0,4cyw,' + str(pair_distance['4cz0']['4cyw'])
    for p in tmp_permutations:
        print p
        tmp_distance = pair_distance[p[0]][p[1]]
        if tmp_distance:
            tmp_distance_list.append(tmp_distance)
            done.append(p)
            done.append(p[::-1]) #Add the inverse tuple to
    print tmp_distance_list
    #sero_main_values = {'H10N7':[np.mean(tmp_distance_list), np.median(tmp_distance_list), np.std(tmp_distance_list)]}
    #print sero_main_values

def main():
    crystals_parameters = {
        'data' : './sero_lists/crystals_sero_list.csv',
        'index_c' : 'p_id',
        'distance_data' : './distances/crystals_rmsd.csv'
        }

    c_sero, c_pair_distance = import_data(crystals_parameters)
    merge(c_sero, c_pair_distance)

main()




#def merge(sero, pair_distance):
#    done = []
#    tmp_distance_list = []
#    sero_main_values = dict()
#    for k, p_list in sero.items():
#        tmp_permutations = itertools.permutations(p_list, 2)
#        for p in tmp_permutations:
#            tmp_distance = pair_distance[p[0]][p[1]]
#            if tmp_distance:
#                tmp_distance_list.append(tmp_distance)
#                done.append(p)
#                done.append(p[::-1]) #Add the inverse tuple to
#        sero_main_values = {k: [np.mean(tmp_distance_list), np.median(tmp_distance_list), np.std(tmp_distance_list)]}
#        tmp_distance_list = []
#        print sero_main_values

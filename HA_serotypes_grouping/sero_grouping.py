#import numpy as np
import pandas as pd


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


def main():
    crystals_parameters = {
        'data' : './sero_lists/crystals_sero_list.csv',
        'index_c' : 'p_id',
        'distance_data' : './distances/crystals_rmsd.csv'
        }

    sero, pairs_distance = import_data(crystals_parameters)


main()
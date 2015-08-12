import numpy as np
import pandas as pd
import time




def import_data():

    #Generate serogroups
    sero_c = pd.read_csv('./sero_lists/crystals_sero_list.csv', index_col='p_id')
    gb_c = sero_c.groupby('sero').groups

    #Generate dict containing protein_pair:distance
    #df_c = pd.read_csv('./distances/crystals_rmsd.csv', index_col='distance')
    #dfg_c = df_c.groupby(['p_id', 'p_id2']).groups
    #print dfg_c



import_data()
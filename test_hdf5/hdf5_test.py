import numpy as np
import pandas as pd
from pandas import *

def hdfs_gen():
    file_path = 'potential.dat'
    file_id = 'potential_id'
    header = []

    with open(file_path, 'r') as f:
        first_line = f.readline().split('\n')[0].split(' ')

    for i in range(len(first_line)-1):
        header.append("C%s" %i)

#    with open(file_id, 'r') as f:
#        id_lines = f.readlines()
#        id_list = [m.split('\n', 1)[0] for m in id_lines]

    #store = HDFStore('store.h5')
    tmp_df_list = pd.read_csv(file_path, index_col=False, names=header, sep=" ", chunksize=3)
    tmp_id_list = pd.read_csv(file_id, index_col=False, chunksize=3, header=False)

    for i in range (tmp_df_list.chunksize):
        df = tmp_df_list.__iter__().next()
        df_id = tmp_id_list.__iter__().next()
        df["id"] = df_id

    #    store.append('df', df)

def operate(df, row_a_num, row_b_num):
    pass
    axis = 0 # 0 == rows, 1 == columns
    #print df[1]
    #row_b = list(df.xs(2, axis))
    #return row_a

def read_store(store_path):
    store = HDFStore(store_path, 'r')
    df = store['df']
    operate(df, int(1), int(2))


hdfs_gen()
#read_store('store.h5')
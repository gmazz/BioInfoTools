import numpy as np
import pandas as pd


def read_data(table):
    df = pd.read_csv(table, sep=',', header=0, index_col=0)
    id = df.index.values
    M = df.values
    return id, M


table = 'data/RMSD_MCent_tab.txt'
id, M = read_data(table)

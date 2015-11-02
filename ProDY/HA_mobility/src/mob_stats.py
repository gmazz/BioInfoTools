import pandas as pd
import sys, os


def file_path(data_name):
    os.chdir('../data')
    root = os.getcwd()
    data_path = root + '/' + data_name
    os.chdir('../src')
    return data_path


def mob_stats(data_path):
    df = pd.read_csv(data_path, index_col=None)

data_name = 'crystals_mob.csv'
data_path = file_path(data_name)
mob_stats(data_path)


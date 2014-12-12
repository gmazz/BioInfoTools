import numpy as np
import pandas as pd
import sklearn.decomposition as deco
from operator import itemgetter
from sklearn.ensemble import ExtraTreesClassifier

def read_data(table):

    serotypes = []
    df = pd.read_csv(table, sep=',', header=0, index_col=0)
    id_list = df.index.values
    M = df.values
    ids = [id.split('.pdb')[0].split('_')[0] for id in id_list]

    id_sero_map = open('data/id_sero_map.txt', 'r')
    lines = id_sero_map.readlines()
    maps = [l.split('\n')[0].split(' ') for l in lines]

    for id in ids:
        try:
            serotypes.append(maps[map(lambda m: m[1].split('.pdb')[0], maps).index(id)][0])
        except:
            pass

    return id_list, M, serotypes

def PCA(M, n):
    pca = deco.PCA(n)
    M_rd = pca.fit(M).transform(M)
    print dir(M_rd)

def FS(M, y, id_list):
    clf = ExtraTreesClassifier()
    M_new = clf.fit(M, y).transform(M)
    fi = clf.feature_importances_
    id_fi = zip(id_list, fi)
    id_fi = sorted(id_fi, key=itemgetter(1), reverse=True)

    for item in id_fi:
        print item


table = 'data/RMSD_MCent_tab.txt'
id_list, M, serotypes = read_data(table)
FS(M, serotypes, id_list)
#PCA(M, 3)
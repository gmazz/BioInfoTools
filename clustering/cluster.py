import numpy as np
import pandas as pd
import sklearn.decomposition as deco
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

    print ids

    for id in ids:
        try:
            serotypes.append(maps[map(lambda m: m[1].split('.pdb')[0], maps).index(id)][0])
        except:
            pass
    #[serotypes.append(s) for s in m for m in maps[0]]
    #print ids, lines

    return id, M, serotypes

def PCA(M, n):
    pca = deco.PCA(n)
    M_rd = pca.fit(M).transform(M)
    print dir(M_rd)

def FS(M, y):
    clf = ExtraTreesClassifier()
    M_new = clf.fit(M, y).transform(X)
    clf.feature_importances_


table = 'data/RMSD_MCent_tab.txt'
id, M, serotypes = read_data(table)
#PCA(M, 3)
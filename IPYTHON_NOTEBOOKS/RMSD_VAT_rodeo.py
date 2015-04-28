import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
%matplotlib inline

# RMSD data
df = pd.read_csv('/Users/johnny/github_home/BioInfoTools/IPYTHON_NOTEBOOKS/data/models_v2/RMSD.csv')
df = df.pivot(index='p_id', columns='p_id2', values='rmsd')
df = df.fillna(0)

# Subtype "classes"
maps = pd.read_csv('/Users/johnny/github_home/BioInfoTools/IPYTHON_NOTEBOOKS/data/models_v2/class_rev.csv', index_col='p_id')
# Reversing order
maps_rev = maps.sort(['sero'], ascending=[0])

data = df.loc[maps.index, maps.index]
plt.imshow(data, interpolation='None')

# Table subselection for testing

n_init_m = 0
n_end_m = len(table.index)
selection_m = table.ix[n_init_m:n_end_m, n_init_m:n_end_m]

#d = maps.sero.to_dict()

# Grouping elements by maps.subtypes (useful for statistics)
subtype_group = maps.groupby('sero').size()
#subtype_group

# Take the class names (ref and cl lists can be used for serotype/protein data labeling)
ref = data.index
cl = [maps.sero[i] for i in ref]

# Cell for plotting heatmap
def plot():
    %matplotlib inline
    fig = plt.figure(figsize=(30, 30), dpi=80)

    plt.pcolor(data, cmap=plt.cm.Blues)
    #plt.xticks(np.arange(min(data.index), max(data.index)+10, fontsize=30))
    plt.xticks(np.arange(0.5, len(data.index), 1), cl, fontsize=5, rotation='vertical')
    plt.yticks(np.arange(0.5, len(data.columns), 1), cl, fontsize=5, rotation='horizontal')
    #plt.show()
    
    fig1 = plt.gcf()
    #plt.show()
    #plt.draw()
    fig1.savefig('VAT_dataset_II.png', dpi=300)
    
plot()
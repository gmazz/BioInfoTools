
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
import sys, os
import collections
from collections import OrderedDict
import matplotlib.pyplot as plt
import Bio
import sklearn


# ### This section is for table reading:

# In[2]:

os.chdir('../data')
root = os.getcwd()
data = root + '/affinity_data.csv'
peptide_file = root + '/binding_peptides.fas'
HLA_file = root + '/HLA_aln.fas'

def to_number(s):
    try:
        s1 = float(s)
        return s1
    except ValueError:
        return s

os.chdir('../src')


# In[69]:

# Additional block for data manipulation

#data_ref = root+'/affinity_data_refined.csv'
#df = df.replace('-', 50000)
#res = df.applymap(lambda x: to_number(x))
#res['DPB1:04:01'][0]
#df.to_csv(data_ref,sep=',', mode='w', index=False)


# ### Data distribution check

# In[522]:

df = pd.read_csv(data, index_col=0)
data_matrix = df.as_matrix()
df.stack().hist(color='k', alpha=0.5, bins=100)
plt.show()
Y_dist_tmp = [i for i in list(data_matrix.flatten().astype(int)) if i < 50000]
Y_dist = np.array(Y_dist_tmp)


# In[523]:

import numpy as np 
import pylab 
import scipy.stats as stats
from scipy.stats import expon
from scipy.stats import poisson

#expon_example = np.random.exponential(scale=50000, size=17000)
#measurements = np.where(expon_example >= 50000)[0]

stats.probplot(Y_dist, dist="norm", plot=pylab)
#r = stats.poisson.rvs(1.5)
#r = expon.ppf([0.001, 0.5, 0.999])
#r = stats.poisson(2)
#r = stats.
stats.probplot(Y_dist, dist=r, plot=pylab)
pylab.show()


# ### Nested Dict HLA-peptide IC50: 

# In[3]:

class NestedDict(dict):
    def __missing__(self, key):
        self[key] = type(self)()
        return self[key]

affinity = NestedDict()     
df = pd.read_csv(data, index_col=0)
for k,v in df.stack().iteritems():
    affinity[k[0]][k[1]] = v


# ### HQI function

# In[4]:

from encode_HQI8 import *
from Bio import SeqIO
import itertools

'''
#Itertools chaining example: 
a = [[1,2,3],[4,5,6]]
list(itertools.chain(*a))
'''

def encode_seq(entry):
    tmp = encode_aaindex_features(entry)
    aaindex = list(itertools.chain(*tmp))    
    return aaindex

# This operation normalize the data 
def encode_seq_norm(entry, max_vals, min_vals):
    delta = max_vals - min_vals
    tmp = encode_aaindex_features(entry)
    vals = list(itertools.chain(*[list((t - min_vals)/delta) for t in tmp]))
    return vals
    
def min_max(entry):
    tmp = encode_aaindex_features(entry)
    max_vals = np.amax(tmp, axis=0)
    min_vals = np.amin(tmp, axis=0)
    return max_vals, min_vals

#res_1 = encode_seq('MASSSSVLLVVVLFA')
#res_2 = encode_seq_norm('MASSSSVLLVVVLFA', max_vals, min_vals)
#print res_1
#print res_2


# ### Featurizing function

# In[5]:

def featurize(entries):
    max_vals, min_vals = min_max('GAVLIPFYWSTCMNQKRHDE')
    feature_dict = {}
    for e in entries[0:]:
        feature_dict[e.id] = encode_seq(e.seq)                         # Not-normalized data
        #feature_dict[e.id] = encode_seq_norm(e.seq, max_vals, min_vals) # Normalized data
    return feature_dict


# ### Peptide features: 

# In[6]:

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC

peptides = list(SeqIO.parse(peptide_file, 'fasta'))
pep_dict = featurize(peptides)
#pep_dict

rec_test = SeqRecord(Seq(''.join('Q'), IUPAC.protein), id='id')
#featurize([rec_test])


# ### HLA descriptors' features:

# In[7]:

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC

HLAs = list(SeqIO.parse(HLA_file, 'fasta'))
HLA_desc = OrderedDict([
                        ('b9', 40),
                        ('b11', 42),
                        ('b13', 44),
                        ('b28', 59),
                        ('b30', 61),
                        ('b37', 68),
                        #('b47', 78), # Y or W
                        ('b57', 88),
                        #('b60', 91), # constant
                        #('b61', 92), # constant
                        ('b67', 98),
                        ('b70', 101), # *
                        ('b71', 102), # *
                        ('b74', 105), # *
                        ('b78', 109), # *
                        #('b81', 112), # almost constant
                        #('b82', 113), # almost constant
                        #('b85', 116), # almost constant
                    ])

def make_SeqRecord(HLAs, HLA_desc):
    HLA_list = []
    for h in HLAs:
        #print h.id, h.seq[HLA_descriptors['b9']], h.seq[HLA_descriptors['b11']], h.seq[HLA_descriptors['b13']]
        sele = [h.seq[i] for i in HLA_desc.values()]
        #print h.id, ''.join(sele)
        record = SeqRecord(Seq(''.join(sele),
                   IUPAC.protein),
                   id=h.id)
        HLA_list.append(record)
    return featurize(HLA_list)

    
HLAs_dict = make_SeqRecord(HLAs, HLA_desc)


# ### Data preparation

# This section allows to prepare the data for the regression analysis, without reading it from external files.
# This allows to easly modify the features used in the regression procedure.

# In[9]:

features_len = len(HLA_desc) * len(HQI8_descriptors) + 15 * len(HQI8_descriptors)
features_count = ['f'+ str(i) for i in range(1,features_len+1)]
features_count.insert(0,'HLA')
features_count.insert(0,'peptide')
features_count.append('IC50')

def get_xy():
    tmp_list = []

    # Iterates over the elements within the 2-level dict
    for k1,v1 in affinity.iteritems():
        for k2,v2 in v1.iteritems():
            tmp_i = list(itertools.chain(*[list([k1]), list([k2]), pep_dict[k1], HLAs_dict[k2], list([int(v2)])]))
            tmp_list.append(tmp_i)
            #list_y.append(y_i)

    return np.array(tmp_list)#, np.array(list_y)

df = pd.DataFrame(get_xy(), columns=features_count)

# Type checking
df[features_count[2:-1]] = df[features_count[2:-1]].astype(np.float32) # This changes all features into floats
df['IC50'] = df['IC50'].astype(np.integer) 


# ### Combining HLA/peptide features with affinity value into new file:

# In[10]:

fo = open('dataset_norm_v2.csv', 'a+')
features_len = len(HLA_desc) * len(HQI8_descriptors) + 15 * len(HQI8_descriptors)
features_count = ['f'+ str(i) for i in range(1,features_len+1)]
header = 'id,peptide,HLA,' + ','.join(str(x) for x in features_count) + ',IC50\n'
fo.write(header)


# In[11]:

# Iterates over the elements within the 2-level dict
i=1
for k,v in affinity.iteritems():
    for k1,v1 in v.iteritems():
        features = list(itertools.chain(*[pep_dict[k], HLAs_dict[k1]]))
        #message = k + '\t' + k1 + '\t' + ','.join(str(x) for x in features) + '\t' + str(v1) + '\n'
        #message = k + '_' + k1 + ',' + ','.join(str(x) for x in features) + ',' + str(v1) + '\n'
        message = str(i) + ',' + k + ',' + k1 + ',' +','.join(str(x) for x in features) + ',' + str(v1) + '\n'
        fo.write(message)
        i += 1


# #### Read data from new file:

# In[140]:

#Just in case you want to read the file
#df = pd.read_csv('../dataset/dataset_norm_v2.csv', index_col=0)


# ### Data -> X, y

# In[37]:

#Filter data y>0, y<50000
df = df[df.IC50 > 0]
df = df[df.IC50 < 50000]
#df = df[~((df.IC50 < 0) & (df.IC50 > 50000))]
df = df.reset_index(drop=True) # Important for re-indexing 
print df

#Generate Training and testing 
def train_test(df, perc):
    sele = []
    while len(sele) <= int(len(df) * perc):
        sele.append(np.random.randint(len(df)))
        sele = list(set(sele))
    
    X_test = df.ix[sele]
    y_test = df.IC50[sele]
    X_train = df.drop(df.index[sele])
    y_train = df.IC50.drop(df.index[sele])
    
    X_test = X_test.reset_index(drop=True)
    y_test = y_test.reset_index(drop=True)
    X_train = X_train.reset_index(drop=True)
    X_train = X_train.reset_index(drop=True)
    
    X_test = X_test.drop(['IC50','peptide','HLA'], axis=1)
    X_train = X_train.drop(['IC50','peptide','HLA'], axis=1)

    # We initially transform the data into 
    #X = X_df.as_matrix()
    #y = y_df.as_matrix()
    #target_names = X_df.columns.values
    return X_test.as_matrix(), y_test.as_matrix(), X_train.as_matrix(), y_train.as_matrix()


# ### PCA

# In[283]:

print(__doc__)

import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.lda import LDA

n_comp = 250
pca = PCA(n_components=n_comp)
X_r = pca.fit(X).transform(X)

# Percentage of variance explained for each components
#print('explained variance ratio (first %s components): \n %s') %(n_comp, str(pca.explained_variance_ratio_))
eigenv = pca.explained_variance_ratio_
plt.bar (range(len(eigenv)), eigenv)
plt.show()


# ### Feature selection 

# In[699]:

import sklearn.feature_selection
from sklearn.ensemble import RandomForestRegressor
#f_select = sklearn.feature_selection.f_regression(X_train, y_train, center=True)
#f_select
X_test, y_test, X_train, y_train =  train_test(df, 1)
transform(X_train, threshold=None)


# In[13]:

import operator
feat_zip = zip(f_select[1], list(target_names))


# In[147]:

#a = [1,4,3,2]
#b = ['a','d','c','b']
#[(x,y) for (y,x) in sorted(zip(a,b))]


# In[70]:

import math

def feat_seed(num):
    res = math.floor((num - 0.1)/4) + 1
    return int(res)

test_dict = {}
feat_importance = [(x,y) for (y,x) in sorted(zip(f_select[1],list(target_names)))]
feats = [str(feat_seed(int(x[1:]))) for (y,x) in sorted(zip(f_select[1],list(target_names)))] # AA importance rank
points = list(reversed(range(1, len(feats)+1)))
feat_points = zip(feats, points)

feat_points
for i in feat_points:
    if test_dict[i[0]]:
        test_dict[i[0]] = test_dict[i[0]] + i[1]
    else:
        test_dict[i[0]] = i[1]


# ### Regression Tree Model 

# In[ ]:

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
#from sklearn.metrics import accuracy_score
#from sklearn.cross_validation import cross_val_score

params = {
            'perc': 0.01,
            'n_estimators' : 3000,
            'max_features': "sqrt",
            'n_jobs' : -1
        }
    
def regressor(params):
    X_test, y_test, X_train, y_train =  train_test(df, params['perc'])
    print "Training points: %s, Testing points: %s" %(len(y_train), len(y_test))
    estimator = RandomForestRegressor(random_state=0, n_estimators=params['n_estimators'], n_jobs=params['n_jobs'])
    estimator.fit(X_train, y_train)
    y_estimated = estimator.predict(X_test)
    score = r2_score(y_test, y_estimated, sample_weight=None)
    return score, y_test, y_estimated

score, y_test, y_estimated = regressor(params)
residuals = y_test - y_estimated
print score
#estimator.score(X, y, sample_weight=None)


# In[689]:

# Residuals distribution
import numpy as np
import matplotlib.pyplot as plt

import numpy as np
#plt.hist(data, bins=np.arange(min(data), max(data) + binwidth, binwidth))

plt.hist(residuals, color='k', alpha=0.5, bins=10)

plt.show()


# In[102]:

from sklearn.metrics import r2_score

# Testing in sample prediction
def score_fun(X, y, estimator):
    sample_weight = None
    return r2_score(y, estimator.predict(X), sample_weight=sample_weight)

score_fun(X, y, estimator)


# ### Gradient Boosted Regression Tree (GBRT)

# In[ ]:

from sklearn.ensemble import GradientBoostingRegressor

gbrt_params = {
            'perc': 0.01,
            'n_estimators': 1000,
            'n_jobs' : -1
        }


def gbrt_regressor(gbrt_params):
    X_test, y_test, X_train, y_train =  train_test(df, gbrt_params['perc'])
    print "Training points: %s, Testing points: %s" %(len(y_train), len(y_test))
    gbrt_estimator = GradientBoostingRegressor(n_estimators=gbrt_params['n_estimators'])
    gbrt_estimator.fit(X_train, y_train)
    y_estimated = gbrt_estimator.predict(X_test)
    score = r2_score(y_test, y_estimated, sample_weight=None)
    return score, y_test, y_estimated

gbrt_score, gbrt_y_test, gbrt_y_estimated = gbrt_regressor(gbrt_params)
gbrt_residuals = gbrt_y_test - gbrt_y_estimated
print gbrt_score





# ### Regression tree test

# In[66]:

import numpy as np
from sklearn.preprocessing import LabelEncoder  
from sklearn.ensemble import RandomForestRegressor

X_test = np.asarray([('a',1,2),('b',2,3),('a',3,2),('c',1,3)]) 
y_test = np.asarray([1,2.5,3,4])

# transform 1st column to numbers
X_test[:, 0] = LabelEncoder().fit_transform(X_test[:,0]) 

regressor = RandomForestRegressor(n_estimators=150, min_samples_split=1)
regressor.fit(X_test, y_test)
print X_test
print y_test
print regressor.predict(X_test)


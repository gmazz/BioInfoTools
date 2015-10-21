
import numpy as np
import pandas as pd
import sys, os
import sklearn
import collections
from collections import OrderedDict
import matplotlib.pyplot as plt
import sklearn
from encode_HQI8 import *
from Bio import SeqIO
import itertools
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import time



# >>Try to assign Float type

def to_number(s):
    try:
        s1 = float(s)
        return s1
    except ValueError:
        return s


# >> Nested Dict HLA-peptide IC50:

class NestedDict(dict):
    def __missing__(self, key):
        self[key] = type(self)()
        return self[key]


# >> HQI function

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


# >>  Featurizing function

def featurize(entries):
    max_vals, min_vals = min_max('GAVLIPFYWSTCMNQKRHDE')
    feature_dict = {}
    for e in entries[0:]:
        feature_dict[e.id] = encode_seq(e.seq)                         # Not-normalized data
        #feature_dict[e.id] = encode_seq_norm(e.seq, max_vals, min_vals) # Normalized data
    return feature_dict


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


def get_xy(affinity, pep_dict, HLAs_dict):
    tmp_list = []
    # Iterates over the elements within the 2-level dict
    for k1,v1 in affinity.iteritems():
        for k2,v2 in v1.iteritems():
            tmp_i = list(itertools.chain(*[list([k1]), list([k2]), pep_dict[k1], HLAs_dict[k2], list([int(v2)])]))
            tmp_list.append(tmp_i)
    return np.array(tmp_list)



# >> Generate Training and testing

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

    return X_test.as_matrix(), y_test.as_matrix(), X_train.as_matrix(), y_train.as_matrix()



# >> Regression Model functions

def regressor(params, df):
    X_test, y_test, X_train, y_train =  train_test(df, params['perc'])
    #print "\tTraining points: %s, Testing points: %s" %(len(y_train), len(y_test))
    estimator = RandomForestRegressor(random_state=0, n_estimators=params['n_estimators'], n_jobs=params['n_jobs'])
    estimator.fit(X_train, y_train)
    y_estimated = estimator.predict(X_test)
    score = r2_score(y_test, y_estimated, sample_weight=None)
    return score, y_test, y_estimated


# >> Gradient Boosted Regression Tree (GBRT)


def gbrt_regressor(gbrt_params, df):
    X_test, y_test, X_train, y_train =  train_test(df, gbrt_params['perc'])
    #print "\tTraining points: %s, Testing points: %s" %(len(y_train), len(y_test))
    gbrt_estimator = GradientBoostingRegressor(n_estimators=gbrt_params['n_estimators'])
    gbrt_estimator.fit(X_train, y_train)
    y_estimated = gbrt_estimator.predict(X_test)
    score = r2_score(y_test, y_estimated, sample_weight=None)
    return score, y_test, y_estimated


# >> Visualization of residuals distribution

def residuals_distribution():
    plt.hist(residuals, color='k', alpha=0.5, bins=10)
    plt.show()

######################## Main function ######################
def iterator(params, df, method_name):

    out_file_1 = open('%s_results.txt' %method_name, 'a+')
    out_file_2 = open('%s_results_repetitions.txt' %method_name, 'a+')
    out_file_1.write('n_trees,mean_r2_score,timestamp\n')
    scores = []
    runs = {}
    step = 50
    n_steps = 40
    repetitions = 5
    params['n_estimators'] = 0
    print "* Computing %s ..." % method_name
    for i in range(n_steps):
        params['n_estimators'] = params['n_estimators'] + step
        for j in range(repetitions):
            if method_name == 'RT':
                score, y_test, y_estimated = regressor(params, df)
                scores.append(score)
            elif method_name == 'GBRT':
                score, y_test, y_estimated = gbrt_regressor(params, df)
                scores.append(score)

        runs[params['n_estimators']] = scores
        print "n_trees: %s, mean_R2_score: %s" %(params['n_estimators'], np.mean(scores))
        message_1 = "%s,%s,%s\n" %(params['n_estimators'], np.mean(scores), time.time())
        message_2 = "%s,%s,%s\n" %(params['n_estimators'], ','.join([str(s) for s in scores]), time.time())
        out_file_1.write(message_1)
        out_file_2.write(message_2)
        scores = []

def main():

    # This section is for table reading:

    os.chdir('../data')
    root = os.getcwd()
    data = root + '/affinity_data.csv'
    peptide_file = root + '/binding_peptides.fas'
    HLA_file = root + '/HLA_aln.fas'
    os.chdir('../src')

    affinity = NestedDict()
    df = pd.read_csv(data, index_col=0)
    for k, v in df.stack().iteritems():
        affinity[k[0]][k[1]] = v
    print "\n* Affinity dictionary generated ..."

    # Peptide featurization:

    peptides = list(SeqIO.parse(peptide_file, 'fasta'))
    pep_dict = featurize(peptides)
    rec_test = SeqRecord(Seq(''.join('Q'), IUPAC.protein), id='id')
    print "* Peptides have been featurized ..."


    # HLA featurization:

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
    HLAs_dict = make_SeqRecord(HLAs, HLA_desc)
    print "* HLAs have been featurized ..."


    # >> Data preparation
    # This section allows to prepare the data for the regression analysis, without reading it from external files.
    # This allows to easly modify the features used in the regression procedure.

    features_len = len(HLA_desc) * len(HQI8_descriptors) + 15 * len(HQI8_descriptors)
    features_count = ['f'+ str(i) for i in range(1,features_len+1)]
    features_count.insert(0,'HLA')
    features_count.insert(0,'peptide')
    features_count.append('IC50')
    df = pd.DataFrame(get_xy(affinity, pep_dict, HLAs_dict), columns=features_count)
    print "* Data aggregation completed: the dataframe has been successfully generated ..."

    # >> Type checking

    df[features_count[2:-1]] = df[features_count[2:-1]].astype(np.float32) # This changes all features into floats
    df['IC50'] = df['IC50'].astype(np.integer)


    # >> Data -> X, y

    #Filter data y>0, y<50000
    df = df[df.IC50 > 0]
    df = df[df.IC50 < 50000]
    #df = df[~((df.IC50 < 0) & (df.IC50 > 50000))]
    df = df.reset_index(drop=True) # Important for re-indexing


    # >> Regressors: RFR

    rf_params = {
        'perc': 0.01,
        'n_estimators': 5000,
        'max_features': 'sqrt',
        'n_jobs': -1
    }


    # >> Regressors: GBRT

    gbrt_params = {
            'perc': 0.01,
            'n_estimators': 5000,
            'n_jobs': -1
        }

    #iterator(rf_params, df, 'RF')
    iterator(gbrt_params, df, 'GBRT')

main()

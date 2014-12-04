import numpy as np
import os, sys, re
from pandas import *
from sklearn.decomposition import PCA


def generate_table(in_file):
    file_id = in_file.split('.txt')[0]
    file_handle = open()
    out_name = '%s_tab.txt' % file_id
    a = np.empty((1203, 1203,))
    a[:] = np.NAN



    #pca = PCA(n_components=5)
    #pca_res = pca.fit(table)

    return data, table

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print """
            ####################################################################################################
            #                                                                                                  #
            #     Please indicate the input file within the "data" directory that you're intending to use.     #
            #     e.g.: $ RMSD_metric_II.py scores_global_trimmed_refactor.dat                                 #
            #                                                                                                  #
            #     Please also be sure that the format of your input file is like follows:                      #
            #                                                                                                  #
            #     AEI30056,AEO91855,0.49                                                                       #
            #     AEI30056,AHA57155,0.47                                                                       #
            #                        ...                                                                       #
            #                                                                                                  #
            ####################################################################################################
              """

    in_file = sys.argv[1]
    data, table = generate_table(in_file)

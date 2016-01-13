import os, sys, re
import numpy

# Script to calculate all the RMSD among all the PDBs within a given directory using the TMalign method.


rootdir = os.getcwd()
lst_files = os.listdir(rootdir)
score_list = []

for f in lst_files:
    if '_scores.txt' in f:
        score_list.append(f)

def metrics(score_list):

    for f in score_list:

        tmp_handle = open(f,'r')
        read_file = tmp_handle.readlines()
        RMSD_array = []
        TM_score_array = []


        for ln in read_file:
            values = ln.split('\t')
            if '.pdb' in values[0]:
                RMSD_array.append(float(values[2]))
                TM_score_array.append(float(values[3]))


        RMSD_np = numpy.array(RMSD_array)
        TM_score_np = numpy.array(TM_score_array)

        RMSD_mean = numpy.mean(RMSD_np)
        RMSD_median = numpy.median(RMSD_np)
        RMSD_std = numpy.std(RMSD_np)

        TM_mean = numpy.mean(TM_score_np)
        TM_median = numpy.median(TM_score_np)
        TM_std = numpy.std(TM_score_np)


        print "\n%s :\nRMSD_mean: %s\tRMSD_median: %s\tRMSD_std: %s\nTM_score_mean: %s\tTM_score_median: %s\tTM_score_std: %s" % (f, RMSD_mean, RMSD_median, RMSD_std, TM_mean, TM_median, TM_std)

metrics(score_list)


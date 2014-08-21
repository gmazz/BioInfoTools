from pymol import *
import os, sys, re
import itertools
import subprocess
import numpy

# Script to calculate all the RMSD among all the PDBs within a given directory using the TMalign method.


rootdir = os.getcwd()
lst_files = os.listdir(rootdir)
list_pdb = []

for f in lst_files:
    if '.pdb' in f:
        list_pdb.append(f)


def TM_RMSD():


    RMSD_array = []
    TM_score_array = []

    for f in pdb_pairs:

        cmd = 'TMalign %s %s -a' %(f[0], f[1])
        result = subprocess.check_output(cmd, shell=True)
        ln_result = result.split('\n')

        RMSD_line = ln_result[16].split(',')[1]
        TM_score_line = ln_result[19]

        regexp_score = re.compile("([A-Za-z\s\W]+)([\d\.]+)")

        RMSD = regexp_score.match(RMSD_line).group(2)
        TM_score = regexp_score.match(TM_score_line).group(2)

        RMSD_array.append(float(RMSD))
        TM_score_array.append(float(TM_score))

        print "%s\t%s\t%s\t%s" % (f[0], f[1], RMSD, TM_score)

    RMSD_np = numpy.array(RMSD_array)
    TM_score_np = numpy.array(TM_score_array)

    RMSD_mean = numpy.mean(RMSD_np)
    RMSD_median = numpy.median(RMSD_np)
    RMSD_std = numpy.std(RMSD_np)

    TM_mean = numpy.mean(TM_score_np)
    TM_median = numpy.median(TM_score_np)
    TM_std = numpy.std(TM_score_np)


    print "\nRMSD_mean: %s\tRMSD_median: %s\tRMSD_std: %s\nTM_score_mean: %s\tTM_median: %s\tTM_score_std: %s" % (RMSD_mean, RMSD_median, RMSD_std, TM_mean, TM_median, TM_std)

pdb_pairs = itertools.combinations(list_pdb, 2)
pairs_number = len(list(itertools.combinations(list_pdb, 2)))
TM_RMSD()

print "Total pairs number: %s" %pairs_number
import os, sys, re
import itertools
import subprocess
import numpy
import Bio

from multiprocessing import Pool
import affinity

# Script to calculate all the RMSD among all the PDBs within a given directory using the TMalign method.
# Note: It takes the best TM_score

def set_affinity():
    affinity.set_process_affinity_mask(os.getpid(), 0xFFFFFFFF)   


#def TM_align(f):
#    return f, subprocess.check_output('TMalign %s %s -a' %(f[0], f[1]), shell=True)

def TM_RMSD():

    file_out = open('scores','w')
    RMSD_array = []
    TM_score_array = []
    pool = Pool(processes=8, initializer=set_affinity)
    results = pool.map(TM_align, pdb_pairs)
    pool.close()
    pool.join()

    for f, result in results:
        ln_result = result.split('\n')
        RMSD_line = ln_result[16].split(',')[1]
        TM_score_line_1 = ln_result[17]
        TM_score_line_2 = ln_result[18]
        regexp_score = re.compile("([A-Za-z\s\W]+)([\d\.]+)")
        RMSD = regexp_score.match(RMSD_line).group(2)
        TM_score_p1 = regexp_score.match(TM_score_line_1).group(2)
        TM_score_p2 = regexp_score.match(TM_score_line_2).group(2)
        TM_max=max([float(TM_score_p1), float(TM_score_p2)])
        RMSD_array.append(float(RMSD))
        TM_score_array.append(float(TM_max))
        message = "%s\t%s\t%s\t%s\n" % (f[0], f[1], RMSD, TM_max)

    file_out.write(message)
    RMSD_np = numpy.array(RMSD_array)
    TM_score_np = numpy.array(TM_score_array)
    RMSD_mean = numpy.mean(RMSD_np)
    RMSD_median = numpy.median(RMSD_np)
    RMSD_std = numpy.std(RMSD_np)
    TM_mean = numpy.mean(TM_score_np)
    TM_median = numpy.median(TM_score_np)
    TM_std = numpy.std(TM_score_np)


    print "\nRMSD_mean: %s\tRMSD_median: %s\tRMSD_std: %s\nTM_score_mean: %s\tTM_score_median: %s\tTM_score_std: %s" % (RMSD_mean, RMSD_median, RMSD_std, TM_mean, TM_median, TM_std)


rootdir = os.getcwd()
lst_files = os.listdir(rootdir)
list_pdb = []

#for f in lst_files:
#    if '.pdb' in f:
#        list_pdb.append(f)


pdb_pairs = itertools.combinations(list_pdb, 2)
pairs_number = len(list(itertools.combinations(list_pdb, 2)))
TM_RMSD()
print "Total pairs number: %s" %pairs_number

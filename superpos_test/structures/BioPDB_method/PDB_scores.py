# This script print the TMscore and RMSD scores of all the bigram combinations of PDB file in a give directory.

from pymol import *
import os, sys, re
import itertools
import subprocess

rootdir = os.getcwd()
lst_files = os.listdir(rootdir)
list_pdb = []

for f in lst_files:
    if '.pdb' in f:
        list_pdb.append(f)


def TM_RMSD():
    for i in pdb_pairs:
        cmd = "TMscore %s %s" % (i[0], i[1])
        result = subprocess.check_output(cmd, shell=True)
        ln_result = result.split('\n')

        N_CR_line = ln_result[13]
        RMSD_line = ln_result[14]
        TM_score_line = ln_result[16]
        MaxSub_line = ln_result[17]

        regexp_score = re.compile("([A-Za-z\s\W]+)([\d\.]+)")
        RMSD = regexp_score.match(RMSD_line).group(2)
        TM_core = regexp_score.match(TM_score_line).group(2)
        print "%s\t%s\t%s\t%s" % (i[0], i[1], RMSD, TM_core)


pdb_pairs = itertools.combinations(list_pdb, 2)
TM_RMSD()

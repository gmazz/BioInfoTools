# This script print the TMscore and RMSD scores of elements with same name, but within different directories (e.g. D1, D2).
# Is a simple way to test two series of models generated from the same sequences but using different methods.

from pymol import *
import os, sys, re
import itertools
import subprocess


def pdb_lists():
    rootdir = os.getcwd()
    D1 = "%s/D1" % rootdir
    D2 = "%s/D2" % rootdir

    D1_files = os.listdir(D1)
    D2_files = os.listdir(D2)
    D1_pdb = []
    D2_pdb = []

    for f in D1_files:
        if '.pdb' in f:
            D1_pdb.append(f)

    for f in D2_files:
        if '.pdb' in f:
            D2_pdb.append(f)

    return D1_pdb, D2_pdb


def TM_RMSD(D1_i, D2_i):
    rootdir = os.getcwd()
    cmd = "TMscore ./D1/%s ./D2/%s" % (D1_i, D2_i)
    result = subprocess.check_output(cmd, shell=True)
    ln_result = result.split('\n')

    N_CR_line = ln_result[13]
    RMSD_line = ln_result[14]
    TM_score_line = ln_result[16]
    MaxSub_line = ln_result[17]

    regexp_score = re.compile("([A-Za-z\s\W]+)([\d\.]+)")
    RMSD = regexp_score.match(RMSD_line).group(2)
    TM_core = regexp_score.match(TM_score_line).group(2)
    print "%s\t%s\t%s\t%s" % (D1_i, D2_i, RMSD, TM_core)


def iterator(D1, D2):
    for k in D2:
        pdb_id = k.split('.pdb')[0]
        D1_id = "%s_D1.pdb" % pdb_id
        if D1_id in D1:
            TM_RMSD(str(k), str(D1_id))


tmp = []
D1, D2 = pdb_lists()
iterator(D1, D2)

# TM_RMSD("AB551875_GM.pdb", "AB551875.pdb")
#pdb_pairs = itertools.combinations(list_pdb, 2)


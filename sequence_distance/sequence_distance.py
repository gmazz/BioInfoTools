import os, sys, re
import itertools
from Bio import SeqIO

#import subprocess
#from multiprocessing import Pool
#import affinity

# Script to calculate protein distances among all the sequences within a given MSA using the pairwise2 library from BioPython.

#def set_affinity():
#    affinity.set_process_affinity_mask(os.getpid(), 0xFFFFFFFF)


def entry_read(fasta_file):
    records = list(SeqIO.parse(fasta_file, 'fasta'))
    print records[1]


    #file_out = open('scores','w')
    #RMSD_array = []
    #TM_score_array = []
    #pool = Pool(processes=8, initializer=set_affinity)
    #results = pool.map(TM_align, pdb_pairs)
    #pool.close()
    #pool.join()

    #for f, result in results:
    #    ln_result = result.split('\n')
    #    RMSD_line = ln_result[16].split(',')[1]
    #    TM_score_line_1 = ln_result[17]
    #    TM_score_line_2 = ln_result[18]
    #    regexp_score = re.compile("([A-Za-z\s\W]+)([\d\.]+)")
    #    RMSD = regexp_score.match(RMSD_line).group(2)
    #    TM_score_p1 = regexp_score.match(TM_score_line_1).group(2)
    #    TM_score_p2 = regexp_score.match(TM_score_line_2).group(2)
    #    TM_max = max([float(TM_score_p1), float(TM_score_p2)])
    #    RMSD_array.append(float(RMSD))
    #    TM_score_array.append(float(TM_max))
    #    message = "%s\t%s\t%s\t%s\n" % (f[0], f[1], RMSD, TM_max)


#pdb_pairs = itertools.combinations(list_pdb, 2)
#pairs_number = len(list(itertools.combinations(list_pdb, 2)))
#TM_RMSD()
#print "Total pairs number: %s" %pairs_number

def main():
    fasta_file = 'crystals.fas'
    entry_read(fasta_file)

main()
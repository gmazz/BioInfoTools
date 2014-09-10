import os, sys, re
import itertools
from collections import defaultdict
import subprocess
import numpy


class scoreObj(object):

    def __init__(self, ID_tuple):
        self.ID_tuple = ID_tuple
        self.RMSD_list = []
        self.TMscore_list = []

    def scores_update(self, RMSD, TMscore):
        self.RMSD = RMSD
        self.TMscore = TMscore
        self.RMSD_list.append(self.RMSD)
        self.TMscore_list.append(self.TMscore)

    def give_RMSD(self):
        return self.RMSD_list

    def give_TMscore(self):
        return self.TMscore_list


class seroList(object):

    def __init__(self, seroID, serolist):
        self.seroID = seroID
        self.serolist = serolist

    def ID_get(self):
        return self.seroID

    def mlist_get(self):
        return self.serolist

def data_import(list_dir, scores_file):
    rootdir = os.getcwd()
    models_list_dir = '%s/%s/' %(rootdir, list_dir)
    list_files = os.listdir(models_list_dir)

    scores_file = '%s/%s' %(rootdir, scores_file)
    file_handle = open(scores_file)
    data_lines = file_handle.readlines()
    return list_files, data_lines

def sero_obj_list_generation(model_dir, list_files):
    sero_obj_list = []
    for f in list_files:
        fname = '%s/%s' %(model_dir, f)
        seroID = f.split('.txt')[0]
        file_handle = open(fname)
        serolines = file_handle.readlines()
        serolist = [m.split('\n', 1)[0] for m in serolines]
        tmp_sero_obj = seroList(seroID, serolist)
        sero_obj_list.append(tmp_sero_obj)
    return sero_obj_list

def list_combination(list_files):
    list_id = [l.split('.txt', 1)[0] for l in list_files]
    list_combo = itertools.combinations_with_replacement(list_id, 2)
    #list_combo = [set(elem) for elem in list_combo]
    return list_combo

def model_sero_assoc(model, sero_obj_list):
    sero_target = [obj.seroID for obj in sero_obj_list if model in obj.serolist]
    return sero_target[0] #takes just one of the possible elements


def object_update(data_lines, objs, sero_obj_list):
    for line in data_lines:
        line = line.split('\n')[0]
        values = line.split('\t')

        model_a = values[0].split('.pdb')[0]
        model_b = values[1].split('.pdb')[0]
        sero_a = model_sero_assoc(model_a, sero_obj_list)
        sero_b = model_sero_assoc(model_b, sero_obj_list)
        serotuple = (sero_a, sero_b)
        RMSD = values[2]
        TMscore = values[3]

        for obj in objs:
            if (sorted(serotuple) == sorted(obj.ID_tuple)):
                obj.scores_update(RMSD, TMscore)

def metrics(objs):
    for o in objs:
        print o.ID_tuple
        print o.RMSD_list[1:10]
        print o.TMscore_list[1:10]

        # TO BE COMPLETED


def main():
    model_dir = 'model_lists'
    list_files, data_lines = data_import(model_dir, 'all_vs_all_correct.txt')
    sero_obj_list = sero_obj_list_generation(model_dir, list_files)

    list_combo = list_combination(list_files)
    objs = [scoreObj(cmb) for cmb in list_combo]
    object_update(data_lines, objs, sero_obj_list)
    metrics(objs)


    #print data_lines
    #print ''.join([str(i) for i in list_combo]) # Tuples

main()
# for f in lst_files:
#     if '.pdb' in f:
#         list_pdb.append(f)
#
#
# def TM_RMSD():
#
#     RMSD_array = []
#     TM_score_array = []
#
#     for f in pdb_pairs:
#
#         cmd = 'TMalign %s %s -a' %(f[0], f[1])
#         result = subprocess.check_output(cmd, shell=True)
#         ln_result = result.split('\n')
#
#
#         RMSD_line = ln_result[16].split(',')[1]
#         TM_score_line_1 = ln_result[17]
#         TM_score_line_2 = ln_result[18]
#
#
#         regexp_score = re.compile("([A-Za-z\s\W]+)([\d\.]+)")
#
#         RMSD = regexp_score.match(RMSD_line).group(2)
#         TM_score_p1 = regexp_score.match(TM_score_line_1).group(2)
#         TM_score_p2 = regexp_score.match(TM_score_line_2).group(2)
#
#         TM_max=max([float(TM_score_p1), float(TM_score_p2)])
#
#         RMSD_array.append(float(RMSD))
#         TM_score_array.append(float(TM_max))
#
#         print "%s\t%s\t%s\t%s" % (f[0], f[1], RMSD, TM_max)
#
#     RMSD_np = numpy.array(RMSD_array)
#     TM_score_np = numpy.array(TM_score_array)
#
#     RMSD_mean = numpy.mean(RMSD_np)
#     RMSD_median = numpy.median(RMSD_np)
#     RMSD_std = numpy.std(RMSD_np)
#
#     TM_mean = numpy.mean(TM_score_np)
#     TM_median = numpy.median(TM_score_np)
#     TM_std = numpy.std(TM_score_np)
#
#
#     print "\nRMSD_mean: %s\tRMSD_median: %s\tRMSD_std: %s\nTM_score_mean: %s\tTM_score_median: %s\tTM_score_std: %s" % (RMSD_mean, RMSD_median, RMSD_std, TM_mean, TM_median, TM_std)
#
# pdb_pairs = itertools.combinations(list_pdb, 2)
# pairs_number = len(list(itertools.combinations(list_pdb, 2)))
# TM_RMSD()
#
# print "Total pairs number: %s" %pairs_number

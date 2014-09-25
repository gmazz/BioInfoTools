import os, sys, re
import itertools
import numpy as np


class scoreObj(object):

    def __init__(self, ID_tuple):
        self.ID_tuple = ID_tuple
        self.RMSD_list = []

    def scores_update(self, RMSD):
        self.RMSD = RMSD
        self.RMSD_list.append(float(self.RMSD))

    def RMSD_metric(self):
        self.RMSD_np = np.array(self.RMSD_list)
        self.RMSD_mms = [np.mean(self.RMSD_np), np.median(self.RMSD_np), np.std(self.RMSD_np), len(self.RMSD_np)]
        return self.RMSD_mms

    def give_RMSD(self):
        return self.RMSD_list


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
    return list_combo


def model_sero_assoc(model, sero_obj_list):
    sero_target = [obj.seroID for obj in sero_obj_list if model in obj.serolist]
    return sero_target[0]


def object_update(data_lines, objs, sero_obj_list):
    for line in data_lines:
        line = line.split('\n')[0]
        values = line.split('\t')

        model_a = values[0]
        model_b = values[1]
        sero_a = model_sero_assoc(model_a, sero_obj_list)
        sero_b = model_sero_assoc(model_b, sero_obj_list)
        serotuple = (sero_a, sero_b)
        RMSD = float(values[2])

        for obj in objs:
            if (sorted(serotuple) == sorted(obj.ID_tuple)):
                obj.scores_update(RMSD)


def metrics(objs):
    RMSDm = open("Corr_median.txt", "w+")
    RMSDstd = open("Corr_std.txt", "w+")

    RMSDm.write("ID1,ID2,val\n")
    RMSDstd.write("ID1,ID2,val\n")

    for obj in objs:
        ID_tuple = obj.ID_tuple
        RMSD_metric = obj.RMSD_metric()
        Rm = "%s,%s,%s\n" %(ID_tuple[0], ID_tuple[1], format(RMSD_metric[1], '.3f'))
        Rstd = "%s,%s,%s\n" %(ID_tuple[0], ID_tuple[1], format(RMSD_metric[2], '.3f'))
	print Rm,Rstd

        RMSDm.write(Rm)
        RMSDstd.write(Rstd)

def main():
    model_dir = '../model_lists'
    input_score_file = 'local_ESP_test_metric.dat'
    list_files, data_lines = data_import(model_dir, input_score_file)
    sero_obj_list = sero_obj_list_generation(model_dir, list_files)
    list_combo = list_combination(list_files)
    objs = [scoreObj(sorted(cmb)) for cmb in list_combo]
    object_update(data_lines, objs, sero_obj_list)
    metrics(objs)


main()

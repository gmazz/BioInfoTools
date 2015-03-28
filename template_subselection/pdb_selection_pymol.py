import re, os, sys, glob
from pymol import cmd
#import pymol
from Bio import SeqIO
import __main__

################################################################################################
#
#
#  Script to select a subsection of a pdb structure.
#
#   i) The PDB to be processed are localized in the subdirectory /local_model_templates
#
#   ii) A multifasta (MFA) file is given as parameter to the script.
#       It should contain the selected regions for the pdb (in fasta format).
#       The IDs in the MFA file should be the same of the *.pdb names.
#       The MFA have to be in the same directory of the script.
#
#   Command:  python pdb_subsection_selection.py
#
################################################################################################


__main__.pymol_argv = ['pymol', '-qc']
pymol.finish_launching()


class LocalSelect(object):

    def __init__(self, multifasta):
        self.multifasta = multifasta
        self.sel_list = []
        self.handle = open(self.multifasta, "rU")
        for record in SeqIO.parse(self.handle, "fasta"):
            self.sel_list.append(record)
        self.handle.close()

    def search_sele(self, pdbID):
        self.pdbID = pdbID
        for i in self.sel_list:
            if self.pdbID in i.id:
                self.seq = i.seq
                return self.seq


def read():
    rootdir = os.getcwd()
    models_dir = "%s/model_templates" %rootdir

    fl = []
    for file in os.listdir(models_dir):
        if file.endswith(".pdb"):
            fl.append(file)

    return fl


def subselect_pdb(fl, multifasta):
    i = 1
    rootdir = os.getcwd()
    models_dir = "%s/local_model_templates" %rootdir
    obj = LocalSelect(multifasta)
    pdb_list = fl[0:] # allows to select a subset of proteins
    for f in pdb_list:
        f_ID = f.split('.pdb')[0]
        sele = obj.search_sele(f_ID)
        if sele:
            #load_path = "%s/%s" %(models_dir, f)
    #        pymol.cmd.load(load_path)
            cmd.select('tmp_sele', '%s and not pepseq %s' %(f_ID, sele))
            cmd.remove('tmp_sele')
            cmd.save("%s_ref.pdb" %(f_ID), f_ID, 0, 'pdb')
            print "%s:    %s/%s\n" %(f_ID, i, len(pdb_list))
            cmd.delete('tmp_sele')
            i += 1



multifasta = "aligned_normalized_selection.fas"
fl = read()
subselect_pdb(fl, multifasta)

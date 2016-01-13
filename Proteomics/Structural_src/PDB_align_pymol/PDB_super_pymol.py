import re, os, sys, glob
from pymol import cmd
import pymol
import __main__

__main__.pymol_argv = ['pymol', '-qc']
pymol.finish_launching()


def read():
    rootdir = os.getcwd()
    fl = []
    for file in os.listdir(rootdir):
        if file.endswith(".pdb"):
            fl.append(file)

    return fl


def load_all(fl, template):
    cmd.load(template)
    template_ID = template.split('.pdb')[0]

    for f in fl:
        f_ID = f.split('.pdb')[0]
        cmd.load(f)
        align = cmd.super("%s" % f_ID, "%s" % template_ID)
        print (align)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "\n Please use template.ID as an argument. e.g.: $PDB_align_pymol.py 4EDA.pdb\n"
    fl = read()
    template = sys.argv[1]
    if template in fl:
        fl.remove(template)
    load_all(fl, template)

    # Command to run it :
    # This pymol-based script takes all the pdb in a given directory and superimpose them to the template structure given as argument.
    #
    # $ python PDB_align_pymol.py template.pdb
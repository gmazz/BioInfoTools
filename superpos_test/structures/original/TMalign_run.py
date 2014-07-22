import re, os, sys, shutil
from split_structures import *

def read():
    rootdir = os.getcwd()
    fl = []
    for file in os.listdir(rootdir):
        if file.endswith(".pdb"):
            fl.append(file)

    return fl


def load_all(fl, template):

    rootdir = os.getcwd()
    newpath = '%s/ALIGNED' %rootdir
    if not os.path.exists(newpath): os.makedirs(newpath)

    template_ID = template.split('.pdb')[0]

    for f in fl:
        f_ID = f.split('.pdb')[0]
        cmd = 'TMalign %s %s -o %s.sup' %(f, template, f_ID)
        os.system(cmd)
        src = '%s/%s.sup_all_atm' %(rootdir, f_ID)
        dst = '%s/%s.sup_all_atm' %(newpath, f_ID)
        shutil.move(src, dst)
        os.system('rm *.sup*')


def main():
    template = sys.argv[1]
    fl = read()
    if template in fl:
        fl.remove(template)
    load_all(fl, template)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "\n Please use template.ID as an argument. e.g.: $PDB_align_pymol.py 4EDA.pdb\n"

    main()
    tSmain()

import re, os, sys, shutil
from split_structures import *

def read():
    rootdir = os.getcwd()
    tar_path = 'MC_cent'
    templ_path = 'originals'  

    targets_dir = '%s/%s' %(rootdir, tar_path)
    templates_dir = '%s/%s'%(rootdir, templ_path)
    targets = []
    templates = []

    [targets.append(file) for file in os.listdir(targets_dir) if file.endswith(".pdb")]	
    [templates.append(file) for file in os.listdir(templates_dir) if file.endswith(".pdb")]

    return targets, templates, tar_path, templ_path


def find(targets, templates, tar_path, templ_path):

   rootdir = os.getcwd()
   newpath = '%s/ALIGNED' %rootdir
   if not os.path.exists(newpath): os.makedirs(newpath)
  
   targets_ref = [target.split('.pdb')[0].split('_')[0] for target in targets]
   templates_ref = [template.split('.pdb')[0] for template in templates]
	
   for i in range(len(targets_ref)):
	if targets_ref[i] in templates_ref:
           templ_i = templates_ref.index(targets_ref[i])
	   tar = str(tar_path) + '/' + str(targets[i])
	   templ = str(templ_path) + '/' + str(templates[templ_i])
	   print tar, templ

           cmd = 'TMalign %s %s -o %s.sup' %(tar, templ, targets_ref[i])
           os.system(cmd)
           src = '%s/%s.sup_all_atm' %(rootdir, targets_ref[i])
           dst = '%s/%s.sup_all_atm' %(newpath, targets_ref[i])
           shutil.move(src, dst)
           os.system('rm *.sup*')
           
	else:
	   print targets_ref[i] + " Doesn't have a corresponding template"

def main():
    targets, templates, tar_path, templ_path = read()
    find(targets, templates, tar_path, templ_path)


main()
tSmain()

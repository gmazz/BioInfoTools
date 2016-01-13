import re, sys, os, shutil

rootdir = os.getcwd()

def generate_path():

	newpath = '%s/DONE' %rootdir 
	if not os.path.exists(newpath): 
		os.makedirs(newpath)

def automate():
	
	
	list = open("list.txt", "r")
	line = list.readline()
	line = line.rstrip('\n') 
	seq_list = line.split(',')
	for seq in seq_list:

		newPath = '%s/%s/' %(rootdir,seq)
		os.chdir(newPath)
		print os.getcwd()
		os.system("python model.py > model.log")
		dst = '%s/DONE' %rootdir
		shutil.move(newPath, dst)	


generate_path()
automate()

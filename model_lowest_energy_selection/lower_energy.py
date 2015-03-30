# This script parse energy results from the ouput files generated by get_energy.sh 
# and print the lower one (best one) for each file. 

import os, sys
from os import listdir
from os.path import isfile, join


def read(file):
    temp_dict = {}
    fileh = open(file, 'r+')
    lines = fileh.readlines()
    for l in lines:
        val = l.split('\n')[0].split(' ')
        if len(val) == 2:
            temp_dict.update({val[0]: float(val[1])})

    v = sorted(temp_dict.items(), key=lambda x: x[1])
    return v[0]


def main():
    rootdir = os.getcwd()
    files = [f for f in listdir(rootdir) if isfile(join(rootdir, f))]
    for file in files:
        if file.endswith('.txt'):
            best = read(file)
            print best[0]


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "\n Please use template.ID as an argument. e.g.: $lower_energy.py energy_file.txt\n"
    fl = read()
    template = sys.argv[1]
main()

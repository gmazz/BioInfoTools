#!/usr/bin/python

# This script converts data interaction data into bedp-like format 

import sys, os, re

def convert(infilepath, i):
    infilename = os.path.basename(infilepath).split('.RAWobserved')[0]
    chr_nr_tmp, res_tmp = infilename.split('_')[0:2]
    chr_nr = int(re.sub('chr', '', chr_nr_tmp))
    res = int(re.sub('kb', '', res_tmp))
    f = open(infilepath)
    sp_lines = (line.split() for line in f)
    prep_lines = ((int(line[0]), int(line[1]), float(line[2])) for line in sp_lines)
    for line in prep_lines:
        bin1, bin2, val = line
        out_line = "chr%s\t%d\t%d\tchr%s:%d-%d,%.2f\t%d\t." %(chr_nr, bin1, bin1+res, chr_nr, bin2, bin2+res, val, i)
        outf.write(out_line + "\n")
        if i%10**6 == 0:
            print i
        i += 1
    f.close()
    return i


def list_reader(path):
    data_list = []
    for file in os.listdir(path):
        if file.endswith(".RAWobserved"):
            filename = '/'.join((path, file))
            data_list.append(filename)
    return data_list


def openFiles():
    global outf
    outf = open('out.txt', 'w')


def main():
    data_list = list_reader('./data')
    i = 1
    openFiles()
    for infilepath in data_list:
        i = convert(infilepath, i)

if __name__ == "__main__":
  main()

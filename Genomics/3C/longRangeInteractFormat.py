#!/usr/bin/python

# This script converts data interaction data into bedp-like format 

import sys

def convert(outfilename, infilename, chr_nr, res):
  f = open(infilename)
  sp_lines = (line.split() for line in f)
  prep_lines = ((int(line[0]), int(line[1]), float(line[2])) for line in sp_lines)

  outf = open(outfilename, 'w')
  i = 1
  for line in prep_lines:
    bin1, bin2, val = line
    out_line = "chr%s\t%d\t%d\tchr%s:%d-%d,%.2f\t%d\t." %(chr_nr, bin1, bin1+res, chr_nr, bin2, bin2+res, val, i)
    outf.write(out_line + "\n")
    if i%10**6 == 0:
      print i
    i += 1

  f.close()
  outf.close()


def main():
  outfilename, infilename, chr_nr, res = sys.argv[1:]
  convert(outfilename, infilename, chr_nr, int(res))



if __name__ == "__main__":
  main()

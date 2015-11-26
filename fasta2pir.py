#!/usr/bin/python

# script converts FASTA-like alignment into PIR-like alignment

import sys
import getopt
import shutil
from Bio import SeqIO
from Bio.PDB import *
from modeller import *
from modeller.automodel import *
from os import listdir
from os.path import isfile, join
import itertools

local = 0  # do we want to downaload pdb file or do we store them locally


def main(argv):
    global local
    if len(argv) == 0:
        argv = ["-h"]
    alignment_file = ''
    target = ''
    templates = ''
    try:
        opts, args = getopt.getopt(argv, "a:t:k:hl", ["alignment=", "target=", "templates=", "help", "local"])
    except getopt.GetoptError:
        print "Use --help or -h for help"
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print "usage -a[--alignment=] alignment_file.fasta\n" + " " * 6 + "-t[--target=] target for modelling\n" + " " * 6 + "-k[--templates=] templates\
separated by commas\n" + " " * 6 + "-l[--local] use when pdb files are stored in current working directory (defoult off)\n"
            sys.exit(2)
        elif opt in ("-a", "--alignment"):
            alignment_file = arg
        elif opt in ("-t", "--target"):
            target = arg.lower()
        elif opt in ("-k", "--templates"):
            templates = arg.lower()
        elif opt in ("-l", "--local"):
            local = 1
        else:
            print "Use --help or -h for help"
    if (not alignment_file) or (not target) or (not templates):
        print "Please provide all necessary data"
        print "Use --help or -h for help"
        sys.exit(2)
    else:
        templates = tuple(templates.split(","))
        return alignment_file, target, templates


def download_pdb(input_arg):
    pdbl = PDBList()
    [pdbl.retrieve_pdb_file(pdb, pdir=".") for pdb in input_arg[2]]

    return True


def fasta2pir(input_arg):
    if "fst" in input_arg[0]:
        out = open(input_arg[0].replace(".fst", ".pir"), "w")
        out2 = input_arg[0].replace(".fst", ".pir")
        record = list(SeqIO.parse(input_arg[0], "fasta"))
    elif "fasta" in input_arg[0]:
        out = open(input_arg[0].replace(".fasta", ".pir"), "w")
        out2 = input_arg[0].replace(".fasta", ".pir")
        record = list(SeqIO.parse(input_arg[0], "fasta"))
    else:
        print "The file you provide must have .fst or .fasta extension"
        sys.exit(2)

    for r in record:
        if r.id.split(":")[0].lower() in input_arg[2] or r.id.split(":")[0].upper() in input_arg[2]:
            out.write(">P1;" + r.id.split(":")[0].lower() + "\n")
            out.write("structureX" + ":" + r.id.split(":")[0].lower() + ":.:.:.:.::::" + "\n")
            out.write(str(r.seq) + "*" + "\n")
        if r.id.split(":")[0].lower() in input_arg[1] or r.id.split(":")[0].upper() in input_arg[1]:
            out.write(">P1;" + r.id.split(":")[0].lower() + "\n")
            out.write("sequence" + ":" + r.id.split(":")[0].lower() + ":.:.:.:.::::" + "\n")
            out.write(str(r.seq) + "*" + "\n")
    return out2


def copy_pdb(input_arg):
    onlyfiles = [f for f in listdir(".") if isfile(join(".", f))]
    [shutil.copyfile(pair[1], str(pair[0] + ".pdb")) for pair in itertools.product(input_arg[2], onlyfiles) if
     (pair[0] in pair[1]) and (str(pair[0]) + ".pdb" != pair[1])]
    return True


def clean_pdb(input_arg):
    return True


def modelowanie(aln, input_arg):
    log.verbose()  # request verbose output
    env = environ()  # create a new MODELLER environment to build this model in

    env.io.atom_files_directory = ['.', '../atom_files']

    a = automodel(env,
                  alnfile=aln,  # alignment filename
                  knowns=input_arg[2],  # codes of the templates
                  sequence=input_arg[1])  # code of the target
    a.starting_model = 1  # index of the first model
    a.ending_model = 5  # index of the last model
    a.md_level = refine.slow
    a.final_malign3d = True
    # (determines how many models to calculate)
    a.make()  # do the actual comparative modeling


if __name__ == "__main__":
    input_arg = main(sys.argv[1:])

aln = fasta2pir(input_arg)

if local == 0:
    download_pdb(input_arg)
    clean_pdb(input_arg)

copy_pdb(input_arg)
modelowanie(aln, input_arg)


#### To do ####
# sciaganie podanej sekwencji

# czyszczenie pdb-a z wody itd..

# alignmnet miedzy sekwencja a pdb

# przycinanie sekwencji 

# liczenei psi-profa

# kontekst domenowy z uniprota

# kontekst genomiczny

# protein-protein-interaction

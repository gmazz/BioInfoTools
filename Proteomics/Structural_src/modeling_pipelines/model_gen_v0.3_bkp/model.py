#!/usr/bin/python

# Comparative modeling by the automodel class
from modeller import *              # Load standard Modeller classes
from modeller.automodel import *    # Load the automodel class

log.verbose()    # request verbose output
env = environ()  # create a new MODELLER environment to build this model in

# directories for input atom files
env.io.atom_files_directory = ['.', '../atom_files']

a = automodel(env,
              alnfile  = 'initial_aln.pir',     # alignment filename
              knowns   = ('3s12_chA','3s13_chA'),              # codes of the templates
              sequence = '3s12_hybryda')              # code of the target
a.starting_model= 1                 # index of the first model
a.ending_model  = 15                # index of the last model
a.md_level=refine.slow
a.final_malign3d = True
                                    # (determines how many models to calculate)
a.make()                            # do the actual comparative modeling


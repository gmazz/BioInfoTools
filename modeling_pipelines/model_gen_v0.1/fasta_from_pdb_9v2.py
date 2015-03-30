#!/usr/bin/python

import sys
import modeller

code=sys.argv[1]
code=code[0:-4]
env=modeller.environ()
mdl = modeller.model(env,file=code)
aln = modeller.alignment(env)
aln.append_model(mdl,align_codes=code)
aln.write(file=code+'.seq')

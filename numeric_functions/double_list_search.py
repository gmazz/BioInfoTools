# Search short list in long list. It returns a dict with the hit for each element in short.


import re
import itertools

short = ['ma','bam','ba','pa']
long = ['mama','papa','bambino']

res = filter(None, map(lambda (s,l): {s:l} if l.find(s) != -1 else '', itertools.product(short,long)))
print res
		

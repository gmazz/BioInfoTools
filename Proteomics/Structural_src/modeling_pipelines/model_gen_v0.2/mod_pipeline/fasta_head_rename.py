import re,os,sys

file = open('input.fa','r')
lines = file.readlines()

for line in lines:
	line = line.rstrip('\n\*')
	ID = re.compile('(>[A-Z0-9]+)[\_]+')
	ID_m = ID.match(line)
	
	if ID_m:
		print "%s" %ID_m.group(1)
	else:
		print line

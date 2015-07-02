import csv, sys
name = sys.argv[1]
with open(name, 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		id = ">%s" %row[0]
		seq = row[1].replace('-','')
		print "%s\n%s" %(id, seq)

from pandas import *

def generate_table(file):
	file_id = file.split('.txt')[0]
	out_name = '%s_table.txt' %file_id 
	file_hand = open(out_name, "w+")
	data = read_csv(file)
	table = pivot_table(data, index=['ID1'], columns=['ID2'], values='val')
	file_hand.write(table)	

file = 'RMSD_median.txt'
generate_table(file)

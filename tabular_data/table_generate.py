from pandas import *


def generate_table(file):
	file_id = file.split('.txt')[0]
	out_name = '%s_tab.txt' % (file_id)
	file_hand = open(out_name, "w+")
	data = read_csv(file)

	#table = np.round(pivot_table(data, index=['ID1'], columns=['ID2'], values='val'), 3)
	table = np.round(pivot_table(data), 3)



	table.to_csv(out_name)


proc_list = ['TMscore.txt', 'RMSD.txt']

for file in proc_list:
	generate_table(file)

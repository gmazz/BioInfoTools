from pandas import *


def generate_table(file, type):
    file_id = file.split('.txt')[0]
    out_name = '%s_%s_tab.txt' % (file_id, type)
    file_hand = open(out_name, "w+")
    data = read_csv(file)
    table = np.round(pivot_table(data, index=['ID1'], columns=['ID2'], values='val'), 3)
    table.to_csv(out_name)


proc_list = ['RMSD_median.txt', 'RMSD_std.txt', 'TMscore_median.txt', 'TMscore_std.txt']
type = 'local'

for file in proc_list:
    generate_table(file, type)

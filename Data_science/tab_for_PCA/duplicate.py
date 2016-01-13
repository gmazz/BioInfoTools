

def duplo(file):
    file_id = file.split('.txt')[0]
    out_name = '%s_duplo.txt' %(file_id)
    file_handle = open(file, 'r')
    lines = file_handle.readlines()

    for l in lines:
        l = l.split()[0]
        mess = '%s,%s,0.0' %(l, l)
        print mess

duplo('ID_all.txt')
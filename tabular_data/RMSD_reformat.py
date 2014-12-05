import os, sys, re
import itertools

def data_import(scores_file):
    data_tuple_list = []
    IDs_set = set()
    rootdir = os.getcwd()
    scores_file = '%s%s' % (rootdir, scores_file)
    file_handle = open(scores_file)
    data_lines = file_handle.readlines()

    for d in data_lines:
        ids = d.split('\t')[0:2]
        data_tuple = tuple(d.split('\n')[0].split('\t')[0:4])
        if len(data_tuple) == 4:
            data_tuple_list.append(data_tuple)
        [IDs_set.add(id) for id in ids if id.endswith('.pdb')]

    return list(IDs_set), data_tuple_list


def list_combination(list_files):
    list_id = [l.split('.txt', 1)[0] for l in list_files]
    list_combo = itertools.combinations_with_replacement(list_id, 2)
    return list_combo


def evaluation(data_tuple_list, list_combo):
    sorted_data = []
    for ids in list_combo:
        if ids[0] == ids[1]:
           tmp_tuple = (ids[0], ids[1], 0.0, 1.0)
           sorted_data.append(tmp_tuple)
        for d in data_tuple_list:
            if ids[0:2] == d[0:2]:
                sorted_data.append(d)

    return sorted_data


def write_order_list(sorted_data):

    RMSD = open("RMSD.txt", "w+")
    TM = open("TMscore.txt", "w+")

    #Headers
    RMSD.write("ID1,ID2,val\n")
    TM.write("ID1,ID2,val\n")

    for d in sorted_data:
        ID1_val = d[0]
        ID2_val = d[1]
        RMSD_val = float(d[2])
        TMscore_val = float(d[3])

        Rm = "%s,%s,%s\n" % (ID1_val, ID2_val, format(RMSD_val, '.3f'))
        Tm = "%s,%s,%s\n" % (ID1_val, ID2_val, format(TMscore_val, '.3f'))

        RMSD.write(Rm)
        TM.write(Tm)


def main(in_file):
    input_score_file = '/data/%s' % in_file
    IDs_set, data_tuple_list = data_import(input_score_file)
    list_combo = list_combination(IDs_set)
    sorted_data = evaluation(data_tuple_list, list_combo)
    write_order_list(sorted_data)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print """
            ####################################################################################################
            #                                                                                                  #
            #     Please indicate the input file within the "data" directory that you're intending to use.     #
            #     e.g.: $ RMSD_metric_II.py scores_global_trimmed_refactor.dat                                 #
            #                                                                                                  #
            #     Please also be sure that the format of your input file is like follows:                      #
            #                                                                                                  #
            #     AEI30056.pdb	AEO91855.pdb	0.49	0.99422                                                #
            #     AEI30056.pdb	AHA57155.pdb	0.47	0.99418                                                #
            #                        ...                                                                       #
            #                                                                                                  #
            ####################################################################################################
              """

    in_file = sys.argv[1]
    main(in_file)


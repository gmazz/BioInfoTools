class NestedDict(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


def get_list(my_file):
    my_list = [l.split('\n')[0] for l in my_file.readlines()]
    return my_list


def select(flu_list, my_data):
    tmp_list = [l.split('\n')[0] for l in my_data.readlines()]
    original_data_dict = NestedDict()
    for t in tmp_list:
        org_id,hla,peplen,org,pep,symbol,ic50 = t.split('\t')
        original_data_dict[pep][hla] = ic50
    data_dict = {v: original_data_dict[v] for v in flu_list if v in original_data_dict}
    return data_dict
    #print data_dict['QIGNIISIW']


def main():
    flu_file = open('flu_antigens_list.txt', 'r')
    HLAI_file = open('HLA_I_epitopes_all.txt', 'r')
    HLAII_file = open('HLA_II_epitopes_all.txt', 'r')

    flu_list = get_list(flu_file)
    HLAI_data = select(flu_list, HLAI_file)
    HLAII_data = select(flu_list, HLAII_file)
    print (len(HLAI_data), len(HLAII_data))    

    #for k,v in HLAI_data.iteritems():
    #	print "%s\t%s\n" %(k,v)
    #print HLAII_data


main()

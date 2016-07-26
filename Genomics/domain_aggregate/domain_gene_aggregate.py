import sys
from os import listdir
from os.path import isfile, join

def file2list(file, **kwargs):
    sep = kwargs.get('sep', None)
    if sep:
        return [r.rsplit('\n')[0].split(sep) for r in open(file, 'r+').readlines()]
    else:
        return [r.rsplit('\n')[0] for r in open(file, 'r+').readlines()]

def aggregate(file):
    data_dict_tmp = {}
    data_list_tmp = file2list(file, sep='\t')
    for dp in data_list_tmp:
        tmp_id = tuple(dp[0:3])
        if tmp_id in data_dict_tmp:
            data_dict_tmp[tmp_id].append(dp[3])
        else:
            data_dict_tmp[tmp_id] = [dp[3]]
    return data_dict_tmp

def select(data_aggregated, target): #Given a file containing a list of genes for which we want ot find the domain
    target_genes = file2list(target)
    for k,v in data_aggregated.iteritems():
        for target in target_genes:
            if target in v:
                v.remove(target)
                message = '%s:%s-%s;%s;%s\n' %(k[0], k[1], k[2], target, ','.join(v))
                print message

def main(target):
    files = [f for f in listdir('./') if (isfile(join('./', f)) and f.endswith('.bed'))]
    data_aggregated = aggregate(files[0])
    select(data_aggregated, target)

if __name__ == '__main__':
    target = sys.argv[1]
    if len(target) >= 2:
        main(target)
    else:
        print "\n Target file missing. \n Please give specify the gene list target\n(e.g. python domain_gene_aggregate.py genelist.txt)\n"

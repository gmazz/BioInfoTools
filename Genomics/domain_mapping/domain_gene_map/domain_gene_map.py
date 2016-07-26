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

def select(data_aggregated, target, fileout): #Given a file containing a list of genes for which we want ot find the domain
    handle = open(fileout, 'w')
    target_genes = file2list(target)
    for k,v in data_aggregated.iteritems():
        for target in target_genes:
            if target in v:
                v.remove(target)
                message = '%s:%s-%s;%s;%s\n' %(k[0], k[1], k[2], target, ','.join(v))
                handle.write(message)

def main(target):
    files = [f for f in listdir('./data') if (isfile(join('./data', f)) and f.endswith('.bed'))]
    for f in files:
        filein = './data/' + f
        fileout = './results/' + f.replace('.bed','.out')
        data_aggregated = aggregate(filein)
        select(data_aggregated, target, fileout)

if __name__ == '__main__':
    try:
        target = sys.argv[1]
        main(target)
    except:
        print "\nTarget file missing\nPlease specify the file containing the list of genes to find\n(e.g. python domain_gene_aggregate.py list_genes.txt)"

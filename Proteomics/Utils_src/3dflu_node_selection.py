import config
import pandas

## This code allows to select the nodes with highest values.

cdf = config.DISTANCE_CRYSTALS_RMSD

def read_distance_file(distance_file):
    distance_df = pandas.read_csv(distance_file)
    return distance_df

def node_select(dis_df, value_header):
    distance_list = []
    dis_df = dis_df.sort(['p_id'], ascending=[1])
    tmp = [dis_df.loc[dis_df['p_id'] == id] for id in set(dis_df.p_id)]
    tmp = [df.sort([value_header], ascending=[1]) for df in tmp]
    for df in tmp:
        #insert selection step in here
        for index, row in df.iterrows():
            distance_list.append({
                'p_id': row['p_id'],
                'p_id2': row['p_id2'],
                'value': row[value_header]
            })


    return distance_list
    #print ndict['4uo7']['5hmg']

def main():
    value_header = 'value'
    distance_df = read_distance_file(cdf)
    distance_list = node_select(distance_df, value_header)

main()
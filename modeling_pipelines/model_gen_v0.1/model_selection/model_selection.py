import os, re, sys, io


def model_selection(model_scores_file):

    models_dir = {}
    file_handle = open(model_scores_file, 'r')
    ms_lines = file_handle.readlines()
    ms_lines = [f.rstrip('\n') for f in ms_lines]
    for line in ms_lines:
        path, score = line.split(':')
        score = float(score)
        id = path.split('/')[3]

        if id not in models_dir.keys():
            models_dir[id] = [score, path]

        else:
            if score < models_dir[id][0]:
                models_dir[id][0] = score
                models_dir[id][1] = path

    return models_dir

def write_selection(model_dir):
    file_out = open('selected_models.txt', 'w+')
    for k, v in models_dir.items():
        line = "%s\t%s\n" %(k, v[1])
        file_out.write(line)

model_scores_file = 'models_raw_scores.txt'
models_dir = model_selection(model_scores_file)
write_selection(models_dir)


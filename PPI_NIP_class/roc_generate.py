import os, sys
import numpy as np
import matplotlib.pyplot as plt
import pickle
import matplotlib.patches as mpatches


def load_obj(pkl_file_name):
    with open(pkl_file_name, 'rb') as f:
        return pickle.load(f)

def gen_patches(label_colors):
    patches = []
    for k,v in label_colors.iteritems():
        patches.append(mpatches.Patch(color=v, label=k))
    return patches


def plot_ROC_all(results, roc_name):
    fig = plt.figure()
    tickness = 1.5
    line_1 = plt.plot(results['Random_Forest']['fpr'], results['Random_Forest']['tpr'], label='RF', linewidth=tickness, color='r')
    line_2 = plt.plot(results['Decision_Tree']['fpr'], results['Decision_Tree']['tpr'], label='DT', linewidth=tickness, color='b')
    line_3 = plt.plot(results['Linear_SVM']['fpr'], results['Linear_SVM']['tpr'], label='SVM linear', linewidth=tickness, color='orange')
    line_4 = plt.plot(results['RBF_SVM']['fpr'], results['RBF_SVM']['tpr'], label='SVM RBF', linewidth=tickness, color='m')
    line_5 = plt.plot(results['Nearest_Neighbors']['fpr'], results['Nearest_Neighbors']['tpr'], label='k-NN', linewidth=tickness, color='c')
    line_6 = plt.plot(results['AdaBoost']['fpr'], results['AdaBoost']['tpr'], label='AdaBoost', linewidth=tickness, color='g')
    line_7 = plt.plot(results['Naive_Bayes']['fpr'], results['Naive_Bayes']['tpr'], label='NB', linewidth=tickness, color='k')
    line_8 = plt.plot(results['LDA']['fpr'], results['LDA']['tpr'], label='LDA', linewidth=tickness, color='pink')
    line_9 = plt.plot(results['MLP']['fpr'], results['MLP']['tpr'], label='MLP', linewidth=1.2, color='sage')


    label_colors = {
                 'RF': 'r',
                 'DT': 'b',
                 'SVM linear': 'orange',
                 'SVM RBF': 'm',
                 'k-NN': 'c',
                 'AdaBoost': 'g',
                 'NB': 'k',
                 'LDA': 'pink',
                 'MLP': 'sage'
                 }

    ROC_title = 'ROC (50,000 balanced class, without DDI features)'
    #ROC_title = 'ROC (50,000 balanced class)'

    plt.rc('font', family='sans-serif')
    plt.rc('xtick', labelsize='small')
    plt.rc('ytick', labelsize='small')
    patches = gen_patches(label_colors)
    plt.legend(handles=patches, loc=4, fancybox=True, fontsize=12, markerscale=2.)
    #plt.legend(loc=4, fancybox=True, fontsize=12, markerscale=2.)
    plt.xlim([-0.02, 1.0])
    plt.ylim([0.0, 1.02])
    plt.xlabel('False Positive Rate', family='sans-serif', weight='light')
    plt.ylabel('True Positive Rate', family='sans-serif', weight='light')
    plt.title(ROC_title, y=1.05, family='sans-serif', weight='light')
    #fig.savefig(roc_name, dpi=600)
    plt.show()


def print_AUC(results, roc_name):
    for k, v in results.iteritems():
        print k, v['roc_auc']


#################### Main control query lunching ####################

if len(sys.argv) != 2:
    print "\n#################################################"
    print "Mae govannen gwad!\nPlease run the script indicating the name of the \nserialized file (.pkl) that you would like to use.\nThanks human!"
    print "#################################################\n"
    sys.exit()

pkl_file_name = sys.argv[1]
roc_name = pkl_file_name.replace('.pkl', '.png')
results = load_obj(pkl_file_name)
plot_ROC_all(results, roc_name)
print_AUC(results, roc_name)
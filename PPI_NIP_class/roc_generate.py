import os, sys
import numpy as np
import matplotlib.pyplot as plt
import pickle


def load_obj(pkl_file_name):
    with open(pkl_file_name, 'rb') as f:
        return pickle.load(f)


def plot_ROC_all(results, roc_name):
    fig = plt.figure()
    line_1 = plt.plot(results['Random_Forest']['fpr'], results['Random_Forest']['tpr'], label='Random Forest', linewidth=1.2)
    line_2 = plt.plot(results['Decision_Tree']['fpr'], results['Decision_Tree']['tpr'], label='Decision Tree', linewidth=1.2)
    line_3 = plt.plot(results['Linear_SVM']['fpr'], results['Linear_SVM']['tpr'], label='Support Vector Machines (linear kernel)', linewidth=1.2)
    line_4 = plt.plot(results['RBF_SVM']['fpr'], results['RBF_SVM']['tpr'], label='Support Vector Machines (RBF kernel)', linewidth=1.2)
    line_5 = plt.plot(results['Nearest_Neighbors']['fpr'], results['Nearest_Neighbors']['tpr'], label='Nearest Neighbors', linewidth=1.2)
    line_6 = plt.plot(results['AdaBoost']['fpr'], results['AdaBoost']['tpr'], label='AdaBoost', linewidth=1.2)
    line_7 = plt.plot(results['Naive_Bayes']['fpr'], results['Naive_Bayes']['tpr'], label='Naive Bayes', linewidth=1.2)
    line_8 = plt.plot(results['LDA']['fpr'], results['LDA']['tpr'], label='Linear Discriminant Analysis', linewidth=1.2)
    #line_9 = plt.plot(results['QDA']['fpr'], results['QDA']['tpr'], label='QDA')
    plt.rc('font', family='sans-serif')
    plt.rc('xtick', labelsize='small')
    plt.rc('ytick', labelsize='small')
    plt.legend(loc=4, fancybox=True)
    plt.xlim([-0.02, 1.0])
    plt.ylim([0.0, 1.02])
    plt.xlabel('False Positive Rate', family='sans-serif', weight='light')
    plt.ylabel('True Positive Rate', family='sans-serif', weight='light')
    plt.title('ROC', y=1.05, family='sans-serif', weight='light')
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
#plot_ROC_all(results, roc_name)
print_AUC(results, roc_name)
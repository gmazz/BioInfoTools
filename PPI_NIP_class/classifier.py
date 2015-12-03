# General libs
import os, sys
import numpy as np
import matplotlib.pyplot as plt

# Data scaling and normalization
from sklearn import preprocessing
#from sklearn.preprocessing import normalize
#from sklearn.preprocessing import StandardScaler

from matplotlib.colors import ListedColormap
from sklearn import cross_validation
from sklearn.cross_validation import train_test_split
from sklearn import decomposition

# Validation libs
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import roc_curve, auc

# Classifiers libs
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.qda import QDA

#################### Data preparation and pre-processing session ####################

def elem_select(feat, bools):
    selection = []
    if len(feat) != len(bools):
        print "\nError! Your selection list doesn't match the feature list\n"
    else:
        for i in range(len(feat)):
            if bools[i] == 1:
                selection.append(feat[i])
            elif bools[i] == 0:
                pass
            else:
                print "\nError! Your selection list should contain just 0 or 1\n"
    return selection


def data_gen(file_name):
    feat_nms = ['numDomainP1', 'numDomainP2', 'numDDI', 'Max_freq_DDI', 'Min_freq_DDI', 'Min_Zscore', 'Max_Zscore',
                'Zscore_of_mostfreq_DDI', 'btw_P1', 'btw_P2', 'dgr_P1', 'dgr_P2', 'cls_P1', 'cls_P2', 'ecc_P1',
                'ecc_P2', 'nb1_P1', 'nb1_P2', 'nb2_P1', 'nb2_P2', 'nb3_P1', 'nb3_P2', 'nb4_P1', 'nb4_P2', 'nb5_P1',
                'nb5_P2', 'CC_P1', 'CC_P2', 'EvCV_P1', 'EvCV_P2', 'Eigen_value', 'Similarity_Jaccard',
                'Similarity_dice', 'Similarity_inverse_log_weighted', 'totalAA_p1', 'totalAA_p2', 'disorder_p1',
                'disorder_p2', 'greater_than_30aa_p1', 'greater_than_30aa_p2', 'greater_than_50aa_p1',
                'greater_than_50aa_p2', 'disordered_segments_p1', 'disordered_segments_p2', 'MR', 'COR',
                'Shortest_path', 'Type']

    ##################### Features selection: All the values bools=1 are choosen as features for ML. ######################

    bools = np.array([
        0,  # numDomainP1
        0,  # numDomainP2
        1,  # > numDDI
        1,  # > Max_freq_DDI
        1,  # > Min_freq_DDI
        1,  # > Min_Zscore
        1,  # > Max_Zscore
        1,  # > Zscore_of_mostfreq_DDI
        1,  # > btw_P1
        1,  # > btw_P2
        1,  # > dgr_P1
        1,  # > dgr_P2
        0,  # cls_P1
        0,  # cls_P2
        0,  # ecc_P1
        0,  # ecc_P2
        0,  # nb1_P1
        0,  # nb1_P2
        0,  # nb2_P1
        0,  # nb2_P2
        0,  # nb3_P1
        0,  # nb3_P2
        0,  # nb4_P1
        0,  # nb4_P2
        0,  # nb5_P1
        0,  # nb5_P2
        0,  # CC_P1
        0,  # CC_P2
        1,  # > EvCV_P1
        1,  # > EvCV_P2
        1,  # > Eigen_value
        0,  # Similarity_Jaccard
        0,  # Similarity_dice
        0,  # Similarity_inverse_log_weighted
        1,  # > totalAA_p1
        1,  # > totalAA_p2
        0,  # disorder_p1
        0,  # disorder_p2
        0,  # greater_than_30aa_p1
        0,  # greater_than_30aa_p2
        0,  # greater_than_50aa_p1
        0,  # greater_than_50aa_p2
        0,  # disordered_segments_p1
        0,  # disordered_segments_p2
        1,  # > MR
        1,  # > COR
        0,  # Shortest_path
        0  # Type
    ])

    def data_format():
        my_data = np.loadtxt(open(file_name, "rb"), delimiter=",", skiprows=1)
        indx_list = []
        selection = elem_select(feat_nms, bools)
        results_file.write("\n#################### LIST OF SELECTED FEATURES ####################\n")
        for arg in selection: results_file.write("* %s\n" % arg)
        for i in range(len(bools)):
            if bools[i] == 1:
                indx_list.append(i)
        X = my_data[:, indx_list]
        y = my_data[:, 47]
        return (X, y)

    ######### Data scaling/normalization

    def data_scale(X):
        min_max_scaler = preprocessing.MinMaxScaler()
        X_scaled = min_max_scaler.fit_transform(X)
        return (X_scaled)

    def data_norm(X):
        X_normalized = preprocessing.normalize(X, norm='l1')
        return X_normalized

    ######### The np.array data matrix is generated and values from bools=1 are selected

    X_orig, y = data_format()
    X = data_scale(X_orig)

    # X = data_norm(X_orig)
    # List of selected classifiers

    names = [
        "Decision_Tree",
        "Random_Forest",
        "Linear_SVM",
        "RBF_SVM",
        "Nearest_Neighbors",
        "AdaBoost",
        "Naive_Bayes",
        "LDA",
        "QDA"
    ]
    classifiers = [
        DecisionTreeClassifier(max_depth=10),
        RandomForestClassifier(max_depth=10, n_estimators=10, max_features=np.sum(bools)),
        SVC(kernel="linear", C=1, probability=True),
        SVC(kernel="rbf", C=1, probability=True),
        KNeighborsClassifier(3),
        AdaBoostClassifier(),
        GaussianNB(),
        LDA(),
        QDA()
    ]
    return names, classifiers, X, y, bools


#################### Classification section: ####################


def simpl_class(names, classifiers, X, y):
    for name, clf in zip(names, classifiers):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5)
        clf = clf.fit(X_train, y_train)
        score = clf.score(X_test, y_test)
        print name, score


def cv_class(names, classifiers, X, y):
    for name, clf in zip(names, classifiers):
        scores = cross_validation.cross_val_score(clf, X, y, cv=10, scoring='f1')
        print "%s Accuracy: %0.4f (+/- %0.4f)" % (name, scores.mean(), scores.std() / 2)


def test_clf(names, clf, X, y):
    cv = StratifiedKFold(y, n_folds=10)
    precision_scores = []
    recall_scores = []
    results_file.write("\n#################### CLASSIFICATION RESULTS ####################\n")
    for name, cl in zip(names, clf):
        for train, test in cv:
            cl.fit(X[train], y[train])
            Yp = cl.predict(X[test])
            # print len(Yp)
            # print len(y[test])
            precision_scores.append(precision_score(y[test], Yp))
            recall_scores.append(recall_score(y[test], Yp))
            # print("Positive prediction: " + str(sum(Yp)))
            # print("Negative prediction: " + str(len(test) - sum(Yp)))
        res_msg = "Classifier: %s\nPrecision: %s ~%s\nRecall: %s ~%s\n\n" % (name, np.mean(precision_scores), np.std(precision_scores), np.mean(recall_scores), np.std(recall_scores))
        results_file.write(res_msg)
    return cv


class resROC(object):
    def __main__(self, fpr, tpr, thresholds, roc_auc):
        self.fpr = fpr
        self.tpr = tpr
        self.thresholds = thresholds
        self.roc_auc = roc_auc


def ROC(names, clf, X, y):
    cv = StratifiedKFold(y, n_folds=10)
    results = {}
    for name, cl in zip(names, clf):
        #resROC_obj = resROC()
        for train, test in cv:
            probas_ = cl.fit(X[train], y[train]).predict_proba(X[test])
        # Compute ROC curve and area the curve
            fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
            roc_auc = auc(fpr, tpr)
            results[name] = {'fpr': fpr, 'tpr': tpr, 'roc_auc': roc_auc}
    return results


def plot_ROC_single(results, roc_name):
    fig = plt.figure()
    name = 'Random_Forest'
    plt.plot(results[name]['fpr'], results[name]['tpr'], label='ROC curve (area = %0.2f)' % results[name]['roc_auc'])
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    #fig.savefig(roc_name, dpi=600)
    plt.show()


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
    #plt.legend(handles=[line_1, line_2, line_3], loc=4)

    plt.rc('font', family='sans-serif')
    plt.rc('xtick', labelsize='small')
    plt.rc('ytick', labelsize='small')


    plt.legend(loc=4, fancybox=True)
    plt.xlim([-0.02, 1.0])
    plt.ylim([0.0, 1.02])
    plt.xlabel('False Positive Rate', family='sans-serif', weight='light')
    plt.ylabel('True Positive Rate', family='sans-serif', weight='light')
    plt.title('ROC', y=1.05, family='sans-serif', weight='light')
    fig.savefig(roc_name, dpi=600)
    #plt.show()


def PCA(X, bools):
    pca = decomposition.PCA()
    pca.fit(X)
    # pca_y = pca.explained_variance_
    # pca_x = np.arange(len(X[0]))
    # labels = []

    pca.n_components = np.sum(bools)
    X_rd = pca.fit_transform(X)

    # plt.plot(pca_x, pca_y, 'ro')
    # plt.show()
    return X_rd


#################### Main control query lunching ####################

if len(sys.argv) != 2:
    print "\n#################################################"
    print "Please run the script indicating the name\nof the CVS data file that you would like to use.\nThanks human!"
    print "#################################################\n"
    sys.exit()

file_name = sys.argv[1]
roc_name = file_name.replace('class_DATA', 'results').replace('.csv', '.png')
res_name = file_name.replace('class_DATA', 'results').replace('.csv', '_results.txt')
results_file = open(res_name, 'w+')

names, clf, X, y, bools = data_gen(file_name)
cv = test_clf(names, clf, X, y)
results = ROC(names, clf, X, y)
plot_ROC_all(results, roc_name)


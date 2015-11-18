# General libs
import os, random, sys
import numpy as np
#from numpy import genfromtxt
#import matplotlib.pyplot as plt

#Data scaling and normalization
from sklearn import preprocessing
from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler

from matplotlib.colors import ListedColormap
from sklearn import cross_validation
from sklearn import datasets
from sklearn.cross_validation import train_test_split
#from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn import decomposition

# Validation libs
from sklearn import metrics
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


results_file = open('class_perform.txt', 'w')

#################### Data preparation and pre-processing session ####################

def elem_select (feat, bools):
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
    feat_nms=['numDomainP1','numDomainP2','numDDI','Max_freq_DDI','Min_freq_DDI','Min_Zscore','Max_Zscore','Zscore_of_mostfreq_DDI','btw_P1','btw_P2','dgr_P1','dgr_P2','cls_P1','cls_P2','ecc_P1','ecc_P2','nb1_P1','nb1_P2','nb2_P1','nb2_P2','nb3_P1','nb3_P2','nb4_P1','nb4_P2','nb5_P1','nb5_P2','CC_P1','CC_P2','EvCV_P1','EvCV_P2','Eigen_value','Similarity_Jaccard','Similarity_dice','Similarity_inverse_log_weighted','totalAA_p1','totalAA_p2','disorder_p1','disorder_p2','greater_than_30aa_p1','greater_than_30aa_p2','greater_than_50aa_p1','greater_than_50aa_p2','disordered_segments_p1','disordered_segments_p2','MR','COR','Shortest_path','Type']

##################### Features selection: All the values bools=1 are choosen as features for ML. ######################

    bools = np.array ([
            0, # numDomainP1
            0, # numDomainP2
            1, # > numDDI
            1, # > Max_freq_DDI
            1, # > Min_freq_DDI
            1, # > Min_Zscore
            1, # > Max_Zscore
            1, # > Zscore_of_mostfreq_DDI
            1, # > btw_P1
            1, # > btw_P2
            1, # > dgr_P1
            1, # > dgr_P2
            0, # cls_P1
            0, # cls_P2
            0, # ecc_P1
            0, # ecc_P2
            0, # nb1_P1
            0, # nb1_P2
            0, # nb2_P1
            0, # nb2_P2
            0, # nb3_P1
            0, # nb3_P2
            0, # nb4_P1
            0, # nb4_P2
            0, # nb5_P1
            0, # nb5_P2
            0, # CC_P1
            0, # CC_P2
            1, # > EvCV_P1
            1, # > EvCV_P2
            1, # > Eigen_value
            0, # Similarity_Jaccard
            0, # Similarity_dice
            0, # Similarity_inverse_log_weighted
            1, # > totalAA_p1
            1, # > totalAA_p2
            0, # disorder_p1
            0, # disorder_p2
            0, # greater_than_30aa_p1
            0, # greater_than_30aa_p2
            0, # greater_than_50aa_p1
            0, # greater_than_50aa_p2
            0, # disordered_segments_p1
            0, # disordered_segments_p2
            1, # > MR
            1, # > COR
            0, # Shortest_path
            0  # Type
            ])


    def data_format():
        my_data = np.loadtxt(open(file_name,"rb"),delimiter=",",skiprows=1)
        indx_list = []

        selection = elem_select(feat_nms, bools)
        results_file.write("\n#################### LIST OF SELECTED FEATURES ####################\n")
        for arg in selection: results_file.write("* %s\n" %arg)

        for i in range (len(bools)):
            if bools[i] == 1:
                indx_list.append(i)

        X = my_data[:,indx_list]
        y = my_data[:, 47]

        return (X, y)

######### Data scaling/normalization

    def data_scale(X):
        min_max_scaler = preprocessing.MinMaxScaler()
        X_scaled = min_max_scaler.fit_transform(X)
        return(X_scaled)

    def data_norm(X):
        X_normalized = preprocessing.normalize(X, norm='l1')
        return X_normalized

######### The np.array data matrix is generated and values from bools=1 are selected

    X_orig, y  = data_format()
    X = data_scale(X_orig)

    #X = data_norm(X_orig)

# List of selected classifiers

    names = [
        "Decision Tree",
        "Random Forest",
        "Linear SVM",
        "RBF SVM",
        "Nearest Neighbors",
        "AdaBoost",
        "Naive Bayes",
        "LDA",
        "QDA"
        ]


    classifiers = [
                DecisionTreeClassifier(max_depth=10),
                RandomForestClassifier(max_depth=10, n_estimators=10, max_features=np.sum(bools)),
                SVC(kernel="linear", C=0.05, probability=True),
                SVC(gamma=2, C=1),
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
            #print len(Yp)
            #print len(y[test])
            precision_scores.append(precision_score(y[test], Yp))
            recall_scores.append(recall_score(y[test], Yp))
            #print("Positive prediction: " + str(sum(Yp)))
            #print("Negative prediction: " + str(len(test) - sum(Yp)))

        res_msg = "Classifier: %s\nPrecision: %s ~%s\nRecall: %s ~%s\n\n" %(name, np.mean(precision_scores), np.std(precision_scores), np.mean(recall_scores), np.std(recall_scores))
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
    resROC_list = []

    results_file.write("\n#################### CLASSIFICATION RESULTS ####################\n")

    for name, cl in zip(names, clf):
        #resROC_obj = resROC()
        fpr_list = []

        for train, test in cv:
            probas_ = cl.fit(X[train], y[train]).predict_proba(X[test])
            # Compute ROC curve and area the curve
            fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
            roc_auc = auc(fpr, tpr)
            #print "Area under the ROC curve for %s is: %f" %(name, roc_auc)
            fpr_list.append(fpr.tolist())

        fpr_np = np.array(fpr_list)
        return fpr_np
        #for i in resROC_list:

        #resROC_obj.fpr = fpr
        #resROC_obj.tpr = tpr
        #resROC_obj.thresholds = thresholds
        #resROC_obj.roc_auc = roc_auc


            #return (fpr, tpr, thresholds, roc_auc)

            # Plot ROC curve
            #print cl,cv
            #pl.clf()
            #pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
            #pl.plot([0, 1], [0, 1], 'k--')
            #pl.xlim([0.0, 1.0])
            #pl.ylim([0.0, 1.0])
            #pl.xlabel('False Positive Rate')
            #pl.ylabel('True Positive Rate')
            #pl.title('Receiver operating characteristic example')
            #pl.legend(loc="lower right")
            #pl.show()

def PCA(X, bools):
    pca = decomposition.PCA()
    pca.fit(X)
    #pca_y = pca.explained_variance_
    #pca_x = np.arange(len(X[0]))
    #labels = []

    pca.n_components = np.sum(bools)
    X_rd = pca.fit_transform(X)

    #plt.plot(pca_x, pca_y, 'ro')
    #plt.show()
    return X_rd

#################### Main control query lunching ####################

if len(sys.argv) != 2:
    print "\n#################################################"
    print "Please run the script indicating the name\nof the CVS data file that you would like to use.\nThanks human!"
    print "#################################################\n"
    sys.exit()

file_name = sys.argv[1]

names, clf, X, y, bools = data_gen(file_name)
#cv = test_clf(names, clf, X, y)

#fpr, tpr, thresholds, roc_auc = ROC(names, clf, X, y)
fpr_np = ROC(names, clf, X, y)


#cv_class(names, clf, X, y)
#X_rd = PCA(X, bools)
#cv_class(names, clf, X_rd, y)

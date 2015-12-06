from neural import *
from classifier import *

def test_NN(file_name):
    # Generate NN object
    NN = py_nn()
    names, clf, X, y, bools = data_gen(file_name)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "\n#################################################"
        print "Mae govannen gwad!\nPlease run the script indicating the name of the \ndata file (.csv) that you would like to use.\nThanks human!"
        print "#################################################\n"
        sys.exit()
    file_name = sys.argv[1]
    test_NN(file_name)
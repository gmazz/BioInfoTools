import re, os


class scoreObj(object):
    def __init__(self, c1, c2, RMSD, TMscore):

        self.c1 = c1
        self.c2 = c2
        self.RMSD = RMSD
        self.TMscore = TMscore


def listAlign():
    rootdir = os.getcwd()
    alPath = '%s/ALIGNED' %rootdir
    os.chdir(alPath)
    fl=[]
    for file in os.listdir(alPath):
        if file.endswith(".sup_all_atm"):
            fl.append(file)
    return fl


def readScores(fl):
    scoreList = []

    for f in fl:
        tmp = []
        handle = open(f, 'r')
        lines = handle.readlines()
        for line in lines:

            regexp_chain_1 = re.compile ("^(REMARK)[\s]+(Chain\s1:)([A-Za-z0-9]+)[.]") # In our case this is the model that have been generated
            regexp_chain_2 = re.compile ("^(REMARK)[\s]+(Chain\s2:)([A-Za-z0-9]+)[.]") # In our case this is the template
            regexp_scores = re.compile ("^(REMARK)([A-Za-z0-9\s\=]+)[,]([A-Za-z\s\W]+)([0-9\.]+)[,]([A-Za-z\s\W]+)([0-9\.]+)[,]([A-Za-z\s\W]+)([0-9\.]+)") #Grep both RMSD and TMscores

            ex1 = regexp_chain_1.match(line)
            ex2 = regexp_chain_2.match(line)
            ex_score = regexp_scores.match(line)


            try:
                tmp.append(ex1.group(3))
            except:
                pass

            try:
                tmp.append(ex2.group(3))
            except:
                pass

            try:
                tmp.append(ex_score.group(4))
                tmp.append(ex_score.group(6))
            except:
                pass


        if tmp:
            c1 = tmp[0]
            c2 = tmp[1]
            RMSD = tmp[2]
            TMscore = tmp[3]

            obj = scoreObj(c1, c2, RMSD, TMscore)
            scoreList.append(obj)

    return scoreList    #Returns the list of objects


def targetSplit(fl): #Copies the 1st sequence (in our case the model) in a new file.
    for f in fl:
        ID = f.split('.')[0]
        name_fout = "%s.pdb" %ID
        handle = open(f, 'r')
        lines = handle.readlines()
        fout = open(name_fout,'w')

        for line in lines:
            if (line.startswith('REMARK') == True or line.startswith('ATOM') == True):
                fout.write(line)
            elif line.startswith('TER') == True:
                fout.write('END')
                fout.close()
                break


def main():
    fl = listAlign()

    #targetSplit(fl)
    scoreList = readScores(fl)

    for obj in scoreList:
        print "%s\t%s\t%s\t%s" %(obj.c1, obj.c2, obj.RMSD, obj.TMscore)


main()
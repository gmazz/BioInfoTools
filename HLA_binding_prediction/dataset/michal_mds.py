#!/usr/bin/python

# skrypt do odpalania i wizualizacji wynikow PCA
# to do
# -lda DONE
# -isomap DONE
# labels dla plot3d
# wszystkie mds-y zaimplementowane w sklearn DONE
# mozliwosc wyswietlania wynikow jednej metody jak i wszystkich naraz Done
# trzeba dodac legende


''' 
Skrypt dziala poki co dla plikow csv w postaci
kolumna1_name,kolumna2_name,kolumna3_name
0,1,1
1,1,1

kolejne obseracje sa w rzedach, a badane cech w kolumnach
prefereowane jest wystepowanie kolumny opisowej

'''
import sys
import getopt
import shutil
import itertools
import numpy as np
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import time
from mpl_toolkits.mplot3d import Axes3D
from sklearn import manifold
from sklearn.utils import check_random_state
import random

def main(argv):
	stand=0
	indeks=0
	result=0
	pca=0
	dim=2
	lab=0
	write=0
	if len(argv) == 0:
		argv=["-h"]
	alignment_file=''
	target=''
	templates=''
	try:
		opts,args = getopt.getopt(argv, "f:p:n:r:d:a:lswh", ["file=", "pca=", "index=", "result_column=", "dimensions=", "program_number=", "labels", "standarization", "write", "help"])
	except getopt.GetoptError:
		print "Use --help or -h for help" 
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print "-f[--file=] input file in csv format\n-n[--index] name of the index column\n-r[--reult_column] name of the result column\n-s[--standarization] perform standarization on raw data[default=off]\
\n-d[--dimensions] number of dimensions to MDS[default=2]\n-l[--labels] add labels to the plot [default=off]\n-a[--program_number] 0 -> PCA 1 -> isomap 2-> mds\
 3 -> t-distributed stochastic neighbor embedding\n                     4 -> LLE 5-> LTSA 6-> Hessian LLE 7-> Spectral Embedding 8-> Modified LLE\
\n                     9-> compare all methods\n-w[--write] save figre to file in PNG format(current date used as a name)\n-h[--help] print this message\
\n"
			sys.exit(2)
		elif opt in ("-f", "--file="):
			inp=arg
		elif opt in ("-p","--pca="):
			pca=arg
		elif opt in ("-s", "--standarization"):
			stand=1
		elif opt in ("-n", "--index="):
			indeks=arg
		elif opt in ("-r", "--result_column="):
			result=arg
		elif opt in ("-d", "--dimensions="):
			dim=arg
		elif opt in ("-l", "--labels="):
			lab=1
		elif opt in ("-a", "--program_number="):
			prog=arg
		elif opt in ("-w", "--write"):
			write=1
	return inp,indeks,result,pca,stand,dim,lab,prog,write

def normalizacja(input_arg):
	if input_arg[1] != 0 :
		plik=pd.read_csv(input_arg[0], index_col=input_arg[1])
	else:
		plik=pd.read_csv(input_arg[0])
	var_matrix=[]
	res_matrix=[]
	for col in plik.columns:
    		if col == input_arg[2]:
			res_matrix.append(list(plik[col]))
		else:
			mu =  plik[col].mean()
    			si =  plik[col].std()
    			var_matrix.append(list((plik[col]- mu) / si))
	var_matrix=np.array(var_matrix,dtype=float)
	res_matrix=np.array(res_matrix,dtype=float)
	return var_matrix.T, res_matrix.T, plik.index

def prepare_data(input_arg):
	if input_arg[1] != 0:
		plik=pd.read_csv(input_arg[0], index_col=input_arg[1])
	else:
		plik=pd.read_csv(input_arg[0])
	var_matrix=[]
	res_matrix=[]
	for col in plik.columns:
		if col == input_arg[2]:
			res_matrix.append(list(plik[col]))
		else:
			var_matrix.append(list(plik[col]))
	var_matrix=np.array(var_matrix,dtype=float)
	res_matrix=np.array(res_matrix,dtype=float)
	return var_matrix.T,res_matrix.T, plik.index

def do_pca(input_arg,mds_data):

	pca = PCA(n_components=int(input_arg[5]))
	pca_results=pca.fit_transform(mds_data[0])
	if int(input_arg[5]) > 1:
		print 'explained variance ratio by first ',input_arg[5], ' components: %s' % str(pca.explained_variance_ratio_)
	else:
		print 'explained variance ratio by first component: %s' % str(pca.explained_variance_ratio_)
	return pca_results


def do_isomap(input_arg,mds_data):
	isomap = manifold.Isomap(n_neighbors=10, n_components=int(input_arg[5])).fit_transform(mds_data[0])
	return isomap

def do_mds(input_arg,mds_data):
	mds = manifold.MDS(int(input_arg[5]), max_iter=200, n_init=1)
	trans_data = mds.fit_transform(mds_data[0])
	return trans_data
def do_stochastic_embedding(input_arg,mds_data):
	tsne = manifold.TSNE(n_components=int(input_arg[5]), init='pca', random_state=0)
	trans_data = tsne.fit_transform(mds_data[0])
	return trans_data

def do_lle(input_arg,mds_data):
	trans_data = manifold.LocallyLinearEmbedding(n_neighbors = 10, n_components=int(input_arg[5]),method='standard').fit_transform(mds_data[0])
	return trans_data

def do_ltsa(input_arg,mds_data):
	trans_data = manifold.LocallyLinearEmbedding(n_neighbors = 10, n_components=int(input_arg[5]),eigen_solver='auto', method='ltsa').fit_transform(mds_data[0])
        return trans_data

def do_hess(input_arg,mds_data):
	trans_data = manifold.LocallyLinearEmbedding(n_neighbors = 10, n_components=int(input_arg[5]),eigen_solver='auto', method='hessian').fit_transform(mds_data[0])
        return trans_data

def do_spectral(input_arg,mds_data):
	se = manifold.SpectralEmbedding(n_components=int(input_arg[5]), n_neighbors=10).fit_transform(mds_data[0])
	return se

def do_mod_lle(input_arg,mds_data):
	trans_data = manifold.LocallyLinearEmbedding(n_neighbors = 10, n_components=int(input_arg[5]),method='modified').fit_transform(mds_data[0])
        return trans_data

def make_plot1d(input_arg,mds_data,mds,ax):
	#Straszny syf, w ogole nie kontroluje tych numpy'owych i pand'owych list przy rysowaniu wykresow
	labels=list(mds_data[2])
	if input_arg[2] != 0:
		Y_u=np.array(list(mds_data[1]), dtype=str)
		Y_u=np.unique(Y_u) # ok tutaj wiemy ile jest kategorii danych
		colors = matplotlib.cm.rainbow(np.linspace(0, 1, len(np.unique(Y_u))))
		for p,g in enumerate(Y_u):
    			ala=[list(mds[i]) for i,n in enumerate(mds_data[1]) if n == float(g)]
			labels_local=[labels[i] for i,n in enumerate(mds_data[1]) if n == float(g)] # musimy sledzic ktor label wpada do tej serii
			zeros=[0]*len(ala)
			ax.plot(ala, zeros, "s",color=colors[p], label=g)
			#plt.plot(ala, zeros, "s",color=colors[p])
			if input_arg[1] != 0 and input_arg[6]:
				for label,x,y in zip(labels_local,ala,zeros):
					ax.annotate(label, xy=(x[0],y), xytext = (10, 10), textcoords = 'offset points', ha = 'right', va = 'bottom', rotation=90)
	else: #tutaj uzytkownik nie podal kolumny wynikowej wiec nie ma po czym kolorowac
		zeros=[0]*len(mds)
		plt.plot(mds, zeros, "s", color="r",label=0)
		if input_arg[1] != 0 and input_arg[6]:
                                for label,x,y in zip(labels,mds,zeros):
                                        plt.annotate(label, xy=(x[0],y), xytext = (10, 10), textcoords = 'offset points', ha = 'right', va = 'bottom', rotation=90)
	ax.legend()

def make_plot2d(input_arg,mds_data,mds,ax):
	
	labels=list(mds_data[2])
	if input_arg[2] != 0:
		Y_u=np.array(list(mds_data[1]), dtype=str)
                Y_u=np.unique(Y_u) # ok tutaj wiemy ile jest kategorii danych
                colors = matplotlib.cm.rainbow(np.linspace(0, 1, len(np.unique(Y_u))))
		for p,g in enumerate(Y_u):
                        ala=[list(mds[i]) for i,n in enumerate(mds_data[1]) if n == float(g)]
			labels_local=[labels[i] for i,n in enumerate(mds_data[1]) if n == float(g)]
			x=[]
			y=[]
			for n,m in ala:
				x.append(n)
				y.append(m)
			ax.plot(x, y, "s",color=colors[p], label=g)
			if input_arg[1] != 0 and input_arg[6]:
                                for label,x,y in zip(labels_local,x,y):
					ax.annotate(label, xy=(x,y), xytext = (10, 10), textcoords = 'offset points', ha = 'right', va = 'bottom')

	else:
		x=[]
                y=[]
		for n,m in mds:
                        x.append(n)
                        y.append(m)
		ax.plot(x, y, "s",color="r",label=0)
		if input_arg[1] != 0 and input_arg[6]:
                                for label,x,y in zip(labels,x,y):
                                        ax.annotate(label, xy=(x,y), xytext = (10, 10), textcoords = 'offset points', ha = 'right', va = 'bottom')
	
	ax.legend()	

def make_plot3d(input_arg,mds_data,mds,ax):
        labels=list(mds_data[2])
        if input_arg[2] != 0:
                Y_u=np.array(list(mds_data[1]), dtype=str)
                Y_u=np.unique(Y_u) # ok tutaj wiemy ile jest kategorii danych
                colors = matplotlib.cm.rainbow(np.linspace(0, 1, len(np.unique(Y_u))))
                for p,g in enumerate(Y_u):
                        ala=[list(mds[i]) for i,n in enumerate(mds_data[1]) if n == float(g)]
                        x=[]
                        y=[]
                        z=[]

                        for n,m,b in ala:
                                x.append(n)
                                y.append(m)
                                z.append(b)

                        ax.plot(x, y, z, "s",color=colors[p],label=g)
        else:
                x=[]
                y=[]
                z=[]
                for n,m,b in mds:
                        x.append(n)
                        y.append(m)
                        z.append(b)
                ax.plot(x, y, z, "s",color="r",label=0)
	ax.legend()

if __name__=="__main__":
	input_arg=main(sys.argv[1:])
	w =time.localtime()[0:6]
	w=[str(n) for n in w]
	z= ''.join(w)
### do standarization###
if input_arg[4] == 1:
	mds_data=normalizacja(input_arg)
else:
	mds_data=prepare_data(input_arg)

#print mds_data[2]
### do pca ###
wszystko = False
if float(input_arg[7]) == 0:
	print "PCA"
	mds=do_pca(input_arg,mds_data)
elif float(input_arg[7]) == 1:
	print "Isomap"
	mds=do_isomap(input_arg,mds_data)
elif float(input_arg[7]) == 2:
	mds=do_mds(input_arg,mds_data)
elif float(input_arg[7]) == 3:
	mds=do_stochastic_embedding(input_arg,mds_data)
elif float(input_arg[7]) == 4:
	mds=do_lle(input_arg,mds_data)	
elif float(input_arg[7]) == 5:
	mds=do_ltsa(input_arg,mds_data)

elif float(input_arg[7]) == 6:
	mds=do_hess(input_arg,mds_data)

elif float(input_arg[7]) == 7:
	mds=do_spectral(input_arg,mds_data)

elif float(input_arg[7]) == 8:
	mds=do_mod_lle(input_arg,mds_data)

elif float(input_arg[7]) == 9:
	all=[do_pca(input_arg,mds_data), do_isomap(input_arg,mds_data), do_mds(input_arg,mds_data), do_stochastic_embedding(input_arg,mds_data), do_lle(input_arg,mds_data), do_ltsa(input_arg,mds_data), do_hess(input_arg,mds_data), do_spectral(input_arg,mds_data), do_mod_lle(input_arg,mds_data)]
	wszystko=True

all_name=["PCA", "isomap", "MDS", "stochastic_embedding", "LLE", "LTSA", "Hessian LLE",  "Spectral_Embedding", "Modified LLE"]

if wszystko:
	pos=0
	for n,p in zip(all,all_name):
		if pos == 0 and float(input_arg[5]) < 3:
			fig = plt.figure(figsize=(20, 10))
		elif pos == 0 and int(input_arg[5]) == 3:
			fig = plt.figure(figsize=(20, 10))
			#fig = plt.figure(figsize=plt.figaspect(1))		


		if float(input_arg[5]) == 1:
			ax = fig.add_subplot(259-pos)
			ax.set_title(p)
			
			make_plot1d(input_arg,mds_data,n,ax)
		elif float(input_arg[5]) == 2:
			ax = fig.add_subplot(259-pos)
			ax.set_title(p)
			#ax.set_xlim(-10,10)
			#ax.set_ylim(-10,10)
			make_plot2d(input_arg,mds_data,n,ax)	
		elif float(input_arg[5]) == 3:
                	ax = fig.add_subplot(259-pos, projection='3d')
			ax.set_title(p)
			make_plot3d(input_arg,mds_data,n,ax)

		pos+=1
### draw plot ###
#	print "Time to plot\n"
else:
	if float(input_arg[5]) == 1:
		ax=plt
		ax.title(all_name[int(input_arg[7])])
		make_plot1d(input_arg,mds_data,mds,ax)
	elif float(input_arg[5]) == 2:
		ax=plt
		ax.title(all_name[int(input_arg[7])])
		make_plot2d(input_arg,mds_data,mds,ax)
	elif float(input_arg[5]) == 3:
		fig = plt.figure()
        	ax = fig.add_subplot(111, projection='3d')
		ax.set_title(all_name[int(input_arg[7])])
		make_plot3d(input_arg,mds_data,mds,ax)
	else:
		print "Can't plot 4 or more dimensions\n"
if int(input_arg[8]) ==0:
	#plt.legend()
	plt.show()
elif int(input_arg[8]) ==1:
	plt.savefig(str(z)+".png")

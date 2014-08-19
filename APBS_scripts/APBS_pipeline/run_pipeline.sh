# This bash script automatize 3 steps (replacing the two previous separate .sh scripts) :

# 1) Translation of all PDBs in PQRs

for i in *.pdb
do
	file=$( basename $i)
	id=${file%%.*}
	/home/users/gmazz/opt/pdb2pqr/pdb2pqr.py --ff=amber ${file} ${id}.pqr
done

# 2) Generation of all the APBS input files .in

python apbs_in_gen.py

# 3) Lauch APBS and generation of .dx mashes

for i in *.in
do
	file=$( basename $i)
	id=${file%%.*}
	/home/users/gmazz/opt/APBS/bin/apbs ${file}
done

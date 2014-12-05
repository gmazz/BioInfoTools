# Extract the energy results from the header of the .pdb files generated from modeller and export
# them in a file that can be furhter parsed by the python script lower_energy.py  

for j in  ./*
do
	cd ${j}
	for i in *.pdb
	do
  		a=$( cat ${i} | grep 'OBJECTIVE FUNCTION' | sed s'/ /\t/'g | cut -f12-13)
  		echo ${i} ${a}
	done >> ${j}_energy_results.txt
	mv ${j}_energy_results.txt ..
	cd ..
done

#/bin/bash

a=`cat my_alignment.fst | grep ">" | sed 's/>//g' | tr '\n' ','`
template=${a:0:4}
pdb_template=${template}.pdb
plist=${a:5:-1}
echo ${plist} > list.txt

if [ -f $pdb_template ]
then
	echo "Preparing the model directories on $pdb_template"
	python fasta_from_pdb_9v2.py $pdb_template
	./make_model_from_fasta.pl -i my_alignment.fst -o ${plist} -t ${template} -n 1
else
	echo "File $pdb_template does not exist"
fi


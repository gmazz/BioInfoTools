Needed file for creating a model:

NOTE: Read the end of the file to see the commands to be lunched in the brand new modified pipeline (easier) :)

1. Multiple sequence alignment file (MSA) in FASTA format, having all the sequence aligned, comprising the template sequence.
(this file can be produced via pcma or other MSA + coping the sequences from SEEVIEW (edit, copy sequences). This will create a MSA in FASTA format)
In our case the file is called my_alignments.fa

2. The creation of the .pir file with the template correctly formatted (pir format) can be done using the original .pdb and lunching fasta_from_pdb_9v2.py
$ fasta_from_pdb_9v2.py template.pdb
The output template.pir file will be the used. Note that the name of pdb should be the same of the one used in the MSA FASTA file (i.e. 3a76_spdbv)

3. The file script make_model_from_fasta.pl using the correct name in the FASTA MSA. 

4. Every model.py file can be run in order to generate the model (additional files can automatize this procedure)

__________________________________________________________________________________________________________________
Create all model-directories:

1) The ./gogo.sh script run the command to generate all the models dirs.
./gogo.sh contains the :

-i (the correct input MSA-formatted file (e.g. my_alignments.fa)),
-o (the correct comma separated output directories correspondent to the protein names contained within my_alignments.fa file)
-t (the target PDB template)
-n (the number of models to be generated)

example: $ ./make_model_from_fasta.pl -i my_alignment.fa -o 7297_1,7297_2,7297_3 -t 3a76.pdb -n 5

2) Each generated model directory has a model.py file that has to be run in order to generate the model.
This process is trivially automatizable, but is better to run at least one model singularly in order to assure that the
files for model generation have been correctly generated.
_________________________________________________________

NEW MODIFIED PIPELINE:

./gogo.sh 	# create all the model directories
python run_auto.py	#run the modeling processes on all the files

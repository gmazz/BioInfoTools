multi_fasta=$($echo pwd)/$1
name=$(echo $multi_fasta | sed s'/.fasta//'g | sed s'/.fst//'g | sed s'/.fas//'g).csv
makeblastdb -in $multi_fasta -dbtype prot -out my_prot_blast_db;
blastp -db my_prot_blast_db -query $multi_fasta -outfmt 6 -out tmp.txt -num_threads 8
header="p_id,p_id2,distance"
echo $header >> $name
cat tmp.txt | cut -f1,2,11 | tr "\t" "," >> $name 
rm my_prot_blast_db* tmp.txt

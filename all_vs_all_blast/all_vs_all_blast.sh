#multi_fasta=$($echo pwd)/test_HA_sequences_db2.fas;
multi_fasta=$($echo pwd)/HA_sequences_db2.fas
makeblastdb -in $multi_fasta -dbtype prot -out my_prot_blast_db;
blastp -db my_prot_blast_db -query $multi_fasta -outfmt 6 -out all-vs-all_blast_nil.tsv -num_threads 24

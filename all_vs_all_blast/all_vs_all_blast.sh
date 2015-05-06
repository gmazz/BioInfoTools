multi_fasta=$($echo pwd)/crystals_local.fas
#multi_fasta=$($echo pwd)/HA_sequences_db2.fas
makeblastdb -in $multi_fasta -dbtype prot -out my_prot_blast_db;
blastp -db my_prot_blast_db -query $multi_fasta -outfmt 6 -out crystals_blastp.tsv -num_threads 8

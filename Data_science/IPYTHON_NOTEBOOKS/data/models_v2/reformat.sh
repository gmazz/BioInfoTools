cat new_models_scores | tr '\t' ',' | awk -F, '{print $1,$2,$3}' OFS=, | sed s'/.pdb//'g > RMSD_fwd.csv
cat new_models_scores | tr '\t' ',' | awk -F, '{print $2,$1,$3}' OFS=, | sed s'/.pdb//'g > RMSD_rev.csv
cat RMSD_fwd.csv RMSD_rev.csv >> RMSD.csv
rm RMSD_fwd.csv RMSD_rev.csv

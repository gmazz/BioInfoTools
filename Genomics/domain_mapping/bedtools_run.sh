for file in ./data/domains/*; do
	out_name=$(echo $file | sed s'/.bed/_genes.bed/'g | sed s'/domains/results/'g)
	echo $file $out_name
	bedtools intersect -a $file -b data/genome/genome_data_hg38_simple.bed -wa -wb\
	| awk '{if ($5>=$2 && $6<=$3) print $0}' | cut -f1,2,3,7 | uniq > $out_name
done

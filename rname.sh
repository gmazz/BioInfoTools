for i in *.pdb
do
	file=$( basename $i )
	id=${file%%.*}
	mv ${i} ${id}_GM.pdb
done


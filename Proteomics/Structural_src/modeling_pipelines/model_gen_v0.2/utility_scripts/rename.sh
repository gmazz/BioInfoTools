for i in *;
do
	if [ -f ${i}/my_alignment.fas ]
		then
			echo ${i}
			mv ${i}/my_alignment.fas ${i}/my_alignment.fst
	fi
done

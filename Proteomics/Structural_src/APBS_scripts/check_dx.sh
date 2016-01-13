for i in *.dx
	do
		num=$( cat ${i} | wc -l)

		if [ ${num} != 893083 ]; then
			if [ -d "TO_CHECK" ]; then
				du -h ${i}
				echo ${num}
				mv ${i} TO_CHECK/
			else
				mkdir TO_CHECK
				du -h ${i}
				echo ${num}
				mv ${i} TO_CHECK/
			fi
		fi
	done

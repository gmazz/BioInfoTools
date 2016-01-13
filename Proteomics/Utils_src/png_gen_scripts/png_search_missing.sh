for i in *.dx
	do
		id=$( ls ${i} | sed s'/.dx//'g)
		png=${id}.png
		if [ ! -f ${png} ]; then
			echo ${i} >> missing.txt
		fi
	done


mkdir missing_png_dx

while read line
do
	mv ${line} missing_png_dx/
done < missing.txt

mv png_gen.py missing_png_dx/
cd missing_png_dx/
python png_gen.py
mv *.dx ..
mv *.png ..
mv png_gen.py ..
cd ..

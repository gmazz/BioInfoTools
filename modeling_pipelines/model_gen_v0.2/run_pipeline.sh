root=$(pwd)
for r in running2/*
do
	name=$(echo ${r} | sed s'/running\///'g)
	cp mod_pipeline/* ${r}/
	cd ${r}
	screen -S ${name} -dm bash -c './run.sh; ./clean.sh ; ./clean_pipeline.sh'
	cd ${root}
done

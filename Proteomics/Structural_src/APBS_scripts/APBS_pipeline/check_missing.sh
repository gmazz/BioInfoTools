# Script to check and run if all dx in a dir are computed (if the APBS algorithm is converging for all the models or not).
# If some of the .dx are missing APBS is re-runned for these corresponding models. 
# Example of usage: $ ./check_missing.sh H1N1_42_algn
# Note the ouputs are located in the parent directory of H1N1_42_algn and NOT directly in the H1N1_42_algn for additional control. 

DIR=$1

i=./${DIR}/*.dx	
j=./${DIR}/*.in

for file in ${i}
do 
   dx_id=$( basename $file)
   echo ${dx_id} | sed s'/.dx//'g >> list_dx
done

for file in ${j}
do
   in_id=$( basename $file)
   echo ${in_id} | sed s'/.in//'g >> list_in
done


diff list_in list_dx > diff_list_${DIR}
final_list=$( cat diff_list_${DIR} | grep "<" | sed s'/< //'g )

for t in ${final_list}
do
  target=./${DIR}/${t}.in
  echo ${target}
  /home/users/gmazz/opt/APBS/bin/apbs ${target}  
done

rm -f list_in
rm -f list_dx


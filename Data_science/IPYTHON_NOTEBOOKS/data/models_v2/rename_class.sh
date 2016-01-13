while read l           
do           
    id=$( echo $l | cut -f1 -d. )
    val=$( echo $l | cut -f2 -d, )	    
    echo $id,$val      

done <class_1.csv 

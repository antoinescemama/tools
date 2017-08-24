 while read my_pass
 do
     echo "$my_pass"
     echo $my_pass | sudo -S whoami &>> suCrackerResult.txt
 done < $1

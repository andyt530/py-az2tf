for i in `ls *_azurerm_*.sh` ;do
j=`echo $i | cut -f1 -d '.'`
#cp $i $j.py
./convert.sh $j.py
done

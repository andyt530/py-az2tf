for i in `ls *_azurerm_*.sh` ;do
j=`echo $i | cut -f1 -d '.'`
echo "#import $j"
done

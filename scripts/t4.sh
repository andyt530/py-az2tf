for i in `ls *_azurerm_*.py` ;do
k=`echo $i | cut -f2,3,4,5,6,7,8 -d '_'`
mv $i $k
done

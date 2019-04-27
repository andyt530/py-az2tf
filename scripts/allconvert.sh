for i in `ls *_azurerm_*.sh` ;do
j=`echo $i | cut -f1 -d '.'`
cp $i $j.pyi
./convert.sh $j.pyi
cp stub.py $j.py
done

for i in `ls *_azurerm_*.sh` ;do
j=`echo $i | cut -f1 -d '.'`
tc=`echo $i | cut -f1 -d '_'`
k=`echo $j | cut -f2,3,4,5,6,7,8 -d '_'`
fpy=`echo "$j.py"`
echo $fpy
fpyi=`echo "$j.pyi"`
echo $fpyi
echo "# $k" > $fpy
echo "def $k(crf,cde,crg,headers,requests,sub,json,az2tfmess):" >> $fpy
printf  "    tfp=\"%s\"\n" $k  >> $fpy
printf  "    tcode=\"%s-\"\n" $tc  >> $fpy
cat stub1.py >> $fpy
cat $fpyi >> $fpy
cat stub2.py >> $fpy
done

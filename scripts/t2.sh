for i in `ls *_azurerm_*.sh` ;do
j=`echo $i | cut -f1 -d '.'`
k=`echo $j | cut -f2,3,4,5,6,7,8 -d '_'`
echo "# $j"
echo "# $j.$k(crf,cde,crg,headers,requests,sub,json,az2tfmess)"
done

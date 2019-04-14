tfp="azurerm_resource_group"
prefixa="rg"
echo $TF_VAR_rgtarget
if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
echo $rgsource
#azr=`az group show -n $rgsource -o json`
comm=`printf "cat %s.json | jq '.[] | select (.name==\"%s\")'" $tfp $rgsource`
azr=`eval $comm`
#echo $azr | jq .
name=`echo $azr | jq '.name' | tr -d '"'`
rname=`echo $name | sed 's/\./-/g'`
loc=`echo $azr | jq '.location' | tr -d '"'`
id=`echo $azr | jq '.id' | tr -d '"'`
rg=$name
prefix=`printf "%s__%s" $tfp $rname`
printf "resource \"%s\" \"%s\" {\n"  $tfp $rname > $prefix.tf
printf "\t name = \"%s\"\n" $name >> $prefix.tf
printf "\t location = \"%s\"\n" $loc >> $prefix.tf


#
# Tags block
#
tags=`echo $azr | jq ".tags"`
tt=`echo $tags | jq .`
tcount=`echo $tags | jq '. | length'`
if [ "$tcount" -gt "0" ]; then
    printf "\t tags { \n" >> $prefix.tf
    tt=`echo $tags | jq .`
 
    keys=`echo $tags | jq 'keys'`
    tcount=`expr $tcount - 1`
    for j in `seq 0 $tcount`; do
        k1=`echo $keys | jq ".[(${j})]"`
        #echo "key=$k1"
        re="[[:space:]]+"
        if [[ $k1 =~ $re ]]; then
        tval=`echo $tt | jq ."$k1"`
        tkey=`echo $k1 | tr -d '"'`
        printf "\t\t\"%s\" = %s \n" "$tkey" "$tval" >> $prefix.tf
        else
        tval=`echo $tt | jq .$k1`
        tkey=`echo $k1 | tr -d '"'`
        printf "\t\t%s = %s \n" $tkey "$tval" >> $prefix.tf
        fi
    done
    printf "\t}\n" >> $prefix.tf
fi

echo "}" >> $prefix.tf
cat $prefix.tf
#
terraform state rm  $tfp.$rname
echo "terraform state rm  $tfp.$rname" >> tf-staterm.sh
terraform import $tfp.$rname $id
echo "terraform import $tfp.$rname $id" >> tf-stateimp.sh
#

tfp="azurerm_management_lock"
prefixa="lck"
if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
azr=`az lock list -g $rgsource`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        oname=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        oname2=`echo $azr | jq ".[(${i})].name"`
        level=`echo $azr | jq ".[(${i})].level"`
        notes=`echo $azr | jq ".[(${i})].notes"`
        id=`echo $azr | jq ".[(${i})].id"`

        echo $azr | jq ".[(${i})]"
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | tr -d '"'`
        echo "name =" $name rg=$rg
        #
        # scope is in the id
        #
        t=`echo $id | awk -F 'Microsoft.Authorization' '{print $1}' `
        scope=`echo ${t%/providers/}`

        prefix=`printf "%s__%s" $prefixa $rg`
        echo "prefix="  $prefix
        rname=`echo ${oname//[/_}` 
        name=`echo ${rname//]/_}` 
        name=`echo ${name// /_}`
        echo "name =" $name rg=$rg
 #      printf "data \"azurerm_subscription\" \"primary\" {}\n\n" $prefix-$name.tf
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $name > $prefix-$name.tf
        printf "name = %s\n"  "$oname2"  >> $prefix-$name.tf
        printf "lock_level = %s\n" "$level" >> $prefix-$name.tf
        printf "notes = %s \n" "$notes" >> $prefix-$name.tf
        printf "scope = %s\" \n"  "$scope" >> $prefix-$name.tf
        #
       
        printf "}\n" >> $prefix-$name.tf
        
        cat $prefix-$name.tf
        statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $name`
        echo $statecomm >> tf-staterm.sh
        eval $statecomm
        evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $name "$id"`
        echo $evalcomm >> tf-stateimp.sh
        eval $evalcomm
        
        
    done
fi

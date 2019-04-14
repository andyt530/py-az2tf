tfp="azurerm_role_assignment"
prefixa="ras"
if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
azr=`az role assignment list -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        echo $i " of " $count
        name=`echo $azr | jq ".[(${i})].name"`
        echo name - $name
        scope=`echo $azr | jq ".[(${i})].scope"`
        rdid=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        prid=`echo $azr | jq ".[(${i})].principalId"`
        roledefid=`echo $azr | jq ".[(${i})].roleDefinitionId" | cut -d'/' -f7 | tr -d '"'`
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        rg="roleAssignments"
        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $name`
        echo $az2tfmess > $prefix-$rdid.tf
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rdid >> $prefix-$rdid.tf
        printf "name = %s\n" "$name"  >> $prefix-$rdid.tf
        printf "role_definition_id = \"\${azurerm_role_definition.%s__%s.id}\"\n" "roleDefinitions" $roledefid >> $prefix-$rdid.tf
        
        printf "principal_id = %s\n" "$prid" >> $prefix-$rdid.tf
        printf "scope = %s\n" "$scope"  >> $prefix-$rdid.tf
   
        printf "}\n" >> $prefix-$rdid.tf
        
        cat $prefix-$rdid.tf
        statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $rdid`
        echo $statecomm >> tf-staterm.sh
        eval $statecomm
        evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $rdid $id`
        echo $evalcomm >> tf-stateimp.sh
        eval $evalcomm
        
        
    done
fi

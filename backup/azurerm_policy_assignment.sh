tfp="azurerm_policy_assignment"
prefixa="pas"
if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
azr=`az policy assignment list`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        
        dname=`echo $azr | jq ".[(${i})].displayName"`
        rdid=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        desc=`echo $azr | jq ".[(${i})].description"`
        scope=`echo $azr | jq ".[(${i})].scope" | tr -d '"'`
        pdid=`echo $azr | jq ".[(${i})].policyDefinitionId" | tr -d '"'`
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        rg="policyAssignments"
        
        params=`echo $azr | jq ".[(${i})].parameters"`
        
        
        prefix=`printf "%s__%s" $prefixa $rg`
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rdid > $prefix-$rdid.tf
        printf "name = \"%s\"\n" "$rdid"  >> $prefix-$rdid.tf
        printf "display_name = %s\n" "$dname"  >> $prefix-$rdid.tf
        printf "policy_definition_id = \"%s\"\n" "$pdid" >> $prefix-$rdid.tf
        printf "scope = \"%s\"\n" $scope >> $prefix-$rdid.tf
        if [ "$desc" != "null" ]; then
            printf "description = %s\n" "$desc" >> $prefix-$rdid.tf
        fi
        pl=`echo $params | jq '. | length'`
        if [ "$pl" -gt "0" ]; then
            printf "parameters =<<PARAMETERS\n"  >> $prefix-$rdid.tf
            printf "%s\n" "$params" >> $prefix-$rdid.tf
            printf "PARAMETERS\n"  "$params" >> $prefix-$rdid.tf
        fi
        printf "\n}\n" >> $prefix-$rdid.tf
        
        cat $prefix-$rdid.tf
        statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $rdid`
        echo $statecomm >> tf-staterm.sh
        eval $statecomm
        evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $rdid $id`
        echo $evalcomm >> tf-stateimp.sh
        eval $evalcomm
        
        
    done
fi

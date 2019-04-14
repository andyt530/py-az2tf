tfp="azurerm_policy_definition"
prefixa="pdf"
if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
azr=`az policy definition list`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        echo $i " of " $count
        pt=`echo $azr | jq ".[(${i})].policyType" | tr -d '"'`
        
        if [ $pt = "Custom" ]; then
            dname=`echo $azr | jq ".[(${i})].displayName"`
            rdid=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
            desc=`echo $azr | jq ".[(${i})].description"`
            mode=`echo $azr | jq ".[(${i})].mode" | tr -d '"'`
            pt=`echo $azr | jq ".[(${i})].policyType" | tr -d '"'`
            id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
            rg="policyDefinitions"
            
            params=`echo $azr | jq ".[(${i})].parameters"`
            prules=`echo $azr | jq ".[(${i})].policyRule"`
            meta=`echo $azr | jq ".[(${i})].metadata"`
            
            prefix=`printf "%s__%s" $prefixa $rg`
            
            printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rdid > $prefix-$rdid.tf
            printf "name = \"%s\"\n" "$rdid"  >> $prefix-$rdid.tf
            printf "display_name = %s\n" "$dname"  >> $prefix-$rdid.tf
            printf "policy_type = \"%s\"\n" "$pt" >> $prefix-$rdid.tf
            printf "mode = \"%s\"\n" $mode >> $prefix-$rdid.tf
            if [ "$desc" != "null" ]; then
                printf "description = %s\n" "$desc" >> $prefix-$rdid.tf
            fi 
            printf "metadata =<<META\n"  >> $prefix-$rdid.tf
            printf "%s\n" "$meta" >> $prefix-$rdid.tf
            printf "META\n" >> $prefix-$rdid.tf



            printf "policy_rule =<<POLICY_RULE\n"  >> $prefix-$rdid.tf
            printf "%s\n" "$prules" >> $prefix-$rdid.tf
            printf "POLICY_RULE\n" >> $prefix-$rdid.tf
            
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
        fi
        
    done
fi

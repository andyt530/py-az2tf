tfp="azurerm_role_definition"
prefixa="rdf"
if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
azr=`az role definition list -o json`
#azr=`az role definition list --query "[?roleType!='BuiltInRole']" -o json` 
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        echo $i " of " $count
        
        name=`echo $azr | jq ".[(${i})].roleName"`
 
        rdid=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        desc=`echo $azr | jq ".[(${i})].description"`
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        rg="roleDefinitions"

        scopes=`echo $azr | jq ".[(${i})].assignableScopes"`
        dactions=`echo $azr | jq ".[(${i})].permissions[0].dataActions"`
        ndactions=`echo $azr | jq ".[(${i})].permissions[0].notDataActions"`
        actions=`echo $azr | jq ".[(${i})].permissions[0].actions"`
        nactions=`echo $azr | jq ".[(${i})].permissions[0].notActions"`

        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $name`
        echo $az2tfmess > $prefix-$rdid.tf
        
 #      printf "data \"azurerm_subscription\" \"primary\" {}\n\n" $prefix-$rdid.tf
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rdid >> $prefix-$rdid.tf
        printf "name = %s\n" "$name"  >> $prefix-$rdid.tf
        printf "role_definition_id = \"%s\"\n" >> $prefix-$rdid.tf
        printf "description = %s\n" "$desc" >> $prefix-$rdid.tf
#        printf "scope = \"\${data.azurerm_subscription.primary.id}\"\n"  >> $prefix-$rdid.tf
#        printf "scope = \"/subscriptions/%s\"\n" $rgsource >> $prefix-$rdid.tf
        printf "scope = \"\"\n"  >> $prefix-$rdid.tf
        #
        printf "permissions { \n" >> $prefix-$rdid.tf
    
        printf "data_actions = \n" >> $prefix-$rdid.tf
        printf "%s\n" $dactions >> $prefix-$rdid.tf

        printf "not_data_actions = \n" >> $prefix-$rdid.tf
        printf "%s\n" $ndactions >> $prefix-$rdid.tf

        printf "actions = \n" >> $prefix-$rdid.tf
        printf "%s\n" $actions >> $prefix-$rdid.tf
    
        printf "not_actions = \n"  >> $prefix-$rdid.tf
        printf "%s\n" $nactions >> $prefix-$rdid.tf
    
        printf "} \n" >> $prefix-$rdid.tf
        
        printf "assignable_scopes =  \n" >> $prefix-$rdid.tf
        printf "%s\n" $scopes >> $prefix-$rdid.tf
       
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

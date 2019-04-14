tfp="azurerm_public_ip"
prefixa="pip"
if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
azr=`az network public-ip list -g $rgsource`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | tr -d '"'`
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`

        prefix=`printf "%s__%s" $prefixa $rg`
        subipalloc=`echo $azr | jq ".[(${i})].publicIpAllocationMethod" | tr -d '"'`
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $name > $prefix-$name.tf
        printf "\t name = \"%s\"\n" $name >> $prefix-$name.tf
        printf "\t location = \"%s\"\n" $loc >> $prefix-$name.tf
        #printf "\t resource_group_name = \"\${var.rgtarget}\"\n" >> $prefix-$name.tf
        printf "\t resource_group_name = \"%s\"\n" $rg >> $prefix-$name.tf
        printf "\t public_ip_address_allocation = \"%s\" \n"  $subipalloc >> $prefix-$name.tf
        #
        printf "}\n" >> $prefix-$name.tf
        #
        cat $prefix-$name.tf
        statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $name`
        echo $statecomm >> tf-staterm.sh
        eval $statecomm
        evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $name $id`
        echo $evalcomm >> tf-stateimp.sh
        eval $evalcomm
    done
fi

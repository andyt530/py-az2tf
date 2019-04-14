tfp="azurerm_subnet"
prefixa="sub"
if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
#
#
vnets=`az network vnet list -g $rgsource`
count=`echo $vnets | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for j in `seq 0 $count`; do
        vname=`echo $vnets | jq ".[(${j})].name" | tr -d '"'`
        #
        azr=`az network vnet subnet list -g $rgsource --vnet-name $vname`
        scount=`echo $azr | jq '. | length'`
        scount=`expr $scount - 1`
        for i in `seq 0 $scount`; do
            name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
            rg=`echo $azr | jq ".[(${i})].resourceGroup" | tr -d '"'`
            id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
            # subnets don't have a location
            prefix=`printf "%s__%s" $prefixa $rg`
            sprefix=`echo $azr | jq ".[(${i})].addressPrefix" | tr -d '"'`
            
            seps=`echo $azr | jq ".[(${i})].serviceEndpoints"`
            sep1=`echo $azr | jq ".[(${i})].serviceEndpoints[0].service"`
            sep2=`echo $azr | jq ".[(${i})].serviceEndpoints[1].service"`
            sep="null"
            rtbid="null"
            if [ "$sep1" != "null" ]; then
                sep=`printf "[%s]" $sep1`
            fi
            if [ "$sep2" != "null" ]; then
                sep=`printf "[%s,%s]" $sep1 $sep2`
            fi
            
            snsg=`echo $azr | jq ".[(${i})].networkSecurityGroup.id" | cut -f9 -d"/" | tr -d '"'`
            snsgrg=`echo $azr | jq ".[(${i})].networkSecurityGroup.id" | cut -f5 -d"/" | tr -d '"'`
            
            echo $az2tfmess > $prefix-$name.tf
            printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $name > $prefix-$name.tf
            printf "\t name = \"%s\"\n" $name >> $prefix-$name.tf
            
            printf "\t virtual_network_name = \"%s\"\n" $vname >> $prefix-$name.tf
            printf "\t address_prefix = \"%s\"\n" $sprefix >> $prefix-$name.tf
            rtbid=`echo $azr | jq ".[(${i})].routeTable.id" | cut -f9 -d"/" | tr -d '"'`
            rtrg=`echo $azr | jq ".[(${i})].routeTable.id" | cut -f5 -d"/" | tr -d '"'`
            #printf "\t resource_group_name = \"\${var.rgtarget}\"\n" >> $prefix-$name.tf
            printf "\t resource_group_name = \"%s\"\n" $rg >> $prefix-$name.tf
            if [ "$snsg" != "null" ]; then
                printf "\t network_security_group_id = \"\${azurerm_network_security_group.%s__%s.id}\"\n" $snsgrg $snsg >> $prefix-$name.tf
            fi
            if [ "$sep" != "null" ]; then
                printf "\t service_endpoints = %s\n" $sep >> $prefix-$name.tf
            fi
            if [ "$rtbid" != "null" ]; then
                printf "\t route_table_id = \"\${azurerm_route_table.%s__%s.id}\"\n" $rtrg $rtbid >> $prefix-$name.tf
            fi

            printf "}\n" >> $prefix-$name.tf
            cat $prefix-$name.tf
            statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $name`
            echo $statecomm >> tf-staterm.sh
            eval $statecomm
            evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $name $id`
            echo $evalcomm >> tf-stateimp.sh
            eval $evalcomm
        done
    done
fi

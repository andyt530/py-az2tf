prefixa=`echo $0 | awk -F 'azurerm_' '{print $2}' | awk -F '.sh' '{print $1}' `
tfp=`printf "azurerm_%s" $prefixa`
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
vnets=`az network vnet list -g $rgsource -o json`
count=`echo $vnets | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for j in `seq 0 $count`; do
        vname=`echo $vnets | jq ".[(${j})].name" | tr -d '"'`
        #
        azr=`az network vnet subnet list -g $rgsource --vnet-name $vname -o json`
        scount=`echo $azr | jq '. | length'`
        scount=`expr $scount - 1`
        for i in `seq 0 $scount`; do
            name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
            rname=`echo $name | sed 's/\./-/g'`
            rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`
            id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
            # subnets don't have a location
            prefix=`printf "%s__%s" $prefixa $rg`
            outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
            echo $az2tfmess > $outfile

            sprefix=`echo $azr | jq ".[(${i})].addressPrefix" | tr -d '"'`
            sep="null"
            rtbid="null"
            seps=`echo $azr | jq ".[(${i})].serviceEndpoints"`
            jcount=`echo $seps | jq '. | length'`
            jcount=`expr $jcount - 1`
            echo $jcount
            echo $seps
            if [ "$seps" != "null" ]; then
            if [ "$seps" != "[]" ]; then
            sep="["
                    for j in `seq 0 $jcount`; do
                        service=`echo $seps | jq ".[(${j})].service" | tr -d '"'`
                        if [ $j -eq $jcount ] ; then 
                            sep=`printf "%s\"%s\"" $sep $service`
                        else
                            sep=`printf "%s\"%s\"," $sep $service`
                        fi
                    done
            sep=`printf "%s]" $sep`
            fi
            fi
            
            snsgid=`echo $azr | jq ".[(${i})].networkSecurityGroup.id" | cut -f9 -d"/" | sed 's/\./-/g' | tr -d '"'`
            snsgrg=`echo $azr | jq ".[(${i})].networkSecurityGroup.id" | cut -f5 -d"/" | sed 's/\./-/g' | tr -d '"'` 
            rtbid=`echo $azr | jq ".[(${i})].routeTable.id" | cut -f9 -d"/" | sed 's/\./-/g' | tr -d '"'`
            rtrg=`echo $azr | jq ".[(${i})].routeTable.id" | cut -f5 -d"/" | sed 's/\./-/g' | tr -d '"'`

            printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
            printf "\t name = \"%s\"\n" $name >> $outfile
            printf "\t virtual_network_name = \"%s\"\n" $vname >> $outfile
            printf "\t address_prefix = \"%s\"\n" $sprefix >> $outfile
            printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
            

            if [ "$snsgrg" != "null" ]; then
                printf "\t network_security_group_id = \"\${azurerm_network_security_group.%s__%s.id}\"\n" $snsgrg $snsgid >> $outfile
            fi
            if [ "$sep" != "null" ]; then

                printf "\t service_endpoints = %s\n" $sep >> $outfile
            fi
            if [ "$rtrg" != "null" ]; then
                printf "\t route_table_id = \"\${azurerm_route_table.%s__%s.id}\"\n" $rtrg $rtbid >> $outfile
            fi

            printf "}\n" >> $outfile
            cat $outfile

# azurerm_subnet_network_security_group_association
     
            r1="skip"
            if [ "$snsgid" != "null" ]; then
                r1="azurerm_subnet_network_security_group_association"
                outsnsg=`printf "%s.%s__%s__%s.tf" $r1 $rg $rname $snsgid`
                echo $az2tfmess > $outsnsg
                printf "resource \"%s\" \"%s__%s__%s\" {\n" $r1 $rg $rname $snsgid  >> $outsnsg
                printf "\tsubnet_id = \"\${azurerm_subnet.%s__%s.id}\"\n" $rg $rname >> $outsnsg
                printf "\tnetwork_security_group_id = \"\${azurerm_network_security_group.%s__%s.id}\"\n" $snsgrg $snsgid >> $outsnsg
                printf "}\n" >> $outsnsg
                cat $outsnsg
            fi

# azurerm_subnet_route_table_association

            r2="skip"
            if [ "$rtbid" != "null" ]; then
                r2="azurerm_subnet_route_table_association"
                outrtbid=`printf "%s.%s__%s__%s.tf" $r2 $rg $rname $rtbid`
                echo $az2tfmess > $outrtbid
                printf "resource \"%s\" \"%s__%s__%s\" {\n" $r2 $rg $rname $rtbid >> $outrtbid
                printf "\tsubnet_id = \"\${azurerm_subnet.%s__%s.id}\"\n" $rg $rname >> $outrtbid
                printf "\troute_table_id = \"\${azurerm_route_table.%s__%s.id}\"\n" $rtrg $rtbid >> $outrtbid
                printf "}\n" >> $outrtbid
                cat $outrtbid
            fi


# azurerm_subnet_network_security_group_association

            if [ "$r1" != "skip" ]; then
            statecomm=`printf "terraform state rm %s.%s__%s__%s" $r1 $rg $rname $snsgid`
            echo $statecomm >> tf-staterm.sh
            eval $statecomm
            evalcomm=`printf "terraform import %s.%s__%s__%s %s" $r1 $rg $rname $snsgid $id` # uses subnet id
            echo $evalcomm >> tf-stateimp.sh
            eval $evalcomm
            fi

# azurerm_subnet_route_table_association

            if [ "$r2" != "skip" ]; then
            statecomm=`printf "terraform state rm %s.%s__%s__%s" $r2 $rg $rname $rtbid`
            echo $statecomm >> tf-staterm.sh
            eval $statecomm
            evalcomm=`printf "terraform import %s.%s__%s__%s %s" $r2 $rg $rname $rtbid $id`  # uses subnet id
            echo $evalcomm >> tf-stateimp.sh
            eval $evalcomm
            fi

# azurerm_subnet

            statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $rname`
            echo $statecomm >> tf-staterm.sh
            eval $statecomm
            evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $rname $id`
            echo $evalcomm >> tf-stateimp.sh
            eval $evalcomm
        done
    done
fi

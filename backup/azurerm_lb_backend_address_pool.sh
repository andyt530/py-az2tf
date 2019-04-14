tfp="azurerm_lb_backend_address_pool"
prefixa="lbbe"
if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
azr=`az network lb list -g $rgsource`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        beap=`echo $azr | jq ".[(${i})].backendAddressPools"`

       
        
        icount=`echo $beap | jq '. | length'`
        if [ "$icount" -gt "0" ]; then
            icount=`expr $icount - 1`
            for j in `seq 0 $icount`; do
                
                name=`echo $azr | jq ".[(${i})].backendAddressPools[(${j})].name" | cut -d'/' -f11 | tr -d '"'`
                id=`echo $azr | jq ".[(${i})].backendAddressPools[(${j})].id" | tr -d '"'`
                rg=`echo $azr | jq ".[(${i})].backendAddressPools[(${j})].resourceGroup" | tr -d '"'`
                
                lbrg=`echo $azr | jq ".[(${i})].id" | cut -d'/' -f5 | tr -d '"'`
                lbname=`echo $azr | jq ".[(${i})].id" | cut -d'/' -f9 | tr -d '"'`
                prefix=`printf "%s__%s--%s" $prefixa $rg $lbname`
                
                
                printf "resource \"%s\" \"%s__%s--%s\" {\n" $tfp $rg $lbname $name > $prefix-$name.tf
                printf "\t\t name = \"%s\" \n"  $name >> $prefix-$name.tf
                printf "\t\t resource_group_name = \"%s\" \n"  $rg >> $prefix-$name.tf
                printf "\t\t loadbalancer_id = \"\${azurerm_lb.%s__%s.id}\"\n" $lbrg $lbname >> $prefix-$name.tf

                printf "}\n" >> $prefix-$name.tf
        #
                cat $prefix-$name.tf
                statecomm=`printf "terraform state rm %s.%s__%s--%s" $tfp $rg $lbname $name`
                echo $statecomm >> tf-staterm.sh
                eval $statecomm
                evalcomm=`printf "terraform import %s.%s__%s--%s %s" $tfp $rg $lbname $name $id`
                echo $evalcomm >> tf-stateimp.sh
                eval $evalcomm




        #

            done
        fi

        


 
    done
fi

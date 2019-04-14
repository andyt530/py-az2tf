tfp="azurerm_lb_rule"
prefixa="lbr"
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
        beap=`echo $azr | jq ".[(${i})].loadBalancingRules"`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | tr -d '"'`
        prefix=`printf "%s__%s" $prefixa $rg`       
        
        icount=`echo $beap | jq '. | length'`
        if [ "$icount" -gt "0" ]; then
            icount=`expr $icount - 1`
            for j in `seq 0 $icount`; do
                
                name=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].name" | cut -d'/' -f11 | tr -d '"'`
                id=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].id" | tr -d '"'`
                rrg=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].resourceGroup" | tr -d '"'`
                fep=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].frontendPort" | tr -d '"'`
                bep=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].backendPort" | tr -d '"'`
                proto=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].protocol" | tr -d '"'`
                feipc=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].frontendIpConfiguration.id" | cut -d'/' -f11 | tr -d '"'`
                efip=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].enableFloatingIp" | tr -d '"'`
                ld=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].loadDistribution" | tr -d '"'`
                itm=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].idleTimeoutInMinutes" | tr -d '"'`

                pid=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].probe.id" | cut -d'/' -f11 | tr -d '"'`
                beadpid=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].backendAddressPool.id" | cut -d'/' -f11 | tr -d '"'`

                
                lbrg=`echo $azr | jq ".[(${i})].id" | cut -d'/' -f5 | tr -d '"'`
                lbname=`echo $azr | jq ".[(${i})].id" | cut -d'/' -f9 | tr -d '"'`
                
                printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $name > $prefix-$name.tf
                printf "\t\t name = \"%s\" \n"  $name >> $prefix-$name.tf
                printf "\t\t resource_group_name = \"%s\" \n"  $rrg >> $prefix-$name.tf
                printf "\t\t loadbalancer_id = \"\${azurerm_lb.%s__%s.id}\"\n" $lbrg $lbname >> $prefix-$name.tf
                printf "\t\t frontend_ip_configuration_name = \"%s\" \n"  $feipc >> $prefix-$name.tf
                printf "\t\t protocol = \"%s\" \n"  $proto >> $prefix-$name.tf   
                printf "\t\t frontend_port = \"%s\" \n"  $fep >> $prefix-$name.tf
                printf "\t\t backend_port = \"%s\" \n"  $bep >> $prefix-$name.tf
                
                printf "\t\t backend_address_pool_id = \"\${azurerm_lb_backend_address_pool.%s__%s--%s.id}\"\n" $rg $lbname $beadpid >> $prefix-$name.tf
                printf "\t\t probe_id = \"\${azurerm_lb_probe.%s__%s.id}\"\n" $rg $pid >> $prefix-$name.tf
                
                printf "\t\t enable_floating_ip = \"%s\" \n"  $efip >> $prefix-$name.tf
                printf "\t\t idle_timeout_in_minutes = \"%s\" \n"  $itm >> $prefix-$name.tf
                printf "\t\t load_distribution = \"%s\" \n"  $ld >> $prefix-$name.tf


                printf "}\n" >> $prefix-$name.tf
        #
                cat $prefix-$name.tf
                statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $name`
                echo $statecomm >> tf-staterm.sh
                eval $statecomm
                evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $name $id`
                echo $evalcomm >> tf-stateimp.sh
                eval $evalcomm




        #

        done
        fi

        


 
    done
fi

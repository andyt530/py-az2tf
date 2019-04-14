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
azr=`az network lb list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        beap=`echo $azr | jq ".[(${i})].loadBalancingRules"`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`
        lbrg=`echo $azr | jq ".[(${i})].id" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
        lbname=`echo $azr | jq ".[(${i})].id" | cut -d'/' -f9 | sed 's/\./-/g' | tr -d '"'`
        
        icount=`echo $beap | jq '. | length'`
        if [ "$icount" -gt "0" ]; then
            icount=`expr $icount - 1`
            for j in `seq 0 $icount`; do
                
                name=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].name" | cut -d'/' -f11 | tr -d '"'`
                rname=`echo $name | sed 's/\./-/g'`
                id=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].id" | tr -d '"'`
                rrg=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`
                fep=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].frontendPort" | tr -d '"'`
                bep=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].backendPort" | tr -d '"'`
                proto=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].protocol" | tr -d '"'`
                feipc=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].frontendIpConfiguration.id" | cut -d'/' -f11 | tr -d '"'`
                efip=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].enableFloatingIp" | tr -d '"'`
                ld=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].loadDistribution" | tr -d '"'`
                itm=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].idleTimeoutInMinutes" | tr -d '"'`

                prg=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].probe.id" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
                pid=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].probe.id" | cut -d'/' -f11 | sed 's/\./-/g' | tr -d '"'`
                beadprg=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].backendAddressPool.id" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
                beadpid=`echo $azr | jq ".[(${i})].loadBalancingRules[(${j})].backendAddressPool.id" | cut -d'/' -f11 | sed 's/\./-/g' | tr -d '"'`

                prefix=`printf "%s__%s" $prefixa $rg` 
                outfile=`printf "%s.%s__%s__%s.tf" $tfp $rrg $lbname $rname`  
                echo $az2tfmess > $outfile 
             
                printf "resource \"%s\" \"%s__%s__%s\" {\n" $tfp $rg $lbname $rname >> $outfile
                printf "\t\t name = \"%s\" \n"  $name >> $outfile
                #printf "\t\t resource_group_name = \"%s\" \n"  $rrg >> $outfile
                printf "\t\t resource_group_name = \"%s\" \n"  $rgsource >> $outfile
                printf "\t\t loadbalancer_id = \"\${azurerm_lb.%s__%s.id}\"\n" $lbrg $lbname >> $outfile
                printf "\t\t frontend_ip_configuration_name = \"%s\" \n"  $feipc >> $outfile
                printf "\t\t protocol = \"%s\" \n"  $proto >> $outfile   
                printf "\t\t frontend_port = \"%s\" \n"  $fep >> $outfile
                printf "\t\t backend_port = \"%s\" \n"  $bep >> $outfile
                
                printf "\t\t backend_address_pool_id = \"\${azurerm_lb_backend_address_pool.%s__%s__%s.id}\"\n" $beadprg $lbname $beadpid >> $outfile
                printf "\t\t probe_id = \"\${azurerm_lb_probe.%s__%s__%s.id}\"\n" $prg $lbname $pid >> $outfile
                
                printf "\t\t enable_floating_ip = \"%s\" \n"  $efip >> $outfile
                printf "\t\t idle_timeout_in_minutes = \"%s\" \n"  $itm >> $outfile
                printf "\t\t load_distribution = \"%s\" \n"  $ld >> $outfile


                printf "}\n" >> $outfile
        #

                cat $outfile
                statecomm=`printf "terraform state rm %s.%s__%s__%s" $tfp $rg $lbname $rname`
                echo $statecomm >> tf-staterm.sh
                eval $statecomm
                evalcomm=`printf "terraform import %s.%s__%s__%s %s" $tfp $rg $lbname $rname $id`

                echo $evalcomm >> tf-stateimp.sh
                eval $evalcomm

        #
        done
        fi
    done
fi

tfp="azurerm_lb_probe"
prefixa="lbpr"
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
        beap=`echo $azr | jq ".[(${i})].probes"`
            
        icount=`echo $beap | jq '. | length'`
        if [ "$icount" -gt "0" ]; then
            icount=`expr $icount - 1`
            for j in `seq 0 $icount`; do
                
                name=`echo $azr | jq ".[(${i})].probes[(${j})].name" | cut -d'/' -f11 | tr -d '"'`
                id=`echo $azr | jq ".[(${i})].probes[(${j})].id" | tr -d '"'`
                rg=`echo $azr | jq ".[(${i})].probes[(${j})].resourceGroup" | tr -d '"'`
                prefix=`printf "%s__%s" $prefixa $rg` 
                np=`echo $azr | jq ".[(${i})].probes[(${j})].numberOfProbes" | tr -d '"'`
                port=`echo $azr | jq ".[(${i})].probes[(${j})].port" | tr -d '"'`
                proto=`echo $azr | jq ".[(${i})].probes[(${j})].protocol" | tr -d '"'`
                int=`echo $azr | jq ".[(${i})].probes[(${j})].intervalInSeconds" | tr -d '"'`
              
                lbrg=`echo $azr | jq ".[(${i})].id" | cut -d'/' -f5 | tr -d '"'`
                lbname=`echo $azr | jq ".[(${i})].id" | cut -d'/' -f9 | tr -d '"'`
                
                printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $name > $prefix-$name.tf
                printf "\t\t name = \"%s\" \n"  $name >> $prefix-$name.tf
                printf "\t\t resource_group_name = \"%s\" \n"  $rg >> $prefix-$name.tf
                printf "\t\t loadbalancer_id = \"\${azurerm_lb.%s__%s.id}\"\n" $lbrg $lbname >> $prefix-$name.tf
                printf "\t\t number_of_probes = \"%s\" \n"  $np >> $prefix-$name.tf
                printf "\t\t protocol = \"%s\" \n"  $proto >> $prefix-$name.tf
                printf "\t\t port = \"%s\" \n"  $port >> $prefix-$name.tf
                printf "\t\t interval_in_seconds = \"%s\" \n"  $int >> $prefix-$name.tf

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

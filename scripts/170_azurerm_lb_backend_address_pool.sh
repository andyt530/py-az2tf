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
        beap=`echo $azr | jq ".[(${i})].backendAddressPools"`

       
        
        icount=`echo $beap | jq '. | length'`
        if [ "$icount" -gt "0" ]; then
            icount=`expr $icount - 1`
            for j in `seq 0 $icount`; do
                
                name=`echo $azr | jq ".[(${i})].backendAddressPools[(${j})].name" | cut -d'/' -f11 | tr -d '"'`
                rname=`echo $name | sed 's/\./-/g'`
                id=`echo $azr | jq ".[(${i})].backendAddressPools[(${j})].id" | tr -d '"'`
                rg=`echo $azr | jq ".[(${i})].backendAddressPools[(${j})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`
                
                lbrg=`echo $azr | jq ".[(${i})].id" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
                lbname=`echo $azr | jq ".[(${i})].id" | cut -d'/' -f9 | sed 's/\./-/g' | tr -d '"'`
                prefix=`printf "%s__%s__%s" $prefixa $rg $lbname`
                outfile=`printf "%s.%s__%s__%s.tf" $tfp $rg $lbname $rname`
                echo $az2tfmess > $outfile
                         
                printf "resource \"%s\" \"%s__%s__%s\" {\n" $tfp $rg $lbname $rname >> $outfile
                printf "\t\t name = \"%s\" \n"  $name >> $outfile
                printf "\t\t resource_group_name = \"%s\" \n"  $rgsource >> $outfile
                printf "\t\t loadbalancer_id = \"\${azurerm_lb.%s__%s.id}\"\n" $lbrg $lbname >> $outfile

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

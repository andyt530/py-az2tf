
azr=`az network lb list -g $rgsource -o json`
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
                rname=`echo $name | sed 's/\./-/g'`
                id=`echo $azr | jq ".[(${i})].probes[(${j})].id" | tr -d '"'`
                rg=`echo $azr | jq ".[(${i})].probes[(${j})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`
 
                np=`echo $azr | jq ".[(${i})].probes[(${j})].numberOfProbes" | tr -d '"'`
                port=`echo $azr | jq ".[(${i})].probes[(${j})].port" | tr -d '"'`
                proto=`echo $azr | jq ".[(${i})].probes[(${j})].protocol" | tr -d '"'`
                int=`echo $azr | jq ".[(${i})].probes[(${j})].intervalInSeconds" | tr -d '"'`
                rpath=`echo $azr | jq ".[(${i})].probes[(${j})].requestPath" | tr -d '"'`
                lbrg=`echo $azr | jq ".[(${i})].id" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
                lbname=`echo $azr | jq ".[(${i})].id" | cut -d'/' -f9 | sed 's/\./-/g' | tr -d '"'`
                
                prefix=`printf "%s__%s__%s" $prefixa $rg $lbname`
                outfile=`printf "%s.%s__%s__%s.tf" $tfp $rg $lbname $rname`
                echo $az2tfmess > $outfile

                printf "resource \"%s\" \"%s__%s__%s\" {\n" $tfp $rg $lbname $rname >> $outfile
                printf "\t\t name = \"%s\" \n"  $name >> $outfile
                printf "\t\t resource_group_name = \"%s\" \n"  $rgsource >> $outfile
                printf "\t\t loadbalancer_id = \"\${azurerm_lb.%s__%s.id}\"\n" $lbrg $lbname >> $outfile
                printf "\t\t protocol = \"%s\" \n"  $proto >> $outfile
                printf "\t\t port = \"%s\" \n"  $port >> $outfile
                if [ "$rpath" != "null" ]; then
                printf "\t\t request_path = \"%s\" \n"  $rpath >> $outfile
                fi
                if [ "$int" != "null" ]; then
                printf "\t\t interval_in_seconds = \"%s\" \n"  $int >> $outfile
                fi
                printf "\t\t number_of_probes = \"%s\" \n"  $np >> $outfile

                printf "}\n" >> $outfile
        #
        done
        fi 
    done
fi


azr=`az network traffic-manager profile list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        pname=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        azr2=`az network traffic-manager endpoint list -g $rgsource --profile-name $pname -o json`
        icount=`echo $azr2 | jq '. | length'`
        if [ "$icount" -gt "0" ]; then
            icount=`expr $icount - 1`
            for j in `seq 0 $icount`; do
                name=`echo $azr2 | jq ".[(${j})].name" | tr -d '"'`
                rname=`echo $name | sed 's/\./-/g'`
                rg=`echo $azr2 | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`
                
                id=`echo $azr2 | jq ".[(${j})].id" | tr -d '"'`
                type=`echo $azr2 | jq ".[(${j})].type" | cut -d'/' -f3 | tr -d '"'`
                pri=`echo $azr2 | jq ".[(${j})].priority" | tr -d '"'`
                wt=`echo $azr2 | jq ".[(${j})].weight" | tr -d '"'`
                tgt=`echo $azr2 | jq ".[(${j})].target" | tr -d '"'`
                eps=`echo $azr2 | jq ".[(${j})].endpointStatus" | tr -d '"'`
                tgtid=`echo $azr2 | jq ".[(${j})].targetResourceId"`
                tgtrrg=`echo $azr2 | jq ".[(${j})].targetResourceId"| cut -f5 -d"/" | sed 's/\./-/g' | tr -d '"'`
                tgtrid=`echo $azr2 | jq ".[(${j})].targetResourceId"| cut -f9 -d"/" | sed 's/\./-/g' | tr -d '"'`
                
                prefix=`printf "%s.%s" $prefixa $rg`
                outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
                echo $az2tfmess > $outfile
                
                printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
                printf "\t name = \"%s\"\n" $name >> $outfile
                printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
                printf "\t profile_name = \"%s\"\n" $pname >> $outfile
                printf "\t type = \"%s\"\n" $type >> $outfile
                printf "\t priority = \"%s\"\n" $pri >> $outfile
                printf "\t weight = \"%s\"\n" $wt >> $outfile
                printf "\t target = \"%s\"\n" $tgt >> $outfile
                printf "\t endpoint_status = \"%s\"\n" $eps >> $outfile
                printf "\t target_resource_id = \"\${azurerm_public_ip.%s__%s.id}\"\n" $tgtrrg $tgtrid >> $outfile
                #
                
                
                printf "}\n" >> $outfile
                #
                
                
            done
        fi
    done
fi

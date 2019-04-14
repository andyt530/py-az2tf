prefixa=`echo $0 | awk -F 'azurerm_' '{print $2}' | awk -F '.sh' '{print $1}' `
tfp=`printf "azurerm_%s" $prefixa`

echo $TF_VAR_rgtarget
if [ "$1" != "" ]; then
    rgsource=$1
fi
at=`az account get-access-token -o json`
bt=`echo $at | jq .accessToken | tr -d '"'`
sub=`echo $at | jq .subscription | tr -d '"'`


ris=`printf "curl -s  -X GET -H \"Authorization: Bearer %s\" -H \"Content-Type: application/json\" https://management.azure.com/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/expressRouteCircuits?api-version=2018-01-01" $bt $sub $rgsource`
# count how many of this provider type there are.
ret=`eval $ris`
azr2=`echo $ret | jq .value`
rg=$rgsource
count2=`echo $azr2 | jq '. | length'`
if [ "$count2" -gt "0" ]; then
    count2=`expr $count2 - 1`
    for j in `seq 0 $count2`; do
        
        name2=`echo $azr2 | jq ".[(${j})].name" | tr -d '"'`
        ris2=`printf "curl -s -X GET -H \"Authorization: Bearer %s\" -H \"Content-Type: application/json\" https://management.azure.com/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/expressRouteCircuits/%s?api-version=2018-01-01" $bt $sub $rgsource $name2`
        #echo $ris2
        ret2=`eval $ris2`
        azr=`echo $ret2 | jq .`
        #echo $ret2 | jq .
        count=`echo $azr | jq '. | length'`
        if [ "$count" -gt "0" ]; then
            name=`echo $azr | jq ".name" | tr -d '"'`
            rname=`echo $name | sed 's/\./-/g'`
            rg=`echo $rgsource| sed 's/\./-/g'`
            
            id=`echo $azr | jq ".id" | tr -d '"'`
            loc=`echo $azr | jq ".location"`
            rg=$rgsource
            tier=`echo $azr | jq ".sku.tier" | tr -d '"'`
            family=`echo $azr | jq ".sku.family" | tr -d '"'`
            aco=`echo $azr | jq ".properties.allowClassicOperations" | tr -d '"'`
            sp=`echo $azr | jq ".properties.serviceProviderProperties.serviceProviderName" | tr -d '"'`
            pl=`echo $azr | jq ".properties.serviceProviderProperties.peeringLocation" | tr -d '"'`
            bw=`echo $azr | jq ".properties.serviceProviderProperties.bandwidthInMbps" | tr -d '"'`
            
            
            prefix=`printf "%s__%s" $prefixa $rg`
            outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
            echo $az2tfmess > $outfile
            
            printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
            printf "\t name = \"%s\"\n" $name >> $outfile
            printf "\t location = %s\n" "$loc" >> $outfile
            printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
            
            printf "\t service_provider_name = \"%s\" \n" $sp >> $outfile
            printf "\t peering_location = \"%s\" \n" $pl >> $outfile
            printf "\t bandwidth_in_mbps = \"%s\" \n" $bw >> $outfile
            
            printf "\t sku { \n"  >> $outfile
            printf "\t\t tier = \"%s\"\n" $tier >> $outfile
            printf "\t\t family = \"%s\"\n" $family >> $outfile
            printf "\t }\n" >> $outfile
            printf "\t allow_classic_operations = \"%s\" \n" $aco >> $outfile
            
            # New Tags block v2
            tags=`echo $azr | jq ".tags"`
            tt=`echo $tags | jq .`
            tcount=`echo $tags | jq '. | length'`
            if [ "$tcount" -gt "0" ]; then
                printf "\t tags { \n" >> $outfile
                tt=`echo $tags | jq .`
                keys=`echo $tags | jq 'keys'`
                tcount=`expr $tcount - 1`
                for j in `seq 0 $tcount`; do
                    k1=`echo $keys | jq ".[(${j})]"`
                    #echo "key=$k1"
                    re="[[:space:]]+"
                    if [[ $k1 =~ $re ]]; then
                        #echo "found a space"
                        tval=`echo $tt | jq ."$k1"`
                        tkey=`echo $k1 | tr -d '"'`
                        printf "\t\t\"%s\" = %s \n" "$tkey" "$tval" >> $outfile
                    else
                        #echo "found no space"
                        tval=`echo $tt | jq .$k1`
                        tkey=`echo $k1 | tr -d '"'`
                        printf "\t\t%s = %s \n" $tkey "$tval" >> $outfile
                    fi
                done
                printf "\t}\n" >> $outfile
            fi
            
            
            printf "}\n" >> $outfile
            cat $outfile
            statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $rname`
            echo $statecomm >> tf-staterm.sh
            eval $statecomm
            evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $rname $id`
            echo $evalcomm >> tf-stateimp.sh
            eval $evalcomm
            
            #done
        fi
        
    done
fi

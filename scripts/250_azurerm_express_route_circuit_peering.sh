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
            
            
            peers=`echo $azr | jq ".properties.peerings"`
            echo $peers | jq .
            
            acount=`echo $peers | jq '. | length'`
            if [ "$acount" -gt "0" ]; then
                acount=`expr $acount - 1`
                for k in `seq 0 $acount`; do
                
                name=`echo $peers | jq ".[(${k})].name" | tr -d '"'`
                id=`echo $peers | jq ".[(${k})].id" | tr -d '"'`
                pt=`echo $peers | jq ".[(${k})].properties.peeringType" | tr -d '"'`
                pap=`echo $peers | jq ".[(${k})].properties.primaryPeerAddressPrefix" | tr -d '"'`
                sap=`echo $peers | jq ".[(${k})].properties.secondaryPeerAddressPrefix" | tr -d '"'`
                vid=`echo $peers | jq ".[(${k})].properties.vlanId" | tr -d '"'`
                pasn=`echo $peers | jq ".[(${k})].properties.peerASN" | tr -d '"'`
  
                rname=`echo $name | sed 's/\./-/g'`
                rg=`echo $rgsource | sed 's/\./-/g'`
                prefix=`printf "%s__%s" $prefixa $rg`
                outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
                echo $az2tfmess > $outfile
                
                printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile

                printf "\t peering_type = \"%s\"\n" $pt >> $outfile
                printf "\t express_route_circuit_name = \"%s\"\n" $name2 >> $outfile
                printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
                printf "\t primary_peer_address_prefix = \"%s\"\n" $pap >> $outfile
                printf "\t secondary_peer_address_prefix = \"%s\"\n" $sap >> $outfile
                printf "\t vlan_id = \"%s\"\n" $vid >> $outfile
                #printf "\t shared_key = \"%s\"\n" $sk >> $outfile
                printf "\t peer_asn = \"%s\"\n" $pasn >> $outfile
                

                if [ "$pt" = "MicrosoftPeering" ] || [ "$pt" = "AzurePrivatePeering" ];then
                    app=`echo $peers | jq ".[(${k})].properties.microsoftPeeringConfig.advertisedPublicPrefixes"`
                    printf "\t microsoft_peering_config {\n" >> $outfile
                    printf "\t\t advertised_public_prefixes = %s\n" "$app" >> $outfile
                    printf "\t } \n" >> $outfile
                fi
                
                printf "}\n" >> $outfile
                cat $outfile
                statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $rname`
                echo $statecomm >> tf-staterm.sh
                eval $statecomm
                evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $rname $id`
                echo $evalcomm >> tf-stateimp.sh
                eval $evalcomm
                
                done
                
            fi
            
            #done
        fi
        
    done
fi

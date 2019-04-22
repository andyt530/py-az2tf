
azr=`az network local-gateway list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`
    
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`
        gwaddr=`echo $azr | jq ".[(${i})].gatewayIpAddress" | tr -d '"'`
        addrpre=`echo $azr | jq ".[(${i})].localNetworkAddressSpace.addressPrefixes"`
        bgps=`echo $azr | jq ".[(${i})].bgpSettings" | tr -d '"'`
        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
        printf "\t location = \"%s\"\n" $loc >> $outfile
        printf "\t gateway_address = \"%s\"\n" $gwaddr >> $outfile
        printf "\t address_space = %s\n" "$addrpre" >> $outfile
    
        if [ "$bgps" != "null" ]; then
            asn=`echo $azr | jq ".[(${i})].bgpSettings.asn" | tr -d '"'`
            peera=`echo $azr | jq ".[(${i})].bgpSettings.bgpPeeringAddress" | tr -d '"'`
            peerw=`echo $azr | jq ".[(${i})].bgpSettings.peerWeight" | tr -d '"'`

            printf "\t bgp_settings {\n"  >> $outfile
            printf "\t\t asn = \"%s\"\n" $asn >> $outfile
            printf "\t\t bgp_peering_address = \"%s\"\n" $peera >> $outfile
            printf "\t\t peer_weight = \"%s\"\n" $peerw >> $outfile
            printf "\t }\n"  >> $outfile
        fi
        
        printf "}\n" >> $outfile


    done
fi

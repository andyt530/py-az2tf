
azr=`az network vpn-connection list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`

        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`
        type=`echo $azr | jq ".[(${i})].connectionType" | tr -d '"'`
        vngrg=`echo $azr | jq ".[(${i})].virtualNetworkGateway1.id" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
        vngnam=`echo $azr | jq ".[(${i})].virtualNetworkGateway1.id" | cut -d'/' -f9 | sed 's/\./-/g' | tr -d '"'`
        
        peerrg=`echo $azr | jq ".[(${i})].peer.id" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
        peernam=`echo $azr | jq ".[(${i})].peer.id" | cut -d'/' -f9 | sed 's/\./-/g' | tr -d '"'`
        
        if [ "$type" = "IPsec" ]; then
            echo "is sec"
            peerrg=`echo $azr | jq ".[(${i})].localNetworkGateway2.id" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
            peernam=`echo $azr | jq ".[(${i})].localNetworkGateway2.id" | cut -d'/' -f9 | sed 's/\./-/g' | tr -d '"'`
            echo $peerrg
            echo $peernam
        fi
        
        
        authkey=`echo $azr | jq ".[(${i})].authorizationKey" | tr -d '"'`
        enbgp=`echo $azr | jq ".[(${i})].enableBgp" | tr -d '"'`
        rw=`echo $azr | jq ".[(${i})].routingWeight" | tr -d '"'`
        echo "RW = $rw"
        sk=`echo $azr | jq ".[(${i})].shared_key" | tr -d '"'`
        pbs=`echo $azr | jq ".[(${i})].usePolicyBasedTrafficSelectors" | tr -d '"'`
        
        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
        printf "\t location = \"%s\"\n" $loc >> $outfile
        printf "\t type = \"%s\"\n" $type >> $outfile
        printf "\t\t virtual_network_gateway_id = \"\${azurerm_virtual_network_gateway.%s__%s.id}\"\n" $vngrg $vngnam >> $outfile
        if [ "$authkey" -ne "null" ]; then
            printf "\t authorization_key = \"%s\"\n" $authkey >> $outfile
        fi
        
        printf "\t enable_bgp = \"%s\"\n" $enbgp >> $outfile
        if [ "$rw" != "null" ] && [ "$rw" != "0" ]; then
            printf "\t routing_weight = \"%s\"\n" $rw >> $outfile
        fi
        if [ "$sk" != "null" ]; then
            printf "\t shared_key = \"%s\"\n" $sk >> $outfile
        fi
        printf "\t use_policy_based_traffic_selectors = \"%s\"\n" $pbs >> $outfile
        echo $type
        if [ "$type" == "ExpressRoute" ]; then
            peerid=`echo $azr | jq ".[(${i})].peer.id" | tr -d '"'`
            printf "\t\t express_route_circuit_id = \"%s\"\n" $peerid >> $outfile
            #printf "\t\t express_route_circuit_id = \"\${azurerm_virtual_network_gateway.%s__%s.id}\"\n" $peerrg $peernam >> $outfile
            peerid=`echo $azr | jq ".[(${i})].peer.id" | tr -d '"'`
            
        fi
        if [ "$type" == "Vnet2Vnet" ]; then
            printf "\t\t peer_virtual_network_gateway_id = \"\${azurerm_virtual_network_gateway.%s__%s.id}\"\n" $peerrg $peernam >> $outfile
        fi
        if [ "$type" == "IPsec" ]; then
            printf "\t\t local_network_gateway_id = \"\${azurerm_local_network_gateway.%s__%s.id}\"\n" $peerrg $peernam >> $outfile
        fi
        
        
        ipsec=`echo $azr | jq ".[(${i})].ipsecPolicies"`
        jcount=`echo $ipsec | jq '. | length'`
        if [ "$jcount" -gt "0" ]; then
            jcount=`expr $jcount - 1`
            for j in `seq 0 $jcount`; do
                printf "\t ipsec_policy {\n" >> $outfile
                
                dhg=`echo $ipsec | jq ".[(${j})].dhGroup"`
                printf "\t dh_group {\n" $dhg >> $outfile
                
                printf "\t}\n" >> $outfile
            done
        fi
            
        
        printf "}\n" >> $outfile
        #

        
    done
fi

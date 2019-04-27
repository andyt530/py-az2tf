
azr=az network vpn-connection list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        name=azr[i]["name"]
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']

        id=azr[i]["id"]
        loc=azr[i]["location"]
        type=azr[i]["connectionType"]
        vngrg=azr[i]["virtualNetworkGateway1.id" | cut -d'/' -f5 | sed 's/\./-/g']
        vngnam=azr[i]["virtualNetworkGateway1.id" | cut -d'/' -f9 | sed 's/\./-/g']
        
        peerrg=azr[i]["peer.id" | cut -d'/' -f5 | sed 's/\./-/g']
        peernam=azr[i]["peer.id" | cut -d'/' -f9 | sed 's/\./-/g']
        
        if type" = "IPsec" :
            print "is sec"
            peerrg=azr[i]["localNetworkGateway2.id" | cut -d'/' -f5 | sed 's/\./-/g']
            peernam=azr[i]["localNetworkGateway2.id" | cut -d'/' -f9 | sed 's/\./-/g']
            print peerrg
            print peernam
        fi
        
        
        authkey=azr[i]["authorizationKey"]
        enbgp=azr[i]["enableBgp"]
        rw=azr[i]["routingWeight"]
        print "RW = rw"
        sk=azr[i]["shared_key"]
        pbs=azr[i]["usePolicyBasedTrafficSelectors"]
        
        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outfile
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        fr.write('\t type = "' +  type + '"\n')
        fr.write('\t\t virtual_network_gateway_id = "'\{'azurerm_virtual_network_gateway. + '__' + .id}'"' vngrg vngnam + '"\n')
        if authkey" -ne "null" :
            fr.write('\t authorization_key = "' +  authkey + '"\n')
        fi
        
        fr.write('\t enable_bgp = "' +  enbgp + '"\n')
        if rw" != "null" ]["&& [ "rw" != "0" :
            fr.write('\t routing_weight = "' +  rw + '"\n')
        fi
        if sk" != "null" :
            fr.write('\t shared_key = "' +  sk + '"\n')
        fi
        fr.write('\t use_policy_based_traffic_selectors = "' +  pbs + '"\n')
        print type
        if type" == "ExpressRoute" :
            peerid=azr[i]["peer.id"]
            fr.write('\t\t express_route_circuit_id = "' +  peerid + '"\n')
            #fr.write('\t\t express_route_circuit_id = "'\{'azurerm_virtual_network_gateway. + '__' + .id}'"' peerrg peernam + '"\n')
            peerid=azr[i]["peer.id"]
            
        fi
        if type" == "Vnet2Vnet" :
            fr.write('\t\t peer_virtual_network_gateway_id = "'\{'azurerm_virtual_network_gateway. + '__' + .id}'"' peerrg peernam + '"\n')
        fi
        if type" == "IPsec" :
            fr.write('\t\t local_network_gateway_id = "'\{'azurerm_local_network_gateway. + '__' + .id}'"' peerrg peernam + '"\n')
        fi
        
        
        ipsec=azr[i]["ipsecPolicies"
        jcount=print ipsec | jq '. | length'
        if jcount" -gt "0" :
            jcount=expr jcount - 1
            for j in range( 0 jcount):
                fr.write('\t ipsec_policy {' + '"\n')
                
                dhg=print ipsec | jq ".[j]["dhGroup"
                fr.write('\t dh_group {' dhg + '"\n')
                
                fr.write('\t}' + '"\n')
            
        fi
            
        
        fr.write('}' + '"\n')
        #

        
    
fi

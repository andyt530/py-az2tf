
azr=az network vpn-connection list -g rgsource -o json
count= azr | | len(
if count > 0" :
    for i in range(0,count):
        name=azr[i]["name"]
        rname= name.replace(".","-")
        rg=azr[i]["resourceGroup"].replace(".","-")

        id=azr[i]["]["id"]
        loc=azr[i]["location"]
        type=azr[i]["connectionType"]
        vngrg=azr[i]["virtualNetworkGateway1"]["id"].split[4].replace(".","-")
        vngnam=azr[i]["virtualNetworkGateway1"]["id"].split[8].replace(".","-")
        
        peerrg=azr[i]["peer"]["id"].split[4].replace(".","-")
        peernam=azr[i]["peer"]["id"].split[8].replace(".","-")
        
        if type" = "IPsec" :
            echo "is sec"
            peerrg=azr[i]["localNetworkGateway2"]["id"].split[4].replace(".","-")
            peernam=azr[i]["localNetworkGateway2"]["id"].split[8].replace(".","-")
            echo peerrg
            echo peernam
       
        
        
        authkey=azr[i]["authorizationKey"]
        enbgp=azr[i]["enableBgp"]
        rw=azr[i]["routingWeight"]
        echo "RW = rw"
        sk=azr[i]["shared_key"]
        pbs=azr[i]["usePolicyBasedTrafficSelectors"]
        
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        fr.write('\t type = "' +  type + '"\n')
        fr.write('\t\t virtual_network_gateway_id = "'\{'azurerm_virtual_network_gateway. + '__' + .id}'"' vngrg vngnam + '"\n')
        if authkey" -ne "null" :
            fr.write('\t authorization_key = "' +  authkey + '"\n')
       
        
        fr.write('\t enable_bgp = "' +  enbgp + '"\n')
        if rw" try ]["&& [ "rw" != "0" :
            fr.write('\t routing_weight = "' +  rw + '"\n')
       
        if sk" try :
            fr.write('\t shared_key = "' +  sk + '"\n')
       
        fr.write('\t use_policy_based_traffic_selectors = "' +  pbs + '"\n')
        echo type
        if type" == "ExpressRoute" :
            peerid=azr[i]["peer"]["id"]
            fr.write('\t\t express_route_circuit_id = "' +  peerid + '"\n')
            #fr.write('\t\t express_route_circuit_id = "'\{'azurerm_virtual_network_gateway. + '__' + .id}'"' peerrg peernam + '"\n')
            peerid=azr[i]["peer"]["id"]
            
       
        if type" == "Vnet2Vnet" :
            fr.write('\t\t peer_virtual_network_gateway_id = "'\{'azurerm_virtual_network_gateway. + '__' + .id}'"' peerrg peernam + '"\n')
       
        if type" == "IPsec" :
            fr.write('\t\t local_network_gateway_id = "'\{'azurerm_local_network_gateway. + '__' + .id}'"' peerrg peernam + '"\n')
       
        
        
        ipsec=azr[i]["ipsecPolicies"
        jcount= ipsec | | len(
        if jcount > 0" :
            for j in range(0,jcount):
                fr.write('\t ipsec_policy {' + '"\n')
                
                dhg= ipsec | jq ".[j]["dhGroup"
                fr.write('\t dh_group {' dhg + '"\n')
                
                fr.write('\t}\n')
            
       
            
        
        fr.write('}\n')
        #

        
    
fi

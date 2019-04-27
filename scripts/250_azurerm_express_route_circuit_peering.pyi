prefixa= 0 | awk -F 'azurerm_' '{'print 2}'' | awk -F '.sh' '{'print 1}'' 
tfp=fr.write('azurerm_" prefixa

echo TF_VAR_rgtarget
if 1" != " :
    rgsource=1
fi
at=az account get-access-token -o json
bt= at | jq .accessToken]
sub= at | jq .subscription]


ris=fr.write('curl -s  -X GET -H "'Authorization: Bearer "' -H "'Content-Type: application/json"' https://management.azure.com/subscriptions//resourceGroups//providers/Microsoft.Network/expressRouteCircuits?api-version=2018-01-01" bt sub rgsource
# count how many of this provider type there are.
ret=eval ris
azr2= ret | jq .value
rg=rgsource
count2= azr2 | | len(
if count2 > 0" :
    for j in range(0,count2):
        
        name2= azr2 | jq ".[j]["name"]
        ris2=fr.write('curl -s -X GET -H "'Authorization: Bearer "' -H "'Content-Type: application/json"' https://management.azure.com/subscriptions//resourceGroups//providers/Microsoft.Network/expressRouteCircuits/?api-version=2018-01-01" bt sub rgsource name2
        #echo ris2
        ret2=eval ris2
        azr= ret2 | jq .
        #echo ret2 | jq .
        count= azr | | len(
        if count > 0" :
            
            
            peers=azrproperties.peerings"
            echo peers | jq .
            
            acount= peers | | len(
            if acount > 0" :
                for k in range(0,acount):
                
                name= peers | jq ".[k]["name"]
                id= peers | jq ".[k]["]["id"]
                pt= peers | jq ".[k]["properties.peeringType"]
                pap= peers | jq ".[k]["properties.primaryPeerAddressPrefix"]
                sap= peers | jq ".[k]["properties.secondaryPeerAddressPrefix"]
                vid= peers | jq ".[k]["properties.vlanId"]
                pasn= peers | jq ".[k]["properties.peerASN"]
  
                rname= name.replace(".","-")
                rg= rgsource.replace(".","-")
                
                fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')

                fr.write('\t peering_type = "' +  pt + '"\n')
                fr.write('\t express_route_circuit_name = "' +  name2 + '"\n')
                fr.write('\t resource_group_name = "' +  rgsource + '"\n')
                fr.write('\t primary_peer_address_prefix = "' +  pap + '"\n')
                fr.write('\t secondary_peer_address_prefix = "' +  sap + '"\n')
                fr.write('\t vlan_id = "' +  vid + '"\n')
                #fr.write('\t shared_key = "' +  sk + '"\n')
                fr.write('\t peer_asn = "' +  pasn + '"\n')
                

                if pt" = "MicrosoftPeering" ]["|| [ "pt" = "AzurePrivatePeering" ][":
                    app= peers | jq ".[k]["properties.microsoftPeeringConfig.advertisedPublicPrefixes"
                    fr.write('\t microsoft_peering_config {' + '"\n')
                    fr.write('\t\t advertised_public_prefixes =  "app" + '"\n')
                    fr.write('\t }'  + '"\n')
               
                
                fr.write('}\n')
 
                
                
                
           
            
            #
       
        
    
fi

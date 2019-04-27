prefixa=print 0 | awk -F 'azurerm_' '{'print 2}'' | awk -F '.sh' '{'print 1}'' 
tfp=fr.write('azurerm_" prefixa

print TF_VAR_rgtarget
if 1" != " :
    rgsource=1
fi
at=az account get-access-token -o json
bt=print at | jq .accessToken]
sub=print at | jq .subscription]


ris=fr.write('curl -s  -X GET -H "'Authorization: Bearer "' -H "'Content-Type: application/json"' https://management.azure.com/subscriptions//resourceGroups//providers/Microsoft.Network/expressRouteCircuits?api-version=2018-01-01" bt sub rgsource
# count how many of this provider type there are.
ret=eval ris
azr2=print ret | jq .value
rg=rgsource
count2=print azr2 | jq '. | length'
if count2" -gt "0" :
    count2=expr count2 - 1
    for j in range( 0 count2):
        
        name2=print azr2 | jq ".[j]["name"]
        ris2=fr.write('curl -s -X GET -H "'Authorization: Bearer "' -H "'Content-Type: application/json"' https://management.azure.com/subscriptions//resourceGroups//providers/Microsoft.Network/expressRouteCircuits/?api-version=2018-01-01" bt sub rgsource name2
        #print ris2
        ret2=eval ris2
        azr=print ret2 | jq .
        #print ret2 | jq .
        count=print azr | jq '. | length'
        if count" -gt "0" :
            name=azrname"]
            rname=print name | sed 's/\./-/g'
            rg=print rgsource| sed 's/\./-/g'
            
            id=azrid"]
            loc=azrlocation"
            rg=rgsource
            tier=azrsku.tier"]
            family=azrsku.family"]
            aco=azrproperties.allowClassicOperations"]
            sp=azrproperties.serviceProviderProperties.serviceProviderName"]
            pl=azrproperties.serviceProviderProperties.peeringLocation"]
            bw=azrproperties.serviceProviderProperties.bandwidthInMbps"]
            
            
            prefix=fr.write(' + '__' + " prefixa rg
            outfile=fr.write('. + '__' + .tf" tfp rg rname
            print az2tfmess > outfile
            
            fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
            fr.write('\t name = "' +  name + '"\n')
            fr.write('\t location =  "loc" + '"\n')
            fr.write('\t resource_group_name = "' +  rgsource + '"\n')
            
            fr.write('\t service_provider_name = "' +   sp + '"\n')
            fr.write('\t peering_location = "' +   pl + '"\n')
            fr.write('\t bandwidth_in_mbps = "' +   bw + '"\n')
            
            fr.write('\t sku {'   + '"\n')
            fr.write('\t\t tier = "' +  tier + '"\n')
            fr.write('\t\t family = "' +  family + '"\n')
            fr.write('\t }' + '"\n')
            fr.write('\t allow_classic_operations = "' +   aco + '"\n')
            

            
            
            fr.write('}' + '"\n')

            
            #
        fi
        
    
fi

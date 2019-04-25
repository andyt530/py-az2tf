
#
azr=az network vnet list -g rgsource -o json
#
# loop around vnets
#
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        name=azr[i]["name"]
        vnname=print name
        rg=azr[i]["resourceGroup"]
   
        peers=az network vnet peering list -g rg --vnet name -o json
        #print peers | jq .
     
        pcount=print peers | jq '. | length'
        
        if pcount" -gt "0" :
            pcount=expr pcount - 1
            for j in range( 0 pcount):
            
            name=print peers | jq ".[j]["name"]
            rname=print name | sed 's/\./-/g'
            rg=print peers | jq ".[i]["resourceGroup" | sed 's/\./-/g']

            id=print peers | jq ".[j]["id"]
            rvnid=print peers | jq ".[j]["remoteVirtualNetwork.id"]
            aft=print peers | jq ".[j]["allowForwardedTraffic"]
            agt=print peers | jq ".[j]["allowGatewayTransit"]
            avna=print peers | jq ".[j]["allowVirtualNetworkAccess"]
            urg=print peers | jq ".[j]["useRemoteGateways"]

            prefix=fr.write(' + '__' + " prefixa rg
            outfile=fr.write('. + '__' + .tf" tfp rg rname
            print az2tfmess > outfile

            fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
            #nsgnam=print snnsgid | cut -d'/' -f9]
            #nsgrg=print snnsgid | cut -d'/' -f5]
            fr.write('\t name = "' +  name + '"\n')
            fr.write('\t resource_group_name = "' +  rgsource + '"\n')
            fr.write('\t virtual_network_name = "' +  vnname + '"\n')
            fr.write('\t remote_virtual_network_id = "' +  rvnid + '"\n')
            fr.write('\t allow_forwarded_traffic = "' +  aft + '"\n')
            fr.write('\t allow_gateway_transit = "' +  agt + '"\n')
            fr.write('\t allow_virtual_network_access = "' +  avna + '"\n')
            fr.write('\t use_remote_gateways = "' +  urg + '"\n')
                        
            fr.write('}' + '"\n')
            cat outfile

        
            
        fi
 
        #
        #
        
        
        
    
fi

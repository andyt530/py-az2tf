
azr=az network local-gateway list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        name=azr[i]["name"]
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']
    
        id=azr[i]["id"]
        loc=azr[i]["location"]
        gwaddr=azr[i]["gatewayIpAddress"]
        addrpre=azr[i]["localNetworkAddressSpace.addressPrefixes"
        bgps=azr[i]["bgpSettings"]
        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outfile
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        fr.write('\t gateway_address = "' +  gwaddr + '"\n')
        fr.write('\t address_space =  "addrpre" + '"\n')
    
        if bgps" != "null" :
            asn=azr[i]["bgpSettings.asn"]
            peera=azr[i]["bgpSettings.bgpPeeringAddress"]
            peerw=azr[i]["bgpSettings.peerWeight"]

            fr.write('\t bgp_settings {'  + '"\n')
            fr.write('\t\t asn = "' +  asn + '"\n')
            fr.write('\t\t bgp_peering_address = "' +  peera + '"\n')
            fr.write('\t\t peer_weight = "' +  peerw + '"\n')
            fr.write('\t }'  + '"\n')
        fi
        
        fr.write('}' + '"\n')


    
fi

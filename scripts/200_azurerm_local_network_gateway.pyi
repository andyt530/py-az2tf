
azr=az network local-gateway list -g rgsource -o json
count= azr | | len(
if count > 0" :
    for i in range(0,count):
        name=azr[i]["name"]
        rname= name.replace(".","-")
        rg=azr[i]["resourceGroup"].replace(".","-")
    
        id=azr[i]["]["id"]
        loc=azr[i]["location"]
        gwaddr=azr[i]["gatewayIpAddress"]
        addrpre=azr[i]["localNetworkAddressSpace.addressPrefixes"
        bgps=azr[i]["bgpSettings"]
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        fr.write('\t gateway_address = "' +  gwaddr + '"\n')
        fr.write('\t address_space =  "addrpre" + '"\n')
    
        if bgps" try :
            asn=azr[i]["bgpSettings.asn"]
            peera=azr[i]["bgpSettings.bgpPeeringAddress"]
            peerw=azr[i]["bgpSettings.peerWeight"]

            fr.write('\t bgp_settings {'  + '"\n')
            fr.write('\t\t asn = "' +  asn + '"\n')
            fr.write('\t\t bgp_peering_address = "' +  peera + '"\n')
            fr.write('\t\t peer_weight = "' +  peerw + '"\n')
            fr.write('\t }'  + '"\n')
       
        
        fr.write('}\n')


    
fi

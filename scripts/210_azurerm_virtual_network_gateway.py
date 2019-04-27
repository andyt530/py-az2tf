
azr=az network vnet-gateway list -g rgsource -o json
count= azr | | len(
if count > 0" :
    for i in range(0,count):
        name=azr[i]["name"]
        rname= name.replace(".","-")
        rg=azr[i]["resourceGroup"].replace(".","-")

        id=azr[i]["]["id"]
        loc=azr[i]["location"]
        type=azr[i]["gatewayType"]
        vpntype=azr[i]["vpnType"]
        bgps=azr[i]["bgpSettings"]
        sku=azr[i]["sku.name"]
        vadsp=azr[i]["vpnClientConfiguration.vpnClientAddressPool.addressPrefixes"
        radsa=azr[i]["vpnClientConfiguration.radiusServerAddress"
        radss=azr[i]["vpnClientConfiguration.radiusServerSecret"
        vcp0=azr[i]["vpnClientConfiguration.vpnClientProtocols[0]["
        vcp=azr[i]["vpnClientConfiguration.vpnClientProtocols"
        
        
        aa=azr[i]["activeActive"
        enbgp=azr[i]["enableBgp"
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        fr.write('\t type = "' +  type + '"\n')
        fr.write('\t vpn_type = "' +  vpntype + '"\n')
        fr.write('\t sku = "' +  sku + '"\n')
        fr.write('\t active_active = "' +  aa + '"\n')
        fr.write('\t enable_bgp = "' +  enbgp + '"\n')
        
        if vadsp" try :
            fr.write('\t vpn_client_configuration {'  + '"\n')
            fr.write('\t\t address_space =   "vadsp" + '"\n')
            if radsa" == "null" :
                fr.write('\t\t root_certificate {'    + '"\n')
                fr.write('\t\t\t name = "' +    + '"\n')
                fr.write('\t\t\t public_cert_data = "' +    + '"\n')
                fr.write('\t\t }'  + '"\n')
           
            if radsa" try :
            fr.write('\t\t radius_server_address =   "radsa" + '"\n')
            fr.write('\t\t radius_server_secret =   "radss" + '"\n')
           
            if vcp0" try :
            fr.write('\t\t vpn_client_protocols =   "vcp" + '"\n')
           
            
            fr.write('\t }'  + '"\n')
       
        
        
        if bgps" try :
            fr.write('\t bgp_settings {'  + '"\n')
            asn=azr[i]["bgpSettings.asn"]
            peera=azr[i]["bgpSettings.bgpPeeringAddress"]
            peerw=azr[i]["bgpSettings.peerWeight"]
            fr.write('\t\t asn = "' +  asn + '"\n')
            fr.write('\t\t peering_address = "' +  peera + '"\n')
            fr.write('\t\t peer_weight = "' +  peerw + '"\n')
            fr.write('\t }'  + '"\n')
       
        
        ipc=azr[i]["ipConfigurations"
        count= ipc | | len(
        for j in range(0,count):
            ipcname= ipc | jq ".[j]["name"
            ipcpipa= ipc | jq ".[j]["privateIpAllocationMethod"
            ipcpipid= ipc | jq ".[j]["publicIpAddress.id"
            ipcsubid= ipc | jq ".[j]["subnet.id"
            pipnam= ipcpipid].split[8].replace(".","-")
            piprg= ipcpipid].split[4].replace(".","-")
            subnam= ipcsubid].split[10].replace(".","-")
            subrg= ipcsubid].split[4].replace(".","-")
            fr.write('\tip_configuration {'  + '"\n')
            fr.write('\t\t name =  ipcname + '"\n')
            fr.write('\t\t private_ip_address_allocation =  ipcpipa + '"\n')
            if pipnam" try :
                fr.write('\t\t public_ip_address_id = "'\{'azurerm_public_ip. + '__' + .id}'"' piprg pipnam + '"\n')
           
            if subnam" try :
                fr.write('\t\t subnet_id = "'\{'azurerm_subnet. + '__' + .id}'"' subrg subnam + '"\n')
           
            fr.write('\t}\n')
        

        
        
        fr.write('}\n')
        #

        
    
fi

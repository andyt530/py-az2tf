# azurerm_virtual_network_gateway
def azurerm_virtual_network_gateway(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_virtual_network_gateway"
    tcode="210-"
    azr=""
    if crf in tfp:
    # REST or cli
        print "REST Managed Disk"
        url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Compute/disks"
        params = {'api-version': '2017-03-30'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]
        if cde:
            print(json.dumps(azr, indent=4, separators=(',', ': ')))

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print tfp,
        count=len(azr)
        print count
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-")

            if crg is not None:
                if rg.lower() != crg.lower():
                    continue  # back to for
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rg + '"\n')

    ###############
    # specific code start
    ###############



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
            ipcpipa= ipc | jq ".[j]["privateAllocationMethod"
            ipcpipid= ipc | jq ".[j]["publicAddress.id"
            ipcsubid= ipc | jq ".[j]["subnet.id"
            pipnam= ipcpipid].split("/")[8].replace(".","-")
            piprg= ipcpipid].split("/")[4].replace(".","-")
            subnam= ipcsubid].split("/")[10].replace(".","-")
            subrg= ipcsubid].split("/")[4].replace(".","-")
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

    ###############
    # specific code end
    ###############

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write('\t "' + key + '"="' + tval + '"\n')
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print f.read()

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub

def azurerm_virtual_network_peering(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #############
    #  080 vnet peering
    tfp="azurerm_virtual_network_peering"
    if crf in tfp: 
    # peering in vnet

        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/virtualNetworks"
        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf="080-"+tfp+"-staterm.sh"
        tfimf="080-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):
            peers=azr[i]["properties"]["virtualNetworkPeerings"]
            vnetname=azr[i]["name"]
            jcount=len(peers)
            
            for j in range(0, jcount):
                name=peers[j]["name"]
                #loc=peers[j]["location"] peers don't have a location
                id=peers[j]["id"]
                rg=id.split("/")[4].replace(".","-").lower()
                if rg[0].isdigit(): rg="rg_"+rg
                rgs=id.split("/")[4]

                if crg is not None:
                    if rgs.lower() != crg.lower():
                        continue  # back to for
                if cde:
                    print(json.dumps(peers[j], indent=4, separators=(',', ': ')))
                    
                rname=name.replace(".","-")
                prefix=tfp+"."+rg+'__'+rname
                    
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write("")
                fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                fr.write('\t resource_group_name = "'+ rgs + '"\n')
                fr.write('\t virtual_network_name = "' + vnetname + '"\n')


                rvnid=peers[j]["properties"]["remoteVirtualNetwork"]["id"]
                aft=str(peers[j]["properties"]["allowForwardedTraffic"]).lower()
                agt=str(peers[j]["properties"]["allowGatewayTransit"]).lower()
                avna=str(peers[j]["properties"]["allowVirtualNetworkAccess"]).lower()
                urg=str(peers[j]["properties"]["useRemoteGateways"]).lower()

                fr.write('\t remote_virtual_network_id = "' +  rvnid + '"\n')
                fr.write('\t allow_forwarded_traffic = ' +  aft + '\n')
                fr.write('\t allow_gateway_transit = ' +  agt + '\n')
                fr.write('\t allow_virtual_network_access = ' +  avna + '\n')
                fr.write('\t use_remote_gateways = ' +  urg + '\n')
                            
                fr.write('}\n') 
                fr.close()   # close .tf file

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(j) + ' of ' + str(jcount-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm)  
            # end for j loop
        # end for i loop

        tfrm.close()
        tfim.close()
    #end peering
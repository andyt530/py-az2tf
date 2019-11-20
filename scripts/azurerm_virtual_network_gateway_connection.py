# azurerm_virtual_network_gateway_connection
def azurerm_virtual_network_gateway_connection(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_virtual_network_gateway_connection"
    tcode="220-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/connections"
        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

    ##  azr=az network vpn-connection list -g rgsource -o json
        
            ctype=azr[i]["properties"]["connectionType"]
            vngrg=azr[i]["properties"]["virtualNetworkGateway1"]["id"].split("/")[4].replace(".","-").lower()
            vngnam=azr[i]["properties"]["virtualNetworkGateway1"]["id"].split("/")[8].replace(".","-")
            

            
            if ctype == "IPsec" :
                
                peerrg=azr[i]["properties"]["localNetworkGateway2"]["id"].split("/")[4].replace(".","-").lower()
                peernam=azr[i]["properties"]["localNetworkGateway2"]["id"].split("/")[8].replace(".","-")
    
            

            enbgp=azr[i]["properties"]["enableBgp"]
            rw=azr[i]["properties"]["routingWeight"]

            pbs=azr[i]["properties"]["usePolicyBasedTrafficSelectors"]
            
            fr.write('\t type = "' +  ctype + '"\n')
            if vngrg[0].isdigit(): vngrg="rg_"+vngrg
            fr.write('\t\t virtual_network_gateway_id = "${azurerm_virtual_network_gateway.' + vngrg + '__' + vngnam + '.id}"\n')
            try:
                authkey=azr[i]["properties"]["authorizationKey"]
                fr.write('\t authorization_key = "' +  authkey + '"\n')
            except KeyError:
                pass
        
            
            fr.write('\t enable_bgp = ' +  str(enbgp).lower() + '\n')
            try:
                rw=azr[i]["properties"]["routingWeight"] 
                if rw != 0 :
                    fr.write('\t routing_weight = "' + str(rw) + '"\n')
            except KeyError:
                pass

            try :
                sk=azr[i]["properties"]["shared_key"]
                fr.write('\t shared_key = "' +  sk + '"\n')
            except KeyError:
                pass   


            fr.write('\t use_policy_based_traffic_selectors = ' + str(pbs).lower() + '\n')
            
            if ctype == "ExpressRoute" :
                peerid=azr[i]["properties"]["peer"]["id"]
                fr.write('\t\t express_route_circuit_id = "' +  peerid + '"\n')
                #fr.write('\t\t express_route_circuit_id = "${azurerm_virtual_network_gateway. + '__' + .id}'"' peerrg peernam + '"\n')
                peerid=azr[i]["properties"]["peer"]["id"]
                peerrg=peerid.split("/")[4].replace(".","-").lower()
                if peerrg[0].isdigit(): peerrg="rg_"+peerrg
                peernam=peerid.split("/")[8].replace(".","-")
        
            if ctype == "Vnet2Vnet" :
                fr.write('\t peer_virtual_network_gateway_id = "${azurerm_virtual_network_gateway.' + peerrg +'__' + peernam + '.id}"\n')
        
            if ctype == "IPsec" :
                fr.write('\t local_network_gateway_id = "${azurerm_local_network_gateway.' + peerrg + '__' + peernam + '.id}" \n')
        
            
            
            ipsec=azr[i]["properties"]["ipsecPolicies"]
            jcount= len(ipsec)
            if jcount > 0 :
                for j in range(0,jcount):
                    fr.write('\t ipsec_policy {' + '\n')
                    dhg= ipsec[j]["dhGroup"]
                    ikee= ipsec[j]["ikeEncryption"]
                    ikei= ipsec[j]["ikeIntegrity"]
                    ipsece= ipsec[j]["ipsecEncryption"]
                    ipseci= ipsec[j]["ipsecIntegrity"]
                    pfsg= ipsec[j]["pfsGroup"]
                    sadata= ipsec[j]["saDataSizeKilobytes"]
                    salife= ipsec[j]["saLifeTimeSeconds"]
                    fr.write('\t dh_group = "' + dhg + '"\n')
                    fr.write('\t ike_encryption = "' + ikee + '"\n')
                    fr.write('\t ike_integrity = "' + ikei + '"\n')
                    fr.write('\t ipsec_encryption = "' + ipsece + '"\n')
                    fr.write('\t ipsec_integrity = "' + ipseci + '"\n')
                    fr.write('\t pfs_group = "' + pfsg + '"\n')
                    fr.write('\t sa_datasize = "' + str(sadata) + '"\n')
                    fr.write('\t sa_lifetime = "' + str(salife) + '"\n')
                    fr.write('\t}\n')
                
    
    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub

# azurerm_virtual_network_gateway_connection
def azurerm_virtual_network_gateway_connection(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_virtual_network_gateway_connection"
    tcode="220-"
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

    ##  azr=az network vpn-connection list -g rgsource -o json
        
            ctype=azr[i]["connectionType"]
            vngrg=azr[i]["virtualNetworkGateway1"]["id"].split("/")[4].replace(".","-")
            vngnam=azr[i]["virtualNetworkGateway1"]["id"].split("/")[8].replace(".","-")
            
            peerrg=azr[i]["peer"]["id"].split("/")[4].replace(".","-")
            peernam=azr[i]["peer"]["id"].split("/")[8].replace(".","-")
            
            if ctype == "IPsec" :
                print "is sec"
                peerrg=azr[i]["localNetworkGateway2"]["id"].split("/")[4].replace(".","-")
                peernam=azr[i]["localNetworkGateway2"]["id"].split("/")[8].replace(".","-")
    
            
            authkey=azr[i]["authorizationKey"]
            enbgp=azr[i]["enableBgp"]
            rw=azr[i]["routingWeight"]
            echo "RW = rw"
            sk=azr[i]["shared_key"]
            pbs=azr[i]["usePolicyBasedTrafficSelectors"]
            
            fr.write('\t type = "' +  ctype + '"\n')
            fr.write('\t\t virtual_network_gateway_id = "'\{'azurerm_virtual_network_gateway. + '__' + .id}'"' vngrg vngnam + '"\n')
            if authkey" -ne "null" :
                fr.write('\t authorization_key = "' +  authkey + '"\n')
        
            
            fr.write('\t enable_bgp = "' +  enbgp + '"\n')
            if rw" try ]["&& [ "rw" != "0" :
                fr.write('\t routing_weight = "' +  rw + '"\n')
        
            if sk" try :
                fr.write('\t shared_key = "' +  sk + '"\n')
        
            fr.write('\t use_policy_based_traffic_selectors = "' +  pbs + '"\n')
            
            if ctype == "ExpressRoute" :
                peerid=azr[i]["peer"]["id"]
                fr.write('\t\t express_route_circuit_id = "' +  peerid + '"\n')
                #fr.write('\t\t express_route_circuit_id = "'\{'azurerm_virtual_network_gateway. + '__' + .id}'"' peerrg peernam + '"\n')
                peerid=azr[i]["peer"]["id"]
                
        
            if ctype == "Vnet2Vnet" :
                fr.write('\t\t peer_virtual_network_gateway_id = "'\{'azurerm_virtual_network_gateway. + '__' + .id}'"' peerrg peernam + '"\n')
        
            if ctype == "IPsec" :
                fr.write('\t\t local_network_gateway_id = "'\{'azurerm_local_network_gateway. + '__' + .id}'"' peerrg peernam + '"\n')
        
            
            
            ipsec=azr[i]["ipsecPolicies"]
            jcount= len(ipsec)
            if jcount > 0 :
                for j in range(0,jcount):
                    fr.write('\t ipsec_policy {' + '"\n')
                    
                    dhg= ipsec | jq ".[j]["dhGroup"
                    fr.write('\t dh_group {' dhg + '"\n')
                    
                    fr.write('\t}\n')
                
    
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

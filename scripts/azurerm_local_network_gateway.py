# azurerm_local_network_gateway
def azurerm_local_network_gateway(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_local_network_gateway"
    tcode="200-"
    azr=""
    if crf in tfp:
    # REST or cli
        print "REST Managed Disk"
        url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Network/localNetworkGateway"
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

  

            gwaddr=azr[i]["proprties"]["gatewayIPAddress"]
            addrpre=azr[i]["proprties"]["localNetworkAddressSpace"]["addressPrefixes"]
            
            
            fr.write('\t gateway_address = "' +  gwaddr + '"\n')
            fr.write('\t address_space =  "' + addrpre +  '"\n')
        
            try :
                bgps=azr[i]["proprties"]["bgpSettings"]
                asn=azr[i]["proprties"]["bgpSettings"]["asn"]
                peera=azr[i]["proprties"]["bgpSettings"]["bgpPeeringAddress"]
                peerw=azr[i]["proprties"]["bgpSettings"]["peerWeight"]

                fr.write('\t bgp_settings {'  + '\n')
                fr.write('\t\t asn = "' + asn + '"\n')
                fr.write('\t\t bgp_peering_address = "' + peera + '"\n')
                fr.write('\t\t peer_weight = "' + peerw + '"\n')
                fr.write('\t } \n')
            except KeyError:
                pass
        
    


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

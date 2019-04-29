# azurerm_express_route_circuit_peering
def azurerm_express_route_circuit_peering(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_express_route_circuit_peering"
    tcode="250-"
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


            
            
            peers=azr[i]["properties"]["peerings"]
            echo peers | jq .
            
            acount= peers | | len(
            if acount > 0" :
                for k in range(0,acount):
                
                name= peers | jq ".[k]["name"]
                id= peers | jq ".[k]["id"]
                pt= peers | jq ".[k]["properties.peeringType"]
                pap= peers | jq ".[k]["properties.primaryPeerAddressPrefix"]
                sap= peers | jq ".[k]["properties.secondaryPeerAddressPrefix"]
                vid= peers | jq ".[k]["properties.vlanId"]
                pasn= peers | jq ".[k]["properties.peerASN"]
  

                

                fr.write('\t peering_type = "' +  pt + '"\n')
                fr.write('\t express_route_circuit_name = "' +  name2 + '"\n')
                fr.write('\t resource_group_name = "' +  rgsource + '"\n')
                fr.write('\t primary_peer_address_prefix = "' +  pap + '"\n')
                fr.write('\t secondary_peer_address_prefix = "' +  sap + '"\n')
                fr.write('\t vlan_id = "' +  vid + '"\n')
                #fr.write('\t shared_key = "' +  sk + '"\n')
                fr.write('\t peer_asn = "' +  pasn + '"\n')
                

                if pt" = "MicrosoftPeering" ]["|| [ "pt" = "AzurePrivatePeering" ][":
                    app= peers | jq ".[k]["properties.microsoftPeeringConfig.advertisedPublicPrefixes"
                    fr.write('\t microsoft_peering_config {' + '"\n')
                    fr.write('\t\t advertised_public_prefixes =  "app" + '"\n')
                    fr.write('\t }'  + '"\n')
               
                
                fr.write('}\n')
 
                


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

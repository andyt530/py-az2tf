# azurerm_express_route_circuit_peering
import ast
def azurerm_express_route_circuit_peering(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_express_route_circuit_peering"
    tcode="250-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/expressRouteCircuits"
        params = {'api-version': '2018-01-01'}
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
            name2=name
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
            
            peers=azr[i]["properties"]["peerings"]          
            acount=len(peers)
           
            for k in range(0,acount):
                
                name=peers[k]["name"]
                id= peers[k]["id"]
                rname=name.replace(".","-")

                id=azr[i]["id"]
                

                prefix=tfp+"."+rg+'__'+rname
                #print prefix
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)
                fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                #fr.write('\t name = "' + name + '"\n')
                #fr.write('\t location = "'+ loc + '"\n')
                fr.write('\t resource_group_name = "'+ rgs + '"\n')

                pt= peers[k]["properties"]["peeringType"]
                pap= peers[k]["properties"]["primaryPeerAddressPrefix"]
                sap= peers[k]["properties"]["secondaryPeerAddressPrefix"]
                vid= peers[k]["properties"]["vlanId"]
                pasn= peers[k]["properties"]["peerASN"]
            

                fr.write('\t peering_type = "' +  pt + '"\n')
                fr.write('\t express_route_circuit_name = "' +  name2 + '"\n')
                #fr.write('\t resource_group_name = "' +  rg + '"\n')
                fr.write('\t primary_peer_address_prefix = "' +  pap + '"\n')
                fr.write('\t secondary_peer_address_prefix = "' +  sap + '"\n')
                fr.write('\t vlan_id = "' +  str(vid) + '"\n')
                #fr.write('\t shared_key = "' +  sk + '"\n')
                fr.write('\t peer_asn = "' +  str(pasn) + '"\n')
                

                if pt == "MicrosoftPeering" or pt == "AzurePrivatePeering":
                    try:
                        app=str(ast.literal_eval(json.dumps(peers[k]["properties"]["microsoftPeeringConfig"]["advertisedPublicPrefixes"])))
                        app=app.replace("'",'"')

                        fr.write('\t microsoft_peering_config {' + '\n')
                        fr.write('\t\t advertised_public_prefixes =  ' + app + ' \n')
                        fr.write('\t }'  + '\n')
                    except KeyError:
                        pass

    # no tags        

                fr.write('}\n') 
                fr.close()   # close .tf file

                if cde:
                    with open(rfilename) as f: 
                        print (f.read())

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm) 

            # end k loop

        # end for i loop
        tfrm.close()
        tfim.close()
    #end stub

# azurerm_local_network_gateway
import ast
def azurerm_local_network_gateway(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_local_network_gateway"
    tcode="200-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Local NW Gateway"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/localNetworkGateways"
        params = {'api-version': '2019-04-01'}
        r = requests.get(url, headers=headers, params=params)
        azr=r.json()["value"]


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

  

            gwaddr=azr[i]["properties"]["gatewayIpAddress"]

            try:
                addrpre=str(ast.literal_eval(json.dumps(azr[i]["properties"]["localNetworkAddressSpace"]["addressPrefixes"])))
                addrpre=addrpre.replace("'",'"')
                if "[]" not in addrpre:
                    fr.write('\t address_space =  ' + addrpre +  '\n')
            except KeyError:
                pass
            
            fr.write('\t gateway_address = "' +  gwaddr + '"\n')
            
        
            try :
                bgps=azr[i]["properties"]["bgpSettings"]
                asn=azr[i]["properties"]["bgpSettings"]["asn"]
                peera=azr[i]["properties"]["bgpSettings"]["bgpPeeringAddress"]
                peerw=azr[i]["properties"]["bgpSettings"]["peerWeight"]

                fr.write('\t bgp_settings {\n')
                fr.write('\t\t asn = "' + str(asn) + '"\n')
                fr.write('\t\t bgp_peering_address = "' + peera + '"\n')
                fr.write('\t\t peer_weight = "' + str(peerw) + '"\n')
                fr.write('\t } \n')
            except KeyError:
                pass
        

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

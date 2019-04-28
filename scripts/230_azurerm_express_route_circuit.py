# azurerm_express_route_circuit
def azurerm_express_route_circuit(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_express_route_circuit"
    tcode="230-"
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


prefixa= 0 | awk -F 'azurerm_' '{'print 2}'' | awk -F '.sh' '{'print 1}'' 
tfp=fr.write('azurerm_" prefixa

echo TF_VAR_rgtarget
if 1" != " :
    rgsource=1
fi
at=az account get-access-token -o json
bt= at | jq .accessToken]
sub= at | jq .subscription]


ris=fr.write('curl -s  -X GET -H "'Authorization: Bearer "' -H "'Content-Type: application/json"' https://management.azure.com/subscriptions//resourceGroups//providers/Microsoft.Network/expressRouteCircuits?api-version=2018-01-01" bt sub rgsource
# count how many of this provider type there are.
ret=eval ris
azr2= ret | jq .value
rg=rgsource
count2= azr2 | | len(
if count2 > 0" :
    for j in range(0,count2):
        
        name2= azr2 | jq ".[j]["name"]
        ris2=fr.write('curl -s -X GET -H "'Authorization: Bearer "' -H "'Content-Type: application/json"' https://management.azure.com/subscriptions//resourceGroups//providers/Microsoft.Network/expressRouteCircuits/?api-version=2018-01-01" bt sub rgsource name2
        #echo ris2
        ret2=eval ris2
        azr= ret2 | jq .
        #echo ret2 | jq .
        count= azr | | len(
        if count > 0" :
            name=azrname"]
            rname= name.replace(".","-")
            rg= rgsource| sed 's/\./-/g'
            
            id=az"]["id"]
            loc=azrlocation"
            rg=rgsource
            tier=azrsku.tier"]
            family=azrsku.family"]
            aco=azrproperties.allowClassicOperations"]
            sp=azrproperties.serviceProviderProperties.serviceProviderName"]
            pl=azrproperties.serviceProviderProperties.peeringLocation"]
            bw=azrproperties.serviceProviderProperties.bandwidthInMbps"]
            
            
            
            fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
            fr.write('\t name = "' +  name + '"\n')
            fr.write('\t location =  "loc" + '"\n')
            fr.write('\t resource_group_name = "' +  rgsource + '"\n')
            
            fr.write('\t service_provider_name = "' +   sp + '"\n')
            fr.write('\t peering_location = "' +   pl + '"\n')
            fr.write('\t bandwidth_in_mbps = "' +   bw + '"\n')
            
            fr.write('\t sku {'   + '"\n')
            fr.write('\t\t tier = "' +  tier + '"\n')
            fr.write('\t\t family = "' +  family + '"\n')
            fr.write('\t }\n')
            fr.write('\t allow_classic_operations = "' +   aco + '"\n')
            

            
            
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

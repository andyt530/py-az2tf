# azurerm_express_route_circuit_authorization
def azurerm_express_route_circuit_authorization(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_express_route_circuit_authorization"
    tcode="240-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Network/expressRouteCircuits"
        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print "# " + tfp,
        count=len(azr)
        print count
        for i in range(0, count):

            name=azr[i]["name"]
            name2=name
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
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

            
            auths=azr[i]["properties"]["authorizations"]            
            acount= len(auths)
            if acount > 0 :
                for k in range(0,acount):
                
                    name=auths[k]["name"]
                    id= auths[k]["id"]
                    
                    rname= name.replace(".","-")

                    fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                    fr.write('\t name = "' + name + '"\n')
                    fr.write('\t resource_group_name = "'+ rgs + '"\n')
               
                    fr.write('\t express_route_circuit_name = "' +  name2 + '"\n')                                  

    # no tags       
 

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

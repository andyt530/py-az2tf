import ast
def azurerm_virtual_network(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #  060 Virtual Networks
    tfp="azurerm_virtual_network"
    azr=""
    if crf in tfp:
        # REST
        # print "REST VNets"

        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/virtualNetworks"
        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf="060-"+tfp+"-staterm.sh"
        tfimf="060-"+tfp+"-stateimp.sh"
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
            fr.write("")
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')
            
            addsp=azr[i]["properties"]["addressSpace"]["addressPrefixes"]
            laddsp='['
            for x in addsp:
                laddsp=laddsp+'"'+x+'",'
            laddsp=laddsp+']'
            #print laddsp
            fr.write('\taddress_space =  ' + laddsp + '\n')
            try:
                dns=str(ast.literal_eval(json.dumps(azr[i]["properties"]["dhcpOptions"]["dnsServers"])))
                dns=dns.replace("'",'"')
                if "[]" not in dns:
                    fr.write('\t dns_servers =  ' + dns + '\n')
            except KeyError:
                pass        


            #
            #loop around subnets
            #
            subs=azr[i]["properties"]["subnets"]
            jcount=len(subs)
            for j in range(0,jcount):
                snname=subs[j]["name"]
                snaddr=subs[j]["properties"]["addressPrefix"]

                fr.write('\tsubnet {\n')
                fr.write('\t\t name = "'+ snname + '"\n')
                fr.write('\t\t address_prefix = "' + snaddr + '"\n')
                try:
                    snnsgid=subs[j]["properties"]["networkSecurityGroup"]["id"]
                    nsgnam=snnsgid.split("/")[8].replace(".","-")
                    nsgrg=snnsgid.split("/")[4].replace(".","-").lower() 
                    if nsgrg[0].isdigit(): nsgrg="rg_"+nsgrg        
                    fr.write('\t\t security_group = "${azurerm_network_security_group.' + nsgrg + '__' + nsgnam + '.id}"' + '\n')
                except KeyError: 
                    pass
                
                fr.write('\t}' + '\n')

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
        return azr
    #end VNET
    #############
def azurerm_network_interface(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    
    tfp="azurerm_network_interface"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/networkInterfaces"
        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf="130-"+tfp+"-staterm.sh"
        tfimf="130-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rgs=id.split("/")[4]
            rg=id.split("/")[4].replace(".","-").lower()
            
            if rg[0].isdigit(): rg="rg_"+rg
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

            ipfor=azr[i]["properties"]["enableIPForwarding"]
            netacc=azr[i]["properties"]["enableAcceleratedNetworking"]
            ipcon=azr[i]["properties"]["ipConfigurations"]
          
            #fr.write('\t internal_dns_name_label  = "' +  ipfor + '"\n')
            fr.write('\t enable_ip_forwarding = ' +  str(ipfor).lower() + '\n')
            fr.write('\t enable_accelerated_networking  = ' +  str(netacc).lower() + '\n')
            #fr.write('\t dns_servers  = "' +  ipfor + '"\n')
            #privip0=azr[i]["properties"]["ipConfigurations"][0]["privateIPAddress"]

            try:
                snsg=azr[i]["properties"]["networkSecurityGroup"]["id"].split("/")[8].replace(".","-")
                snsgrg=azr[i]["properties"]["networkSecurityGroup"]["id"].split("/")[4].replace(".","-").lower()
                if snsgrg[0].isdigit(): snsgrg="rg_"+snsgrg
                fr.write('\t network_security_group_id = "${azurerm_network_security_group.' + snsgrg + '__' + snsg + '.id}"\n')
            except KeyError:
                pass
               
            icount=len(ipcon)
            for j in range(0,icount):
                ipcname=azr[i]["properties"]["ipConfigurations"][j]["name"]
                subname=azr[i]["properties"]["ipConfigurations"][j]["properties"]["subnet"]["id"].split("/")[10].replace(".","-")
                subrg=azr[i]["properties"]["ipConfigurations"][j]["properties"]["subnet"]["id"].split("/")[4].replace(".","-").lower()
                #subipid=azr[i]["properties"]["ipConfigurations"][j]["properties"]["publicIPAddress"]["id"].split("/")[8]
                subipalloc=azr[i]["properties"]["ipConfigurations"][j]["properties"]["privateIPAllocationMethod"]
                privip=azr[i]["properties"]["ipConfigurations"][j]["properties"]["privateIPAddress"]
                prim=azr[i]["properties"]["ipConfigurations"][j]["properties"]["primary"]

                                      
                fr.write('\t ip_configuration {' + '\n')
                fr.write('\t\t name = "' + ipcname + '"\n')
                if subrg[0].isdigit(): subrg="rg_"+subrg
                fr.write('\t\t subnet_id = "${azurerm_subnet.' + subrg + '__' + subname + '.id}"\n')
                if subipalloc != "Dynamic":
                    fr.write('\t\t private_ip_address = "' + privip + '"\n')
               
                fr.write('\t\t private_ip_address_allocation = "' +    subipalloc + '"\n')
                try:
                    pubipnam=azr[i]["properties"]["ipConfigurations"][j]["properties"]["publicIPAddress"]["id"].split("/")[8].replace(".","-")
                    pubiprg=azr[i]["properties"]["ipConfigurations"][j]["properties"]["publicIPAddress"]["id"].split("/")[4].replace(".","-").lower()
                    if pubiprg[0].isdigit(): pubiprg="rg_"+pubiprg
                    fr.write('\t\t public_ip_address_id = "${azurerm_public_ip.' + pubiprg + '__' + pubipnam + '.id}"\n')
                except KeyError:
                    pass

                #fr.write('\t\t application_gateway_backend_address_pools_ids = "' +    subipalloc + '"\n')
                #fr.write('\t\t load_balancer_backend_address_pools_ids = "' +    subipalloc + '"\n')
                #fr.write('\t\t load_balancer_inbound_nat_rules_ids = "' +    subipalloc + '"\n')
                #fr.write('\t\t application_security_group_ids = "' +    subipalloc + '"\n')
                fr.write('\t\t primary = ' + str(prim).lower() + '\n')
                try:
                    asgs=azr[i]["properties"]["ipConfigurations"][j]["properties"]["applicationSecurityGroups"]
                    kcount=len(asgs)
                    for k in range(0,kcount):
                        asgnam=azr[i]["properties"]["ipConfigurations"][j]["properties"]["applicationSecurityGroups"][k]["id"].split("/")[8].replace(".","-")
                        asgrg=azr[i]["properties"]["ipConfigurations"][j]["properties"]["applicationSecurityGroups"][k]["id"].split("/")[4].replace(".","-").lower()
                        if asgrg[0].isdigit(): asgrg="rg_"+asgrg
                        fr.write('\t\t application_security_group_ids = ["${azurerm_application_security_group.' + asgrg + '__' + asgnam + '.id}"]\n')
                except KeyError:
                    pass


                fr.write('\t}\n') # end ip configurations
            # end j           

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
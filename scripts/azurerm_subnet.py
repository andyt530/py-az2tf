import ast
def azurerm_subnet(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #  070 subnets
    tfp="azurerm_subnet"
    azr=""
    if crf in tfp:
        # REST
        # print "REST VNets"

        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/virtualNetworks"
        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

    # subnet in vnet
        tfrmf="070-"+tfp+"-staterm.sh"
        tfimf="070-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):
            subs=azr[i]["properties"]["subnets"]
            vnetname=azr[i]["name"]
            jcount=len(subs)
            

            for j in range(0, jcount):
                name=subs[j]["name"]
                #loc=subs[j]["location"] subnets don't have location
                id=subs[j]["id"]
                rg=id.split("/")[4].replace(".","-").lower()
                if rg[0].isdigit(): rg="rg_"+rg
                rgs=id.split("/")[4]
                if crg is not None:
                    if rgs.lower() != crg.lower():
                        continue  # back to for
                if cde:
                    print(json.dumps(subs[j], indent=4, separators=(',', ': ')))
                
                rname=name.replace(".","-")
                prefix=tfp+"."+rg+'__'+rname
                #print prefix
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                fr.write('\t virtual_network_name = "' + vnetname + '"\n') 
                fr.write('\t resource_group_name = "' +  rgs + '"\n')

                sprefix=subs[j]["properties"]["addressPrefix"]
                fr.write('\t address_prefix = "' +  sprefix + '"\n')
                rtbid="null"
                try:
                    seps=subs[j]["properties"]["serviceEndpoints"]
                    kcount=len(seps)
                    #print (json.dumps(seps, indent=4, separators=(',', ': ')))
                    #print kcount
                    lseps='['
                    for k in range(0, kcount):
                        x=seps[k]["service"]
                        lseps=lseps+'"'+x+'",'
                    lseps=lseps+']'
                    fr.write('\t service_endpoints = '+ lseps + '\n')
                except KeyError:
                    pass
                
                try:
                    snsgid=subs[j]["properties"]["networkSecurityGroup"]["id"].split("/")[8].replace(".","-")
                    snsgrg=subs[j]["properties"]["networkSecurityGroup"]["id"].split("/")[4].replace(".","-").lower()
                    if snsgrg[0].isdigit(): snsgrg="rg_"+snsgrg
                    fr.write('\t network_security_group_id = "${azurerm_network_security_group.' + snsgrg + '__' + snsgid +'.id}"' + '\n')
                except KeyError:
                    pass
                
                try:
                    rtbid=subs[j]["properties"]["routeTable"]["id"].split("/")[8].replace(".","-")
                    rtrg=subs[j]["properties"]["routeTable"]["id"].split("/")[4].replace(".","-").lower()
                    if rtrg[0].isdigit(): rtrg="rg_"+rtrg
                    fr.write('\t route_table_id = "${azurerm_route_table.' + rtrg + '__' + rtbid +'.id}"' + '\n')
                except KeyError:
                    pass   

                try:
                    delegn=subs[j]["properties"]["delegations"]
                    kcount=len(delegn)
                    for k in range(0, kcount):
                        delegn=subs[j]["properties"]["delegations"][k]["name"]
                        fr.write('delegation {\n')
                        fr.write('\t name = "' + delegn + '"\n')
                        try:
                            sdn=subs[j]["properties"]["delegations"][k]["properties"]["serviceName"]
                            sdact=str(ast.literal_eval(json.dumps(subs[j]["properties"]["delegations"][k]["properties"]["actions"])))                                 
                            sdact=sdact.replace("'",'"')
                            fr.write('\t service_delegation {\n')
                            fr.write('\t name = "' + sdn + '"\n')
                            #fr.write('\t actions = ' + sdact + '\n')
                            fr.write('\t} \n')
                        except KeyError:
                            pass         

                        fr.write('} \n')
                    # end k loop
                except KeyError:
                    pass 


                fr.write('}' + ' \n')

    # azurerm_subnet_network_security_group_association
        
                r1="skip"
                try:
                    snsgid=subs[j]["properties"]["networkSecurityGroup"]["id"].split("/")[8].replace(".","-")
                    r1="azurerm_subnet_network_security_group_association"
                    fr.write('resource ' + r1 + ' ' + rg + '__' + rname + '__' + snsgid + ' {\n') 
                    fr.write('\tsubnet_id = "${azurerm_subnet.' + rg + '__' + rname + '.id}"' + '\n')
                    if snsgrg[0].isdigit(): snsgrg="rg_"+snsgrg
                    fr.write('\tnetwork_security_group_id = "${azurerm_network_security_group.' + snsgrg + '__' + snsgid +'.id}"' + '\n')
                    fr.write('}' + ' \n')
                except KeyError:
                    pass
                    

    # azurerm_subnet_route_table_association

                r2="skip"
                try:
                    rtbid=subs[j]["properties"]["routeTable"]["id"].split("/")[8].replace(".","-")
                    r2="azurerm_subnet_route_table_association"
                    fr.write('resource ' + r2 + ' ' + rg + '__' + rname + '__' + rtbid + ' {\n') 
                    fr.write('\tsubnet_id = "${azurerm_subnet.' + rg + '__' + rname + '.id}"' + '\n')
                    if rtrg[0].isdigit(): rtrg="rg_"+rtrg
                    fr.write('\troute_table_id = "${azurerm_route_table.' + rtrg + '__' + rtbid +'.id}"' + '\n')
                    fr.write('}' + ' \n')
                except KeyError:
                    pass
                

                #fr.write('}\n') 
                fr.close()   # close .tf file


                # azurerm_subnet

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(j) + ' of ' + str(jcount-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm) 

    # azurerm_subnet_network_security_group_association

                if "skip" not in r1:
        
                    tfrm.write('terraform state rm ' + r1 + '.' + rg + '__' + rname + '__' + snsgid + '\n')
                    tfcomm='terraform import '+r1 +'.'+rg+'__'+rname+'__'+snsgid+' '+id+'\n'
                    tfim.write(tfcomm)
            

    # azurerm_subnet_route_table_association

                if "skip" not in r2:

                    tfrm.write('terraform state rm ' + r2 + '.' + rg + '__' + rname + '__' + rtbid + '\n')
                    tfcomm='terraform import '+r2 +'.'+rg+'__'+rname+'__'+rtbid+' '+id+'\n'
                    tfim.write(tfcomm)
                

            # end j

        ###############
        # specific code end
        ###############
    

        # end for i loop

        tfrm.close()
        tfim.close()
    #end subnet
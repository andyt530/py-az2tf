# azurerm_application_gateway
def azurerm_application_gateway(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_application_gateway"
    tcode="193-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/applicationGateways"
        params = {'api-version': '2018-07-01'}
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
            
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')


            skun=azr[i]["properties"]["sku"]["name"]
           
            skut=azr[i]["properties"]["sku"]["tier"]
            
            
            # the blocks
            gwipc=azr[i]["properties"]["gatewayIPConfigurations"]
            feps=azr[i]["properties"]["frontendPorts"]
            fronts=azr[i]["properties"]["frontendIPConfigurations"]
            beap=azr[i]["properties"]["backendAddressPools"]
            bhttps=azr[i]["properties"]["backendHttpSettingsCollection"]
            httpl=azr[i]["properties"]["httpListeners"]
            probes=azr[i]["properties"]["probes"]
            rrrs=azr[i]["properties"]["requestRoutingRules"]
            urlpm=azr[i]["properties"]["urlPathMaps"]
            
            sslcerts=azr[i]["properties"]["sslCertificates"]
            #wafc=azr[i]["properties"]["webApplicationFirewallConfiguration"]

            fr.write('sku { \n')
            fr.write('\t name = "' +  skun + '"\n')
            try :
                skuc=azr[i]["properties"]["sku"]["capacity"]
                fr.write('\t capacity = "' +  str(skuc) + '"\n')
            except KeyError:
                fr.write('\t capacity = "' + '1'  + '"\n')
                pass

            fr.write('\t tier = "' +  skut + '"\n')
            fr.write('} \n')



            icount=len(gwipc)
            for j in range(0,icount):
                gname=azr[i]["properties"]["gatewayIPConfigurations"][j]["name"]
                subrg=azr[i]["properties"]["gatewayIPConfigurations"][j]["properties"]["subnet"]["id"].split("/")[4].replace(".","-").lower()
                subname=azr[i]["properties"]["gatewayIPConfigurations"][j]["properties"]["subnet"]["id"].split("/")[10].replace(".","-")
                fr.write('gateway_ip_configuration {' + '\n')
                fr.write('\t name = "' + gname + '"\n')
                try:
                    subrg=azr[i]["properties"]["gatewayIPConfigurations"][j]["properties"]["subnet"]["id"].split("/")[4].replace(".","-").lower()
                    subname=azr[i]["properties"]["gatewayIPConfigurations"][j]["properties"]["subnet"]["id"].split("/")[10].replace(".","-")
                    if subrg[0].isdigit(): subrg="rg_"+subrg
                    fr.write('\t subnet_id = "${azurerm_subnet.' + subrg + '__' + subname + '.id}" \n')
                except KeyError:  
                    pass
                fr.write('}\n')
                
        
            
    # front end port
            icount=len(feps)
            if icount > 0 :
                for j in range(0,icount):
                    fname=azr[i]["properties"]["frontendPorts"][j]["name"]
                    fport=azr[i]["properties"]["frontendPorts"][j]["properties"]["port"]
                    fr.write('frontend_port {\n')
                    fr.write('\t name = "' + fname + '"\n')
                    fr.write('\t port = "' + str(fport) + '"\n')
                    fr.write('}\n')
                
        
            
    # front end IP config block
            icount=len(fronts)
            if icount > 0 :
                for j in range(0,icount):
                    
                    fname=azr[i]["properties"]["frontendIPConfigurations"][j]["name"]
                    fr.write('frontend_ip_configuration {\n')
                    fr.write('\t name = "' + fname + '"\n')
                    try :
                        subrg=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["subnet"]["id"].split("/")[4].replace(".","-").lower()
                        subname=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["subnet"]["id"].split("/")[10].replace(".","-")                 
                        if subrg[0].isdigit(): subrg="rg_"+subrg
                        fr.write('\t subnet_id = "${azurerm_subnet.' + subrg + '__'  + subname + '.id}" \n')
                    except KeyError:
                        pass

                    try :
                        priv=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["privateIPAddress"]
                        fr.write('\t private_ip_address = "' + priv + '"\n')
                    except KeyError:
                        pass
                
                    try :
                        privalloc=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["privateIPAllocationMethod"]
                        fr.write('\t private_ip_address_allocation  = "' + privalloc + '"\n')
                    except KeyError:
                        pass

                    try :
                        pubrg=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["publicIPAddress"]["id"].split("/")[4].replace(".","-").lower()
                        pubname=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["publicIPAddress"]["id"].split("/")[8].replace(".","-")  
                        if pubrg[0].isdigit(): pubrg="rg_"+pubrg
                        fr.write('\t public_ip_address_id = "${azurerm_public_ip.' + pubrg + '__' + pubname + '.id}" \n')
                    except KeyError:
                        pass
                    
                    fr.write('}\n')
                    
                
        

    # backend_address_pool          beap=azr[i]["backendAddressPools"

            icount=len(beap)
            if icount > 0:
                for j in range(0,icount):
                    bname=azr[i]["properties"]["backendAddressPools"][j]["name"]
                    fr.write('backend_address_pool {' + '\n')
                    fr.write('\t name = "' + bname + '"\n')
                    beaddr=azr[i]["properties"]["backendAddressPools"][j]["properties"]["backendAddresses"]         
                    kcount=len(beaddr)    
                    if kcount > 0 :
                        for k in range(0,kcount):       
                            try :
                                beadip=azr[i]["properties"]["backendAddressPools"][j]["properties"]["backendAddresses"][k]["IPAddress"]
                                fr.write('\t ip_address ="' +  beadip + '"\n')
                            except KeyError:
                                pass
                            try:
                                beadfq=azr[i]["properties"]["backendAddressPools"][j]["properties"]["backendAddresses"][k]["fqdn"]
                                fr.write('\t fqdns = ["' + beadfq + '"] \n')         
                            except KeyError:
                                pass
                    fr.write('}\n')
                

    # backend_http_settings
            icount=len(bhttps)
            if icount > 0:
                for j in range(0,icount):
                    bname=azr[i]["properties"]["backendHttpSettingsCollection"][j]["name"]
                    bport=azr[i]["properties"]["backendHttpSettingsCollection"][j]["properties"]["port"]
                    bproto=azr[i]["properties"]["backendHttpSettingsCollection"][j]["properties"]["protocol"]
                    bcook=azr[i]["properties"]["backendHttpSettingsCollection"][j]["properties"]["cookieBasedAffinity"]
                    btimo=azr[i]["properties"]["backendHttpSettingsCollection"][j]["properties"]["requestTimeout"]
                    #pname=azr[i]["properties"]["backendHttpSettingsCollection"][j]["properties"]["probe"]["id"].split("/")[10]
                    
                    fr.write('backend_http_settings {\n')
                    fr.write('\t name = "' + bname + '"\n')
                    fr.write('\t port = "' + str(bport) + '"\n')
                    fr.write('\t protocol = "' + bproto + '"\n')
                    fr.write('\t cookie_based_affinity = "' + bcook + '"\n')
                    fr.write('\t request_timeout = "' + str(btimo) + '"\n')
                    try :
                        pname=azr[i]["properties"]["backendHttpSettingsCollection"][j]["properties"]["probe"]["id"].split("/")[10]
                        fr.write('\t probe_name = "' + pname + '"\n')
                    except KeyError:
                        pass
                    try :
                        bhn=azr[i]["properties"]["backendHttpSettingsCollection"][j]["properties"]["hostName"]
                        try:
                            fr.write('\t host_name = "' + bhn + '"\n')
                        except TypeError:
                            pass
                    except KeyError:
                        pass               
                   
                    try :
                        acert=azr[i]["properties"]["backendHttpSettingsCollection"][j]["properties"]["authenticationCertificates"][0]["id"].split("/")[10]
                        #print acert
                        fr.write('\t authentication_certificate { \n')
                        fr.write('\t\t name = "' + acert + '"\n')
                        fr.write('\t}\n')
                    except KeyError:
                        pass
                    fr.write('}\n')
                
            
            
    # http listener block          httpl=azr[i]["httpListeners"

            icount=len(httpl)
            if icount > 0:
                for j in range(0,icount):
                    bname=azr[i]["properties"]["httpListeners"][j]["name"]
                    feipcn=azr[i]["properties"]["httpListeners"][j]["properties"]["frontendIPConfiguration"]["id"].split("/")[10]
                    fepn=azr[i]["properties"]["httpListeners"][j]["properties"]["frontendPort"]["id"].split("/")[10]
                    bproto=azr[i]["properties"]["httpListeners"][j]["properties"]["protocol"]
                                                                     

                    fr.write('http_listener {\n')
                    fr.write('\t name = "' +    bname + '"\n')
                    fr.write('\t frontend_ip_configuration_name = "' +    feipcn + '"\n')
                    fr.write('\t frontend_port_name = "' +    fepn + '"\n')
                    fr.write('\t protocol = "' +    bproto + '"\n')
                    try :
                        bhn=azr[i]["properties"]["httpListeners"][j]["properties"]["hostName"]
                        fr.write('\t host_name = "' +    bhn + '"\n')
                    except KeyError:
                        pass
                    try :
                        bssl=azr[i]["properties"]["httpListeners"][j]["properties"]["sslCertificate"]["id"].split("/")[10]
                        fr.write('\t ssl_certificate_name = "' +    bssl + '"\n')
                    except KeyError:
                        pass
                    try :
                        rsni=azr[i]["properties"]["httpListeners"][j]["properties"]["requireServerNameIndication"]
                        fr.write('\t require_sni = ' +  str(rsni).lower() + '\n')
                    except KeyError:
                        pass
                    fr.write('}\n')
                
# probe block

            icount=len(probes)
            if icount > 0 :
                for j in range(0,icount):
                    bname=azr[i]["properties"]["probes"][j]["name"]
                    bproto=azr[i]["properties"]["probes"][j]["properties"]["protocol"]
                    bpath=azr[i]["properties"]["probes"][j]["properties"]["path"]
                    bint=azr[i]["properties"]["probes"][j]["properties"]["interval"]
                    btimo=azr[i]["properties"]["probes"][j]["properties"]["timeout"]
                    bunth=azr[i]["properties"]["probes"][j]["properties"]["unhealthyThreshold"]
                                   
                                
                    #bmstat=azr[i]["properties"]["probes"][j]["properties"]["match"]["statusCodes"]

                    fr.write('probe {' + '\n')
                    fr.write('\t name = "' +    bname + '"\n')
                    fr.write('\t protocol = "' +    bproto + '"\n')
                    fr.write('\t path = "' +    bpath + '"\n')
                    try:
                        bhost=azr[i]["properties"]["probes"][j]["properties"]["host"]
                        fr.write('\t host = "' +    bhost + '"\n')
                    except KeyError:
                        pass
                    fr.write('\t interval = "' +  str(bint) + '"\n')
                    fr.write('\t timeout = "' +    str(btimo) + '"\n')
                    fr.write('\t unhealthy_threshold = "' +  str(bunth) + '"\n')


                    try :
                        bmsrv=azr[i]["properties"]["probes"][j]["properties"]["minServers"]
                        fr.write('\t minimum_servers = "' + str(bmsrv) + '"\n')
                    except KeyError:
                        pass

                    fr.write('\t match {' + '\n')
                    
                    try :
                        bmbod=azr[i]["properties"]["probes"][j]["properties"]["match"]["body"] 
                        if bmbod == "":
                            fr.write('\t\t body = "' + '*' + '"\n')
                        else:
                            fr.write('\t\t body = "' + bmbod + '"\n')
                    except KeyError:
                        pass
                
                    fr.write('\t }\n')
                    fr.write('}\n')
                    

# routing rules

            icount=len(rrrs)
            if icount > 0 :
                for j in range(0,icount):
                    bname=azr[i]["properties"]["requestRoutingRules"][j]["name"]
                    btyp=azr[i]["properties"]["requestRoutingRules"][j]["properties"]["ruleType"]
                    blin=azr[i]["properties"]["requestRoutingRules"][j]["properties"]["httpListener"]["id"].split("/")[10]

                    fr.write('request_routing_rule { \n')

                    fr.write('\t name = "' + bname + '"\n')
                    fr.write('\t rule_type = "' + btyp + '"\n')
                    fr.write('\t http_listener_name = "' + blin + '"\n')
                    try :
                        bapn=azr[i]["properties"]["requestRoutingRules"][j]["properties"]["backendAddressPool"]["id"].split("/")[10]
                        fr.write('\t backend_address_pool_name = "' +    bapn + '"\n')
                    except KeyError:
                        pass
                    try :
                        bhsn=azr[i]["properties"]["requestRoutingRules"][j]["properties"]["backendHttpSettings"]["id"].split("/")[10]
                        fr.write('\t backend_http_settings_name = "' +    bhsn + '"\n')
                    except KeyError:
                        pass
                    fr.write('\t }\n')
                
        


    # ssl_certificate block   sslcerts=azr[i]["sslCertificates"

            jcount=len(sslcerts)
            if jcount > 0 :
                for j in range(0,jcount):
                    #print "***********"
                    #print(json.dumps(sslcerts[j], indent=4, separators=(',', ': ')))

                    try :
                        bname=azr[i]["properties"]["sslCertificates"][j]["name"]
                        fr.write('ssl_certificate {' + '\n')
                        fr.write('\t name = "' + bname + '"\n')


                        try :
                            bdata=azr[i]["properties"]["sslCertificates"][j]["properties"]["dummy"]
                            fr.write('\t data = "' + bdata + '"\n')
                        except KeyError:
                            fr.write('\t data = ""\n') 
                            pass
                        
                        try :
                            bpw=azr[i]["properties"]["sslCertificates"][j]["password"]
                            fr.write('\t password = "' + bpw + '"\n')       
                        except KeyError:
                            fr.write('\t password = ""\n')
                            pass




                        fr.write('\t }\n')

                    except KeyError:
                        pass
                
                
        

    # waf configuration block     wafc=azr[i]["webApplicationFirewallConfiguration"]
    # - not an array like the other blocks 
    #
            
            try :
                fmode=azr[i]["properties"]["webApplicationFirewallConfiguration"]["firewallMode"]
                rst=azr[i]["properties"]["webApplicationFirewallConfiguration"]["ruleSetType"]
                rsv=azr[i]["properties"]["webApplicationFirewallConfiguration"]["ruleSetVersion"]
                fen=azr[i]["properties"]["webApplicationFirewallConfiguration"]["enabled"]
                    
                fr.write('waf_configuration { \n')
                fr.write('\t firewall_mode = "' + fmode + '"\n')
                fr.write('\t rule_set_type = "' + rst + '"\n')
                fr.write('\t rule_set_version = "' + rsv + '"\n')
                fr.write('\t enabled = ' + str(fen).lower() + '\n')
                fr.write('\t }\n') 
            except KeyError:
                pass         
            
            #if cde:
            #    print(json.dumps(authcerts, indent=4, separators=(',', ': ')))
            try:
                authcerts=azr[i]["properties"]["authenticationCertificates"]
                jcount=len(authcerts)
                for j in range(0,jcount):
                    cname=azr[i]["properties"]["authenticationCertificates"][j]["name"]
                    cdata=azr[i]["properties"]["authenticationCertificates"][j]["properties"]["data"]
                    fr.write('authentication_certificate {\n')
                    fr.write('\t name = "' + cname + '"\n')  
                    fr.write('\t data = "' + '"\n') 
                    fr.write('\t }\n')
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

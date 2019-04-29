# azurerm_application_gateway
def azurerm_application_gateway(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_application_gateway"
    tcode="193-"
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


            skun=azr[i]["sku"]["name"]

            skut=azr[i]["sku"]["tier"]
            
            
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
            authcerts=azr[i]["properties"]["authenticationCertificates"]
            sslcerts=azr[i]["properties"]["sslCertificates"]
            wafc=azr[i]["properties"]["webApplicationFirewallConfiguration"]

            fr.write('sku { \n')
            fr.write('\t name = "' +  skun + '"\n')
            try :
                skuc=azr[i]["sku"]["capacity"]
                fr.write('\t capacity = "' +  skuc + '"\n')
            except KeyError:
                fr.write('\t capacity = "' + '1'  + '"\n')
                pass

            fr.write('\t tier = "' +  skut + '"\n')
            fr.write('} \n')
            
    # gateway ip config block
            
            icount=len(gwipc)
            for j in range(0,icount):
                gname=azr[i]["properties"]["gatewayIpConfigurations"][j]["name"]
                subrg=azr[i]["properties"]["gatewayIpConfigurations"][j]["properties"]["subnet"]["id"].split("/")[4].replace(".","-")
                subname=azr[i]["gatewayIpConfigurations"][j]["subnet"]["id"].split("/")[10].replace(".","-")
                fr.write('gateway_ip_configuration {' + '\n')
                fr.write('\t name = "' +    gname + '"\n')
                try:
                    subrg=azr[i]["properties"]["gatewayIpConfigurations"][j]["properties"]["subnet"]["id"].split("/")[4].replace(".","-")
                    subname=azr[i]["properties"]["gatewayIpConfigurations"][j]["properties"]["subnet"]["id"].split("/")[10].replace(".","-")
                    fr.write('\t subnet_id = "${azurerm_subnet.' + subrg + '__' + subname + '.id} \n')
                except KeyError:  
                    pass
                fr.write('}\n')
                
        
            
    # front end port
            icount=len(feps)
            if icount > 0 :
                for j in range(0,icount):
                    fname=azr[i]["properties"]["frontendPorts"][j]["name"]
                    fport=azr[i]["properties"]["frontendPorts"][j]["port"]
                    fr.write('frontend_port {' + '\n')
                    fr.write('\t name = "' + fname + '"\n')
                    fr.write('\t port = "' + fport + '"\n')
                    fr.write('}\n')
                
        
            
    # front end ip config block
            icount=len(fronts)
            if icount > 0 :
                for j in range(0,icount):
                    
                    fname=azr[i]["properties"]["frontendIpConfigurations"][j]["name"]
                    priv=azr[i]["properties"]["frontendIpConfigurations"][j]["properties"]["privateIPAddress"]
                    
                    pubrg=azr[i]["properties"]["frontendIpConfigurations"][j]["properties"]["publicIPAddress"]["id"].split("/")[4].replace(".","-")
                    pubname=azr[i]["properties"]["frontendIpConfigurations"][j]["properties"]["publicIPAddress"]["id"].split("/")[8].replace(".","-")
                    
                    subrg=azr[i]["properties"]["frontendIpConfigurations"][j]["properties"]["subnet"]["id"].split("/")[4].replace(".","-")
                    subname=azr[i]["properties"]["frontendIpConfigurations"][j]["properties"]["subnet"]["id"].split("/")[10].replace(".","-")
                    privalloc=azr[i]["properties"]["frontendIpConfigurations"][j]["properties"]["privateIPAllocationMethod"]
                    
                    fr.write('frontend_ip_configuration {' + '"\n')
                    fr.write('\t name = "' +    fname + '"\n')
                    try :
                        subrg=azr[i]["properties"]["frontendIpConfigurations"][j]["properties"]["subnet"]["id"].split("/")[4].replace(".","-")
                        subname=azr[i]["properties"]["frontendIpConfigurations"][j]["properties"]["subnet"]["id"].split("/")[10].replace(".","-")                 
                        fr.write('\t subnet_id = "${azurerm_subnet.' + subrg + '__'  + subname + '.id}" \n')
                    except KeyError:
                        pass

                    try :

                        fr.write('\t private_ip_address = "' +  priv + '"\n')
                    except KeyError:
                        pass
                
                    try :

                        fr.write('\t private_ip_address_allocation  = "' +  privalloc + '"\n')
                    except KeyError:
                        pass

                    try :

                        fr.write('\t public_ip_address_id = "'\{'azurerm_public_ip. + '__' + .id}'"' pubrg pubname + '"\n')
                    except KeyError:
                        pass
                    
                    fr.write('}\n')
                    
                
        

    # backend_address_pool          beap=azr[i]["backendAddressPools"

            icount=len(beap)
            if icount > 0:
                for j in range(0,icount):
                    bname=azr[i]["properties"]["backendAddressPools[j]["name"]
                    fr.write('backend_address_pool {' + '"\n')
                    fr.write('\t name = "' +    bname + '"\n')
                    beaddr=azr[i]["properties"]["backendAddressPools[j]["properties"]["backendAddresses"]         
                    kcount= len(beaddr)    
                    if kcount > 0 :
                        for k in range(0,kcount):
                            beadip=azr[i]["properties"]["backendAddressPools[j]["properties"]["backendAddresses"][k]["IPAddress"]
                            beadfq=azr[i]["properties"]["backendAddressPools[j]["properties"]["backendAddresses"][k]["fqdn"]
                            try :
                                fr.write('\t ip_address ="' +  beadip + '"\n')
                        
                            try:
                                fr.write('\t fqdns = ["' + beadfq + '"] \n')         

                    fr.write('}\n')
                

    # backend_http_settings
            icount=len(bhttps)
            if icount > 0:
                for j in range(0,icount):
                    bname=azr[i]["properties"]["backendHttpSettingsCollection[j]["name"]
                    bport=azr[i]["properties"]["backendHttpSettingsCollection[j]["properties"]["port"]
                    bproto=azr[i]["properties"]["backendHttpSettingsCollection[j]["properties"]["protocol"]
                    bcook=azr[i]["properties"]["backendHttpSettingsCollection[j]["properties"]["cookieBasedAffinity"]
                    btimo=azr[i]["properties"]["backendHttpSettingsCollection[j]["properties"]["requestTimeout"]
                    pname=azr[i]["properties"]["backendHttpSettingsCollection[j]["properties"]["probe"]["id"].split("/")[10]]
                    acert=azr[i]["properties"]["backendHttpSettingsCollection[j]["properties"]["authenticationCertificates"][0]["id"].split("/")[10]]

                    fr.write('backend_http_settings {' + '"\n')
                    fr.write('\t name = "' +    bname + '"\n')
                    fr.write('\t port = "' +    bport + '"\n')
                    fr.write('\t protocol = "' +    bproto + '"\n')
                    fr.write('\t cookie_based_affinity = "' +    bcook + '"\n')
                    fr.write('\t request_timeout = "' +    btimo + '"\n')
                    if pname" try :
                    fr.write('\t probe_name = "' +    pname + '"\n')
                
                    if acert" try :
                        fr.write('\t au:tication_certificate {' + '"\n')
                        fr.write('\t\t name = "' +    acert + '"\n')
                        fr.write('\t}\n')
                
                    fr.write('}\n')
                
            
            
    # http listener block          httpl=azr[i]["httpListeners"

            icount=len(httpl)
            if icount > 0:
                for j in range(0,icount):
                    bname=azr[i]["httpListeners[j]["name"]
                    feipcn=azr[i]["httpListeners[j]["frontendIpConfiguration"]["id"].split("/")[10]]
                    fepn=azr[i]["httpListeners[j]["frontendPort"]["id"].split("/")[10]]  
                    bproto=azr[i]["httpListeners[j]["protocol"]
                    bhn=azr[i]["httpListeners[j]["hostName"]
                    bssl=azr[i]["httpListeners[j]["sslCertificate"]["id"].split("/")[10]]
                    rsni=azr[i]["httpListeners[j]["requireServerNameIndication"]                               

                    fr.write('http_listener {' + '"\n')
                    fr.write('\t name = "' +    bname + '"\n')
                    fr.write('\t frontend_ip_configuration_name = "' +    feipcn + '"\n')
                    fr.write('\t frontend_port_name = "' +    fepn + '"\n')
                    fr.write('\t protocol = "' +    bproto + '"\n')
                    if bhn" try :
                    fr.write('\t host_name = "' +    bhn + '"\n')
                
                    if bssl" try :
                    fr.write('\t ssl_certificate_name = "' +    bssl + '"\n')
                
                    if rsni" try :
                    fr.write('\t require_sni = "' +    rsni + '"\n')
                
                    fr.write('}\n')
                
            

    # proble block  probes=azr[i]["probes"

            icount=len(probes)
            if icount > 0 :
                for j in range(0,icount):
                    bname=azr[i]["probes[j]["name"]
                    bproto=azr[i]["probes[j]["protocol"]
                    bpath=azr[i]["probes[j]["path"]
                    bhost=azr[i]["probes[j]["host"]
                    bint=azr[i]["probes[j]["interval"]
                    btimo=azr[i]["probes[j]["timeout"]
                    bunth=azr[i]["probes[j]["unhealthyThreshold"]
                    bmsrv=azr[i]["probes[j]["minServers"]               
                    bmbod=azr[i]["probes[j]["match.body"]             
                    bmstat=azr[i]["probes[j]["match.statusCodes" 

                    fr.write('probe{' + '"\n')
                    fr.write('\t name = "' +    bname + '"\n')
                    fr.write('\t protocol = "' +    bproto + '"\n')
                    fr.write('\t path = "' +    bpath + '"\n')
                    fr.write('\t host = "' +    bhost + '"\n')
                    fr.write('\t interval = "' +    bint + '"\n')
                    fr.write('\t timeout = "' +    btimo + '"\n')
                    fr.write('\t unhealthy_threshold = "' +    bunth + '"\n')


                    if bmsrv" try :
                    fr.write('\t minimum_servers = "' +    bmsrv + '"\n')
                

                    fr.write('\t match {' + '"\n')
                    if bmbod" try :
                        if bmbod" = " :
                            fr.write('\t\t body = "' + '*' + '"\n')
                        else
                            fr.write('\t\t body = "' + bmbod + '"\n')
                    
                
                    fr.write('\t }\n')
                    
                    #if bmstat" try :
                    #fr.write('\t status_code = "' +    bmstat + '"\n')
                    #fi
                    

                    fr.write('}\n')
                
            

    # request routing rules    block rrrs=azr[i]["requestRoutingRules"

            icount=len(rrrs)
            if icount > 0 :
                for j in range(0,icount):
                    bname=azr[i]["requestRoutingRules[j]["name"]
                    btyp=azr[i]["requestRoutingRules[j]["ruleType"]
                    blin=azr[i]["requestRoutingRules[j]["httpListener"]["id"].split("/")[10]]
                    bapn=azr[i]["requestRoutingRules[j]["backendAddressPool"]["id"].split("/")[10]]
                    bhsn=azr[i]["requestRoutingRules[j]["backendHttpSettings"]["id"].split("/")[10]]

                    fr.write('request_routing_rule {' + '"\n')

                    fr.write('\t name = "' +    bname + '"\n')
                    fr.write('\t rule_type = "' +    btyp + '"\n')
                    fr.write('\t http_listener_name = "' +    blin + '"\n')
                    if bapn" try :
                        fr.write('\t backend_address_pool_name = "' +    bapn + '"\n')
                
                    if bhsn" try :
                        fr.write('\t backend_http_settings_name = "' +    bhsn + '"\n')
                
                    fr.write('\t }\n')
                
        


    # ssl_certificate block   sslcerts=azr[i]["sslCertificates"

            icount=len(sslcerts)
            if icount > 0 :
                for j in range(0,icount):
                    bname=azr[i]["sslCertificates[j]["name"]
                    bdata=azr[i]["sslCertificates[j]["publicCertData"]
                    bpw=azr[i]["sslCertificates[j]["password"]

                    if [ bname try :
                        fr.write('ssl_certificate {' + '"\n')
                        fr.write('\t name = "' +    bname + '"\n')

                        if bdata" try :
                        fr.write('\t data = "' +    bdata + '"\n')
                        else
                        fr.write('\t data = "' +    + '"\n')                
                    
                        
                        if bpw" try :
                        fr.write('\t password = "' +    bpw + '"\n')
                        else
                        fr.write('\t password = "' +    + '"\n')
                    
                        fr.write('\t }\n')
                
                
        

    # waf configuration block     wafc=azr[i]["webApplicationFirewallConfiguration"
    # - not an array like the other blocks 
    #
            fmode=azr[i]["webApplicationFirewallConfiguration.firewallMode"]
            if fmode" try :
                    rst=azr[i]["webApplicationFirewallConfiguration.ruleSetType"]
                    rsv=azr[i]["webApplicationFirewallConfiguration.ruleSetVersion"]
                    fen=azr[i]["webApplicationFirewallConfiguration.enabled"]
                    
                    fr.write('waf_configuration {' + '"\n')
                    fr.write('\trewall_mode = "' +    fmode + '"\n')
                    fr.write('\t rule_set_type = "' +    rst + '"\n')
                    fr.write('\t rule_set_version = "' +    rsv + '"\n')
                    fr.write('\t enabled = "' +    fen + '"\n')
                    fr.write('\t }\n')          
        

        
            fr.write('}\n')
            #

    
fi



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

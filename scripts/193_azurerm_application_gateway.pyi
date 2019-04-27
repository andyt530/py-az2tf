
azr=az network application-gateway list -g rgsource -o json
count= azr | | len(
if count > 0" :
    for i in range(0,count):       
        name=azr[i]["name"]
        rname= name.replace(".","-")
        rg=azr[i]["resourceGroup"].replace(".","-")    

        id=azr[i]["]["id"]
        loc=azr[i]["location"
        skun=azr[i]["sku.name"]
        skuc=azr[i]["sku.capacity"]
        skut=azr[i]["sku.tier"]
        
        
        # the blocks
        gwipc=azr[i]["gatewayIpConfigurations"
        feps=azr[i]["frontendPorts"
        fronts=azr[i]["frontendIpConfigurations"
        beap=azr[i]["backendAddressPools"
        bhttps=azr[i]["backendHttpSettingsCollection"
        httpl=azr[i]["httpListeners"
        probes=azr[i]["probes"
        rrrs=azr[i]["requestRoutingRules"
        urlpm=azr[i]["urlPathMaps"
        authcerts=azr[i]["au:ticationCertificates"
        sslcerts=azr[i]["sslCertificates"
        wafc=azr[i]["webApplicationFirewallConfiguration"
        
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location =  "loc" + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('sku {' sku + '"\n')
        fr.write('\t name = "' +  skun + '"\n')
        if [ skuc try :
            fr.write('\t capacity = "' +  skuc + '"\n')
        else
            fr.write('\t capacity = "'1"'  + '"\n')
       
        fr.write('\t tier = "' +  skut + '"\n')
        fr.write('}' sku + '"\n')
        
# gateway ip config block
        
        icount= gwipc | | len(
        if icount > 0" :
            for j in range(0,icount):
                gname=azr[i]["gatewayIpConfigurations[j]["name"]
                subrg=azr[i]["gatewayIpConfigurations[j]["subnet"]["id"].split[4].replace(".","-")
                subname=azr[i]["gatewayIpConfigurations[j]["subnet"]["id"].split[10].replace(".","-")
                fr.write('gateway_ip_configuration {' + '"\n')
                fr.write('\t name = "' +    gname + '"\n')
                if subname" try :
                    fr.write('\t subnet_id = "'\{'azurerm_subnet. + '__' + .id}'"' subrg subname + '"\n')
               
                fr.write('}\n')
            
       
        
# front end port
        icount= feps | | len(
        if icount > 0" :
            for j in range(0,icount):
                fname=azr[i]["frontendPorts[j]["name"]
                fport=azr[i]["frontendPorts[j]["port"]
                fr.write('frontend_port {' + '"\n')
                fr.write('\t name = "' +    fname + '"\n')
                fr.write('\t port = "' +    fport + '"\n')
                fr.write('}\n')
            
       
        
# front end ip config block
        icount= fronts | | len(
        if icount > 0" :
            for j in range(0,icount):
                
                fname=azr[i]["frontendIpConfigurations[j]["name"]
                priv=azr[i]["frontendIpConfigurations[j]["privateIpAddress"]
                
                pubrg=azr[i]["frontendIpConfigurations[j]["publicIpAddress"]["id"].split[4].replace(".","-")
                pubname=azr[i]["frontendIpConfigurations[j]["publicIpAddress"]["id"].split[8].replace(".","-")
                
                subrg=azr[i]["frontendIpConfigurations[j]["subnet"]["id"].split[4].replace(".","-")
                subname=azr[i]["frontendIpConfigurations[j]["subnet"]["id"].split[10].replace(".","-")
                privalloc=azr[i]["frontendIpConfigurations[j]["privateIpAllocationMethod"]
                
                fr.write('frontend_ip_configuration {' + '"\n')
                fr.write('\t name = "' +    fname + '"\n')
                if subname" try :
                    fr.write('\t subnet_id = "'\{'azurerm_subnet. + '__' + .id}'"' subrg subname + '"\n')
               
                if priv" try :
                    fr.write('\t private_ip_address = "' +    priv + '"\n')
               
                if privalloc" try :
                    fr.write('\t private_ip_address_allocation  = "' +    privalloc + '"\n')
               
                if pubname" try :
                    fr.write('\t public_ip_address_id = "'\{'azurerm_public_ip. + '__' + .id}'"' pubrg pubname + '"\n')
               
                
                fr.write('}\n')
                
            
       

# backend_address_pool          beap=azr[i]["backendAddressPools"

        icount= beap | | len(
        if icount > 0" :
            for j in range(0,icount):
                bname=azr[i]["backendAddressPools[j]["name"]
                fr.write('backend_address_pool {' + '"\n')
                fr.write('\t name = "' +    bname + '"\n')
                beaddr=azr[i]["backendAddressPools[j]["backendAddresses"          
                kcount= beaddr | | len(    
                if kcount > 0" :
                    for k in range(0,kcount):
                        beadip=azr[i]["backendAddressPools[j]["backendAddresses[k]["ipAddress"
                        beadfq=azr[i]["backendAddressPools[j]["backendAddresses[k]["fqdn"
                        if [ beadip try :
                            fr.write('\t ip_address =    "beadip" + '"\n')
                       
                        if [ beadip try :
                            fr.write('\t fqdns = ["' + ]["  "beadfq" + '"\n')
                       
                    
               

                fr.write('}\n')
            
       

# backend_http_settings
        icount= bhttps | | len(
        if icount > 0" :
            for j in range(0,icount):
                bname=azr[i]["backendHttpSettingsCollection[j]["name"]
                bport=azr[i]["backendHttpSettingsCollection[j]["port"]
                bproto=azr[i]["backendHttpSettingsCollection[j]["protocol"]
                bcook=azr[i]["backendHttpSettingsCollection[j]["cookieBasedAffinity"]
                btimo=azr[i]["backendHttpSettingsCollection[j]["requestTimeout"]
                pname=azr[i]["backendHttpSettingsCollection[j]["probe"]["id"].split[10]]
                acert=azr[i]["backendHttpSettingsCollection[j]["au:ticationCertificates[0]["]["id"].split[10]]

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

        icount= httpl | | len(
        if icount > 0" :
            for j in range(0,icount):
                bname=azr[i]["httpListeners[j]["name"]
                feipcn=azr[i]["httpListeners[j]["frontendIpConfiguration"]["id"].split[10]]
                fepn=azr[i]["httpListeners[j]["frontendPort"]["id"].split[10]]  
                bproto=azr[i]["httpListeners[j]["protocol"]
                bhn=azr[i]["httpListeners[j]["hostName"]
                bssl=azr[i]["httpListeners[j]["sslCertificate"]["id"].split[10]]
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

        icount= probes | | len(
        if icount > 0" :
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
                        fr.write('\t\t body = "'*"'  + '"\n')
                    else
                        fr.write('\t\t body = "' +    bmbod + '"\n')
                   
               
                fr.write('\t }\n')
                
                #if bmstat" try :
                #fr.write('\t status_code = "' +    bmstat + '"\n')
                #fi
                

                fr.write('}\n')
            
         

# request routing rules    block rrrs=azr[i]["requestRoutingRules"

        icount= rrrs | | len(
        if icount > 0" :
            for j in range(0,icount):
                bname=azr[i]["requestRoutingRules[j]["name"]
                btyp=azr[i]["requestRoutingRules[j]["ruleType"]
                blin=azr[i]["requestRoutingRules[j]["httpListener"]["id"].split[10]]
                bapn=azr[i]["requestRoutingRules[j]["backendAddressPool"]["id"].split[10]]
                bhsn=azr[i]["requestRoutingRules[j]["backendHttpSettings"]["id"].split[10]]

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

        icount= rrrs | | len(
        if icount > 0" :
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

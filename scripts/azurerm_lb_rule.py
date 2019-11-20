# azurerm_lb_rule
def azurerm_lb_rule(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_lb_rule"
    tcode="190-"
    
    if crf in tfp:
    # REST or cli
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/loadBalancers"
        params = {'api-version': '2019-02-01'}
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
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
 
            beap=azr[i]["properties"]["loadBalancingRules"]   
            jcount=len(beap)
            
            for j in range(0,jcount):
                
                name=azr[i]["properties"]["loadBalancingRules"][j]["name"]
                rname= name.replace(".","-")
                id=azr[i]["properties"]["loadBalancingRules"][j] ["id"]
    
                lbrg=azr[i]["id"].split("/")[4].replace(".","-").lower()
                lbname=azr[i]["id"].split("/")[8].replace(".","-")
                prefix=tfp+"."+rg+ '__' + lbname+'__'+rname
                #print prefix
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)
                fr.write('resource ' + tfp + ' ' + rg + '__' + lbname + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                fr.write('\t resource_group_name = "'+ rgs + '"\n')


     
                fep=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["frontendPort"]
                bep=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["backendPort"]
                proto=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["protocol"]
                feipc=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["frontendIPConfiguration"]["id"].split("/")[10]
                efip=str(azr[i]["properties"]["loadBalancingRules"][j]["properties"]["enableFloatingIP"]).lower()
                ld=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["loadDistribution"]
                itm=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["idleTimeoutInMinutes"]
                if lbrg[0].isdigit(): lbrg="rg_"+lbrg 
                fr.write('\t\t loadbalancer_id = "${azurerm_lb.' + lbrg + '__' + lbname + '.id}" \n')
                fr.write('\t\t frontend_ip_configuration_name = "' + feipc + '"\n')
                fr.write('\t\t protocol = "' + proto + '"\n')   
                fr.write('\t\t frontend_port = "' + str(fep) + '"\n')
                fr.write('\t\t backend_port = "' + str(bep) + '"\n')
                
                try:
                    beadprg=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["backendAddressPool"]["id"].split("/")[4].replace(".","-").lower()
                    beadpid=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["backendAddressPool"]["id"].split("/")[10].replace(".","-")
                    if beadprg[0].isdigit(): beadprg="rg_"+beadprg
                    fr.write('\t\t backend_address_pool_id = "${azurerm_lb_backend_address_pool.' + beadprg + '__' + lbname + '__' + beadpid + '.id}"\n')
                except KeyError:
                    pass
                
                try:
                    prg=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["probe"]["id"].split("/")[4].replace(".","-").lower()
                    pid=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["probe"]["id"].split("/")[10].replace(".","-")
                    if prg[0].isdigit(): prg="rg_"+prg 
                    fr.write('\t\t probe_id = "${azurerm_lb_probe.' + prg + '__' + lbname + '__' + pid + '.id}" \n')
                except KeyError:
                    pass
                fr.write('\t\t enable_floating_ip = ' + efip + '\n')
                fr.write('\t\t idle_timeout_in_minutes = "' + str(itm) + '"\n')
                fr.write('\t\t load_distribution = "' + ld + '"\n')


                fr.write('}\n') 
                fr.close()   # close .tf file

                if cde:
                    with open(rfilename) as f: 
                        print (f.read())

                tfrm.write('terraform state rm '+tfp+'.'+rg+ '__' + lbname+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+ '__' + lbname+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub

# azurerm_lb_rule
def azurerm_lb_rule(crf,cde,crg,headers,requests,sub,json,az2tfmess,azr):
    tfp="azurerm_lb_rule"
    tcode="190-"
    
    if crf in tfp:
    # REST or cli

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
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-")

            if crg is not None:
                if rg.lower() != crg.lower():
                    continue  # back to for
 
            beap=azr[i]["properties"]["loadBalancingRules"]   
            jcount=len(beap)

            for j in range(0,jcount):
                
                name=azr[i]["properties"]["loadBalancingRules"][j]["name"]
                rname= name.replace(".","-")
                id=azr[i]["properties"]["loadBalancingRules"][j] ["id"]
    
                prefix=tfp+"."+rg+'__'+rname
                #print prefix
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)
                fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
  
                fr.write('\t resource_group_name = "'+ rg + '"\n')


                lbrg=azr[i]["id"].split("/")[4].replace(".","-")
                lbname=azr[i]["id"].split("/")[8].replace(".","-")




     
                fep=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["frontendPort"]
                bep=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["backendPort"]
                proto=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["protocol"]
                feipc=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["frontendIpConfiguration"]["id"]
                efip=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["enableFloatingIp"]
                ld=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["loadDistribution"]
                itm=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["idleTimeoutInMinutes"]

                prg=azr[i]["properties"]["loadBalancingRules"][j]["probe"]["id"].split("/")[4].replace(".","-")
                pid=azr[i]["properties"]["loadBalancingRules"][j]["probe"]["id"].split("/")[10].replace(".","-")
                beadprg=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["backendAddressPool"]["id"].split("/")[4].replace(".","-")
                beadpid=azr[i]["properties"]["loadBalancingRules"][j]["properties"]["backendAddressPool"]["id"].split("/")[10].replace(".","-")

             
                fr.write('resource "' + tfp + ' ' + rg + '__' + lbname + '__' + rname + ' {  "\n')
                fr.write('\t\t name = "' + name + '"\n')
                fr.write('\t\t loadbalancer_id = "${azurerm_lb.' + lbrg + '__' + lbname + '.id}" \n')
                fr.write('\t\t frontend_ip_configuration_name = "' + feipc + '"\n')
                fr.write('\t\t protocol = "' + proto + '"\n')   
                fr.write('\t\t frontend_port = "' + fep + '"\n')
                fr.write('\t\t backend_port = "' + bep + '"\n')
                
                fr.write('\t\t backend_address_pool_id = "${azurerm_lb_backend_address_pool.' + beadprg + '__' + lbname + '__' + beadpid + '.id} \n')
                fr.write('\t\t probe_id = "${azurerm_lb_probe.' + prg + '__' + lbname + '__' + pid + '.id}" \n')
                
                fr.write('\t\t enable_floating_ip = "' + efip + '"\n')
                fr.write('\t\t idle_timeout_in_minutes = "' + itm + '"\n')
                fr.write('\t\t load_distribution = "' + ld + '"\n')


             


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

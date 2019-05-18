# azurerm_lb_nat_rule
def azurerm_lb_nat_rule(crf,cde,crg,headers,requests,sub,json,az2tfmess,azr):
    tfp="azurerm_lb_nat_rule"
    tcode="150-"
    if crf in tfp:
    # REST or cli
        #if cde:
            #print(json.dumps(azr, indent=4, separators=(',', ': ')))

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print "# " + tfp,
        count=len(azr)
        print count
        for i in range(0, count):
            try:
                beap=azr[i]["properties"]["inboundNatRules"] 
                id=azr[i]["id"]
                rg=id.split("/")[4].replace(".","-").lower()
                if crg is not None:
                    if rg.lower() != crg.lower():
                        continue  # back to for
   
                jcount=len(beap)   
                        
                for j in range(0,jcount):
                    
                    name=azr[i]["properties"]["inboundNatRules"][j]["name"]
                    rname=name.replace(".","-")

                    id=azr[i]["properties"]["inboundNatRules"][j]["id"]
                    rg=id.split("/")[4].replace(".","-").lower()
                    if crg is not None:
                        if rg.lower() != crg.lower():
                            continue  # back to for

                    prefix=tfp+"."+rg+'__'+rname
                    #print prefix
                    rfilename=prefix+".tf"
                    fr=open(rfilename, 'w')
                    fr.write(az2tfmess)
                       
                    lbrg=azr[i]["id"].split("/")[4].replace(".","-").lower()
                    lbname=azr[i]["id"].split("/")[8].replace(".","-")
                    
                    fep=azr[i]["properties"]["inboundNatRules"][j]["properties"]["frontendPort"]
                    bep=azr[i]["properties"]["inboundNatRules"][j]["properties"]["backendPort"]
                    proto=azr[i]["properties"]["inboundNatRules"][j]["properties"]["protocol"]
                    feipc=azr[i]["properties"]["inboundNatRules"][j]["properties"]["frontendIPConfiguration"]["id"].split("/")[10]
                    
                    fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')   

                    fr.write('\t\t name = "' +    name + '"\n')
                    fr.write('\t\t resource_group_name = "' +  rg + '"\n')
                    fr.write('\t\t loadbalancer_id = "${azurerm_lb.' + lbrg + '__' + lbname + '.id}" \n')
                    fr.write('\t\t frontend_ip_configuration_name = "' +    feipc + '"\n')
                    fr.write('\t\t protocol = "' + proto + '"\n')
                    fr.write('\t\t backend_port = "' + str(bep) + '"\n')
                    fr.write('\t\t frontend_port = "' + str(fep) + '"\n')
                    try:
                        enfip=azr[i]["properties"]["inboundNatRules"][j]["properties"]["enableFloatingIP"]
                        fr.write('\t\t enable_floating_ip = "' + str(enfip) + '"\n')
                    except KeyError:
                        pass

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

                # end for j loop
            except KeyError:
                pass        
        # end for i

        tfrm.close()
        tfim.close()

    #end stub

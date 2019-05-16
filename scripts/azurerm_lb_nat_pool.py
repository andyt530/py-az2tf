# azurerm_lb_nat_pool
def azurerm_lb_nat_pool(crf,cde,crg,headers,requests,sub,json,az2tfmess,azr):
    tfp="azurerm_lb_nat_pool"
    tcode="160-"
    print tfp,
    if crf in tfp:
    # REST or cli

        if cde:
            print(json.dumps(azr, indent=4, separators=(',', ': ')))

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        
        count=len(azr)
        print count
        for i in range(0, count):
         
            name=azr[i]["name"]
         
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-")

            if crg is not None:
                if rg.lower() != crg.lower():
                    continue  # back to for
            


    ###############
    # specific code start
    ###############

    
            beap=azr[i]["properties"]["inboundNatPools"]
            jcount= len(beap)
            if cde:
                print "********** beap ***********"
                print(json.dumps(beap, indent=4, separators=(',', ': ')))  
                print "j=" +str(jcount)
            
            
            for j in range(0,jcount):
                
                name=azr[i]["properties"]["inboundNatPools"][j]["name"]
                rname=name.replace(".","-")
                if cde:
                    print "j=" +str(j)
                    print "********** beap ***********"
                    print(json.dumps(beap, indent=4, separators=(',', ': ')))
                id=azr[i]["properties"]["inboundNatPools"][j]["id"]
                rg=id.split("/")[4].replace(".","-")
                rgs=id.split("/")[4]
                if crg is not None:
                    if rg.lower() != crg.lower():
                        continue  # back to for

                prefix=tfp+"."+rg+'__'+rname
                print prefix
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)

                fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                fr.write('\t resource_group_name = "'+ rgs + '"\n')

                proto=azr[i]["properties"]["inboundNatPools"][j]["properties"]["protocol"]
                bep=azr[i]["properties"]["inboundNatPools"][j]["properties"]["backendPort"]
                feipc=azr[i]["properties"]["inboundNatPools"][j]["properties"]["frontendConfiguration"]["id"].split("/")[10]
                try:
                    feps=azr[i]["properties"]["inboundNatPools"][j]["properties"]["frontendPortStart"]
                except:
                    feps=bep
                try:
                    fepe=azr[i]["properties"]["inboundNatPools"][j]["properties"]["frontendPortEnd"]
                except:
                    fepe=bep
                
                lbrg=azr[i]["id"].split("/")[4].replace(".","-")
                lbname=azr[i]["id"].split("/")[8].replace(".","-")
                
                fr.write('\t\t loadbalancer_id = "${azurerm_lb.' + lbrg + '__' + lbname + '.id}"\n')
                fr.write('\t\t protocol = "' +    proto + '"\n')
                fr.write('\t\t frontend_port_start = "' +    feps + '"\n')
                fr.write('\t\t frontend_port_end = "' +    fepe + '"\n')
                fr.write('\t\t backend_port = "' +    bep + '"\n')
                fr.write('\t\t frontend_ip_configuration_name = "' +    feipc + '"\n')


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

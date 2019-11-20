# azurerm_lb_nat_pool
def azurerm_lb_nat_pool(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_lb_nat_pool"
    tcode="160-"

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
    
            beap=azr[i]["properties"]["inboundNatPools"]
            jcount= len(beap)
           
            if cde:
                print(json.dumps(beap, indent=4, separators=(',', ': ')))  
      
            
            
            for j in range(0,jcount):
                
                name=azr[i]["properties"]["inboundNatPools"][j]["name"]
                rname=name.replace(".","-")
                if cde:
                    print(json.dumps(beap, indent=4, separators=(',', ': ')))
                id=azr[i]["properties"]["inboundNatPools"][j]["id"]
                rg=id.split("/")[4].replace(".","-").lower()
                rgs=id.split("/")[4]
                if crg is not None:
                    if rgs.lower() != crg.lower():
                        continue  # back to for

                prefix=tfp+"."+rg+'__'+rname
                
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)

                fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                fr.write('\t resource_group_name = "'+ rgs + '"\n')

                proto=azr[i]["properties"]["inboundNatPools"][j]["properties"]["protocol"]
                bep=azr[i]["properties"]["inboundNatPools"][j]["properties"]["backendPort"]

                try:
                    feps=azr[i]["properties"]["inboundNatPools"][j]["properties"]["frontendPortStart"]
                except:
                    feps=bep
                try:
                    fepe=azr[i]["properties"]["inboundNatPools"][j]["properties"]["frontendPortEnd"]
                except:
                    fepe=bep
                
                lbrg=azr[i]["id"].split("/")[4].replace(".","-").lower()
                lbname=azr[i]["id"].split("/")[8].replace(".","-")
                if lbrg[0].isdigit(): lbrg="rg_"+lbrg 
                fr.write('\t\t loadbalancer_id = "${azurerm_lb.' + lbrg + '__' + lbname + '.id}"\n')
                fr.write('\t\t protocol = "' +    proto + '"\n')
                fr.write('\t\t frontend_port_start = "' +    str(feps) + '"\n')
                fr.write('\t\t frontend_port_end = "' +    str(fepe) + '"\n')
                fr.write('\t\t backend_port = "' +    str(bep) + '"\n')
                try:
                    feipc=azr[i]["properties"]["inboundNatPools"][j]["properties"]["frontendConfiguration"]["id"].split("/")[10]
                    fr.write('\t\t frontend_ip_configuration_name = "' +    feipc + '"\n')
                except KeyError:
                    fr.write('\t\t frontend_ip_configuration_name = "' +  "default" + '"\n')
                    pass


        # no tags block       


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

# azurerm_lb_backend_address_pool
def azurerm_lb_backend_address_pool(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_lb_backend_address_pool"
    tcode="170-"
    
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
            lbname=name
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            beap=azr[i]["properties"]["backendAddressPools"]       
            jcount= len(beap)
            
            for j in range(0,jcount):
                
                name=azr[i]["properties"]["backendAddressPools"][j]["name"]
                rname= name.replace(".","-")
                id=azr[i]["properties"]["backendAddressPools"][j]["id"]
                rg=id.split("/")[4].replace(".","-").lower()

                prefix=tfp+"."+rg+'__'+lbname+'__'+rname
                #print prefix
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)

                fr.write('resource ' + tfp + ' ' + rg + '__' +lbname+'__'+ rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                fr.write('\t resource_group_name = "'+ rgs + '"\n')

                try:
                    #lbrg=azr[i]["id"].split("/")[4].replace(".","-").lower()
                    #lbname=azr[i]["id"].split("/")[8].replace(".","-")   
                    lbrg=id.split("/")[4].replace(".","-").lower()
                    lbname=id.split("/")[8].replace(".","-")    
                    if lbrg[0].isdigit(): lbrg="rg_"+lbrg      
                    fr.write('\t\t loadbalancer_id = "${azurerm_lb.' + lbrg + '__' + lbname + '.id}" \n')    
                except KeyError:
                    pass
                
        # should be more stuff in here ?


                fr.write('}\n') 
                fr.close()   # close .tf file

                if cde:
                    with open(rfilename) as f: 
                        print (f.read())

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+lbname+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+lbname+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm)  

            # end for j loop
        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub

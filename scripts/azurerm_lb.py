# azurerm_lb
def azurerm_lb(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_lb"
    tcode="140-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Load Balancers"
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
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            sku=azr[i]["sku"]["name"]
            fronts=azr[i]["properties"]["frontendIPConfigurations"]
        
            fr.write('\t sku = "' +  sku + '"\n')
           
            jcount=len(fronts)
       
   
            for j in range(0,jcount):
                    
                fname=azr[i]["properties"]["frontendIPConfigurations"][j]["name"]             
                fr.write('\t frontend_ip_configuration {' + '\n')
                fr.write('\t\t name = "' +    fname + '"\n')
                try:
                    subrg=azr[i]["properties"]["frontendIPConfigurations"][j]["subnet"]["id"].split("/")[4].replace(".","-").lower()
                    subname=azr[i]["properties"]["frontendIPConfigurations"][j]["subnet"]["id"].split("/")[10].replace(".","-")
                    if subrg[0].isdigit(): subrg="rg_"+subrg
                    fr.write('\t\t subnet_id = "${azurerm_subnet.' + subrg + '__' + subname +'.id}"\n')
                except KeyError:
                    pass
               
                try:
                    priv=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["privateIPAddress"]
                    fr.write('\t\t private_ip_address = "' +    priv + '"\n')
                except KeyError:
                    pass         
                    privalloc=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["privateIPAllocationMethod"]
                    fr.write('\t\t private_ip_address_allocation  = "' + privalloc + '"\n')
                except KeyError:
                    pass
                try:
                    pubrg=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["publicAddress"]["id"].split("/")[4].replace(".","-").lower()
                    pubname=azr[i]["properties"]["frontendIPConfigurations"][j]["properties"]["publicAddress"]["id"].split("/")[8].replace(".","-")
                    if pubrg[0].isdigit(): pubrg="rg_"+pubrg
                    fr.write('\t\t public_ip_address_id = "${azurerm_public_ip.' + pubrg + '__' + pubname + '.id}"\n')
                except KeyError:
                    pass

                fr.write('\t }\n')
            # end j    

    ###############
    # specific code end
    ###############

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

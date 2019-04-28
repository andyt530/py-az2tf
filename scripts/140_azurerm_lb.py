# azurerm_lb
def azurerm_lb(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_lb"
    tcode="140-"
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

    ###############
    # specific code start
    ###############



azr=az network lb list -g rgsource -o json
count= azr | | len(
if count > 0" :
    for i in range(0,count):
       
        name=azr[i]["name"]
        rname= name.replace(".","-")
        rg=azr[i]["resourceGroup"].replace(".","-")

        id=azr[i]["]["id"]
        loc=azr[i]["location"
        sku=azr[i]["sku.name"]
        fronts=azr[i]["frontendIpConfigurations"
        

        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location =  "loc" + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t sku = "' +  sku + '"\n')
           
        icount= fronts | | len(
       
        if icount > 0" :
            for j in range(0,icount):
                    
                fname=azr[i]["frontendIpConfigurations[j]["name"]
                priv=azr[i]["frontendIpConfigurations[j]["privateIpAddress"]

                pubrg=azr[i]["frontendIpConfigurations[j]["publicIpAddress"]["id"].split("/")[4].replace(".","-")
                pubname=azr[i]["frontendIpConfigurations[j]["publicIpAddress"]["id"].split("/")[8].replace(".","-")
                
                subrg=azr[i]["frontendIpConfigurations[j]["subnet"]["id"].split("/")[4].replace(".","-")
                subname=azr[i]["frontendIpConfigurations[j]["subnet"]["id"].split("/")[10].replace(".","-")
                privalloc=azr[i]["frontendIpConfigurations[j]["privateIpAllocationMethod"]
                
                fr.write('\t frontend_ip_configuration {' + '"\n')
                fr.write('\t\t name = "' +    fname + '"\n')
                if subname" try :
                    fr.write('\t\t subnet_id = "'\{'azurerm_subnet. + '__' + .id}'"' subrg subname + '"\n')
               
                if priv" try :
                    fr.write('\t\t private_ip_address = "' +    priv + '"\n')
                          
                if privalloc" try :
                    fr.write('\t\t private_ip_address_allocation  = "' +    privalloc + '"\n')
               
                if pubname" try :
                    fr.write('\t\t public_ip_address_id = "'\{'azurerm_public_ip. + '__' + .id}'"' pubrg pubname + '"\n')
               

                fr.write('\t }\n')
                
            
       
        
        
        fr.write('}\n')
        #
 
    
fi

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

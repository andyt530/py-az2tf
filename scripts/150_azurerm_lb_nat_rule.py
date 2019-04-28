# azurerm_lb_nat_rule
def azurerm_lb_nat_rule(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_lb_nat_rule"
    tcode="150-"
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
        beap=azr[i]["inboundNatRules"

      
        
        icount= beap | | len(
        if icount > 0" :
            for j in range(0,icount):
                
                name=azr[i]["inboundNatRules[j]["name"].split("/")[10]]
                rname= name.replace(".","-")

                id=azr[i]["inboundNatRules[j]["]["id"]
                rg=azr[i]["inboundNatRules[j]["resourceGroup"].replace(".","-")
                
                lbrg=azr[i]["]["id"].split("/")[4].replace(".","-")
                lbname=azr[i]["]["id"].split("/")[8].replace(".","-")

                fep=azr[i]["inboundNatRules[j]["frontendPort"]
                bep=azr[i]["inboundNatRules[j]["backendPort"]
                proto=azr[i]["inboundNatRules[j]["protocol"]
                feipc=azr[i]["inboundNatRules[j]["frontendIpConfiguration"]["id"].split("/")[10]]
                enfip=azr[i]["inboundNatRules[j]["enableFloatingIp"].split("/")[10]]

                
                fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
                fr.write('\t\t name = "' +    name + '"\n')
                fr.write('\t\t resource_group_name = "' +    rgsource + '"\n')
                fr.write('\t\t loadbalancer_id = "'\{'azurerm_lb. + '__' + .id}'"' lbrg lbname + '"\n')
                fr.write('\t\t frontend_ip_configuration_name = "' +    feipc + '"\n')
                fr.write('\t\t protocol = "' +    proto + '"\n')
                fr.write('\t\t backend_port = "' +    bep + '"\n')
                fr.write('\t\t frontend_port = "' +    fep + '"\n')
                if enfip" try :
                fr.write('\t\t enable_floating_ip = "' +    enfip + '"\n')
               
                fr.write('}\n')
        #
 

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

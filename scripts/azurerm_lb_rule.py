# azurerm_lb_rule
def azurerm_lb_rule(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_lb_rule"
    tcode="190-"
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
        beap=azr[i]["loadBalancingRules"
        rg=azr[i]["resourceGroup"].replace(".","-")
        lbrg=azr[i]["]["id"].split("/")[4].replace(".","-")
        lbname=azr[i]["]["id"].split("/")[8].replace(".","-")
        
        icount= beap | | len(
        if icount > 0" :
            for j in range(0,icount):
                
                name=azr[i]["loadBalancingRules[j]["name"].split("/")[10]]
                rname= name.replace(".","-")
                id=azr[i]["loadBalancingRules[j]["]["id"]
                rrg=azr[i]["loadBalancingRules[j]["resourceGroup"].replace(".","-")
                fep=azr[i]["loadBalancingRules[j]["frontendPort"]
                bep=azr[i]["loadBalancingRules[j]["backendPort"]
                proto=azr[i]["loadBalancingRules[j]["protocol"]
                feipc=azr[i]["loadBalancingRules[j]["frontendIpConfiguration"]["id"].split("/")[10]]
                efip=azr[i]["loadBalancingRules[j]["enableFloatingIp"]
                ld=azr[i]["loadBalancingRules[j]["loadDistribution"]
                itm=azr[i]["loadBalancingRules[j]["idleTimeoutInMinutes"]

                prg=azr[i]["loadBalancingRules[j]["probe"]["id"].split("/")[4].replace(".","-")
                pid=azr[i]["loadBalancingRules[j]["probe"]["id"].split("/")[10].replace(".","-")
                beadprg=azr[i]["loadBalancingRules[j]["backendAddressPool"]["id"].split("/")[4].replace(".","-")
                beadpid=azr[i]["loadBalancingRules[j]["backendAddressPool"]["id"].split("/")[10].replace(".","-")

             
                fr.write('resource "' +  "' + '__' +  + '__' + "' {' tfp rg lbname rname + '"\n')
                fr.write('\t\t name = "' +    name + '"\n')
                #fr.write('\t\t resource_group_name = "' +    rrg + '"\n')
                fr.write('\t\t resource_group_name = "' +    rgsource + '"\n')
                fr.write('\t\t loadbalancer_id = "'\{'azurerm_lb. + '__' + .id}'"' lbrg lbname + '"\n')
                fr.write('\t\t frontend_ip_configuration_name = "' +    feipc + '"\n')
                fr.write('\t\t protocol = "' +    proto + '"\n')   
                fr.write('\t\t frontend_port = "' +    fep + '"\n')
                fr.write('\t\t backend_port = "' +    bep + '"\n')
                
                fr.write('\t\t backend_address_pool_id = "'\{'azurerm_lb_backend_address_pool. + '__' +  + '__' + .id}'"' beadprg lbname beadpid + '"\n')
                fr.write('\t\t probe_id = "'\{'azurerm_lb_probe. + '__' +  + '__' + .id}'"' prg lbname pid + '"\n')
                
                fr.write('\t\t enable_floating_ip = "' +    efip + '"\n')
                fr.write('\t\t idle_timeout_in_minutes = "' +    itm + '"\n')
                fr.write('\t\t load_distribution = "' +    ld + '"\n')


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

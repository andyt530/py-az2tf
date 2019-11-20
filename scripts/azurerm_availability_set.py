def azurerm_availability_set(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #  020 Avail Sets
    tfp="azurerm_availability_set"
    azr=""
    if crf in tfp:

        # print "REST Avail Set"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Compute/availabilitySets"
        params = {'api-version': '2018-10-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf="020-"+tfp+"-staterm.sh"
        tfimf="020-"+tfp+"-stateimp.sh"
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
            fd=str(azr[i]["properties"]["platformFaultDomainCount"])
            ud=str(azr[i]["properties"]["platformUpdateDomainCount"])
            #avm=azr[i]["virtualMachines"]
            skuname=azr[i]["sku"]["name"]
            rmtype="false"
            if "Aligned" in skuname:
                #print "skuname is true"
                rmtype="true"

            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rgl=rg.lower()
            rname=name.replace(".","-").lower()
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write("")
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')   
            fr.write('\t platform_fault_domain_count = "' + fd + '"\n')
            fr.write('\t platform_update_domain_count = "' + ud + '"\n')
            fr.write('\t managed = "' + rmtype + '"\n')

        # tags block
            
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                    #print tval
                #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
                fr.write('}\n')
            except KeyError:
                pass
            
            fr.write('}\n') 
            fr.close()   # close .tf file

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')
                
            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end Avail Set
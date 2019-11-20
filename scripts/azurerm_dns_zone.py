# azurerm_dns_zone
def azurerm_dns_zone(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_dns_zone"
    tcode="131-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/dnszones"
        #params = {'api-version': '2016-04-01'}
        params = {'api-version': '2018-05-01'}       
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
            #loc=azr[i]["location"]
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
            #fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

    ###############
    # specific code start
    ###############

            #azr=az network dns zone list -g rgsource -o json
 
            zt=azr[i]["properties"]["zoneType"]
            try:
                resvn=azr[i]["properties"]["resolutionVirtualNetworks"]
                kcount=len(resvn)
                for k in range(0,kcount):
                    vid=resvn[k]["id"]
                    fr.write('\t resolution_virtual_network_ids = ["' + vid  + '"]\n')
            except KeyError:
                pass
            try:
                regvn=azr[i]["properties"]["registrationVirtualNetworks"] 
                kcount=len(regvn)
                for k in range(0,kcount):
                    vid=regvn[k]["id"]
                    fr.write('\t registration_virtual_network_ids = "' +  regvn + '"\n') 
            except KeyError:
                pass  

            fr.write('\t zone_type = "' +  zt + '"\n')
      

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

def azurerm_storage_account(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    #  110 storage account
    tfp="azurerm_storage_account"
    azr=""
    if crf in tfp:
    # REST or cli
        print "REST Managed Disk"
        url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Storage/storageAccounts"
        params = {'api-version': '2017-10-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]
        if cde:
            print(json.dumps(azr, indent=4, separators=(',', ': ')))

        tfrmf="110-"+tfp+"-staterm.sh"
        tfimf="110-"+tfp+"-stateimp.sh"
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
            fr.write("")
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rg + '"\n')

            satier=azr[i]["sku"]["tier"]
            sakind=azr[i]["kind"]
            
            sartype=azr[i]["sku"]["name"].split("_")[1]
            print sartype
            saencrypt=str(azr[i]["properties"]["encryption"]["services"]["blob"]["enabled"])
            fiencrypt=str(azr[i]["properties"]["encryption"]["services"]["file"]["enabled"])
            sahttps=str(azr[i]["properties"]["supportsHttpsTrafficOnly"])
            #nrs=azr[i]["properties"]["networkAcls"]
            saencs=azr[i]["properties"]["encryption"]["keySource"]
            
            fr.write('\t account_tier = "' + satier + '"\n')
            fr.write('\t account_kind = "' + sakind + '"\n')
            fr.write('\t account_replication_type = "' +  sartype + '"\n')
            fr.write('\t enable_blob_encryption = "' +  saencrypt + '"\n')
            fr.write('\t enable_file_encryption = "' +  fiencrypt + '"\n')
            fr.write('\t enable_https_traffic_only = "' +  sahttps + '"\n')
            fr.write('\t account_encryption_source = "' +  saencs + '"\n')
            
            try:
                byp=azr[i]["properties"]["networkAcls"]["bypass"]

                ipr=azr[i]["properties"]["networkAcls"]["ipRules"]
                vnr=azr[i]["properties"]["networkAcls"]["virtualNetworkRules"]
                
                icount=len(ipr)
                vcount=len(vnr)
            
                # if the only network rule is AzureServices, dont need a network_rules block
                if "AzureServices" not in byp or icount > 0 or vcount > 0:
                    fr.write('\t network_rules { \n')
                    fr.write('\t\t bypass = ["' +  byp + '"]\n')
                    
                    if icount > 0:
                        for ic in range(0, icount): 
                            ipa=ipr[ic]["value"]
                            fr.write('\t\t ip_rules = ["' + ipa + '"]\n')
                    if vcount > 0:
                        for vc in range(0,vcount):
                            vnsid=vnr[vc]["id"]
                            fr.write('\t\t virtual_network_subnet_ids = ["' + vnsid + '"]\n')
                    fr.write('}\n')
                # end if

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

        # end for i loop

        tfrm.close()
        tfim.close()
    #end storage account
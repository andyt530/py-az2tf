import ast
def azurerm_storage_account(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #  110 storage account
    
    tfp="azurerm_storage_account"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST Storage Acc"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Storage/storageAccounts"
        params = {'api-version': '2019-04-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf="110-"+tfp+"-staterm.sh"
        tfimf="110-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ('# '+tfp,)
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
            if cde: print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write("")
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            satier=azr[i]["sku"]["tier"]
            sakind=azr[i]["kind"]
            
            sartype=azr[i]["sku"]["name"].split("_")[1]
            saencrypt=str(azr[i]["properties"]["encryption"]["services"]["blob"]["enabled"]).lower()
            fiencrypt=str(azr[i]["properties"]["encryption"]["services"]["file"]["enabled"]).lower()
            sahttps=str(azr[i]["properties"]["supportsHttpsTrafficOnly"]).lower()
            #nrs=azr[i]["properties"]["networkAcls"]
            saencs=azr[i]["properties"]["encryption"]["keySource"]
            
            fr.write('\t account_tier = "' + satier + '"\n')
            fr.write('\t account_kind = "' + sakind + '"\n')
            fr.write('\t account_replication_type = "' +  sartype + '"\n')
            fr.write('\t enable_blob_encryption = ' +  saencrypt + '\n')
            fr.write('\t enable_file_encryption = ' +  fiencrypt + '\n')
            fr.write('\t enable_https_traffic_only = ' +  sahttps + '\n')
            fr.write('\t account_encryption_source = "' +  saencs + '"\n')
            #fr.write('\t enable_advanced_threat_protection = ' +  'false' + '\n')

            try:
                ishns=str(azr[i]["properties"]["isHnsEnabled"]).lower()
                fr.write('\t is_hns_enabled = ' + ishns + '\n')
            except KeyError:
                pass   


            try:        
                byp=str(ast.literal_eval(json.dumps(azr[i]["properties"]["networkAcls"]["bypass"])))
                byp=byp.replace("'",'"')
                byp=byp.replace(", ",'", "')
                dfa=azr[i]["properties"]["networkAcls"]["defaultAction"]
                ipr=azr[i]["properties"]["networkAcls"]["ipRules"]
                #print(json.dumps(ipr, indent=4, separators=(',', ': ')))


                vnr=azr[i]["properties"]["networkAcls"]["virtualNetworkRules"]
                
                icount=len(ipr)
                vcount=len(vnr)
            
                # if off skip
                if "None" not in byp and "Allow" not in dfa :
                # if the only network rule is AzureServices, dont need a network_rules block
                    if "AzureServices" not in byp or icount > 0 or vcount > 0:
                        fr.write('\t network_rules { \n')
                        fr.write('\t\t default_action = "' +  dfa + '"\n')
                        fr.write('\t\t bypass = ["' +  byp + '"]\n')
                        
                        if icount > 0:
                            fr.write('\t\t ip_rules = [')
                            for ic in range(0, icount): 
                                ipa=ipr[ic]["value"]
                                fr.write('"' + ipa + '",')
                            fr.write(']\n')
                        if vcount > 0:
                            fr.write('\t\t virtual_network_subnet_ids = [')
                            for vc in range(0,vcount):
                                vnsid=vnr[vc]["id"]
                                fr.write('\t\t"' + vnsid + '",')
                            fr.write(']\n')
                        fr.write('}\n')
                    # end if
                # end if

            except KeyError:
                pass            

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
    #end storage account
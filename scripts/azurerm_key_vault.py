def azurerm_key_vault(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    #############
    #  090 key vault
    
    tfp="azurerm_key_vault"
    azr=""
    if crf in tfp:
        # REST or cli

        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.KeyVault/vaults"
        params = {'api-version': '2016-10-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf="090-"+tfp+"-staterm.sh"
        tfimf="090-"+tfp+"-stateimp.sh"
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
            fr.write("")
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            sku=azr[i]["properties"]["sku"]["name"]
            if sku == "Premium" : sku="premium" 
            if sku == "Standard" : sku="standard" 
    
              
            fr.write('\t sku_name="' + sku + '"\n')
          

            ten=azr[i]["properties"]["tenantId"]     
            fr.write('\t tenant_id="' + ten + '"\n')


            try:
                #netacls=azr[i]["properties"]["networkAcls"]
                netacldf=azr[i]["properties"]["networkAcls"]["defaultAction"]
                netaclby=azr[i]["properties"]["networkAcls"]["bypass"]
                netaclipr=azr[i]["properties"]["networkAcls"]["ipRules"]
                vnr=azr[i]["properties"]["networkAcls"]["virtualNetworkRules"]
                vcount=len(vnr)
                ipcount=len(netaclipr)

                
                fr.write('\t network_acls {\n')
                fr.write('\t\t bypass="' + netaclby + '"\n')
                fr.write('\t\t default_action="' + netacldf + '"\n')
                
                if ipcount > 0 :
                    print(json.dumps(netaclipr, indent=4, separators=(',', ': ')))
                    fr.write('\t\t ip_rules = [\n')
                    for ip in range(0, ipcount): 
                        aip=netaclipr[ip]["value"]
                        fr.write('\t\t\t"'+aip + '",\n')
                    fr.write('\t\t ]' + '\n')
                
                
                if vcount > 0:
                    fr.write('\t\t virtual_network_subnet_ids = [\n')
                    for v in range(0, vcount): 
                        aid=vnr[v]["id"]
                        fr.write('\t\t\t"'+aid + '",\n')
                    fr.write('\t\t ]' + '\n')
                    
                fr.write('\t }' + '\n')
            except KeyError:
                pass


            try: 
                endep=str(azr[i]["properties"]["enabledForDeployment"]).lower()
                fr.write('\t enabled_for_deployment=' + endep + '\n')
            except KeyError:
                pass
            
            try:
                endisk=str(azr[i]["properties"]["enabledForDiskEncryption"]).lower()
                if endisk != "None":
                    fr.write('\t enabled_for_disk_encryption=' + endisk + '\n')
            except KeyError:
                pass       
            
            try:
                entemp=str(azr[i]["properties"]["enabledForTemplateDeployment"]).lower()
                if entemp != "None":
                    fr.write('\t enabled_for_template_deployment=' +  entemp + '\n')
            except KeyError:
                pass

            ap=azr[i]["properties"]["accessPolicies"]
                    
            #
            # Access Policies
            #
            pcount=len(ap)
            for j in range(0, pcount):    
                fr.write('\t access_policy {' + '\n')
                apten=azr[i]["properties"]["accessPolicies"][j]["tenantId"]           
                fr.write('\t\t tenant_id="' + apten + '"\n')
                apoid=azr[i]["properties"]["accessPolicies"][j]["objectId"]
                fr.write('\t\t object_id="' + apoid + '"\n')

                try:         
                    jkl=azr[i]["properties"]["accessPolicies"][j]["permissions"]["keys"]    
                    try:
                        kl=len(jkl)
                        fr.write('\t\t key_permissions = [ \n')
                        for k in range(0,kl):
                            tk=azr[i]["properties"]["accessPolicies"][j]["permissions"]["keys"][k]
                            if tk != "all":
                                fr.write('\t\t\t "' + tk + '",\n')
                        fr.write('\t\t ]\n') 
                    except TypeError:
                        pass 
                except KeyError:
                    pass

                try:
                    jsl=azr[i]["properties"]["accessPolicies"][j]["permissions"]["secrets"]
                    try:
                        sl=len(jsl)
                        fr.write('\t\t secret_permissions = [ \n')
                        for k in range(0,sl):
                            tk=azr[i]["properties"]["accessPolicies"][j]["permissions"]["secrets"][k]
                            if tk != "all":
                                fr.write('\t\t\t "' + tk + '",\n')
                        fr.write('\t\t ]\n') 
                    except TypeError:
                        pass 
                except KeyError:
                    pass
                
                try:
                    jcl=azr[i]["properties"]["accessPolicies"][j]["permissions"]["certificates"]
                    try:
                        cl=len(jcl)
                        fr.write('\t\t certificate_permissions = [ \n')
                        for k in range(0,cl):
                            tk=azr[i]["properties"]["accessPolicies"][j]["permissions"]["certificates"][k]
                            if tk != "all":    
                                fr.write('\t\t\t "' + tk + '",\n')
                        fr.write('\t\t ]\n')                          
                        
                    except TypeError:
                        pass       
                except KeyError:
                    pass
                fr.write('\t}\n')
            
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

            

            fr.write('} \n')
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
    #end key vault
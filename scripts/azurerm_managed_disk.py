def azurerm_managed_disk(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_managed_disk"
    azr=""
    if crf in tfp:
    # REST or cli
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Compute/disks"
        params = {'api-version': '2017-03-30'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf="100-"+tfp+"-staterm.sh"
        tfimf="100-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            oname=azr[i]["name"]
            name=oname.replace("/.vhd","/_vhd") 
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
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')


            try:
                ostyp=azr[i]["properties"]["osType"]
                fr.write('\t os_type = "' +  ostyp + '"\n')
            except KeyError:
                pass
                
            try:
                creopt=azr[i]["properties"]["creationData"]["createOption"]
                fr.write('\t create_option = "' +  creopt + '"\n')
            except KeyError:
                pass

            try:
                creopt=azr[i]["properties"]["creationData"]["sourceResourceId"]
                fr.write('\t source_resource_id = "' +  creopt + '"\n')
            except KeyError:
                pass        

            try:
                imid=azr[i]["properties"]["creationData"]["imageReference"]["id"]
                fr.write('\t image_reference_id = "' +  imid + '"\n')
            except KeyError:
                pass 
            """        
            try:      
                creid=azr[i]["properties"]["creationData"]["imageReference"]["id"]
                fr.write('\t source_resource_id = "' +  creid + '"\n')
            except KeyError:
                pass
            """        
            try:
                enc=azr[i]["properties"]["encryptionSettings"]["enabled"]
                fr.write('\t encryption_settings { \n')
                fr.write('\t\t enabled = ' +  str(enc).lower() + '\n')
                try:
                    kekurl=azr[i]["properties"]["encryptionSettings"]["keyEncryptionKey"]["keyUrl"]
                    kekvltid=azr[i]["properties"]["encryptionSettings"]["keyEncryptionKey"]["sourceVault"]["id"]
                    fr.write('\t\t key_encryption_key { \n')
                    fr.write('\t\t\t key_url = "' +  kekurl + '"\n')
                    fr.write('\t\t\t source_vault_id = "' +  kekvltid + '"\n')
                    fr.write('\t\t } \n')
                except KeyError:
                    pass       

                try:
                    dekurl=azr[i]["properties"]["encryptionSettings"]["diskEncryptionKey"]["secretUrl"]
                    dekvltid=azr[i]["properties"]["encryptionSettings"]["diskEncryptionKey"]["sourceVault"]["id"]
                    fr.write('\t\t disk_encryption_key { \n')
                    fr.write('\t\t\t secret_url = "' +  dekurl + '"\n')
                    fr.write('\t\t\t source_vault_id = "' +  dekvltid + '"\n')               
                    fr.write('\t\t } \n')
                except KeyError:
                    pass


                fr.write('\t } \n')
            except KeyError:
                pass


            try:
                stopt=azr[i]["sku"]["name"]
                fr.write('\t storage_account_type = "' +  stopt + '"\n')
            except KeyError:
                fr.write('\t storage_account_type = "' +  "StandardSSD_LRS" + '"\n')
                pass    
            
        

            try:
                dsize=str(azr[i]["properties"]["diskSizeGB"])
                fr.write('\t disk_size_gb = "' +  dsize + '"\n')
                    
            except KeyError:
                pass


            try:
                zones=azr[i]["zones"]
                fr.write('zones = ')
                fr.write(json.dumps(zones, indent=4, separators=(',', ': ')))
                fr.write('\n')
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
    #end managed disk
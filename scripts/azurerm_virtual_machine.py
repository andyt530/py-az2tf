# azurerm_virtual_machine
def azurerm_virtual_machine(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_virtual_machine"
    tcode="290-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Compute/virtualMachines"
        params = {'api-version': '2019-03-01'}
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
        
            
            
            vmtype=azr[i]["properties"]["storageProfile"]["osDisk"]["osType"]
            vmsize=azr[i]["properties"]["hardwareProfile"]["vmSize"]
            #vmdiags=azr[i]["properties"]["diagnosticsProfile"]
            #vmbturi=azr[i]["properties"]["diagnosticsProfile"]["bootDiagnostics"]["storageUri"]
            netifs=azr[i]["properties"]["networkProfile"]["networkInterfaces"]
            datadisks=azr[i]["properties"]["storageProfile"]["dataDisks"]


    

            try : 
                avsid=azr[i]["properties"]["availabilitySet"]["id"].split("/")[8].replace(".","-").lower()
                avsrg=azr[i]["properties"]["availabilitySet"]["id"].split("/")[4].replace(".","-").lower()
                if avsrg[0].isdigit(): avsrg="rg_"+avsrg
                fr.write('\t availability_set_id = "${azurerm_availability_set.' + avsrg + '__' +avsid + '.id}"\n')
            except KeyError:
                pass


            try : 
                vmlic=azr[i]["properties"]["licenseType"]
                fr.write('\t license_type = "' +  vmlic + '"\n')
            except KeyError:
                pass

            fr.write('\t vm_size = "' + vmsize + '"\n')
            #
            # Multiples
            #
            icount=len(netifs)
            priif=""
            if icount > 0 :
                fr.write('\t network_interface_ids = [\n')
                for j in range(0,icount):
                    vmnetpri=False
                    vmnetid=azr[i]["properties"]["networkProfile"]["networkInterfaces"][j]["id"].split("/")[8].replace(".","-")
                    vmnetrg=azr[i]["properties"]["networkProfile"]["networkInterfaces"][j]["id"].split("/")[4].replace(".","-").lower()
                    if vmnetrg[0].isdigit(): vmnetrg="rg_"+vmnetrg
                    try:
                        vmnetpri=azr[i]["properties"]["networkProfile"]["networkInterfaces"][j]["properties"]["primary"]
                        priif='\t primary_network_interface_id = "${azurerm_network_interface.' + vmnetrg + '__' +  vmnetid + '.id}"\n'
                    except KeyError:
                        pass
                    fr.write('\t "${azurerm_network_interface.' + vmnetrg + '__' + vmnetid + '.id}",')
                    if vmnetpri :
                        priif='\t primary_network_interface_id = "${azurerm_network_interface.' + vmnetrg + '__' +  vmnetid + '.id}"\n'
                        #print "priif="+priif    
                fr.write('\t]\n')
                fr.write(priif) 
            #
            fr.write('\t delete_data_disks_on_termination = "'+ 'false' + '"\n')
            fr.write('\t delete_os_disk_on_termination = "'+ 'false' + '"\n')
            #
            try:
                vmcn=azr[i]["properties"]["osProfile"]["computerName"]
                vmadmin=azr[i]["properties"]["osProfile"]["adminUsername"]
                fr.write('os_profile {\n')
                fr.write('\tcomputer_name = "' +    vmcn + '"\n')
                fr.write('\tadmin_username = "' +    vmadmin + '"\n')
          
                try : 
                    vmadminpw=azr[i]["properties"]["osProfile"]["Password"]
                    fr.write('\t admin_password = "' +  vmadminpw + '"\n')
                except KeyError:
                    pass

                #  admin_password ?
                fr.write('}\n')
            except KeyError:
                pass 
        
            #
           
            try:
                vmimid=azr[i]["properties"]["storageProfile"]["imageReference"]["id"]  
                #print "do something with "+vmimid
            except KeyError:
                try:
                    vmimpublisher=azr[i]["properties"]["storageProfile"]["imageReference"]["publisher"]
                    vmimoffer=azr[i]["properties"]["storageProfile"]["imageReference"]["offer"]
                    vmimpublisher=azr[i]["properties"]["storageProfile"]["imageReference"]["publisher"]
                    vmimsku=azr[i]["properties"]["storageProfile"]["imageReference"]["sku"]
                    vmimversion=azr[i]["properties"]["storageProfile"]["imageReference"]["version"]
                    fr.write('storage_image_reference {\n')
                    fr.write('\t publisher = "' +  vmimpublisher  + '"\n')
                    fr.write('\t offer = "' +   vmimoffer + '"\n')
                    fr.write('\t sku = "' +   vmimsku + '"\n')
                    fr.write('\t version = "' +   vmimversion + '"\n')
                    havesir=1
                    fr.write('}\n')
                except KeyError:
                    pass
       
            
        
            try :
                vmplname=azr[i]["plan"]["name"]
                vmplprod=azr[i]["plan"]["product"]
                vmplpub=azr[i]["plan"]["publisher"] 
                fr.write('plan {\n')
                fr.write('\t name = "' +  vmplname  + '"\n')
                fr.write('\t publisher = "' +  vmplpub  + '"\n')
                fr.write('\t product = "' +  vmplprod  + '"\n')
                fr.write('}\n')
            except KeyError:
                pass
            #
            #
            #
            try :
                vmdiags=azr[i]["properties"]["diagnosticsProfile"]
                vmbturi=azr[i]["properties"]["diagnosticsProfile"]["bootDiagnostics"]["storageUri"]
                fr.write('boot_diagnostics {\n')
                fr.write('\t enabled = true \n')
                fr.write('\t storage_uri = "' +  vmbturi + '"\n')
                fr.write('}\n')
            except KeyError:
                pass
            #
            if vmtype == "Windows" :
                try:
                    vmwvma=azr[i]["properties"]["osProfile"]["windowsConfiguration"]["provisionVMAgent"]
                    try :
                        vmwau=azr[i]["properties"]["osProfile"]["windowsConfiguration"]["enableAutomaticUpdates"]
                        fr.write('os_profile_windows_config {\n')
                        fr.write('\t enable_automatic_upgrades = ' +  str(vmwau).lower() + '\n')
                        fr.write('\t provision_vm_agent = ' +  str(vmwvma).lower() + '\n')
                        try :
                            vmwtim=azr[i]["properties"]["osProfile"]["windowsConfiguration"]["timeZone"]
                            fr.write('\t timezone =   "' + vmwtim + '"\n')
                        except KeyError:
                            pass
                        fr.write('}\n')
                    except KeyError:
                        pass
                except KeyError:
                    pass
        
            #
            if  vmtype == "Linux" :
                fr.write('os_profile_linux_config {\n')
                try:
                    vmdispw=azr[i]["properties"]["osProfile"]["linuxConfiguration"]["disablePasswordAuthentication"]
                except KeyError:
                    vmdispw="false"
            
                fr.write('\tdisable_password_authentication = ' +  str(vmdispw).lower() + '\n')
                if vmdispw :
                    try:
                        vmsshpath=azr[i]["properties"]["osProfile"]["linuxConfiguration"]["ssh"]["publicKeys"][0]["path"]
                        vmsshkey=azr[i]["properties"]["osProfile"]["linuxConfiguration"]["ssh"]["publicKeys"][0]["keyData"]
                        t1=str(vmsshkey).rstrip()
                        fr.write('\tssh_keys {\n')
                        fr.write('\t\tpath = "' +   vmsshpath + '"\n')
                        if "----"  not in vmsshkey:
                            fr.write('\t\tkey_data = "' + t1 + '"\n') 
                        else:
                             fr.write('\t\tkey_data = "' + '"\n')
                        fr.write('\t}\n')
                    except KeyError:
                        pass
            
                
                fr.write('}\n')
        

            #
            # OS Disk
            #
            try:
                vmosdiskname=azr[i]["properties"]["storageProfile"]["osDisk"]["name"]
                vmosdiskcache=azr[i]["properties"]["storageProfile"]["osDisk"]["caching"]
                vmoscreoption=azr[i]["properties"]["storageProfile"]["osDisk"]["createOption"]
                fr.write('storage_os_disk {\n')
                fr.write('\t\tname = "' +    vmosdiskname + '"\n')
                fr.write('\t\tcaching = "' +   vmosdiskcache  + '"\n')
                fr.write('\t\tcreate_option = "' + vmoscreoption + '"\n')
                fr.write('\t\tos_type = "' +   vmtype + '"\n')

        
                try :
                    vmossiz=azr[i]["properties"]["storageProfile"]["osDisk"]["diskSizeGB"]
                    fr.write('\t\t disk_size_gb = "' +   str(vmossiz) + '"\n')
                except KeyError:
                    pass   

                try :
                    vmosvhd=azr[i]["properties"]["storageProfile"]["osDisk"]["vhd"]["uri"]
                    fr.write('\t\tvhd_uri = "' +   vmosvhd + '"\n')
                except KeyError:
                    pass
                try :
                    vmoswa=azr[i]["properties"]["storageProfile"]["osDisk"]["writeAcceleratorEnabled"]
                    fr.write('\t write_accelerator_enabled = ' +   str(vmoswa).lower() + '\n')
                except KeyError:
                    pass

                
                if vmoscreoption == "Attach" :
                    try :
                        vmosmdtyp=azr[i]["properties"]["storageProfile"]["osDisk"]["managedDisk"]["storageAccountType"]
                        fr.write('\tmanaged_disk_type = "' +   vmosmdtyp + '"\n')
                    except KeyError:
                        pass
                    try :
                        vmosmdid=azr[i]["properties"]["storageProfile"]["osDisk"]["managedDisk"]["id"]
                        fr.write('\tmanaged_disk_id = "' +   vmosmdid + '"\n')
                    except KeyError:
                        pass
            

                fr.write('}\n')
            except KeyError:
                pass
            #if vmosmdid" try :
            #    if [ havesir -eq 0 :
                    #fr.write('storage_image_reference {'}'  + '"\n')
            #   
            #fi

            #
            # Data disks
            #
            #echo datadisks | jq .
            dcount= len(datadisks)
            
            for j in range(0,dcount):             
                try :
                    ddname= datadisks[j]["name"]
                    ddcreopt= datadisks[j]["createOption"]
                    ddlun= datadisks[j]["lun"]
                    ddvhd= datadisks[j]["vhd.uri"]
                    ddmd= datadisks[j]["managedDisk"]
                    fr.write('storage_data_disk {\n')
                    fr.write('\t name = "' +  ddname + '"\n')
                    fr.write('\t create_option = "' +  ddcreopt + '"\n')
                    fr.write('\t lun = "' +  ddlun + '"\n')
                    # caching , disk_size_gn, write_accelerator_enabled 
                    
                    if ddcreopt == "Attach" :
                        try:
                            ddmdid= datadisks[j]["managedDisk"]["id"].split("/")[8].replace(".","-")
                            ddmdrg= datadisks[j]["managedDisk"]["id"].split("/")[4].replace(".","-").lower()
                            ## ddmdrg  from cut is upper case - not good
                            ## probably safe to assume managed disk in same RG as VM ??
                            # check id lowercase rg = ddmdrg if so use rg
                            #
                            #if not will have to get from terraform state - convert ddmdrg to lc and terraform state output
                            #
                            
                            fr.write('\t managed_disk_id = "${azurerm_managed_disk.' + rg + '__' + ddmdid + '.id} \n')
                        except KeyError:
                            pass
                
                    try :
                        ddvhd= datadisks[j]["vhd"]["uri"]
                        fr.write('\t vhd_uri = "' +  ddvhd + '"\n')
                    except KeyError:
                            pass
                    
                    fr.write('}\n')
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
                    tval=tval.replace('"',"'")
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

# azurerm_virtual_machine
def azurerm_virtual_machine(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_virtual_machine"
    tcode="290-"
    azr=""
    if crf in tfp:
    # REST or cli
        print "REST Managed Disk"
        url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Compute/virtualMachine"
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

            avsid=azr[i]["availabilitySet"]["id"].split("/")[8].replace(".","-")
            avsrg=azr[i]["availabilitySet"]["id"].split("/")[8].replace(".","-")
            lavs=avsrg + '__' + avsid

            lavs=lavs.lower()
            #for tavs in terraform state list | grep azurerm_availability_set):     
            uavs= tavs.split("/")[2].lower() 
            if uavs == "lavs" :            
                myavs= tavs.split("/")[2]
            
            
            #echo "myavs=myavs"

            vmlic=azr[i]["licenseType"]
            vmtype=azr[i]["storageProfile"]["osDisk.osType"]
            vmsize=azr[i]["hardwareProfile"]["vmSize"]
            vmdiags=azr[i]["diagnosticsProfile"]
            vmbturi=azr[i]["diagnosticsProfile"]["bootDiagnostics"]["storageUri"]
            netifs=azr[i]["networkProfile"]["networkInterfaces"]
            datadisks=azr[i]["storageProfile"]["dataDisks"]

            vmosdiskname=azr[i]["storageProfile"]["osDisk"]["name"]
            vmosdiskcache=azr[i]["storageProfile"]["osDisk"]["caching"]
            vmosvhd=azr[i]["storageProfile"]["osDisk"]["vhd"]["uri"]
            vmoscreoption=azr[i]["storageProfile"]["osDisk"]["createOption"]
            vmoswa=azr[i]["storageProfile"]["osDisk"]["writeAcceleratorEnabled"]
            vmossiz=azr[i]["storageProfile"]["osDisk"]["diskSizeGb"]
            vmosmdid=azr[i]["storageProfile"]["osDisk"]["managedDisk"]["id"]
            vmosmdtyp=azr[i]["storageProfile"]["osDisk"]["managedDisk"]["storageAccountType"]
            #
            
            osvhd=azr[i]["osProfile"]["linuxConfiguration"]["ssh"]["publicKeys"][0]["keyData"]
            
            #
            vmimid=azr[i]["storageProfile"]["imageReference"]["id"]

            vmimoffer=azr[i]["storageProfile"]["imageReference"]["offer"]
            vmimpublisher=azr[i]["storageProfile"]["imageReference"]["publisher"]
            vmimsku=azr[i]["storageProfile"]["imageReference"]["sku"]
            vmimversion=azr[i]["storageProfile"]["imageReference"]["version"]
            #
            vmadmin=azr[i]["osProfile"]["adminUsername"]
            vmadminpw=azr[i]["osProfile"]["Password"]
            vmcn=azr[i]["osProfile"]["computerName"]
            vmdispw=azr[i]["osProfile"]["linuxConfiguration"]["disablePasswordAu:tication"]
            vmsshpath=azr[i]["osProfile"]["linuxConfiguration"]["ssh"]["publicKeys"][0]["path"]
            vmsshkey=azr[i]["osProfile"]["linuxConfiguration.ssh"]["publicKeys"][0]["keyData"]
            #
            vmplname=azr[i]["plan"]["name"]  
            #

            try : 
                avsid=azr[i]["availabilitySet"]["id"].split("/")[8].replace(".","-")
                avsrg=azr[i]["availabilitySet"]["id"].split("/")[8].replace(".","-")
                fr.write('\t availability_set_id = "${azurerm_availability_set.' + myavs + '.id}\n')
            except KeyError:
                pass


            try : 
                vmlic=azr[i]["licenseType"]
                fr.write('\t license_type = "' +  vmlic + '"\n')
            except KeyError:
                pass

            fr.write('\t vm_size = "' + vmsize + '"\n')
            #
            # Multiples
            #
            icount=len(netifs)
            if icount > 0 :
                for j in range(0,icount):
                    vmnetid=azr[i]["networkProfile"]["networkInterfaces"][j]["id"].split("/")[8].replace(".","-")
                    vmnetrg=azr[i]["networkProfile"]["networkInterfaces"][j]["id"].split("/")[4].replace(".","-")
                    vmnetpri=azr[i]["networkProfile"]["networkInterfaces"][j]["primary"]
                    fr.write('\t network_interface_ids = ["${azurerm_network_interface.' + vmnetrg + '__' + vmnetid + '.id}"\n')
                    if vmnetpri == "true" :
                        fr.write('\t primary_network_interface_id = "${azurerm_network_interface.' + vmnetrg + '__' +  vmnetid + '.id}"\n')     
            
            #
            fr.write('\t delete_data_disks_on_termination = "'+ false + '"\n')
            fr.write('\t delete_os_disk_on_termination = "'+ false + '"\n')
            #
            try:
                vmcn=azr[i]["osProfile"]["computerName"]
                fr.write('os_profile {'  + '"\n')
                fr.write('\tcomputer_name = "' +    vmcn + '"\n')
                fr.write('\tadmin_username = "' +    vmadmin + '"\n')
            except KeyError:
                pass
                     
            
            try : 
                vmadminpw=azr[i]["osProfile"]["Password"]
                fr.write('\t admin_password = "' +  vmadminpw + '"\n')
            except KeyError:
                pass

            #  admin_password ?
            fr.write('}\n')
        
            #
            havesir=0
            if vmimid == "null" :
                try:
                    vmimpublisher=azr[i]["storageProfile"]["imageReference"]["publisher"]
                    fr.write('storage_image_reference {'  + '"\n')
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
                fr.write('plan {'  + '"\n')
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
                vmdiags=azr[i]["diagnosticsProfile"]
                fr.write('boot_diagnostics {'  + '"\n')
                fr.write('\t enabled = "' + true + '"\n')
                fr.write('\t storage_uri = "' +  vmbturi + '"\n')
                fr.write('}\n')
            except KeyError:
                pass
            #
            if vmtype == "Windows" :
                vmwau=azr[i]["osProfile"]["windowsConfiguration"]["enableAutomaticUpdates"]
                vmwvma=azr[i]["osProfile"]["windowsConfiguration"]["provisionVmAgent"]
                vmwtim=azr[i]["osProfile"]["windowsConfiguration"]["timeZone"]
                try :
                    vmwau=azr[i]["osProfile"]["windowsConfiguration"]["enableAutomaticUpdates"]
                    fr.write('os_profile_windows_config {'  + '"\n')
                    fr.write('\t enable_automatic_upgrades = "' +  vmwau + '"\n')
                    fr.write('\t provision_vm_agent = "' +  vmwvma + '"\n')
                    try :
                        vmwtim=azr[i]["osProfile"]["windowsConfiguration"]["timeZone"]
                        fr.write('\t timezone =   "' + vmwtim + '"\n')
                    except KeyError:
                        pass
                    fr.write('}\n')
                except KeyError:
                    pass
        
            #
            if  vmtype == "Linux" :
                fr.write('os_profile_linux_config {'  + '"\n')
                if  vmdispw == "null" :
                # osprofile can by null for vhd imported images - must make an artificial one.
                    vmdispw="false"
            
                fr.write('\tdisable_password_authentication = "' +   vmdispw + '"\n')
                if vmdispw != "false" :
                    fr.write('\tssh_keys {'  + '\n')
                    fr.write('\t\tpath = "' +   vmsshpath + '"\n')
             
                    fr.write('\t}\n')
            
                
                fr.write('}\n')
        

            #
            # OS Disk
            #
            fr.write('\t storage_os_disk {'  + '"\n')
            fr.write('\t\tname = "' +    vmosdiskname + '"\n')
            fr.write('\t\tcaching = "' +   vmosdiskcache  + '"\n')
            fr.write('\t\tcreate_option = "' + vmoscreoption + '"\n')
            fr.write('\t\tos_type = "' +   vmtype + '"\n')

    
            try :
                vmossiz=azr[i]["storageProfile"]["osDisk"]["diskSizeGb"]
                fr.write('\t\t disk_size_gb = "' +   vmossiz + '"\n')
            except KeyError:
                pass   

            try :
                vmosvhd=azr[i]["storageProfile"]["osDisk"]["vhd"]["uri"]
                fr.write('\t\tvhd_uri = "' +   vmosvhd + '"\n')
            except KeyError:
                pass
            if vmoswa" try :
                fr.write('\t write_accelerator_enabled = "' +   vmoswa + '"\n')
            except KeyError:
                pass

            vmosmdid=azr[i]["storageProfile.osDisk.managedDisk"]["id"]
            vmosmdtyp=azr[i]["storageProfile.osDisk.managedDisk.storageAccountType"]


            if vmoscreoption" = "Attach" :
                if vmosmdtyp" try :
                    fr.write('\tmanaged_disk_type = "' +   vmosmdtyp + '"\n')
                except KeyError:
                    pass
                if vmosmdid" try :
                    fr.write('\tmanaged_disk_id = "' +   vmosmdid + '"\n')
                except KeyError:
                    pass
        

            fr.write('}\n')
            #if vmosmdid" try :
            #    if [ havesir -eq 0 :
                    #fr.write('storage_image_reference {'}'  + '"\n')
            #   
            #fi

            #
            # Data disks
            #
            #echo datadisks | jq .
            dcount= datadisks | | len(
            dcount=((dcount-1))
            
            for j in range(0,dcount):
                ddname= datadisks | jq ".[j]["name"]
                if ddname" try :
                    ddcreopt= datadisks | jq ".[j]["createOption"]
                    ddlun= datadisks | jq ".[j]["lun"]
                    ddvhd= datadisks | jq ".[j]["vhd.uri"]
                    ddmd= datadisks | jq ".[j]["managedDisk"]
                    fr.write('storage_data_disk {'  + '"\n')
                    fr.write('\t name = "' +  ddname + '"\n')
                    fr.write('\t create_option = "' +  ddcreopt + '"\n')
                    fr.write('\t lun = "' +  ddlun + '"\n')
                    # caching , disk_size_gn, write_accelerator_enabled 
                    
                    if ddcreopt" = "Attach" :
                        if ddmd" try ][":
                        ddmdid= datadisks | jq ".[j]["managedDisk"]["id"].split("/")[8].replace(".","-")
                        ddmdrg= datadisks | jq ".[j]["managedDisk"]["id"].split("/")[4].replace(".","-")
                        ## ddmdrg  from cut is upper case - not good
                        ## probably safe to assume managed disk in same RG as VM ??
                        # check id lowercase rg = ddmdrg if so use rg
                        #
                        #if not will have to get from terraform state - convert ddmdrg to lc and terraform state output
                        #
                        
                        fr.write('\t managed_disk_id = "${azurerm_managed_disk. + '__' + .id}'"' rg ddmdid + '"\n')
                        except KeyError:
                            pass
                
                    if ddvhd" try :
                        fr.write('\t vhd_uri = "' +  ddvhd + '"\n')
                    except KeyError:
                            pass
                    
                    fr.write('}\n')
                except KeyError:
                            pass
            

            
            fr.write('}\n')

        


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

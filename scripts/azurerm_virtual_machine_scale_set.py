# azurerm_virtual_machine_scale_set
def azurerm_virtual_machine_scale_set(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_virtual_machine_scale_set"
    tcode="295-"
    azr=""
    if crf in tfp:
    # REST or cli
        print "REST Managed Disk"
        url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Compute/virtualMachineScaleSets"
        params = {'api-version': '2019-03-01'}
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

            upm=azr[i]["upgradePolicy"]["mode"]
            op=azr[i]["overprovision"]
            spg=azr[i]["singlePlacementGroup"]
            vmlic=azr[i]["virtualMachineProfile"]["licenseType"]
            vmpri=azr[i]["virtualMachineProfile"]["priority"]


            vmtype=azr[i]["virtualMachineProfile"]["storageProfile"]["osDisk"]["osType"]
            datadisks=azr[i]["virtualMachineProfile"]["storageProfile"]["dataDisks"]

            vmosdiskname=azr[i]["virtualMachineProfile"]["storageProfile"]["osDisk"]["name"]
            vmosdiskcache=azr[i]["virtualMachineProfile"]["storageProfile"]["osDisk"]["caching"]
            vmosvhdc=azr[i]["virtualMachineProfile"]["storageProfile"]["osDisk"]["vhdContainers"]
            vmoscreoption=azr[i]["virtualMachineProfile"]["storageProfile"]["osDisk"]["createOption"]
            vmoswa=azr[i]["virtualMachineProfile"]["storageProfile"]["osDisk"]["writeAcceleratorEnabled"]
            #  
            osvhd=azr[i]["virtualMachineProfile"]["osProfile"]["linuxConfiguration"]["ssh"]["publicKeys"][0]["keyData"]
            #
            vmimid=azr[i]["virtualMachineProfile"]["storageProfile"]["imageReference"]["id"]

            vmimoffer=azr[i]["virtualMachineProfile"]["storageProfile"]["imageReference"]["offer"]
            vmimpublisher=azr[i]["virtualMachineProfile"]["storageProfile"]["imageReference"]["publisher"]
            vmimsku=azr[i]["virtualMachineProfile"]["storageProfile"]["imageReference"]["sku"]
            vmimversion=azr[i]["virtualMachineProfile"]["storageProfile"]["imageReference"]["version"]
            #

            vmdispw=azr[i]["virtualMachineProfile"]["osProfile"]["linuxConfiguration"]["disablePasswordAuthentication"]
            vmsshpath=azr[i]["virtualMachineProfile"]["osProfile"]["linuxConfiguration"]["ssh"]["publicKeys"][0]["path"]
            vmsshkey=azr[i]["virtualMachineProfile"]["osProfile"]["linuxConfiguration"]["ssh"]["publicKeys"][0]["keyData"]
            #
            vmplname=azr[i]["plan"]["name"]  
            #

    # sku block
            skun=azr[i]["sku"]["name"]
            skuc=azr[i]["sku"]["capacity"]
            skut=azr[i]["sku"]["tier"]
            fr.write('sku { \n')
            fr.write('\tname = "' +  skun + '"\n')
            fr.write('\ttier = "' +  skut + '"\n')
            fr.write('\tcapacity = "' +  skuc + '"\n')
            fr.write('} \n')
    # basic settings continued
    
            try : 
                vmlic=azr[i]["virtualMachineProfile"]["licenseType"]
                fr.write('license_type = "' +  vmlic + '"\n')
            except KeyError:
                pass
            
            fr.write('upgrade_policy_mode = "' +  upm + '"\n')
            fr.write('overprovision = "' +  op + '"\n')
            fr.write('single_placement_group = "' +  spg + '"\n')
            try : 
                vmpri=azr[i]["virtualMachineProfile"]["priority"]
                fr.write('priority = "' +  vmpri + '"\n')
            except KeyError:
                pass 



    #os_profile block
            vmadmin=azr[i]["virtualMachineProfile.osProfile"]["adminUsername"]
            vmadminpw=azr[i]["virtualMachineProfile"]["osProfile"]["Password"]
            vmcn=azr[i]["virtualMachineProfile"]["osProfile"]["computerNamePrefix"]
            fr.write('os_profile { \n')
            fr.write('\tcomputer_name_prefix = "' +  vmcn + '"\n')
            fr.write('\tadmin_username = "' +  vmadmin + '"\n')
            try :
                vmadminpw=azr[i]["virtualMachineProfile"]["osProfile"]["Password"]
                fr.write('\tadmin_password = "' +  vmadminpw + '"\n')
            except KeyError:
                pass 
        
            fr.write('}\n')

    # os_profile_secrets - not used ?

    # os_profile_windows_config
            winb=azr[i]["virtualMachineProfile"]["osProfile"]["windowsConfiguration"]
            
        #
            try : # winb
                winb=azr[i]["virtualMachineProfile"]["osProfile"]["windowsConfiguration"]
                vmwau=azr[i]["virtualMachineProfile"]["osProfile"]["windowsConfiguration"]["enableAutomaticUpdates"]
                vmwvma=azr[i]["virtualMachineProfile"]["osProfile"]["windowsConfiguration"]["provisionVmAgent"]
                vmwtim=azr[i]["virtualMachineProfile"]["osProfile"]["windowsConfiguration"]["timeZone"]
                try :
                    vmwau=azr[i]["virtualMachineProfile"]["osProfile"]["windowsConfiguration"]["enableAutomaticUpdates"]
                    fr.write('os_profile_windows_config {'  + '\n')
                    fr.write('\t enable_automatic_upgrades = "' +  vmwau + '"\n')
                    fr.write('\t provision_vm_agent = "' +  vmwvma + '"\n')
                    try :
                        vmwtim=azr[i]["virtualMachineProfile"]["osProfile"]["windowsConfiguration"]["timeZone"]
                        fr.write('\t timezone =   "' +vmwtim + '"\n')
                    except KeyError:
                        pass 
                    fr.write('}\n')
                except KeyError:
                    pass 
            except KeyError:
                pass 
        

    # os_profile_linux_config block
            linuxb=azr[i]["virtualMachineProfile"]["osProfile"]["linuxConfiguration"]
            

            try: #linuxb" try :
                linuxb=azr[i]["virtualMachineProfile"]["osProfile"]["linuxConfiguration"]
                fr.write('os_profile_linux_config {'  + '\n')
                if vmdispw == "null" :
                # osprofile can by null for vhd imported images - must make an artificial one.
                    vmdispw="false"
            
                fr.write('\tdisable_password_authentication = "' + vmdispw + '"\n')
                if vmdispw != "false" :
                    fr.write('\tssh_keys { \n')
                    fr.write('\t\tpath = "' +  vmsshpath + '"\n')
                    fr.write('\t}\n')
            
                
                fr.write('}\n')
            except KeyError:
                pass
      

# network profile block
            netifs=azr[i]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"]    
            icount=len(netifs) 
            if icount > 0 :
                for j in range(0,icount):
                    fr.write('network_profile { \n')
                       
                    nn=azr[i]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["name"]
                    pri=azr[i]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["primary"]
                    ipc=azr[i]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["ipConfigurations"]
                    fr.write('\tname = "' +  nn + '"\n')
                    fr.write('\tprimary = "' +  pri + '"\n')
                    kcount= len(ipc)
                    
                    if kcount > 0 :
                        for k in range(0,kcount):
                            fr.write('\tip_configuration { \n')
                            ipcn=azr[i]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["ipConfigurations"][k]["name"]
                            ipcp=azr[i]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["ipConfigurations"][k]["primary"]
                            ipcsrg=azr[i]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["ipConfigurations"][k]["subnet"]["id"].split("/")[4].replace(".","-")
                            ipcsn=azr[i]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["ipConfigurations"][k]["subnet"]["id"].split("/")[10].replace(".","-")                                                    
                            beapids=azr[i]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["ipConfigurations"][k]["loadBalancerBackendAddressPools"]
                            natrids=azr[i]["virtualMachineProfile"]["networkProfile"]["networkInterfaceConfigurations"][j]["ipConfigurations"][k]["loadBalancerInboundNatPools"]                                
             
                            if ipcp == "null" : 
                                ipcp=""
                            fr.write('\t\tname = "' +  ipcn + '"\n')
                            fr.write('\t\tprimary = "' +  ipcp + '"\n')
                            fr.write('\t\tsubnet_id = "${azurerm_subnet.' + ipcsrg+ '__' + ipcsn + '.id}"\n')
                            fr.write('\t}\n')
                            
                        
                    fr.write('}\n')
              
        

    # storage_profile_os_disk  block
            fr.write('storage_profile_os_disk {'  + '"\n')
            fr.write('\tname = "' +    vmosdiskname + '"\n')
            fr.write('\tcaching = "' +   vmosdiskcache + '"\n') 
            #### look at this
            ##if vmosacctype != "" :
            ##    fr.write('\tmanaged_disk_type = "' +   vmosacctype + '"\n')
        
            fr.write('\tcreate_option = "' +   vmoscreoption + '"\n')
            if vmtype == "null" : 
                vmtype=""
            fr.write('\tos_type = "' +   vmtype + '"\n')
            try :
                vmoswa=azr[i]["virtualMachineProfile"]["storageProfile"]["osDisk"]["writeAcceleratorEnabled"]
                fr.write('\t write_accelerator_enabled = "' +   vmoswa + '"\n')
            except KeyError:
                pass


            vmosvhdc=azr[i]["virtualMachineProfile"]["storageProfile"]["osDisk"]["vhdContainers"]

            try :
                vmosvhdc=azr[i]["virtualMachineProfile"]["storageProfile"]["osDisk"]["vhdContainers"]
                fr.write('\tvhd_containers =    "' +vmosvhdc +'"\n')
            except KeyError:
                pass
        
            fr.write('}\n')
            #
        
    # storage_profile_data_disk  block
            
            #echo datadisks | jq .
            dcount= len(datadisks) 
            
            for j in range(0,dcount):
                ddname= datadisks["name"]
                try :
                    ddname= datadisks["name"]
                    ddcreopt= datadisks["createOption"]
                    ddlun= datadisks[j]["lun"]
                    ddvhd= datadisks[j]["vhd"]["uri"]
                    ddmd= datadisks[j]["managedDisk"]
                    fr.write('storage_profile_data_disk { \n')
                    fr.write('\t name = "' +  ddname + '"\n')
                    fr.write('\t create_option = "' +  ddcreopt + '"\n')
                    fr.write('\t lun = "' +  ddlun + '"\n')
                    # caching , disk_size_gn, write_accelerator_enabled 
                    
                    if ddcreopt == "Attach" :
                        try:
                            ddmd= datadisks[j]["managedDisk"]
                            ddmdid= datadisks[j]["managedDisk"]["id"].split("/")[8].replace(".","-")
                            ddmdrg= datadisks[j]["managedDisk"]["id"].split("/")[4].replace(".","-")
                            ## ddmdrg from cut is upper case - not good
                            ## probably safe to assume managed disk in same RG as VM ??
                            # check id lowercase rg = ddmdrg if so use rg
                            #
                            #if not will have to get from terraform state - convert ddmdrg to lc and terraform state output
                            #
                            
                            fr.write('\t managed_disk_id = "${azurerm_managed_disk.' + rg + '__' + ddmdid + '.id}"\n')
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
            # end for j
            

    # storage_profile_image_reference block

        if vmimid == "null" :
            try:
                vmimpublisher=azr[i]["virtualMachineProfile"]["storageProfile"]["imageReference"]["publisher"]
                fr.write('storage_profile_image_reference { \n')
                fr.write('\t publisher = "' +  vmimpublisher  + '"\n')
                fr.write('\t offer = "' +   vmimoffer + '"\n')
                fr.write('\t sku = "' +   vmimsku + '"\n')
                fr.write('\t version = "' +   vmimversion + '"\n')
                
                fr.write('}\n')  
            except KeyError:
                pass   

    # extensions:

    # boot diagnostics block

            vmbturi=azr[i]["virtualMachineProfile"]["diagnosticsProfile"]["bootDiagnostics"]["storageUri"]
            vmbten=azr[i]["virtualMachineProfile"]["diagnosticsProfile"]["bootDiagnostics"]["enabled"]

            try :
                vmdiags=azr[i]["virtualMachineProfile"]["diagnosticsProfile"]
                fr.write('boot_diagnostics {'  + '"\n')
                fr.write('\t enabled = "' +  vmbten + '"\n')
                fr.write('\t storage_uri = "' +  vmbturi + '"\n')
                fr.write('}\n')
            except KeyError:
                pass

    # plan block
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
                
    

    # zones block
   


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

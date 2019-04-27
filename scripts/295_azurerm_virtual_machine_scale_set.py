
azr=az vmss list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        name=azr[i]["name"]
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']

        id=azr[i]["id"]
        loc=azr[i]["location"]
        upm=azr[i]["upgradePolicy.mode"]
        op=azr[i]["overprovision"]
        spg=azr[i]["singlePlacementGroup"]
        vmlic=azr[i]["virtualMachineProfile.licenseType"]
        vmpri=azr[i]["virtualMachineProfile.priority"]


        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outfile


        vmtype=azr[i]["virtualMachineProfile.storageProfile.osDisk.osType"]
        datadisks=azr[i]["virtualMachineProfile.storageProfile.dataDisks"

        vmosdiskname=azr[i]["virtualMachineProfile.storageProfile.osDisk.name"]
        vmosdiskcache=azr[i]["virtualMachineProfile.storageProfile.osDisk.caching"]
        vmosvhdc=azr[i]["virtualMachineProfile.storageProfile.osDisk.vhdContainers"
        vmoscreoption=azr[i]["virtualMachineProfile.storageProfile.osDisk.createOption"]
        vmoswa=azr[i]["virtualMachineProfile.storageProfile.osDisk.writeAcceleratorEnabled"]
        #  
        osvhd=azr[i]["virtualMachineProfile.osProfile.linuxConfiguration.ssh.publicKeys[0]["keyData"]
        #
        vmimid=azr[i]["virtualMachineProfile.storageProfile.imageReference.id"]

        vmimoffer=azr[i]["virtualMachineProfile.storageProfile.imageReference.offer"]
        vmimpublisher=azr[i]["virtualMachineProfile.storageProfile.imageReference.publisher"]
        vmimsku=azr[i]["virtualMachineProfile.storageProfile.imageReference.sku"]
        vmimversion=azr[i]["virtualMachineProfile.storageProfile.imageReference.version"]
        #

        vmdispw=azr[i]["virtualMachineProfile.osProfile.linuxConfiguration.disablePasswordAu:tication"]
        vmsshpath=azr[i]["virtualMachineProfile.osProfile.linuxConfiguration.ssh.publicKeys[0]["path"]
        vmsshkey=azr[i]["virtualMachineProfile.osProfile.linuxConfiguration.ssh.publicKeys[0]["keyData"]
        #
        vmplname=azr[i]["plan.name"]  
        #
# basic settings 
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('name = "' +  name + '"\n')
        fr.write('location = "' +   loc + '"\n')
# sku block
        skun=azr[i]["sku.name"]
        skuc=azr[i]["sku.capacity"]
        skut=azr[i]["sku.tier"]
        fr.write('sku {' upm + '"\n')
        fr.write('\tname = "' +  skun + '"\n')
        fr.write('\ttier = "' +  skut + '"\n')
        fr.write('\tcapacity = "' +  skuc + '"\n')
        fr.write('}' upm + '"\n')
# basic settings continued
        fr.write('resource_group_name = "' +  rgsource + '"\n')
        if vmlic" != "null" : 
            fr.write('license_type = "' +  vmlic + '"\n')
           
        fr.write('upgrade_policy_mode = "' +  upm + '"\n')
        fr.write('overprovision = "' +  op + '"\n')
        fr.write('single_placement_group = "' +  spg + '"\n')
        if vmpri" != "null" : 
        fr.write('priority = "' +  vmpri + '"\n')
        fi
#os_profile block
        vmadmin=azr[i]["virtualMachineProfile.osProfile.adminUsername"]
        vmadminpw=azr[i]["virtualMachineProfile.osProfile.Password"]
        vmcn=azr[i]["virtualMachineProfile.osProfile.computerNamePrefix"]
        fr.write('os_profile {' + '"\n')
        fr.write('\tcomputer_name_prefix = "' +  vmcn + '"\n')
        fr.write('\tadmin_username = "' +  vmadmin + '"\n')
        if vmadminpw" != "null" :
        fr.write('\tadmin_password = "' +  vmadminpw + '"\n')
        fi
        fr.write('}' + '"\n')

# os_profile_secrets - not used ?

# os_profile_windows_config
        winb=azr[i]["virtualMachineProfile.osProfile.windowsConfiguration"
        
       #
        if winb" != "null" :
            vmwau=azr[i]["virtualMachineProfile.osProfile.windowsConfiguration.enableAutomaticUpdates"]
            vmwvma=azr[i]["virtualMachineProfile.osProfile.windowsConfiguration.provisionVmAgent"]
            vmwtim=azr[i]["virtualMachineProfile.osProfile.windowsConfiguration.timeZone"
            if vmwau" != "null" :
                fr.write('os_profile_windows_config {'  + '"\n')
                fr.write('\t enable_automatic_upgrades = "' +  vmwau + '"\n')
                fr.write('\t provision_vm_agent = "' +  vmwvma + '"\n')
                if vmwtim" != "null" :
                    fr.write('\t timezone =   "vmwtim" + '"\n')
                fi
                fr.write('}' + '"\n')
            fi
        fi

# os_profile_linux_config block
        linuxb=azr[i]["virtualMachineProfile.osProfile.linuxConfiguration"
        

        if linuxb" != "null" :
            fr.write('os_profile_linux_config {'  + '"\n')
            if [ vmdispw = "null" :
            # osprofile can by null for vhd imported images - must make an artificial one.
            vmdispw="false"
            fi
            fr.write('\tdisable_password_au:tication = "' +   vmdispw + '"\n')
            if vmdispw" != "false" :
               fr.write('\tssh_keys {'  + '"\n')
                fr.write('\t\tpath = "' +   vmsshpath + '"\n')
                print "		key_data = "'vmsshkey"'"  + '"\n')
                fr.write('\t}' + '"\n')
            fi
            
            fr.write('}' + '"\n')
        fi

# network profile block
        netifs=azr[i]["virtualMachineProfile.networkProfile.networkInterfaceConfigurations"      
        icount=print netifs | jq '. | length'
        if icount" -gt "0" :
            icount=expr icount - 1
            for j in range( 0 icount):
                fr.write('network_profile {' + '"\n')
                nn=azr[i]["virtualMachineProfile.networkProfile.networkInterfaceConfigurations[j]["name"]
                pri=azr[i]["virtualMachineProfile.networkProfile.networkInterfaceConfigurations[j]["primary"]
                ipc=azr[i]["virtualMachineProfile.networkProfile.networkInterfaceConfigurations[j]["ipConfigurations"
                fr.write('\tname = "' +  nn + '"\n')
                fr.write('\tprimary = "' +  pri + '"\n')
                kcount=print ipc | jq '. | length'
                if kcount" -gt "0" :
                    kcount=expr kcount - 1
                        for k in range( 0 kcount):
                            fr.write('\tip_configuration {' + '"\n')
                                ipcn=azr[i]["virtualMachineProfile.networkProfile.networkInterfaceConfigurations[j]["ipConfigurations[k]["name"]
                                ipcp=azr[i]["virtualMachineProfile.networkProfile.networkInterfaceConfigurations[j]["ipConfigurations[k]["primary"]
                                ipcsrg=azr[i]["virtualMachineProfile.networkProfile.networkInterfaceConfigurations[j]["ipConfigurations[k]["subnet.id" | cut -f5 -d'/' | sed 's/\./-/g']
                                ipcsn=azr[i]["virtualMachineProfile.networkProfile.networkInterfaceConfigurations[j]["ipConfigurations[k]["subnet.id" | cut -f11 -d'/' | sed 's/\./-/g']                    
                                beapids=azr[i]["virtualMachineProfile.networkProfile.networkInterfaceConfigurations[j]["ipConfigurations[k]["loadBalancerBackendAddressPools"
                                natrids=azr[i]["virtualMachineProfile.networkProfile.networkInterfaceConfigurations[j]["ipConfigurations[k]["loadBalancerInboundNatPools"                                
                                print "*************************************************"
                                print beapids
                                print natrids  
                                print "-------------------------------------------------"               
                                if ipcp" = "null" : ipcp=";fi
                                fr.write('\t\tname = "' +  ipcn + '"\n')
                                fr.write('\t\tprimary = "' +  ipcp + '"\n')
                                fr.write('\t\tsubnet_id = "'\{'azurerm_subnet. + '__' + .id}'"' ipcsrg ipcsn + '"\n')
                            fr.write('\t}' + '"\n')
                        
                      
                fr.write('}' + '"\n')
            
        fi

        #print "*************************************************"
        #print "-------------------------------------------------"
        #print "================================================="

# storage_profile_os_disk  block
        fr.write('storage_profile_os_disk {'  + '"\n')
        fr.write('\tname = "' +    vmosdiskname + '"\n')
        fr.write('\tcaching = "' +   vmosdiskcache  >>  outfile
        if vmosacctype" != " :
            fr.write('\tmanaged_disk_type = "' +   vmosacctype + '"\n')
        fi

        fr.write('\tcreate_option = "' +   vmoscreoption + '"\n')
        if vmtype" = "null" : vmtype=" ; fi
        fr.write('\tos_type = "' +   vmtype + '"\n')
        if vmoswa" != "null" :
            fr.write('\t write_accelerator_enabled = "' +   vmoswa + '"\n')
        fi
        vmosvhdc=azr[i]["virtualMachineProfile.storageProfile.osDisk.vhdContainers"

        if vmosvhdc" != "null" :
            fr.write('\tvhd_containers =    "vmosvhdc" + '"\n')
        fi
        fr.write('}' + '"\n')
        #
       
# storage_profile_data_disk  block
        
        #print datadisks | jq .
        dcount=print datadisks | jq '. | length'
        dcount=((dcount-1))
        
        for j in range( 0 dcount):
            ddname=print datadisks | jq ".[j]["name"]
            if ddname" != "null" :
                ddcreopt=print datadisks | jq ".[j]["createOption"]
                ddlun=print datadisks | jq ".[j]["lun"]
                ddvhd=print datadisks | jq ".[j]["vhd.uri"]
                ddmd=print datadisks | jq ".[j]["managedDisk"]
                fr.write('storage_profile_data_disk {'  + '"\n')
                fr.write('\t name = "' +  ddname + '"\n')
                fr.write('\t create_option = "' +  ddcreopt + '"\n')
                fr.write('\t lun = "' +  ddlun + '"\n')
                # caching , disk_size_gn, write_accelerator_enabled 
                
                if ddcreopt" = "Attach" :
                    if ["ddmd" != "null" ][":
                    ddmdid=print datadisks | jq ".[j]["managedDisk.id" | cut -d'/' -f9 | sed 's/\./-/g']
                    ddmdrg=print datadisks | jq ".[j]["managedDisk.id" | cut -d'/' -f5 | sed 's/\./-/g']
                    ## ddmdrg from cut is upper case - not good
                    ## probably safe to assume managed disk in same RG as VM ??
                    # check id lowercase rg = ddmdrg if so use rg
                    #
                    #if not will have to get from terraform state - convert ddmdrg to lc and terraform state output
                    #
                    
                    fr.write('\t managed_disk_id = "'\{'azurerm_managed_disk. + '__' + .id}'"' rg ddmdid + '"\n')
                    fi
                fi
                if ddvhd" != "null" :
                    fr.write('\t vhd_uri = "' +  ddvhd + '"\n')
                fi
                
                fr.write('}' + '"\n')
            fi
        

# storage_profile_image_reference block

        if vmimid" = "null" :
            if vmimpublisher" != "null" ][":
            fr.write('storage_profile_image_reference {'  + '"\n')
            fr.write('\t publisher = "' +  vmimpublisher  + '"\n')
            fr.write('\t offer = "' +   vmimoffer + '"\n')
            fr.write('\t sku = "' +   vmimsku + '"\n')
            fr.write('\t version = "' +   vmimversion + '"\n')
            
            fr.write('}' + '"\n')
            fi
          
        fi

# extensions

# boot diagnostics block

        vmdiags=azr[i]["virtualMachineProfile.diagnosticsProfile"]
        vmbturi=azr[i]["virtualMachineProfile.diagnosticsProfile.bootDiagnostics.storageUri"]
        vmbten=azr[i]["virtualMachineProfile.diagnosticsProfile.bootDiagnostics.enabled"]

        if vmdiags" != "null" :
            fr.write('boot_diagnostics {'  + '"\n')
            fr.write('\t enabled = "' +  vmbten + '"\n')
            fr.write('\t storage_uri = "' +  vmbturi + '"\n')
            fr.write('}' + '"\n')
        fi

# plan block
        if vmplname" != "null" :
            vmplprod=azr[i]["plan.product"]
            vmplpub=azr[i]["plan.publisher"] 
            fr.write('plan {'  + '"\n')
            fr.write('\t name = "' +  vmplname  + '"\n')
            fr.write('\t publisher = "' +  vmplpub  + '"\n')
            fr.write('\t product = "' +  vmplprod  + '"\n')
            fr.write('}' + '"\n')
              
 

# zones block
        
# finish

        fr.write('}' + '"\n')

    
fi

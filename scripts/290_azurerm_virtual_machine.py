
azr=az vm list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        name=azr[i]["name"]
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']

        id=azr[i]["id"]
        loc=azr[i]["location"]
    
        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outfile

        avsid=azr[i]["availabilitySet.id" | cut -f9 -d'/' | sed 's/\./-/g']
        avsrg=azr[i]["availabilitySet.id" | cut -f5 -d'/' | sed 's/\./-/g']
        lavs=fr.write(' + '__' + " avsrg avsid

        lavs=print lavs | awk '{'print tolower(0)}''
        for tavs in terraform state list | grep azurerm_availability_set):     
            uavs=print tavs | cut -f2 -d'.' | awk '{'print tolower(0)}'' 
            if uavs" == "lavs" :            
                myavs=print tavs | cut -f2 -d'.' 
           
        
        #print "myavs=myavs"

        vmlic=azr[i]["licenseType"]
        vmtype=azr[i]["storageProfile.osDisk.osType"]
        vmsize=azr[i]["hardwareProfile.vmSize"]
        vmdiags=azr[i]["diagnosticsProfile"]
        vmbturi=azr[i]["diagnosticsProfile.bootDiagnostics.storageUri"]
        netifs=azr[i]["networkProfile.networkInterfaces"
        datadisks=azr[i]["storageProfile.dataDisks"

        vmosdiskname=azr[i]["storageProfile.osDisk.name"]
        vmosdiskcache=azr[i]["storageProfile.osDisk.caching"]
        vmosvhd=azr[i]["storageProfile.osDisk.vhd.uri"]
        vmoscreoption=azr[i]["storageProfile.osDisk.createOption"]
        vmoswa=azr[i]["storageProfile.osDisk.writeAcceleratorEnabled"]
        vmossiz=azr[i]["storageProfile.osDisk.diskSizeGb"]
        vmosmdid=azr[i]["storageProfile.osDisk.managedDisk.id"]
        vmosmdtyp=azr[i]["storageProfile.osDisk.managedDisk.storageAccountType"]
        #
        
        osvhd=azr[i]["osProfile.linuxConfiguration.ssh.publicKeys[0]["keyData"]
        
        #
        vmimid=azr[i]["storageProfile.imageReference.id"]

        vmimoffer=azr[i]["storageProfile.imageReference.offer"]
        vmimpublisher=azr[i]["storageProfile.imageReference.publisher"]
        vmimsku=azr[i]["storageProfile.imageReference.sku"]
        vmimversion=azr[i]["storageProfile.imageReference.version"]
        #
        vmadmin=azr[i]["osProfile.adminUsername"]
        vmadminpw=azr[i]["osProfile.Password"]
        vmcn=azr[i]["osProfile.computerName"]
        vmdispw=azr[i]["osProfile.linuxConfiguration.disablePasswordAu:tication"]
        vmsshpath=azr[i]["osProfile.linuxConfiguration.ssh.publicKeys[0]["path"]
        vmsshkey=azr[i]["osProfile.linuxConfiguration.ssh.publicKeys[0]["keyData"]
        #
        vmplname=azr[i]["plan.name"]  
        #
 
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location = "' +   loc + '"\n')
        #fr.write('\t resource_group_name = "'\{'var.rgtarget}'"' myrg + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        if avsid" != "null" : 
            fr.write('\t availability_set_id = "'\{'azurerm_availability_set..id}'"' myavs + '"\n')
        fi
        if vmlic" != "null" : 
            fr.write('\t license_type = "' +  vmlic + '"\n')
        fi
        fr.write('\t vm_size = "' +  vmsize + '"\n')
        #
        # Multiples
        #
        icount=print netifs | jq '. | length'
        if icount" -gt "0" :
            icount=expr icount - 1
            for j in range( 0 icount):
                vmnetid=azr[i]["networkProfile.networkInterfaces[j]["id" | cut -d'/' -f9 | sed 's/\./-/g']
                vmnetrg=azr[i]["networkProfile.networkInterfaces[j]["id" | cut -d'/' -f5 | sed 's/\./-/g']
                vmnetpri=azr[i]["networkProfile.networkInterfaces[j]["primary"]
                fr.write('\t network_interface_ids = ["'\{'azurerm_network_interface. + '__' + .id}'"']["n" vmnetrg vmnetid + '"\n')
                if vmnetpri" == "true" :
                    fr.write('\t primary_network_interface_id = "'\{'azurerm_network_interface. + '__' + .id}'"' vmnetrg vmnetid + '"\n')
                fi
            
        fi
        #
        #
        fr.write('\t delete_data_disks_on_termination = "'false"'  + '"\n')
        fr.write('\t delete_os_disk_on_termination = "'false"'  + '"\n')
        #
        if vmcn" != "null" ][":
        fr.write('os_profile {'  + '"\n')
        fr.write('\tcomputer_name = "' +    vmcn + '"\n')
        fr.write('\tadmin_username = "' +    vmadmin + '"\n')
        if vmadminpw" != "null" : 
            fr.write('\t admin_password = "' +  vmadminpw + '"\n')
        fi

        #  admin_password ?
        fr.write('}' + '"\n')
        fi
        
        #
        #
        havesir=0
        if vmimid" = "null" :
            if vmimpublisher" != "null" ][":
            fr.write('storage_image_reference {'  + '"\n')
            fr.write('\t publisher = "' +  vmimpublisher  + '"\n')
            fr.write('\t offer = "' +   vmimoffer + '"\n')
            fr.write('\t sku = "' +   vmimsku + '"\n')
            fr.write('\t version = "' +   vmimversion + '"\n')
            havesir=1
            fr.write('}' + '"\n')
            fi
          
        fi
        if vmplname" != "null" :
            vmplprod=azr[i]["plan.product"]
            vmplpub=azr[i]["plan.publisher"] 
            fr.write('plan {'  + '"\n')
            fr.write('\t name = "' +  vmplname  + '"\n')
            fr.write('\t publisher = "' +  vmplpub  + '"\n')
            fr.write('\t product = "' +  vmplprod  + '"\n')
            fr.write('}' + '"\n')
        fi
        #
        #
        #
        if vmdiags" != "null" :
            fr.write('boot_diagnostics {'  + '"\n')
            fr.write('\t enabled = "'true"'  + '"\n')
            fr.write('\t storage_uri = "' +  vmbturi + '"\n')
            fr.write('}' + '"\n')
        fi
        #
        if [ vmtype = "Windows" :
            vmwau=azr[i]["osProfile.windowsConfiguration.enableAutomaticUpdates"]
            vmwvma=azr[i]["osProfile.windowsConfiguration.provisionVmAgent"]
            vmwtim=azr[i]["osProfile.windowsConfiguration.timeZone"
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
        #
        if [ vmtype = "Linux" :
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

        #
        # OS Disk
        #
        fr.write('\t storage_os_disk {'  + '"\n')
        fr.write('\t\tname = "' +    vmosdiskname + '"\n')
        fr.write('\t\tcaching = "' +   vmosdiskcache  >>  outfile
        fr.write('\t\tcreate_option = "' +   vmoscreoption + '"\n')
        fr.write('\t\tos_type = "' +   vmtype + '"\n')

 
        if vmossiz" != "null" :
            fr.write('\t\t disk_size_gb = "' +   vmossiz + '"\n')
             

        if vmosvhd" != "null" :
            fr.write('\t\tvhd_uri = "' +   vmosvhd + '"\n')
        fi
        if vmoswa" != "null" :
            fr.write('\t write_accelerator_enabled = "' +   vmoswa + '"\n')
        fi

        vmosmdid=azr[i]["storageProfile.osDisk.managedDisk.id"]
        vmosmdtyp=azr[i]["storageProfile.osDisk.managedDisk.storageAccountType"]


        if vmoscreoption" = "Attach" :
            if vmosmdtyp" != "null" :
                fr.write('\tmanaged_disk_type = "' +   vmosmdtyp + '"\n')
            fi
            if vmosmdid" != "null" :
                fr.write('\tmanaged_disk_id = "' +   vmosmdid + '"\n')
            fi
        fi

        fr.write('}' + '"\n')
        #if vmosmdid" != "null" :
        #    if [ havesir -eq 0 :
                #fr.write('storage_image_reference {'}'  + '"\n')
        #    fi
        #fi

        #
        # Data disks
        #
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
                fr.write('storage_data_disk {'  + '"\n')
                fr.write('\t name = "' +  ddname + '"\n')
                fr.write('\t create_option = "' +  ddcreopt + '"\n')
                fr.write('\t lun = "' +  ddlun + '"\n')
                # caching , disk_size_gn, write_accelerator_enabled 
                
                if ddcreopt" = "Attach" :
                    if ddmd" != "null" ][":
                    ddmdid=print datadisks | jq ".[j]["managedDisk.id" | cut -d'/' -f9 | sed 's/\./-/g']
                    ddmdrg=print datadisks | jq ".[j]["managedDisk.id" | cut -d'/' -f5 | sed 's/\./-/g']
                    ## ddmdrg  from cut is upper case - not good
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
        

           
        fr.write('}' + '"\n')

    
fi

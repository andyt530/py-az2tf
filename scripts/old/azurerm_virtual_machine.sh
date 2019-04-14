tfp="azurerm_virtual_machine"
prefixa="vm"
if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
azr=`az vm list -g $rgsource`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | tr -d '"'`
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`
    
        prefix=`printf "%s__%s" $prefixa $rg`


        avsid=`echo $azr | jq ".[(${i})].availabilitySet.id" | cut -f9 -d'/' | tr -d '"'`
        avsrg=`echo $azr | jq ".[(${i})].availabilitySet.id" | cut -f5 -d'/' | tr -d '"'`
        lavs=`printf "%s__%s" $avsrg $avsid`

        lavs=`echo $lavs | awk '{print tolower($0)}'`
        for tavs in `terraform state list | grep azurerm_availability_set`; do     
            uavs=`echo $tavs | cut -f2 -d'.' | awk '{print tolower($0)}'` 
            if [ "$uavs" == "$lavs" ]; then            
                myavs=`echo $tavs | cut -f2 -d'.'` 
            fi 
        done
        #echo "myavs=$myavs"

        vmlic=`echo $azr | jq ".[(${i})].licenseType" | tr -d '"'`
        vmtype=`echo $azr | jq ".[(${i})].storageProfile.osDisk.osType" | tr -d '"'`
        vmsize=`echo $azr | jq ".[(${i})].hardwareProfile.vmSize" | tr -d '"'`
        vmdiags=`echo $azr | jq ".[(${i})].diagnosticsProfile" | tr -d '"'`
        vmbturi=`echo $azr | jq ".[(${i})].diagnosticsProfile.bootDiagnostics.storageUri" | tr -d '"'`
        netifs=`echo $azr | jq ".[(${i})].networkProfile.networkInterfaces"`
        datadisks=`echo $azr | jq ".[(${i})].storageProfile.dataDisks"`

        vmosdiskname=`echo $azr | jq ".[(${i})].storageProfile.osDisk.name" | tr -d '"'`
        vmosdiskcache=`echo $azr | jq ".[(${i})].storageProfile.osDisk.caching" | tr -d '"'`
        vmosvhd=`echo $azr | jq ".[(${i})].storageProfile.osDisk.vhd.uri" | tr -d '"'`
        vmoscreoption=`echo $azr | jq ".[(${i})].storageProfile.osDisk.createOption" | tr -d '"'`
        vmoswa=`echo $azr | jq ".[(${i})].storageProfile.osDisk.writeAcceleratorEnabled" | tr -d '"'`
        #
        
        osvhd=`echo $azr | jq ".[(${i})].osProfile.linuxConfiguration.ssh.publicKeys[0].keyData" | tr -d '"'`
        
        #
        vmimid=`echo $azr | jq ".[(${i})].storageProfile.imageReference.id" | tr -d '"'`

        vmimoffer=`echo $azr | jq ".[(${i})].storageProfile.imageReference.offer" | tr -d '"'`
        vmimpublisher=`echo $azr | jq ".[(${i})].storageProfile.imageReference.publisher" | tr -d '"'`
        vmimsku=`echo $azr | jq ".[(${i})].storageProfile.imageReference.sku" | tr -d '"'`
        vmimversion=`echo $azr | jq ".[(${i})].storageProfile.imageReference.version" | tr -d '"'`
        #
        vmadmin=`echo $azr | jq ".[(${i})].osProfile.adminUsername" | tr -d '"'`
        vmadminpw=`echo $azr | jq ".[(${i})].osProfile.Password" | tr -d '"'`
        vmcn=`echo $azr | jq ".[(${i})].osProfile.computerName" | tr -d '"'`
        vmdispw=`echo $azr | jq ".[(${i})].osProfile.linuxConfiguration.disablePasswordAuthentication" | tr -d '"'`
        vmsshpath=`echo $azr | jq ".[(${i})].osProfile.linuxConfiguration.ssh.publicKeys[0].path" | tr -d '"'`
        vmsshkey=`echo $azr | jq ".[(${i})].osProfile.linuxConfiguration.ssh.publicKeys[0].keyData" | tr -d '"'`
        #
        vmplname=`echo $azr | jq ".[(${i})].plan.name" | tr -d '"'`  
        #
        echo $az2tfmess > $prefix-$name.tf
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $name > $prefix-$name.tf
        printf "\t name = \"%s\"\n" $name >> $prefix-$name.tf
        printf "\t location = \"%s\"\n"  $loc >> $prefix-$name.tf
        #printf "\t resource_group_name = \"\${var.rgtarget}\"\n" $myrg >> $prefix-$name.tf
        printf "\t resource_group_name = \"%s\"\n" $rg >> $prefix-$name.tf
        if [ "$avsid" != "null" ]; then 
            printf "\t availability_set_id = \"\${azurerm_availability_set.%s.id}\"\n" $myavs >> $prefix-$name.tf
        fi
        if [ "$vmlic" != "null" ]; then 
            printf "\t license_type = \"%s\"\n" $vmlic >> $prefix-$name.tf
        fi
        printf "\t vm_size = \"%s\"\n" $vmsize >> $prefix-$name.tf
        #
        # Multiples
        #
        icount=`echo $netifs | jq '. | length'`
        if [ "$icount" -gt "0" ]; then
            icount=`expr $icount - 1`
            for j in `seq 0 $icount`; do
                vmnetid=`echo $azr | jq ".[(${i})].networkProfile.networkInterfaces[(${j})].id" | cut -d'/' -f9 | tr -d '"'`
                vmnetrg=`echo $azr | jq ".[(${i})].networkProfile.networkInterfaces[(${j})].id" | cut -d'/' -f5 | tr -d '"'`
                vmnetpri=`echo $azr | jq ".[(${i})].networkProfile.networkInterfaces[(${j})].primary" | tr -d '"'`
                printf "\t network_interface_ids = [\"\${azurerm_network_interface.%s__%s.id}\"]\n" $vmnetrg $vmnetid >> $prefix-$name.tf
                if [ "$vmnetpri" == "true" ]; then
                    printf "\t primary_network_interface_id = \"\${azurerm_network_interface.%s__%s.id}\"\n" $vmnetrg $vmnetid >> $prefix-$name.tf
                fi
            done
        fi
        #
        #
        printf "\t delete_data_disks_on_termination = \"false\"\n"  >> $prefix-$name.tf
        printf "\t delete_os_disk_on_termination = \"false\"\n"  >> $prefix-$name.tf
        #
        if [ "$vmcn" != "null" ];then
        printf "os_profile {\n"  >> $prefix-$name.tf
        printf "\tcomputer_name = \"%s\" \n"  $vmcn >> $prefix-$name.tf
        printf "\tadmin_username = \"%s\" \n"  $vmadmin >> $prefix-$name.tf
        if [ "$vmadminpw" != "null" ]; then 
            printf "\t admin_password = \"%s\"\n" $vmadminpw >> $prefix-$name.tf
        fi

        #  admin_password ?
        printf "}\n" >> $prefix-$name.tf
        fi
        #
        # OS Disk
        #

        printf "storage_os_disk {\n"  >> $prefix-$name.tf
        printf "\tname = \"%s\" \n"  $vmosdiskname >> $prefix-$name.tf
        printf "\tcaching = \"%s\" \n" $vmosdiskcache  >>  $prefix-$name.tf
        if [ "$vmosacctype" != "" ]; then
            printf "\tmanaged_disk_type = \"%s\" \n" $vmosacctype >> $prefix-$name.tf
        fi
        if [ "$vmosvhd" != "null" ]; then
            printf "\tvhd_uri = \"%s\" \n" $vmosvhd >> $prefix-$name.tf
        fi
        printf "\tcreate_option = \"%s\" \n" $vmoscreoption >> $prefix-$name.tf
        printf "\tos_type = \"%s\" \n" $vmtype >> $prefix-$name.tf
        if [ "$vmoswa" != "null" ]; then
            printf "\t write_accelerator_enabled = \"%s\" \n" $vmoswa >> $prefix-$name.tf
        fi
        printf "}\n" >> $prefix-$name.tf
        #
        #
        #
        if [ "$vmimid" = "null" ]; then
            if [ "$vmimpublisher" != "null" ];then
            printf "storage_image_reference {\n"  >> $prefix-$name.tf
            printf "\t publisher = \"%s\"\n" $vmimpublisher  >> $prefix-$name.tf
            printf "\t offer = \"%s\"\n"  $vmimoffer >> $prefix-$name.tf
            printf "\t sku = \"%s\"\n"  $vmimsku >> $prefix-$name.tf
            printf "\t version = \"%s\"\n"  $vmimversion >> $prefix-$name.tf
            
            printf "}\n" >> $prefix-$name.tf
            fi
          
        fi
        if [ "$vmplname" != "null" ]; then
            vmplprod=`echo $azr | jq ".[(${i})].plan.product" | tr -d '"'`
            vmplpub=`echo $azr | jq ".[(${i})].plan.publisher" | tr -d '"'` 
            printf "plan {\n"  >> $prefix-$name.tf
            printf "\t name = \"%s\"\n" $vmplname  >> $prefix-$name.tf
            printf "\t publisher = \"%s\"\n" $vmplpub  >> $prefix-$name.tf
            printf "\t product = \"%s\"\n" $vmplprod  >> $prefix-$name.tf
            printf "}\n" >> $prefix-$name.tf
        fi
        #
        #
        #
        if [ "$vmdiags" != "null" ]; then
            printf "boot_diagnostics {\n"  >> $prefix-$name.tf
            printf "\t enabled = \"true\"\n"  >> $prefix-$name.tf
            printf "\t storage_uri = \"%s\"\n" $vmbturi >> $prefix-$name.tf
            printf "}\n" >> $prefix-$name.tf
        fi
        #
        if [ $vmtype = "Windows" ]; then
            vmwau=`echo $azr | jq ".[(${i})].osProfile.windowsConfiguration.enableAutomaticUpdates" | tr -d '"'`
            vmwvma=`echo $azr | jq ".[(${i})].osProfile.windowsConfiguration.provisionVmAgent" | tr -d '"'`
            vmwtim=`echo $azr | jq ".[(${i})].osProfile.windowsConfiguration.timeZone"`
            if [ "$vmwau" != "null" ]; then
                printf "os_profile_windows_config {\n"  >> $prefix-$name.tf
                printf "\t enable_automatic_upgrades = \"%s\"\n" $vmwau >> $prefix-$name.tf
                printf "\t provision_vm_agent = \"%s\"\n" $vmwvma >> $prefix-$name.tf
                if [ "$vmwtim" != "null" ]; then
                    printf "\t timezone = %s \n" "$vmwtim" >> $prefix-$name.tf
                fi
                printf "}\n" >> $prefix-$name.tf
            fi
        fi
        #
        if [ $vmtype = "Linux" ]; then
            printf "os_profile_linux_config {\n"  >> $prefix-$name.tf
            if [ $vmdispw = "null" ]; then
            # osprofile can by null for vhd imported images - must make an artificial one.
            vmdispw="false"
            fi
            printf "\tdisable_password_authentication = \"%s\" \n" $vmdispw >> $prefix-$name.tf
            if [ "$vmdispw" != "false" ]; then
               printf "\tssh_keys {\n"  >> $prefix-$name.tf
                printf "\t\tpath = \"%s\" \n" $vmsshpath >> $prefix-$name.tf
                echo "		key_data = \"$vmsshkey\""  >> $prefix-$name.tf
                printf "\t}\n" >> $prefix-$name.tf
            fi
            
            printf "}\n" >> $prefix-$name.tf
        fi
        #
        # Data disks
        #
        #echo $datadisks | jq .
        dcount=`echo $datadisks | jq '. | length'`
        dcount=$(($dcount-1))
        
        for j in `seq 0 $dcount`; do
            ddname=`echo $datadisks | jq ".[(${j})].name" | tr -d '"'`
            if [ "$ddname" != "null" ]; then
                ddcreopt=`echo $datadisks | jq ".[(${j})].createOption" | tr -d '"'`
                ddlun=`echo $datadisks | jq ".[(${j})].lun" | tr -d '"'`
                ddvhd=`echo $datadisks | jq ".[(${j})].vhd.uri" | tr -d '"'`
                ddmd=`echo $datadisks | jq ".[(${j})].managedDisk" | tr -d '"'`
                printf "storage_data_disk {\n"  >> $prefix-$name.tf
                printf "\t name = \"%s\"\n" $ddname >> $prefix-$name.tf
                printf "\t create_option = \"%s\"\n" $ddcreopt >> $prefix-$name.tf
                printf "\t lun = \"%s\"\n" $ddlun >> $prefix-$name.tf
                # caching , disk_size_gn, write_accelerator_enabled 
                
                if [ "$ddcreopt" = "Attach" ]; then
                    if ["$ddmd" != "null" ];then
                    ddmdid=`echo $datadisks | jq ".[(${j})].managedDisk.id" | cut -d'/' -f9 | tr -d '"'`
                    ddmdrg=`echo $datadisks | jq ".[(${j})].managedDisk.id" | cut -d'/' -f5 | tr -d '"'`
                    ## ddmdrg  from cut is upper case - not good
                    ## probably safe to assume managed disk in same RG as VM ??
                    # check id lowercase rg = ddmdrg if so use rg
                    #
                    #if not will have to get from terraform state - convert ddmdrg to lc and terraform state output
                    #
                    
                    printf "\t managed_disk_id = \"\${azurerm_managed_disk.%s__%s.id}\"\n" $rg $ddmdid >> $prefix-$name.tf
                    fi
                fi
                if [ "$ddvhd" != "null" ]; then
                    printf "\t vhd_uri = \"%s\"\n" $ddvhd >> $prefix-$name.tf
                fi
                
                printf "}\n" >> $prefix-$name.tf
            fi
        done
        
        #
        # New Tags block
        tags=`echo $azr | jq ".[(${i})].tags"`
        tt=`echo $tags | jq .`
        tcount=`echo $tags | jq '. | length'`
        if [ "$tcount" -gt "0" ]; then
            printf "\t tags { \n" >> $prefix-$name.tf
            tt=`echo $tags | jq .`
            keys=`echo $tags | jq 'keys'`
            tcount=`expr $tcount - 1`
            for j in `seq 0 $tcount`; do
                k1=`echo $keys | jq ".[(${j})]"`
                tval=`echo $tt | jq .$k1`
                tkey=`echo $k1 | tr -d '"'`
                printf "\t\t%s = %s \n" $tkey "$tval" >> $prefix-$name.tf
            done
            printf "\t}\n" >> $prefix-$name.tf
        fi
        
        
        printf "}\n" >> $prefix-$name.tf
        cat $prefix-$name.tf
        statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $name`
        echo $statecomm >> tf-staterm.sh
        eval $statecomm
        evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $name $id`
        echo $evalcomm >> tf-stateimp.sh
        eval $evalcomm
    done
fi

prefixa=`echo $0 | awk -F 'azurerm_' '{print $2}' | awk -F '.sh' '{print $1}' `
tfp=`printf "azurerm_%s" $prefixa`

if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
azr=`az vm list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`

        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`
    
        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile

        avsid=`echo $azr | jq ".[(${i})].availabilitySet.id" | cut -f9 -d'/' | sed 's/\./-/g' | tr -d '"'`
        avsrg=`echo $azr | jq ".[(${i})].availabilitySet.id" | cut -f5 -d'/' | sed 's/\./-/g' | tr -d '"'`
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
        vmossiz=`echo $azr | jq ".[(${i})].storageProfile.osDisk.diskSizeGb" | tr -d '"'`
        vmosmdid=`echo $azr | jq ".[(${i})].storageProfile.osDisk.managedDisk.id" | tr -d '"'`
        vmosmdtyp=`echo $azr | jq ".[(${i})].storageProfile.osDisk.managedDisk.storageAccountType" | tr -d '"'`
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
 
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        printf "\t location = \"%s\"\n"  $loc >> $outfile
        #printf "\t resource_group_name = \"\${var.rgtarget}\"\n" $myrg >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
        if [ "$avsid" != "null" ]; then 
            printf "\t availability_set_id = \"\${azurerm_availability_set.%s.id}\"\n" $myavs >> $outfile
        fi
        if [ "$vmlic" != "null" ]; then 
            printf "\t license_type = \"%s\"\n" $vmlic >> $outfile
        fi
        printf "\t vm_size = \"%s\"\n" $vmsize >> $outfile
        #
        # Multiples
        #
        icount=`echo $netifs | jq '. | length'`
        if [ "$icount" -gt "0" ]; then
            icount=`expr $icount - 1`
            for j in `seq 0 $icount`; do
                vmnetid=`echo $azr | jq ".[(${i})].networkProfile.networkInterfaces[(${j})].id" | cut -d'/' -f9 | sed 's/\./-/g' | tr -d '"'`
                vmnetrg=`echo $azr | jq ".[(${i})].networkProfile.networkInterfaces[(${j})].id" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
                vmnetpri=`echo $azr | jq ".[(${i})].networkProfile.networkInterfaces[(${j})].primary" | tr -d '"'`
                printf "\t network_interface_ids = [\"\${azurerm_network_interface.%s__%s.id}\"]\n" $vmnetrg $vmnetid >> $outfile
                if [ "$vmnetpri" == "true" ]; then
                    printf "\t primary_network_interface_id = \"\${azurerm_network_interface.%s__%s.id}\"\n" $vmnetrg $vmnetid >> $outfile
                fi
            done
        fi
        #
        #
        printf "\t delete_data_disks_on_termination = \"false\"\n"  >> $outfile
        printf "\t delete_os_disk_on_termination = \"false\"\n"  >> $outfile
        #
        if [ "$vmcn" != "null" ];then
        printf "os_profile {\n"  >> $outfile
        printf "\tcomputer_name = \"%s\" \n"  $vmcn >> $outfile
        printf "\tadmin_username = \"%s\" \n"  $vmadmin >> $outfile
        if [ "$vmadminpw" != "null" ]; then 
            printf "\t admin_password = \"%s\"\n" $vmadminpw >> $outfile
        fi

        #  admin_password ?
        printf "}\n" >> $outfile
        fi
        
        #
        #
        havesir=0
        if [ "$vmimid" = "null" ]; then
            if [ "$vmimpublisher" != "null" ];then
            printf "storage_image_reference {\n"  >> $outfile
            printf "\t publisher = \"%s\"\n" $vmimpublisher  >> $outfile
            printf "\t offer = \"%s\"\n"  $vmimoffer >> $outfile
            printf "\t sku = \"%s\"\n"  $vmimsku >> $outfile
            printf "\t version = \"%s\"\n"  $vmimversion >> $outfile
            havesir=1
            printf "}\n" >> $outfile
            fi
          
        fi
        if [ "$vmplname" != "null" ]; then
            vmplprod=`echo $azr | jq ".[(${i})].plan.product" | tr -d '"'`
            vmplpub=`echo $azr | jq ".[(${i})].plan.publisher" | tr -d '"'` 
            printf "plan {\n"  >> $outfile
            printf "\t name = \"%s\"\n" $vmplname  >> $outfile
            printf "\t publisher = \"%s\"\n" $vmplpub  >> $outfile
            printf "\t product = \"%s\"\n" $vmplprod  >> $outfile
            printf "}\n" >> $outfile
        fi
        #
        #
        #
        if [ "$vmdiags" != "null" ]; then
            printf "boot_diagnostics {\n"  >> $outfile
            printf "\t enabled = \"true\"\n"  >> $outfile
            printf "\t storage_uri = \"%s\"\n" $vmbturi >> $outfile
            printf "}\n" >> $outfile
        fi
        #
        if [ $vmtype = "Windows" ]; then
            vmwau=`echo $azr | jq ".[(${i})].osProfile.windowsConfiguration.enableAutomaticUpdates" | tr -d '"'`
            vmwvma=`echo $azr | jq ".[(${i})].osProfile.windowsConfiguration.provisionVmAgent" | tr -d '"'`
            vmwtim=`echo $azr | jq ".[(${i})].osProfile.windowsConfiguration.timeZone"`
            if [ "$vmwau" != "null" ]; then
                printf "os_profile_windows_config {\n"  >> $outfile
                printf "\t enable_automatic_upgrades = \"%s\"\n" $vmwau >> $outfile
                printf "\t provision_vm_agent = \"%s\"\n" $vmwvma >> $outfile
                if [ "$vmwtim" != "null" ]; then
                    printf "\t timezone = %s \n" "$vmwtim" >> $outfile
                fi
                printf "}\n" >> $outfile
            fi
        fi
        #
        if [ $vmtype = "Linux" ]; then
            printf "os_profile_linux_config {\n"  >> $outfile
            if [ $vmdispw = "null" ]; then
            # osprofile can by null for vhd imported images - must make an artificial one.
            vmdispw="false"
            fi
            printf "\tdisable_password_authentication = \"%s\" \n" $vmdispw >> $outfile
            if [ "$vmdispw" != "false" ]; then
               printf "\tssh_keys {\n"  >> $outfile
                printf "\t\tpath = \"%s\" \n" $vmsshpath >> $outfile
                echo "		key_data = \"$vmsshkey\""  >> $outfile
                printf "\t}\n" >> $outfile
            fi
            
            printf "}\n" >> $outfile
        fi

        #
        # OS Disk
        #
        printf "\t storage_os_disk {\n"  >> $outfile
        printf "\t\tname = \"%s\" \n"  $vmosdiskname >> $outfile
        printf "\t\tcaching = \"%s\" \n" $vmosdiskcache  >>  $outfile
        printf "\t\tcreate_option = \"%s\" \n" $vmoscreoption >> $outfile
        printf "\t\tos_type = \"%s\" \n" $vmtype >> $outfile

 
        if [ "$vmossiz" != "null" ]; then
            printf "\t\t disk_size_gb = \"%s\" \n" $vmossiz >> $outfile
        fi       

        if [ "$vmosvhd" != "null" ]; then
            printf "\t\tvhd_uri = \"%s\" \n" $vmosvhd >> $outfile
        fi
        if [ "$vmoswa" != "null" ]; then
            printf "\t write_accelerator_enabled = \"%s\" \n" $vmoswa >> $outfile
        fi

        vmosmdid=`echo $azr | jq ".[(${i})].storageProfile.osDisk.managedDisk.id" | tr -d '"'`
        vmosmdtyp=`echo $azr | jq ".[(${i})].storageProfile.osDisk.managedDisk.storageAccountType" | tr -d '"'`


        if [ "$vmoscreoption" = "Attach" ]; then
            if [ "$vmosmdtyp" != "null" ]; then
                printf "\tmanaged_disk_type = \"%s\" \n" $vmosmdtyp >> $outfile
            fi
            if [ "$vmosmdid" != "null" ]; then
                printf "\tmanaged_disk_id = \"%s\" \n" $vmosmdid >> $outfile
            fi
        fi

        printf "}\n" >> $outfile
        #if [ "$vmosmdid" != "null" ]; then
        #    if [ $havesir -eq 0 ]; then
                #printf "storage_image_reference {}\n"  >> $outfile
        #    fi
        #fi

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
                printf "storage_data_disk {\n"  >> $outfile
                printf "\t name = \"%s\"\n" $ddname >> $outfile
                printf "\t create_option = \"%s\"\n" $ddcreopt >> $outfile
                printf "\t lun = \"%s\"\n" $ddlun >> $outfile
                # caching , disk_size_gn, write_accelerator_enabled 
                
                if [ "$ddcreopt" = "Attach" ]; then
                    if [ "$ddmd" != "null" ];then
                    ddmdid=`echo $datadisks | jq ".[(${j})].managedDisk.id" | cut -d'/' -f9 | sed 's/\./-/g' | tr -d '"'`
                    ddmdrg=`echo $datadisks | jq ".[(${j})].managedDisk.id" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
                    ## ddmdrg  from cut is upper case - not good
                    ## probably safe to assume managed disk in same RG as VM ??
                    # check id lowercase rg = ddmdrg if so use rg
                    #
                    #if not will have to get from terraform state - convert ddmdrg to lc and terraform state output
                    #
                    
                    printf "\t managed_disk_id = \"\${azurerm_managed_disk.%s__%s.id}\"\n" $rg $ddmdid >> $outfile
                    fi
                fi
                if [ "$ddvhd" != "null" ]; then
                    printf "\t vhd_uri = \"%s\"\n" $ddvhd >> $outfile
                fi
                
                printf "}\n" >> $outfile
            fi
        done
        
        #
        # New Tags block v2
        tags=`echo $azr | jq ".[(${i})].tags"`
        tt=`echo $tags | jq .`
        tcount=`echo $tags | jq '. | length'`
        if [ "$tcount" -gt "0" ]; then
            printf "\t tags { \n" >> $outfile
            tt=`echo $tags | jq .`
            keys=`echo $tags | jq 'keys'`
            tcount=`expr $tcount - 1`
            for j in `seq 0 $tcount`; do
                k1=`echo $keys | jq ".[(${j})]"`
                #echo "key=$k1"
                re="[[:space:]]+"
                if [[ $k1 =~ $re ]]; then
                #echo "found a space"
                tval=`echo $tt | jq ."$k1"`
                tkey=`echo $k1 | tr -d '"'`
                printf "\t\t\"%s\" = %s \n" "$tkey" "$tval" >> $outfile
                else
                #echo "found no space"
                tval=`echo $tt | jq .$k1`
                tkey=`echo $k1 | tr -d '"'`
                printf "\t\t%s = %s \n" $tkey "$tval" >> $outfile
                fi
            done
            printf "\t}\n" >> $outfile
        fi
           
        printf "}\n" >> $outfile
        cat $outfile
        statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $rname`
        echo $statecomm >> tf-staterm.sh
        eval $statecomm
        evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $rname $id`
        echo $evalcomm >> tf-stateimp.sh
        eval $evalcomm
    done
fi

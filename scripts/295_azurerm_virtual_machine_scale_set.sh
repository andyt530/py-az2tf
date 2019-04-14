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
azr=`az vmss list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`

        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`
        upm=`echo $azr | jq ".[(${i})].upgradePolicy.mode" | tr -d '"'`
        op=`echo $azr | jq ".[(${i})].overprovision" | tr -d '"'`
        spg=`echo $azr | jq ".[(${i})].singlePlacementGroup" | tr -d '"'`
        vmlic=`echo $azr | jq ".[(${i})].virtualMachineProfile.licenseType" | tr -d '"'`
        vmpri=`echo $azr | jq ".[(${i})].virtualMachineProfile.priority" | tr -d '"'`


        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile


        vmtype=`echo $azr | jq ".[(${i})].virtualMachineProfile.storageProfile.osDisk.osType" | tr -d '"'`
        datadisks=`echo $azr | jq ".[(${i})].virtualMachineProfile.storageProfile.dataDisks"`

        vmosdiskname=`echo $azr | jq ".[(${i})].virtualMachineProfile.storageProfile.osDisk.name" | tr -d '"'`
        vmosdiskcache=`echo $azr | jq ".[(${i})].virtualMachineProfile.storageProfile.osDisk.caching" | tr -d '"'`
        vmosvhdc=`echo $azr | jq ".[(${i})].virtualMachineProfile.storageProfile.osDisk.vhdContainers"`
        vmoscreoption=`echo $azr | jq ".[(${i})].virtualMachineProfile.storageProfile.osDisk.createOption" | tr -d '"'`
        vmoswa=`echo $azr | jq ".[(${i})].virtualMachineProfile.storageProfile.osDisk.writeAcceleratorEnabled" | tr -d '"'`
        #  
        osvhd=`echo $azr | jq ".[(${i})].virtualMachineProfile.osProfile.linuxConfiguration.ssh.publicKeys[0].keyData" | tr -d '"'`
        #
        vmimid=`echo $azr | jq ".[(${i})].virtualMachineProfile.storageProfile.imageReference.id" | tr -d '"'`

        vmimoffer=`echo $azr | jq ".[(${i})].virtualMachineProfile.storageProfile.imageReference.offer" | tr -d '"'`
        vmimpublisher=`echo $azr | jq ".[(${i})].virtualMachineProfile.storageProfile.imageReference.publisher" | tr -d '"'`
        vmimsku=`echo $azr | jq ".[(${i})].virtualMachineProfile.storageProfile.imageReference.sku" | tr -d '"'`
        vmimversion=`echo $azr | jq ".[(${i})].virtualMachineProfile.storageProfile.imageReference.version" | tr -d '"'`
        #

        vmdispw=`echo $azr | jq ".[(${i})].virtualMachineProfile.osProfile.linuxConfiguration.disablePasswordAuthentication" | tr -d '"'`
        vmsshpath=`echo $azr | jq ".[(${i})].virtualMachineProfile.osProfile.linuxConfiguration.ssh.publicKeys[0].path" | tr -d '"'`
        vmsshkey=`echo $azr | jq ".[(${i})].virtualMachineProfile.osProfile.linuxConfiguration.ssh.publicKeys[0].keyData" | tr -d '"'`
        #
        vmplname=`echo $azr | jq ".[(${i})].plan.name" | tr -d '"'`  
        #
# basic settings 
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "name = \"%s\"\n" $name >> $outfile
        printf "location = \"%s\"\n"  $loc >> $outfile
# sku block
        skun=`echo $azr | jq ".[(${i})].sku.name" | tr -d '"'`
        skuc=`echo $azr | jq ".[(${i})].sku.capacity" | tr -d '"'`
        skut=`echo $azr | jq ".[(${i})].sku.tier" | tr -d '"'`
        printf "sku {\n" $upm >> $outfile
        printf "\tname = \"%s\"\n" $skun >> $outfile
        printf "\ttier = \"%s\"\n" $skut >> $outfile
        printf "\tcapacity = \"%s\"\n" $skuc >> $outfile
        printf "}\n" $upm >> $outfile
# basic settings continued
        printf "resource_group_name = \"%s\"\n" $rgsource >> $outfile
        if [ "$vmlic" != "null" ]; then 
            printf "license_type = \"%s\"\n" $vmlic >> $outfile
        fi     
        printf "upgrade_policy_mode = \"%s\"\n" $upm >> $outfile
        printf "overprovision = \"%s\"\n" $op >> $outfile
        printf "single_placement_group = \"%s\"\n" $spg >> $outfile
        if [ "$vmpri" != "null" ]; then 
        printf "priority = \"%s\"\n" $vmpri >> $outfile
        fi
#os_profile block
        vmadmin=`echo $azr | jq ".[(${i})].virtualMachineProfile.osProfile.adminUsername" | tr -d '"'`
        vmadminpw=`echo $azr | jq ".[(${i})].virtualMachineProfile.osProfile.Password" | tr -d '"'`
        vmcn=`echo $azr | jq ".[(${i})].virtualMachineProfile.osProfile.computerNamePrefix" | tr -d '"'`
        printf "os_profile {\n" >> $outfile
        printf "\tcomputer_name_prefix = \"%s\"\n" $vmcn >> $outfile
        printf "\tadmin_username = \"%s\"\n" $vmadmin >> $outfile
        if [ "$vmadminpw" != "null" ]; then
        printf "\tadmin_password = \"%s\"\n" $vmadminpw >> $outfile
        fi
        printf "}\n" >> $outfile

# os_profile_secrets - not used ?

# os_profile_windows_config
        winb=`echo $azr | jq ".[(${i})].virtualMachineProfile.osProfile.windowsConfiguration"`
        
       #
        if [ "$winb" != "null" ]; then
            vmwau=`echo $azr | jq ".[(${i})].virtualMachineProfile.osProfile.windowsConfiguration.enableAutomaticUpdates" | tr -d '"'`
            vmwvma=`echo $azr | jq ".[(${i})].virtualMachineProfile.osProfile.windowsConfiguration.provisionVmAgent" | tr -d '"'`
            vmwtim=`echo $azr | jq ".[(${i})].virtualMachineProfile.osProfile.windowsConfiguration.timeZone"`
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

# os_profile_linux_config block
        linuxb=`echo $azr | jq ".[(${i})].virtualMachineProfile.osProfile.linuxConfiguration"`
        

        if [ "$linuxb" != "null" ]; then
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

# network profile block
        netifs=`echo $azr | jq ".[(${i})].virtualMachineProfile.networkProfile.networkInterfaceConfigurations"`      
        icount=`echo $netifs | jq '. | length'`
        if [ "$icount" -gt "0" ]; then
            icount=`expr $icount - 1`
            for j in `seq 0 $icount`; do
                printf "network_profile {\n" >> $outfile
                nn=`echo $azr | jq ".[(${i})].virtualMachineProfile.networkProfile.networkInterfaceConfigurations[(${j})].name" | tr -d '"'`
                pri=`echo $azr | jq ".[(${i})].virtualMachineProfile.networkProfile.networkInterfaceConfigurations[(${j})].primary" | tr -d '"'`
                ipc=`echo $azr | jq ".[(${i})].virtualMachineProfile.networkProfile.networkInterfaceConfigurations[(${j})].ipConfigurations"`
                printf "\tname = \"%s\"\n" $nn >> $outfile
                printf "\tprimary = \"%s\"\n" $pri >> $outfile
                kcount=`echo $ipc | jq '. | length'`
                if [ "$kcount" -gt "0" ]; then
                    kcount=`expr $kcount - 1`
                        for k in `seq 0 $kcount`; do
                            printf "\tip_configuration {\n" >> $outfile
                                ipcn=`echo $azr | jq ".[(${i})].virtualMachineProfile.networkProfile.networkInterfaceConfigurations[(${j})].ipConfigurations[(${k})].name" | tr -d '"'`
                                ipcp=`echo $azr | jq ".[(${i})].virtualMachineProfile.networkProfile.networkInterfaceConfigurations[(${j})].ipConfigurations[(${k})].primary" | tr -d '"'`
                                ipcsrg=`echo $azr | jq ".[(${i})].virtualMachineProfile.networkProfile.networkInterfaceConfigurations[(${j})].ipConfigurations[(${k})].subnet.id" | cut -f5 -d'/' | sed 's/\./-/g' | tr -d '"'`
                                ipcsn=`echo $azr | jq ".[(${i})].virtualMachineProfile.networkProfile.networkInterfaceConfigurations[(${j})].ipConfigurations[(${k})].subnet.id" | cut -f11 -d'/' | sed 's/\./-/g' | tr -d '"'`                    
                                beapids=`echo $azr | jq ".[(${i})].virtualMachineProfile.networkProfile.networkInterfaceConfigurations[(${j})].ipConfigurations[(${k})].loadBalancerBackendAddressPools"`
                                natrids=`echo $azr | jq ".[(${i})].virtualMachineProfile.networkProfile.networkInterfaceConfigurations[(${j})].ipConfigurations[(${k})].loadBalancerInboundNatPools"`                                
                                echo "*************************************************"
                                echo $beapids
                                echo $natrids  
                                echo "-------------------------------------------------"               
                                if [ "$ipcp" = "null" ]; then ipcp="";fi
                                printf "\t\tname = \"%s\"\n" $ipcn >> $outfile
                                printf "\t\tprimary = \"%s\"\n" $ipcp >> $outfile
                                printf "\t\tsubnet_id = \"\${azurerm_subnet.%s__%s.id}\"\n" $ipcsrg $ipcsn >> $outfile
                            printf "\t}\n" >> $outfile
                        done
                fi        
                printf "}\n" >> $outfile
            done
        fi

        #echo "*************************************************"
        #echo "-------------------------------------------------"
        #echo "================================================="

# storage_profile_os_disk  block
        printf "storage_profile_os_disk {\n"  >> $outfile
        printf "\tname = \"%s\" \n"  $vmosdiskname >> $outfile
        printf "\tcaching = \"%s\" \n" $vmosdiskcache  >>  $outfile
        if [ "$vmosacctype" != "" ]; then
            printf "\tmanaged_disk_type = \"%s\" \n" $vmosacctype >> $outfile
        fi

        printf "\tcreate_option = \"%s\" \n" $vmoscreoption >> $outfile
        if [ "$vmtype" = "null" ]; then vmtype="" ; fi
        printf "\tos_type = \"%s\" \n" $vmtype >> $outfile
        if [ "$vmoswa" != "null" ]; then
            printf "\t write_accelerator_enabled = \"%s\" \n" $vmoswa >> $outfile
        fi
        vmosvhdc=`echo $azr | jq ".[(${i})].virtualMachineProfile.storageProfile.osDisk.vhdContainers"`

        if [ "$vmosvhdc" != "null" ]; then
            printf "\tvhd_containers =  %s \n" "$vmosvhdc" >> $outfile
        fi
        printf "}\n" >> $outfile
        #
       
# storage_profile_data_disk  block
        
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
                printf "storage_profile_data_disk {\n"  >> $outfile
                printf "\t name = \"%s\"\n" $ddname >> $outfile
                printf "\t create_option = \"%s\"\n" $ddcreopt >> $outfile
                printf "\t lun = \"%s\"\n" $ddlun >> $outfile
                # caching , disk_size_gn, write_accelerator_enabled 
                
                if [ "$ddcreopt" = "Attach" ]; then
                    if ["$ddmd" != "null" ];then
                    ddmdid=`echo $datadisks | jq ".[(${j})].managedDisk.id" | cut -d'/' -f9 | sed 's/\./-/g' | tr -d '"'`
                    ddmdrg=`echo $datadisks | jq ".[(${j})].managedDisk.id" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
                    ## ddmdrg from cut is upper case - not good
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

# storage_profile_image_reference block

        if [ "$vmimid" = "null" ]; then
            if [ "$vmimpublisher" != "null" ];then
            printf "storage_profile_image_reference {\n"  >> $outfile
            printf "\t publisher = \"%s\"\n" $vmimpublisher  >> $outfile
            printf "\t offer = \"%s\"\n"  $vmimoffer >> $outfile
            printf "\t sku = \"%s\"\n"  $vmimsku >> $outfile
            printf "\t version = \"%s\"\n"  $vmimversion >> $outfile
            
            printf "}\n" >> $outfile
            fi
          
        fi

# extensions

# boot diagnostics block

        vmdiags=`echo $azr | jq ".[(${i})].virtualMachineProfile.diagnosticsProfile" | tr -d '"'`
        vmbturi=`echo $azr | jq ".[(${i})].virtualMachineProfile.diagnosticsProfile.bootDiagnostics.storageUri" | tr -d '"'`
        vmbten=`echo $azr | jq ".[(${i})].virtualMachineProfile.diagnosticsProfile.bootDiagnostics.enabled" | tr -d '"'`

        if [ "$vmdiags" != "null" ]; then
            printf "boot_diagnostics {\n"  >> $outfile
            printf "\t enabled = \"%s\"\n" $vmbten >> $outfile
            printf "\t storage_uri = \"%s\"\n" $vmbturi >> $outfile
            printf "}\n" >> $outfile
        fi

# plan block
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

# zones block
        
# finish

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

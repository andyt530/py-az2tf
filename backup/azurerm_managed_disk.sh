tfp="azurerm_managed_disk"
prefixa="md"
if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
azr=`az disk list -g $rgsource`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        # note the fixup to name - as some folks put ".vhd" in the name
        oname=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | tr -d '"'`
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`
        prefix=`printf "%s__%s" $prefixa $rg`
       
        dsize=`echo $azr | jq ".[(${i})].diskSizeGb" | tr -d '"'`
        ostyp=`echo $azr | jq ".[(${i})].osType" | tr -d '"'`
        creopt=`echo $azr | jq ".[(${i})].creationData.createOption" | tr -d '"'`
        creid=`echo $azr | jq ".[(${i})].creationData.sourceResourceId" | tr -d '"'`
        enc=`echo $azr | jq ".[(${i})].encryptionSettings.enabled" | tr -d '"'`
        kekurl=`echo $azr | jq ".[(${i})].encryptionSettings.keyEncryptionKey.keyUrl" | tr -d '"'`
        kekvltid=`echo $azr | jq ".[(${i})].encryptionSettings.keyEncryptionKey.sourceVault.id" | tr -d '"'`
        dekurl=`echo $azr | jq ".[(${i})].encryptionSettings.diskEncryptionKey.secretUrl" | tr -d '"'`
        dekvltid=`echo $azr | jq ".[(${i})].encryptionSettings.diskEncryptionKey.sourceVault.id" | tr -d '"'`

        stopt=`echo $azr | jq ".[(${i})].sku.name" | tr -d '"'`
        imid=`echo $azr | jq ".[(${i})].creationData.imageReference.id" | tr -d '"'`
        name=`echo ${oname/.vhd/_vhd}` 
        echo "name=" $name


        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $name > $prefix-$name.tf
        printf "\t name = \"%s\"\n" $oname >> $prefix-$name.tf
        printf "\t location = \"%s\"\n" $loc >> $prefix-$name.tf
        #printf "\t resource_group_name = \"\${var.rgtarget}\"\n" >> $prefix-$name.tf
        printf "\t resource_group_name = \"%s\"\n" $rg >> $prefix-$name.tf
        printf "\t disk_size_gb = \"%s\"\n" $dsize >> $prefix-$name.tf
        if [ "$ostyp" != "null" ]; then 
            printf "\t os_type = \"%s\"\n" $ostyp >> $prefix-$name.tf
        fi
        if [ "$imid" != "null" ]; then 
            printf "\t image_reference_id = \"%s\"\n" $imid >> $prefix-$name.tf
        fi
        if [ "$creopt" != "null" ]; then 
            printf "\t create_option = \"%s\"\n" $creopt >> $prefix-$name.tf
        fi
        if [ "$creid" != "null" ]; then 
            printf "\t source_resource_id = \"%s\"\n" $creid >> $prefix-$name.tf
        fi
        if [ "$enc" != "null" ]; then 
            printf "\t encryption_settings {\n" >> $prefix-$name.tf
            printf "\t\t enabled = \"%s\"\n" $enc >> $prefix-$name.tf
            if [ "$kekurl" != "null" ]; then 
                printf "\t\t key_encryption_key {\n" >> $prefix-$name.tf
                printf "\t\t\t key_url = \"%s\"\n" $kekurl >> $prefix-$name.tf
                printf "\t\t\t source_vault_id = \"%s\"\n" $kekvltid >> $prefix-$name.tf
                printf "\t\t }\n" >> $prefix-$name.tf
            fi
            if [ "$dekurl" != "null" ]; then 
                printf "\t\t disk_encryption_key {\n" >> $prefix-$name.tf
                printf "\t\t\t secret_url = \"%s\"\n" $dekurl >> $prefix-$name.tf
                printf "\t\t\t source_vault_id = \"%s\"\n" $dekvltid >> $prefix-$name.tf               
                printf "\t\t }\n" >> $prefix-$name.tf

            fi

            printf "\t }\n" >> $prefix-$name.tf
        fi

        if [ "$stopt" != "null" ]; then 
            printf "\t storage_account_type = \"%s\"\n" $stopt >> $prefix-$name.tf
        fi


        printf "}\n" >> $prefix-$name.tf
        #
        cat $prefix-$name.tf
        statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $name`
        echo $statecomm >> tf-staterm.sh
        eval $statecomm
        evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $name $id`
        echo $evalcomm >> tf-stateimp.sh
        eval $evalcomm
    done
fi

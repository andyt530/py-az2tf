
azr=`az disk list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        # note the fixup to name - as some folks put ".vhd" in the name
        oname=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        name=`echo ${oname/.vhd/_vhd}` 
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g'| tr -d '"'`

        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`
        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile

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

        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $oname >> $outfile
        printf "\t location = \"%s\"\n" $loc >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
        printf "\t disk_size_gb = \"%s\"\n" $dsize >> $outfile
        if [ "$ostyp" != "null" ]; then 
            printf "\t os_type = \"%s\"\n" $ostyp >> $outfile
        fi
        if [ "$imid" != "null" ]; then 
            printf "\t image_reference_id = \"%s\"\n" $imid >> $outfile
        fi
        if [ "$creopt" != "null" ]; then 
            printf "\t create_option = \"%s\"\n" $creopt >> $outfile
        fi
        if [ "$creid" != "null" ]; then 
            printf "\t source_resource_id = \"%s\"\n" $creid >> $outfile
        fi
        if [ "$enc" != "null" ]; then 
            printf "\t encryption_settings {\n" >> $outfile
            printf "\t\t enabled = \"%s\"\n" $enc >> $outfile
            if [ "$kekurl" != "null" ]; then 
                printf "\t\t key_encryption_key {\n" >> $outfile
                printf "\t\t\t key_url = \"%s\"\n" $kekurl >> $outfile
                printf "\t\t\t source_vault_id = \"%s\"\n" $kekvltid >> $outfile
                printf "\t\t }\n" >> $outfile
            fi
            if [ "$dekurl" != "null" ]; then 
                printf "\t\t disk_encryption_key {\n" >> $outfile
                printf "\t\t\t secret_url = \"%s\"\n" $dekurl >> $outfile
                printf "\t\t\t source_vault_id = \"%s\"\n" $dekvltid >> $outfile               
                printf "\t\t }\n" >> $outfile

            fi

            printf "\t }\n" >> $outfile
        fi

        if [ "$stopt" != "null" ]; then 
            printf "\t storage_account_type = \"%s\"\n" $stopt >> $outfile
        fi


        printf "}\n" >> $outfile
        #

    done
fi

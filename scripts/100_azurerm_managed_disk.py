
azr=az disk list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        # note the fixup to name - as some folks put ".vhd" in the name
        oname=azr[i]["name"]
        name=print {'oname/.vhd/_vhd}' 
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g'| tr -d '"'

        id=azr[i]["id"]
        loc=azr[i]["location"]
        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outfile

        dsize=azr[i]["diskSizeGb"]
        ostyp=azr[i]["osType"]
        creopt=azr[i]["creationData.createOption"]
        creid=azr[i]["creationData.sourceResourceId"]
        enc=azr[i]["encryptionSettings.enabled"]
        kekurl=azr[i]["encryptionSettings.keyEncryptionKey.keyUrl"]
        kekvltid=azr[i]["encryptionSettings.keyEncryptionKey.sourceVault.id"]
        dekurl=azr[i]["encryptionSettings.diskEncryptionKey.secretUrl"]
        dekvltid=azr[i]["encryptionSettings.diskEncryptionKey.sourceVault.id"]

        stopt=azr[i]["sku.name"]
        imid=azr[i]["creationData.imageReference.id"]

        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  oname + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t disk_size_gb = "' +  dsize + '"\n')
        if ostyp" != "null" : 
            fr.write('\t os_type = "' +  ostyp + '"\n')
        fi
        if imid" != "null" : 
            fr.write('\t image_reference_id = "' +  imid + '"\n')
        fi
        if creopt" != "null" : 
            fr.write('\t create_option = "' +  creopt + '"\n')
        fi
        if creid" != "null" : 
            fr.write('\t source_resource_id = "' +  creid + '"\n')
        fi
        if enc" != "null" : 
            fr.write('\t encryption_settings {' + '"\n')
            fr.write('\t\t enabled = "' +  enc + '"\n')
            if kekurl" != "null" : 
                fr.write('\t\t key_encryption_key {' + '"\n')
                fr.write('\t\t\t key_url = "' +  kekurl + '"\n')
                fr.write('\t\t\t source_vault_id = "' +  kekvltid + '"\n')
                fr.write('\t\t }' + '"\n')
            fi
            if dekurl" != "null" : 
                fr.write('\t\t disk_encryption_key {' + '"\n')
                fr.write('\t\t\t secret_url = "' +  dekurl + '"\n')
                fr.write('\t\t\t source_vault_id = "' +  dekvltid + '"\n')               
                fr.write('\t\t }' + '"\n')

            fi

            fr.write('\t }' + '"\n')
        fi

        if stopt" != "null" : 
            fr.write('\t storage_account_type = "' +  stopt + '"\n')
        fi


        fr.write('}' + '"\n')
        #

    
fi

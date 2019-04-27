
azr=az snapshot list -g rgsource -o json
count=print azr | jq '. | length'
if count" != "0" :
    count=expr count - 1
    for i in range( 0 count):
        name=azr[i]["name"]
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']

        id=azr[i]["id"]
        loc=azr[i]["location"]
        co=azr[i]["creationData.createOption"]
        sz=azr[i]["diskSizeGb"]

        suri=azr[i]["creationData.sourceUri"]
        srid=azr[i]["creationData.sourceResourceId"]
        said=azr[i]["creationData.storageAccountId"]

        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outfile
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t create_option = "' +  co + '"\n')
        
        if sz" != "null" :
        fr.write('\t disk_size_gb = "' +  sz + '"\n')
        fi
        #if suri" != "null" :
        #    fr.write('\t source_uri = "' +  suri + '"\n')
        #fi
        #if srid" != "null" :
        #    fr.write('\t source_resource_id = "' +  srid + '"\n')
        #fi
        #if said" != "null" :
        #    fr.write('\t source_account_id = "' +  said + '"\n')
        #fi        

        
        #
        fr.write('}' + '"\n')
        #

        
    
fi

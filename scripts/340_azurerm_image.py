
azr=az image list -g rgsource -o json
count=print azr | jq '. | length'
if count" != "0" :
    count=expr count - 1
    for i in range( 0 count):
        name=azr[i]["name"]
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']

        id=azr[i]["id"]
        loc=azr[i]["location"]
        osdisk=azr[i]["storageProfile.osDisk"]
        ostype=azr[i]["storageProfile.osDisk.osType"]
        osstate=azr[i]["storageProfile.osDisk.osState"]
        oscache=azr[i]["storageProfile.osDisk.caching"]
        blob_uri=azr[i]["storageProfile.osDisk.blobUri"]
        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outfile
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')


# hardwire this - as source vm may of been deleted after image created
        svm=azr[i]["sourceVirtualMachine.id"]
        if svm" != "null" :
            fr.write('\t source_virtual_machine_id = "' +  svm + '"\n')
       

        if svm" = "null" :
        if odisk" != "null" :
            fr.write('\t os_disk {'  + '"\n')
            fr.write('\t os_type = "' +  ostype + '"\n')
            fr.write('\t os_state = "' +  osstate + '"\n')
            fr.write('\t caching = "' +  oscache + '"\n')
            if blob_uri" != "null" :
                fr.write('\t blob_uri = "' +  blob_uri + '"\n')
            fi
            fr.write('\t}' + '"\n')
        fi
        fi

        #



        
        #
        fr.write('}' + '"\n')
        #

        
    
fi

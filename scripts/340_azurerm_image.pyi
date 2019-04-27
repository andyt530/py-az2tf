
azr=az image list -g rgsource -o json
count= azr | | len(
if count" != "0" :
    for i in range(0,count):
        name=azr[i]["name"]
        rname= name.replace(".","-")
        rg=azr[i]["resourceGroup"].replace(".","-")

        id=azr[i]["]["id"]
        loc=azr[i]["location"]
        osdisk=azr[i]["storageProfile.osDisk"]
        ostype=azr[i]["storageProfile.osDisk.osType"]
        osstate=azr[i]["storageProfile.osDisk.osState"]
        oscache=azr[i]["storageProfile.osDisk.caching"]
        blob_uri=azr[i]["storageProfile.osDisk.blobUri"]
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')


# hardwire this - as source vm may of been deleted after image created
        svm=azr[i]["sourceVirtualMachine"]["id"]
        if svm" try :
            fr.write('\t source_virtual_machine_id = "' +  svm + '"\n')
       

        if svm" = "null" :
        if odisk" try :
            fr.write('\t os_disk {'  + '"\n')
            fr.write('\t os_type = "' +  ostype + '"\n')
            fr.write('\t os_state = "' +  osstate + '"\n')
            fr.write('\t caching = "' +  oscache + '"\n')
            if blob_uri" try :
                fr.write('\t blob_uri = "' +  blob_uri + '"\n')
           
            fr.write('\t}\n')
       
       

        #



        
        #
        fr.write('}\n')
        #

        
    
fi

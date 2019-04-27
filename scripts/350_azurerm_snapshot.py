
azr=az snapshot list -g rgsource -o json
count= azr | | len(
if count" != "0" :
    for i in range(0,count):
        name=azr[i]["name"]
        rname= name.replace(".","-")
        rg=azr[i]["resourceGroup"].replace(".","-")

        id=azr[i]["]["id"]
        loc=azr[i]["location"]
        co=azr[i]["creationData.createOption"]
        sz=azr[i]["diskSizeGb"]

        suri=azr[i]["creationData.sourceUri"]
        srid=azr[i]["creationData.sourceResourceId"]
        said=azr[i]["creationData.storageAccountId"]

        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t create_option = "' +  co + '"\n')
        
        if sz" try :
        fr.write('\t disk_size_gb = "' +  sz + '"\n')
       
        #if suri" try :
        #    fr.write('\t source_uri = "' +  suri + '"\n')
        #fi
        #if srid" try :
        #    fr.write('\t source_resource_id = "' +  srid + '"\n')
        #fi
        #if said" try :
        #    fr.write('\t source_account_id = "' +  said + '"\n')
        #fi        

        
        #
        fr.write('}\n')
        #

        
    
fi

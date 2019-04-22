
azr=`az image list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" != "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`

        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`
        osdisk=`echo $azr | jq ".[(${i})].storageProfile.osDisk" | tr -d '"'`
        ostype=`echo $azr | jq ".[(${i})].storageProfile.osDisk.osType" | tr -d '"'`
        osstate=`echo $azr | jq ".[(${i})].storageProfile.osDisk.osState" | tr -d '"'`
        oscache=`echo $azr | jq ".[(${i})].storageProfile.osDisk.caching" | tr -d '"'`
        blob_uri=`echo $azr | jq ".[(${i})].storageProfile.osDisk.blobUri" | tr -d '"'`
        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        printf "\t location = \"%s\"\n" $loc >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile


# hardwire this - as source vm may of been deleted after image created
        svm=`echo $azr | jq ".[(${i})].sourceVirtualMachine.id" | tr -d '"'`
        if [ "$svm" != "null" ]; then
            printf "\t source_virtual_machine_id = \"%s\"\n" $svm >> $outfile
        fi 

        if [ "$svm" = "null" ]; then
        if [ "$odisk" != "null" ]; then
            printf "\t os_disk { \n" >> $outfile
            printf "\t os_type = \"%s\"\n" $ostype >> $outfile
            printf "\t os_state = \"%s\"\n" $osstate >> $outfile
            printf "\t caching = \"%s\"\n" $oscache >> $outfile
            if [ "$blob_uri" != "null" ]; then
                printf "\t blob_uri = \"%s\"\n" $blob_uri >> $outfile
            fi
            printf "\t}\n" >> $outfile
        fi
        fi

        #



        
        #
        printf "}\n" >> $outfile
        #

        
    done
fi

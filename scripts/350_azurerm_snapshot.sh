
azr=`az snapshot list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" != "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`

        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`
        co=`echo $azr | jq ".[(${i})].creationData.createOption" | tr -d '"'`
        sz=`echo $azr | jq ".[(${i})].diskSizeGb" | tr -d '"'`

        suri=`echo $azr | jq ".[(${i})].creationData.sourceUri" | tr -d '"'`
        srid=`echo $azr | jq ".[(${i})].creationData.sourceResourceId" | tr -d '"'`
        said=`echo $azr | jq ".[(${i})].creationData.storageAccountId" | tr -d '"'`

        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        printf "\t location = \"%s\"\n" $loc >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
        printf "\t create_option = \"%s\"\n" $co >> $outfile
        
        if [ "$sz" != "null" ]; then
        printf "\t disk_size_gb = \"%s\"\n" $sz >> $outfile
        fi
        #if [ "$suri" != "null" ]; then
        #    printf "\t source_uri = \"%s\"\n" $suri >> $outfile
        #fi
        #if [ "$srid" != "null" ]; then
        #    printf "\t source_resource_id = \"%s\"\n" $srid >> $outfile
        #fi
        #if [ "$said" != "null" ]; then
        #    printf "\t source_account_id = \"%s\"\n" $said >> $outfile
        #fi        

        
        #
        printf "}\n" >> $outfile
        #

        
    done
fi

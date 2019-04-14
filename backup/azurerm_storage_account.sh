tfp="azurerm_storage_account"
prefixa="stor"
if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
azr=`az storage account list -g $rgsource`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        #echo $i
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | tr -d '"'`
        
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`
        
        
        prefix=`printf "%s__%s" $prefixa $rg`
        satier=`echo $azr | jq ".[(${i})].sku.tier" | tr -d '"'`
        sakind=`echo $azr | jq ".[(${i})].kind" | tr -d '"'`
        sartype=`echo $azr | jq ".[(${i})].sku.name" | cut -f2 -d'_' | tr -d '"'`
        saencrypt=`echo $azr | jq ".[(${i})].encryption.services.blob.enabled" | tr -d '"'`
        fiencrypt=`echo $azr | jq ".[(${i})].encryption.services.file.enabled" | tr -d '"'`
        sahttps=`echo $azr | jq ".[(${i})].enableHttpsTrafficOnly" | tr -d '"'`
        nrs=`echo $azr | jq ".[(${i})].networkRuleSet" | tr -d '"'`
        
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $name > $prefix-$name.tf
        printf "\t name = \"%s\"\n" $name >> $prefix-$name.tf
        printf "\t location = \"%s\"\n" $loc >> $prefix-$name.tf
        #printf "\t resource_group_name = \"\${var.rgtarget}\"\n" >> $prefix-$name.tf
        printf "\t resource_group_name = \"%s\"\n" $rg >> $prefix-$name.tf
        printf "\t account_tier = \"%s\"\n" $satier >> $prefix-$name.tf
        printf "\t account_kind = \"%s\"\n" $sakind >> $prefix-$name.tf
        printf "\t account_replication_type = \"%s\"\n" $sartype >> $prefix-$name.tf
        printf "\t enable_blob_encryption = \"%s\"\n" $saencrypt >> $prefix-$name.tf
        printf "\t enable_file_encryption = \"%s\"\n" $fiencrypt >> $prefix-$name.tf
        printf "\t enable_https_traffic_only = \"%s\"\n" $sahttps >> $prefix-$name.tf
        #
        
        #
        # New Tags block
        tags=`echo $azr | jq ".[(${i})].tags"`
        tt=`echo $tags | jq .`
        tcount=`echo $tags | jq '. | length'`
        if [ "$tcount" -gt "0" ]; then
            printf "\t tags { \n" >> $prefix-$name.tf
            tt=`echo $tags | jq .`
            keys=`echo $tags | jq 'keys'`
            tcount=`expr $tcount - 1`
            for j in `seq 0 $tcount`; do
                k1=`echo $keys | jq ".[(${j})]"`
                tval=`echo $tt | jq .$k1`
                tkey=`echo $k1 | tr -d '"'`
                printf "\t\t%s = %s \n" $tkey "$tval" >> $prefix-$name.tf
            done
            printf "\t}\n" >> $prefix-$name.tf
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

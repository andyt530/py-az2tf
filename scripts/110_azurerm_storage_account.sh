
azr=`az storage account list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        #echo $i
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`
        
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`
                
        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile

        satier=`echo $azr | jq ".[(${i})].sku.tier" | tr -d '"'`
        sakind=`echo $azr | jq ".[(${i})].kind" | tr -d '"'`
        sartype=`echo $azr | jq ".[(${i})].sku.name" | cut -f2 -d'_' | tr -d '"'`
        saencrypt=`echo $azr | jq ".[(${i})].encryption.services.blob.enabled" | tr -d '"'`
        fiencrypt=`echo $azr | jq ".[(${i})].encryption.services.file.enabled" | tr -d '"'`
        sahttps=`echo $azr | jq ".[(${i})].enableHttpsTrafficOnly" | tr -d '"'`
        nrs=`echo $azr | jq ".[(${i})].networkRuleSet"`
        saencs=`echo $azr | jq ".[(${i})].encryption.keySource" | tr -d '"'`
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        printf "\t location = \"%s\"\n" $loc >> $outfile
        
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
        printf "\t account_tier = \"%s\"\n" $satier >> $outfile
        printf "\t account_kind = \"%s\"\n" $sakind >> $outfile
        printf "\t account_replication_type = \"%s\"\n" $sartype >> $outfile
        printf "\t enable_blob_encryption = \"%s\"\n" $saencrypt >> $outfile
        printf "\t enable_file_encryption = \"%s\"\n" $fiencrypt >> $outfile
        printf "\t enable_https_traffic_only = \"%s\"\n" $sahttps >> $outfile
        printf "\t account_encryption_source = \"%s\"\n" $saencs >> $outfile
        
        if [ "$nrs.bypass" != "null" ]; then
            byp=`echo $azr | jq ".[(${i})].networkRuleSet.bypass" | tr -d '"'`
            ipr=`echo $azr | jq ".[(${i})].networkRuleSet.ipRules"`
            vnr=`echo $azr | jq ".[(${i})].networkRuleSet.virtualNetworkRules"`

            icount=`echo $ipr | jq '. | length'`
            vcount=`echo $vnr | jq '. | length'`
            
            # if the only network rule is AzureServices, dont need a network_rules block
            if [ "$byp" != "AzureServices" ] || [ "$icount" -gt "0" ] || [ "$vcount" -gt "0" ]; then
                printf "\t network_rules { \n" >> $outfile
                byp=`echo $byp | tr -d ','`
                printf "\t\t bypass = [\"%s\"]\n" $byp >> $outfile

                if [ "$icount" -gt "0" ]; then
                    icount=`expr $icount - 1`
                    for ic in `seq 0 $icount`; do 
                        ipa=`echo $ipr | jq ".[(${ic})].ipAddressOrRange" | tr -d '"'`
                        printf "\t\t ip_rules = [\"%s\"]\n" $ipa >> $outfile
                    done
                fi
                
                if [ "$vcount" -gt "0" ]; then
                    vcount=`expr $vcount - 1`
                    for vc in `seq 0 $vcount`; do
                        vnsid=`echo $vnr | jq ".[(${vc})].virtualNetworkResourceId" | tr -d '"'`
                        printf "\t\t virtual_network_subnet_ids = [\"%s\"]\n" $vnsid >> $outfile
                    done
                fi

                printf "\t } \n" >> $outfile
            fi
        fi


                
        printf "}\n" >> $outfile


    done
fi


azr=`az network public-ip list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`
        sku=`echo $azr | jq ".[(${i})].sku.name" | tr -d '"'`
        timo=`echo $azr | jq ".[(${i})].idleTimeoutInMinutes" | tr -d '"'`
        dnsname=`echo $azr | jq ".[(${i})].dnsSettings.domainNameLabel" | tr -d '"'`
        dnsfqdn=`echo $azr | jq ".[(${i})].dnsSettings.fqdn" | tr -d '"'`

        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile

        subipalloc=`echo $azr | jq ".[(${i})].publicIpAllocationMethod" | tr -d '"'`
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        printf "\t location = \"%s\"\n" $loc >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
        printf "\t allocation_method = \"%s\" \n"  $subipalloc >> $outfile
        if [ "$sku" != "null" ]; then
            printf "\t sku = \"%s\" \n"  $sku >> $outfile
        fi
        #printf "\t idle_timeout_in_minutes = \"%s\" \n"  $timo >> $outfile
        if [ "$dnsname" != "null" ]; then
        printf "\t domain_name_label = \"%s\"\n" $dnsname >> $outfile
        fi
        #
        printf "}\n" >> $outfile
        #
        cat $outfile

    done
fi

tfp="azurerm_availability_set"
prefixa="avs"
if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
azr=`az vm availability-set list -g $rgsource`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        #name=`echo $name | awk '{print tolower($0)}'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | tr -d '"'`
        prefix=`printf "%s__%s" $prefixa $rg`
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location"`
        fd=`echo $azr | jq ".[(${i})].platformFaultDomainCount" | tr -d '"'`
        ud=`echo $azr | jq ".[(${i})].platformUpdateDomainCount" | tr -d '"'`
        avm=`echo $azr | jq ".[(${i})].virtualMachines"`
        skuname=`echo $azr | jq ".[(${i})].sku.name" | tr -d '"'`
        rmtype="false"
        if [ $skuname = "Aligned" ]; then
            #echo "skuname is true"
            rmtype="true"
        fi
        
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $name > $prefix-$name.tf
        printf "\t name = \"%s\"\n" $name >> $prefix-$name.tf
        #printf "\t id = \"%s\"\n" $id >> $prefix-$name.tf
        printf "\t location = %s\n" "$loc" >> $prefix-$name.tf
        #printf "\t resource_group_name = \"\${var.rgtarget}\"\n" >> $prefix-$name.tf
        printf "\t resource_group_name = \"%s\"\n" $rg >> $prefix-$name.tf
        printf "\t platform_fault_domain_count = \"%s\"\n" $fd >> $prefix-$name.tf
        printf "\t platform_update_domain_count = \"%s\"\n" $ud >> $prefix-$name.tf
        printf "\t managed = \"%s\"\n" $rmtype >> $prefix-$name.tf
        
        
        
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
        cat $prefix-$name.tf
        statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $name`
        echo $statecomm >> tf-staterm.sh
        eval $statecomm
        evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $name $id`
        echo $evalcomm >> tf-stateimp.sh
        eval $evalcomm
    done
fi

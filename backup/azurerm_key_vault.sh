tfp="azurerm_key_vault"
prefixa="kv"
if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
azr=`az keyvault list -g $rgsource`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        kvshow=`az keyvault show -n $name`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | tr -d '"'`
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location"`
        
        sku=`echo $kvshow | jq ".properties.sku.name" | tr -d '"'`
        ten=`echo $kvshow | jq ".properties.tenantId" | tr -d '"'`

        endep=`echo $kvshow | jq ".properties.enabledForDeployment" | tr -d '"'`
        endisk=`echo $kvshow | jq ".properties.enabledForDiskEncryption" | tr -d '"'`
        entemp=`echo $kvshow | jq ".properties.enabledForTemplateDeployment" | tr -d '"'`

        #echo $tags | jq .
        ap=`echo $kvshow | jq ".properties.accessPolicies"`
        
        prefix=`printf "%s__%s" $prefixa $rg`
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $name > $prefix-$name.tf
        printf "\t name = \"%s\"\n" $name >> $prefix-$name.tf
        printf "location = %s\n" "$loc" >> $prefix-$name.tf
        printf "\t resource_group_name = \"%s\"\n" $rg >> $prefix-$name.tf
        #
        printf "\t sku { \n" >> $prefix-$name.tf
        printf "\t\t name=\"%s\"\n" $sku >> $prefix-$name.tf
        printf "\t } \n" >> $prefix-$name.tf
        
        printf "\t tenant_id=\"%s\"\n" $ten >> $prefix-$name.tf
        printf "\t enabled_for_deployment=\"%s\"\n" $endep >> $prefix-$name.tf
        printf "\t enabled_for_disk_encryption=\"%s\"\n" $endisk >> $prefix-$name.tf
        printf "\t enabled_for_template_deployment=\"%s\"\n" $entemp >> $prefix-$name.tf

        #
        # Access Policies
        #
        pcount=`echo $ap | jq '. | length'`
        if [ "$pcount" -gt "0" ]; then
        
            pcount=`expr $pcount - 1`
            for j in `seq 0 $pcount`; do
                
                printf "\taccess_policy {\n" >> $prefix-$name.tf

                apten=`echo $kvshow | jq ".properties.accessPolicies[(${j})].tenantId" | tr -d '"'`
                apoid=`echo $kvshow | jq ".properties.accessPolicies[(${j})].objectId" | tr -d '"'`

                printf "\t\t tenant_id=\"%s\"\n" $apten >> $prefix-$name.tf
                printf "\t\t object_id=\"%s\"\n" $apoid >> $prefix-$name.tf
                
                kl=`echo $kvshow | jq ".properties.accessPolicies[(${j})].permissions.keys" | jq '. | length'`
                sl=`echo $kvshow | jq ".properties.accessPolicies[(${j})].permissions.secrets" | jq '. | length'`
                cl=`echo $kvshow | jq ".properties.accessPolicies[(${j})].permissions.certificates" | jq '. | length'`
               
                kl=`expr $kl - 1`
                sl=`expr $sl - 1`
                cl=`expr $cl - 1`
          
                printf "\t\t key_permissions = [\n" >> $prefix-$name.tf
                if [ "$kl" -ge "0" ]; then
                    
                    for k in `seq 0 $kl`; do
                        tk=`echo $kvshow | jq ".properties.accessPolicies[(${j})].permissions.keys[(${k})]"`
                        if [ $k -lt $kl ]; then
                            tk=`printf "%s," $tk`
                        fi
                        printf "\t\t\t%s\n" $tk >> $prefix-$name.tf
                    done
                    #printf "\t\t ]\n" >> $prefix-$name.tf
                fi
                printf "\t\t ]\n" >> $prefix-$name.tf
                
                if [ "$sl" -ge "0" ]; then
                    printf "\t\t secret_permissions = [\n" >> $prefix-$name.tf
                    for k in `seq 0 $sl`; do
                        tk=`echo $kvshow | jq ".properties.accessPolicies[(${j})].permissions.secrets[(${k})]"`
                        if [ $k -lt $sl ]; then
                            tk=`printf "%s," $tk`
                        fi
                        printf "\t\t\t%s\n" $tk >> $prefix-$name.tf
                    done
                    printf "\t\t ]\n" >> $prefix-$name.tf
                fi
                
                if [ "$cl" -gt "99" ]; then  # coded to prevent cert permissions until fix in tf provider
                    printf "\t\t certificate_permissions = [\n" >> $prefix-$name.tf
                    for k in `seq 0 $cl`; do
                        tk=`echo $kvshow | jq ".properties.accessPolicies[(${j})].permissions.certificates[(${k})]"`
                        echo $tk
                        if [ "$tk" != "Recover" ]; then
                            if [ $k -lt $cl ]; then
                                tk=`printf "%s," $tk`
                            fi
                            printf "\t\t\t%s\n" $tk >> $prefix-$name.tf
                        fi
                    done
                    printf "\t\t ]\n" >> $prefix-$name.tf
                fi
                
                printf "\t}\n" >> $prefix-$name.tf
            done
        fi

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

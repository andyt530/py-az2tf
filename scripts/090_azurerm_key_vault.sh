
azr=`az keyvault list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`

        kvshow=`az keyvault show -n $name -o json`
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location"`
        
        sku=`echo $kvshow | jq ".properties.sku.name" | tr -d '"'`
        #if [ "$sku" = "premium" ]; then sku="Premium" ; fi
        #if [ "$sku" = "standard" ]; then sku="Standard" ; fi

        ten=`echo $kvshow | jq ".properties.tenantId" | tr -d '"'`
        
        endep=`echo $kvshow | jq ".properties.enabledForDeployment" | tr -d '"'`
        endisk=`echo $kvshow | jq ".properties.enabledForDiskEncryption" | tr -d '"'`
        entemp=`echo $kvshow | jq ".properties.enabledForTemplateDeployment" | tr -d '"'`
        
        #echo $tags | jq .
        ap=`echo $kvshow | jq ".properties.accessPolicies"`
        
        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile

        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        printf "location = %s\n" "$loc" >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
        #
        printf "\t sku { \n" >> $outfile
        
        printf "\t\t name=\"%s\"\n" $sku >> $outfile
        printf "\t } \n" >> $outfile
        
        printf "\t tenant_id=\"%s\"\n" $ten >> $outfile
        if [ "$endep" != "null" ]; then
            printf "\t enabled_for_deployment=\"%s\"\n" $endep >> $outfile
        fi
        if [ "$endisk" != "null" ] ; then
            printf "\t enabled_for_disk_encryption=\"%s\"\n" $endisk >> $outfile
        fi
        if [ "$entemp" != "null" ]; then
        printf "\t enabled_for_template_deployment=\"%s\"\n" $entemp >> $outfile
        fi
        #
        # Access Policies
        #
        pcount=`echo $ap | jq '. | length'`
        if [ "$pcount" -gt "0" ]; then
            
            pcount=`expr $pcount - 1`
            for j in `seq 0 $pcount`; do
                
                printf "\taccess_policy {\n" >> $outfile
                
                apten=`echo $kvshow | jq ".properties.accessPolicies[(${j})].tenantId" | tr -d '"'`
                apoid=`echo $kvshow | jq ".properties.accessPolicies[(${j})].objectId" | tr -d '"'`
                
                printf "\t\t tenant_id=\"%s\"\n" $apten >> $outfile
                printf "\t\t object_id=\"%s\"\n" $apoid >> $outfile
                
                kl=`echo $kvshow | jq ".properties.accessPolicies[(${j})].permissions.keys" | jq '. | length'`
                sl=`echo $kvshow | jq ".properties.accessPolicies[(${j})].permissions.secrets" | jq '. | length'`
                cl=`echo $kvshow | jq ".properties.accessPolicies[(${j})].permissions.certificates" | jq '. | length'`
                
                kl=`expr $kl - 1`
                sl=`expr $sl - 1`
                cl=`expr $cl - 1`
                
                printf "\t\t key_permissions = [\n" >> $outfile
                if [ "$kl" -ge "0" ]; then
                    
                    for k in `seq 0 $kl`; do
                        tk=`echo $kvshow | jq ".properties.accessPolicies[(${j})].permissions.keys[(${k})]"`
                        if [ $k -lt $kl ]; then
                            tk=`printf "%s," $tk`
                        fi
                        printf "\t\t\t%s\n" $tk >> $outfile
                    done
                    #printf "\t\t ]\n" >> $outfile
                fi
                printf "\t\t ]\n" >> $outfile
                
                if [ "$sl" -ge "0" ]; then
                    printf "\t\t secret_permissions = [\n" >> $outfile
                    for k in `seq 0 $sl`; do
                        tk=`echo $kvshow | jq ".properties.accessPolicies[(${j})].permissions.secrets[(${k})]"`
                        if [ $k -lt $sl ]; then
                            tk=`printf "%s," $tk`
                        fi
                        printf "\t\t\t%s\n" $tk >> $outfile
                    done
                    printf "\t\t ]\n" >> $outfile
                else
                    printf "\t\t secret_permissions = []\n" >> $outfile
            
                fi
                
                if [ "$cl" -ge "0" ]; then
                    printf "\t\t certificate_permissions = [\n" >> $outfile
                    for k in `seq 0 $cl`; do
                        tk=`echo $kvshow | jq ".properties.accessPolicies[(${j})].permissions.certificates[(${k})]"`
                        ttk=`echo $tk | tr -d '"'`
                        if [ $k -lt $cl ]; then
                            tk=`printf "%s," $tk`   # add comma to all but last
                        fi
                        printf "\t\t\t%s\n" $tk >> $outfile                       
                    done
                    printf "\t\t ]\n" >> $outfile
                fi              
                printf "\t}\n" >> $outfile
            done
        fi
        
        printf "}\n" >> $outfile
                
        
    done
fi

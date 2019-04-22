
azr=`az container list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" != "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`

        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`
        iptype=`echo $azr | jq ".[(${i})].ipAddress.type" | tr -d '"'`
        ostyp=`echo $azr | jq ".[(${i})].osType" | tr -d '"'`
        rp=`echo $azr | jq ".[(${i})].restartPolicy" | tr -d '"'`
        dnsl=`echo $azr | jq ".[(${i})].ipAddress.dnsNameLabel" | tr -d '"'`
        fqdn=`echo $azr | jq ".[(${i})].ipAddress.fqdn" | tr -d '"'`
        cont=`echo $azr | jq ".[(${i})].containers"`
        vols=`echo $azr | jq ".[(${i})].volumes"`
        irc=`echo $azr | jq ".[(${i})].imageRegistryCredentials"`
        
        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile

        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        printf "\t location = \"%s\"\n" $loc >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
        printf "\t ip_address_type = \"%s\"\n" $iptype >> $outfile
        printf "\t os_type = \"%s\"\n" $ostyp >> $outfile
        printf "\t restart_policy = \"%s\"\n" $rp >> $outfile
        if [ "$dnsl" != "null" ]; then
            printf "\t dns_name_label = \"%s\"\n" $dnsl >> $outfile
        fi
        
        
        icount=`echo $cont | jq '. | length'`
        if [ "$icount" -gt "0" ]; then
            icount=`expr $icount - 1`
            for j in `seq 0 $icount`; do
                cname=`echo $azr | jq ".[(${i})].containers[(${j})].name"`
                cimg=`echo $azr | jq ".[(${i})].containers[(${j})].image"`
                ccpu=`echo $azr | jq ".[(${i})].containers[(${j})].resources.requests.cpu"`
                cmem=`echo $azr | jq ".[(${i})].containers[(${j})].resources.requests.memoryInGb"`
                cvols=`echo $azr | jq ".[(${i})].containers[(${j})].volumeMounts"`
                cport=`echo $azr | jq ".[(${i})].containers[(${j})].ports[0].port"`
                
                cport=`echo $azr | jq ".[(${i})].containers[(${j})].ports[0].port"`
                cproto=`echo $azr | jq ".[(${i})].containers[(${j})].ports[0].protocol"`
                cproto=`echo $cproto | awk '{print tolower($0)}'`
                
                vshr=`echo $azr | jq ".[(${i})].volumes[0].azureFile.shareName"`
                vsacc=`echo $azr | jq ".[(${i})].volumes[0].azureFile.storageAccountName"`
                vskey=`echo $azr | jq ".[(${i})].volumes[0].azureFile.storageAccountKey"`
                vmpath=`echo $azr | jq ".[(${i})].containers[(${j})].volumeMounts[0].mountPath"`
                vmname=`echo $azr | jq ".[(${i})].containers[(${j})].volumeMounts[0].name"`
                vmro=`echo $azr | jq ".[(${i})].containers[(${j})].volumeMounts[0].readOnly"`
                
                envs=`echo $azr | jq ".[(${i})].containers[(${j})].environmentVariables"`
                
                printf "\t container {\n" >> $outfile
                printf "\t\t name = %s\n" $cname >> $outfile
                printf "\t\t image = %s\n" $cimg >> $outfile
                printf "\t\t cpu = \"%s\"\n" $ccpu >> $outfile
                printf "\t\t memory = \"%s\"\n" $cmem >> $outfile
                # should be looped
                
                printf "\t\t port = \"%s\"\n" $cport >> $outfile
                if [ "$cproto" != "null" ]; then
                    printf "\t\t protocol = %s\n" $cproto >> $outfile
                fi

                if [ "$cvols" != "null" ]; then
                    printf "\t\t volume {\n" >> $outfile
                    printf "\t\t\t  name = %s\n" $vmname >> $outfile
                    printf "\t\t\t  mount_path = %s\n" $vmpath >> $outfile
                    printf "\t\t\t  read_only = \"%s\"\n" $vmro >> $outfile
                    printf "\t\t\t  share_name = %s\n" $vshr >> $outfile
                    printf "\t\t\t  storage_account_name = %s\n" $vsacc >> $outfile
                    if [ "$vskey" == "null" ]; then
                        printf "\t\t\t  storage_account_key = \"%s\"\n" >> $outfile
                    else
                        printf "\t\t\t  storage_account_key = \"%s\"\n" $vskey >> $outfile
                    fi
                    printf "\t\t }\n" >> $outfile
                fi
                
                kcount=`echo $envs | jq '. | length'`
                if [ "$kcount" -gt "0" ]; then
                    printf "\t\t environment_variables {\n" >> $outfile
                    kcount=`expr $kcount - 1`
                    for k in `seq 0 $kcount`; do
                        envn=`echo $azr | jq ".[(${i})].containers[(${j})].environmentVariables[(${k})].name"`
                        envv=`echo $azr | jq ".[(${i})].containers[(${j})].environmentVariables[(${k})].value"`
                        envs=`echo $azr | jq ".[(${i})].containers[(${j})].environmentVariables[(${k})].secureValue"`
                        printf "\t\t\t  %s = %s\n" $envn $envv >> $outfile
                    done
                    printf "\t\t }\n" >> $outfile
                fi
                             
                printf "\t }\n" >> $outfile
            done
        fi
        
        if [ ]; then  # comment - skip this block
        if [ "$irc" != "null" ]; then
            
            isrv=`echo $azr | jq ".[(${i})].imageRegistryCredentials[0].server"`
            iun=`echo $azr | jq ".[(${i})].imageRegistryCredentials[0].username"`
            ipw=`echo $azr | jq ".[(${i})].imageRegistryCredentials[0].password"`
            printf "\t image_registry_credential {\n" >> $outfile
            printf "\t\t server = %s\n" $isrv >> $outfile 
            printf "\t\t username = %s\n" $iun >> $outfile  
            # pw is problematic
            #if [ "$ipw" == "null" ]; then
            #printf "\t\t password = \"<Replace Me>\"\n"  >> $outfile
            #else
            #printf "\t\t password = \"%s\"\n" $ipw >> $outfile
            #fi
            printf "\t }\n" >> $outfile
        fi
        fi


        #
 
        
        #
        printf "}\n" >> $outfile
        #

        
    done
fi

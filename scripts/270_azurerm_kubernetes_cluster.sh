
azr=`az aks list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" != "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`

        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`
        admin=`echo $azr | jq ".[(${i})].adminUserEnabled" | tr -d '"'`
        dnsp=`echo $azr | jq ".[(${i})].dnsPrefix" | tr -d '"'`
        rbac=`echo $azr | jq ".[(${i})].enableRbac" | tr -d '"'`
        kv=`echo $azr | jq ".[(${i})].kubernetesVersion" | tr -d '"'`
        clid=`echo $azr | jq ".[(${i})].servicePrincipalProfile.clientId" | tr -d '"'`
        au=`echo $azr | jq ".[(${i})].linuxProfile.adminUsername" | tr -d '"'`
        lp=`echo $azr | jq ".[(${i})].linuxProfile" | tr -d '"'`
        sshk=`echo $azr | jq ".[(${i})].linuxProfile.ssh.publicKeys[0].keyData"`
        pname=`echo $azr | jq ".[(${i})].agentPoolProfiles[0].name" | tr -d '"'`
        vms=`echo $azr | jq ".[(${i})].agentPoolProfiles[0].vmSize" | tr -d '"'`
        pcount=`echo $azr | jq ".[(${i})].agentPoolProfiles[0].count" | tr -d '"'`
        ost=`echo $azr | jq ".[(${i})].agentPoolProfiles[0].osType" | tr -d '"'`
        vnsrg=`echo $azr | jq ".[(${i})].agentPoolProfiles[0].vnetSubnetId" | cut -d'/' -f5 | tr -d '"'`
        vnsid=`echo $azr | jq ".[(${i})].agentPoolProfiles[0].vnetSubnetId" | cut -d'/' -f11 | tr -d '"'`
        np=`echo $azr | jq ".[(${i})].networkProfile" | tr -d '"'`
        
        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile

        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        printf "\t location = \"%s\"\n" $loc >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
        printf "\t dns_prefix = \"%s\"\n" $dnsp >> $outfile
        printf "\t kubernetes_version = \"%s\"\n" $kv >> $outfile
        
        if [ "$rbac" = "true" ]; then
        printf "\t role_based_access_control {\n" >> $outfile
        printf "\t\t enabled = \"true\"\n" >> $outfile
        printf "\t }\n" >> $outfile
        fi
        
        if [ "$lp" != "null" ]; then
            printf "\t linux_profile {\n" >> $outfile
            printf "\t\t admin_username =  \"%s\"\n" $au >> $outfile
            printf "\t\t ssh_key {\n" >> $outfile
            printf "\t\t\t key_data =  %s \n" "$sshk" >> $outfile
            printf "\t\t }\n" >> $outfile
            printf "\t }\n" >> $outfile
        #else
            #printf "\t linux_profile {\n" >> $outfile
            #printf "\t\t admin_username =  \"%s\"\n" "" >> $outfile
            #printf "\t\t ssh_key {\n" >> $outfile
            #printf "\t\t\t key_data =  \"%s\" \n" "" >> $outfile
            #printf "\t\t }\n" >> $outfile
            #printf "\t }\n" >> $outfile
        fi
        
        if [ "$np" != "null" ]; then
            netp=`echo $azr | jq ".[(${i})].networkProfile.networkPlugin" | tr -d '"'`
            srvcidr=`echo $azr | jq ".[(${i})].networkProfile.serviceCidr" | tr -d '"'`
            dnssrvip=`echo $azr | jq ".[(${i})].networkProfile.dnsServiceIp" | tr -d '"'`
            dbrcidr=`echo $azr | jq ".[(${i})].networkProfile.dockerBridgeCidr" | tr -d '"'`
            podcidr=`echo $azr | jq ".[(${i})].networkProfile.podCidr" | tr -d '"'`

            printf "\t network_profile {\n" >> $outfile
            printf "\t\t network_plugin =  \"%s\"\n" $netp >> $outfile
            if [ "$srvcidr" != "null" ]; then
            printf "\t\t service_cidr =  \"%s\"\n" $srvcidr >> $outfile
            fi
            if [ "$dnssrvip" != "null" ]; then
            printf "\t\t dns_service_ip =  \"%s\"\n" $dnssrvip >> $outfile
            fi
            if [ "$dbrcidr" != "null" ]; then
            printf "\t\t docker_bridge_cidr =  \"%s\"\n" $dbrcidr >> $outfile
            fi
            if [ "$podcidr" != "null" ]; then
            printf "\t\t pod_cidr =  \"%s\"\n" $podcidr >> $outfile
            fi

            printf "\t }\n" >> $outfile
        fi

        
        printf "\t agent_pool_profile {\n" >> $outfile
        printf "\t\t name =  \"%s\"\n" $pname >> $outfile
        printf "\t\t vm_size =  \"%s\"\n" $vms >> $outfile
        printf "\t\t count =  \"%s\"\n" $pcount >> $outfile
        printf "\t\t os_type =  \"%s\"\n" $ost >> $outfile
        if [ "$vnsrg" != "null" ]; then
        printf "\t\t vnet_subnet_id = \"\${azurerm_subnet.%s__%s.id}\"\n" $vnsrg $vnsid >> $outfile      
        fi
        printf "\t }\n" >> $outfile
        
        printf "\t service_principal {\n" >> $outfile
        printf "\t\t client_id =  \"%s\"\n" $clid >> $outfile
        printf "\t\t client_secret =  \"%s\"\n" "" >> $outfile
        printf "\t }\n" >> $outfile

        
        #
        printf "}\n" >> $outfile
        #

        
    done
fi

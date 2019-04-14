prefixa=`echo $0 | awk -F 'azurerm_' '{print $2}' | awk -F '.sh' '{print $1}' `
tfp=`printf "azurerm_%s" $prefixa`

if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
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
        
          
       # New Tags block v2
        tags=`echo $azr | jq ".[(${i})].tags"`
        tt=`echo $tags | jq .`
        tcount=`echo $tags | jq '. | length'`
        if [ "$tcount" -gt "0" ]; then
            printf "\t tags { \n" >> $outfile
            tt=`echo $tags | jq .`
            keys=`echo $tags | jq 'keys'`
            tcount=`expr $tcount - 1`
            for j in `seq 0 $tcount`; do
                k1=`echo $keys | jq ".[(${j})]"`
                #echo "key=$k1"
                re="[[:space:]]+"
                if [[ $k1 =~ $re ]]; then
                    #echo "found a space"
                    tval=`echo $tt | jq ."$k1"`
                    tkey=`echo $k1 | tr -d '"'`
                    printf "\t\t\"%s\" = %s \n" "$tkey" "$tval" >> $outfile
                else
                    #echo "found no space"
                    tval=`echo $tt | jq .$k1`
                    tkey=`echo $k1 | tr -d '"'`
                    printf "\t\t%s = %s \n" $tkey "$tval" >> $outfile
                fi
            done
            printf "\t}\n" >> $outfile
        fi
        
        #
        printf "}\n" >> $outfile
        #
        cat $outfile
        statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $rname`
        echo $statecomm >> tf-staterm.sh
        eval $statecomm
        evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $rname $id`
        echo $evalcomm >> tf-stateimp.sh
        eval $evalcomm
        
    done
fi

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
azr=`az network nic list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`
        ipfor=`echo $azr | jq ".[(${i})].enableIpForwarding" | tr -d '"'`
        netacc=`echo $azr | jq ".[(${i})].enableAcceleratedNetworking" | tr -d '"'`
        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile

        snsg=`echo $azr | jq ".[(${i})].networkSecurityGroup.id" | cut -d'/' -f9 | sed 's/\./-/g' | tr -d '"'`
        snsgrg=`echo $azr | jq ".[(${i})].networkSecurityGroup.id" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
        ipcon=`echo $azr | jq ".[(${i})].ipConfigurations"`
        
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
        printf "\t location = \"%s\"\n" $loc >> $outfile
        if [ "$snsg" != "null" ]; then
            printf "\t network_security_group_id = \"\${azurerm_network_security_group.%s__%s.id}\"\n" $snsgrg $snsg >> $outfile
        fi
        
        #printf "\t internal_dns_name_label  = \"%s\"\n" $ipfor >> $outfile
        printf "\t enable_ip_forwarding = \"%s\"\n" $ipfor >> $outfile
        printf "\t enable_accelerated_networking  = \"%s\"\n" $netacc >> $outfile
        #printf "\t dns_servers  = \"%s\"\n" $ipfor >> $outfile
        privip0=`echo $azr | jq ".[(${i})].ipConfigurations[(0)].privateIpAddress" | tr -d '"'`
        
        
        
        
        icount=`echo $ipcon | jq '. | length'`
        if [ "$icount" -gt "0" ]; then
            icount=`expr $icount - 1`
            for j in `seq 0 $icount`; do
                ipcname=`echo $azr | jq ".[(${i})].ipConfigurations[(${j})].name" | cut -d'/' -f11 | tr -d '"'`
                subname=`echo $azr | jq ".[(${i})].ipConfigurations[(${j})].subnet.id" | cut -d'/' -f11 | sed 's/\./-/g' | tr -d '"'`
                subrg=`echo $azr | jq ".[(${i})].ipConfigurations[(${j})].subnet.id" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
                subipid=`echo $azr | jq ".[(${i})].ipConfigurations[(${j})].publicIpAddress.id" | cut -d'/' -f9 | tr -d '"'`
                subipalloc=`echo $azr | jq ".[(${i})].ipConfigurations[(${j})].privateIpAllocationMethod" | tr -d '"'`
                privip=`echo $azr | jq ".[(${i})].ipConfigurations[(${j})].privateIpAddress" | tr -d '"'`
                prim=`echo $azr | jq ".[(${i})].ipConfigurations[(${j})].primary" | tr -d '"'`
                pubipnam=`echo $azr | jq ".[(${i})].ipConfigurations[(${j})].publicIpAddress.id" | cut -d'/' -f9 | sed 's/\./-/g' | tr -d '"'`
                pubiprg=`echo $azr | jq ".[(${i})].ipConfigurations[(${j})].publicIpAddress.id" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
                
                
                
                printf "\t ip_configuration {\n" >> $outfile
                printf "\t\t name = \"%s\" \n"  $ipcname >> $outfile
                printf "\t\t subnet_id = \"\${azurerm_subnet.%s__%s.id}\"\n" $subrg $subname >> $outfile
                if [ "$subipalloc" != "Dynamic" ]; then
                    printf "\t\t private_ip_address = \"%s\" \n"  $privip >> $outfile
                fi
                printf "\t\t private_ip_address_allocation = \"%s\" \n"  $subipalloc >> $outfile
                if [ "$subipid" != "null" ]; then
                    printf "\t\t public_ip_address_id = \"\${azurerm_public_ip.%s__%s.id}\"\n" $pubiprg $pubipnam >> $outfile
                fi
                #printf "\t\t application_gateway_backend_address_pools_ids = \"%s\" \n"  $subipalloc >> $outfile
                #printf "\t\t load_balancer_backend_address_pools_ids = \"%s\" \n"  $subipalloc >> $outfile
                #printf "\t\t load_balancer_inbound_nat_rules_ids = \"%s\" \n"  $subipalloc >> $outfile
                #printf "\t\t application_security_group_ids = \"%s\" \n"  $subipalloc >> $outfile
                printf "\t\t primary = \"%s\" \n"  $prim >> $outfile
                
                asgs=`echo $azr | jq ".[(${i})].ipConfigurations[(${j})].applicationSecurityGroups"`
                #if [ $asgs != null ]; then
                    kcount=`echo $asgs | jq '. | length'`
                    if [ "$kcount" -gt "0" ]; then
                        kcount=`expr $kcount - 1`
                        for k in `seq 0 $kcount`; do
                            asgnam=`echo $azr | jq ".[(${i})].ipConfigurations[(${j})].applicationSecurityGroups[(${k})].id" | cut -d'/' -f9 | sed 's/\./-/g' | tr -d '"'`
                            asgrg=`echo $azr | jq ".[(${i})].ipConfigurations[(${j})].applicationSecurityGroups[(${k})].id" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
                            
                            printf "\t\t application_security_group_ids = [\"\${azurerm_application_security_group.%s__%s.id}\"]\n" $asgrg $asgnam >> $outfile
                        done
                    fi
                #fi
                
                printf "\t}\n" >> $outfile
                #
                
            done
        fi
        #printf "\t private_ip_address = \"%s\" \n"  $pprivip >> $outfile
        #

            #
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
                    re="[[:space:]]+"
                    if [[ $k1 =~ $re ]]; then
                        tval=`echo $tt | jq ."$k1"`
                        tkey=`echo $k1 | tr -d '"'`
                        printf "\t\t\"%s\" = %s \n" "$tkey" "$tval" >> $outfile
                    else
                        tval=`echo $tt | jq .$k1`
                        tkey=`echo $k1 | tr -d '"'`
                        printf "\t\t%s = %s \n" $tkey "$tval" >> $outfile
                    fi
                done
                printf "\t}\n" >> $outfile
            fi

        
        
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

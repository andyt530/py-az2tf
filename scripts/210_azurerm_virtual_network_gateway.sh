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
azr=`az network vnet-gateway list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`

        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`
        type=`echo $azr | jq ".[(${i})].gatewayType" | tr -d '"'`
        vpntype=`echo $azr | jq ".[(${i})].vpnType" | tr -d '"'`
        bgps=`echo $azr | jq ".[(${i})].bgpSettings" | tr -d '"'`
        sku=`echo $azr | jq ".[(${i})].sku.name" | tr -d '"'`
        vadsp=`echo $azr | jq ".[(${i})].vpnClientConfiguration.vpnClientAddressPool.addressPrefixes"`
        radsa=`echo $azr | jq ".[(${i})].vpnClientConfiguration.radiusServerAddress"`
        radss=`echo $azr | jq ".[(${i})].vpnClientConfiguration.radiusServerSecret"`
        vcp0=`echo $azr | jq ".[(${i})].vpnClientConfiguration.vpnClientProtocols[0]"`
        vcp=`echo $azr | jq ".[(${i})].vpnClientConfiguration.vpnClientProtocols"`
        
        
        aa=`echo $azr | jq ".[(${i})].activeActive"`
        enbgp=`echo $azr | jq ".[(${i})].enableBgp"`
        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
        printf "\t location = \"%s\"\n" $loc >> $outfile
        printf "\t type = \"%s\"\n" $type >> $outfile
        printf "\t vpn_type = \"%s\"\n" $vpntype >> $outfile
        printf "\t sku = \"%s\"\n" $sku >> $outfile
        printf "\t active_active = \"%s\"\n" $aa >> $outfile
        printf "\t enable_bgp = \"%s\"\n" $enbgp >> $outfile
        
        if [ "$vadsp" != "null" ]; then
            printf "\t vpn_client_configuration {\n"  >> $outfile
            printf "\t\t address_space = %s\n"  "$vadsp" >> $outfile
            if [ "$radsa" == "null" ]; then
                printf "\t\t root_certificate { \n"   >> $outfile
                printf "\t\t\t name = \"\"\n"   >> $outfile
                printf "\t\t\t public_cert_data = \"\"\n"   >> $outfile
                printf "\t\t }\n"  >> $outfile
            fi
            if [ "$radsa" != "null" ]; then
            printf "\t\t radius_server_address = %s\n"  "$radsa" >> $outfile
            printf "\t\t radius_server_secret = %s\n"  "$radss" >> $outfile
            fi
            if [ "$vcp0" != "null" ]; then
            printf "\t\t vpn_client_protocols = %s\n"  "$vcp" >> $outfile
            fi
            
            printf "\t }\n"  >> $outfile
        fi
        
        
        if [ "$bgps" != "null" ]; then
            printf "\t bgp_settings {\n"  >> $outfile
            asn=`echo $azr | jq ".[(${i})].bgpSettings.asn" | tr -d '"'`
            peera=`echo $azr | jq ".[(${i})].bgpSettings.bgpPeeringAddress" | tr -d '"'`
            peerw=`echo $azr | jq ".[(${i})].bgpSettings.peerWeight" | tr -d '"'`
            printf "\t\t asn = \"%s\"\n" $asn >> $outfile
            printf "\t\t peering_address = \"%s\"\n" $peera >> $outfile
            printf "\t\t peer_weight = \"%s\"\n" $peerw >> $outfile
            printf "\t }\n"  >> $outfile
        fi
        
        ipc=`echo $azr | jq ".[(${i})].ipConfigurations"`
        count=`echo $ipc | jq '. | length'`
        count=`expr $count - 1`
        for j in `seq 0 $count`; do
            ipcname=`echo $ipc | jq ".[(${j})].name"`
            ipcpipa=`echo $ipc | jq ".[(${j})].privateIpAllocationMethod"`
            ipcpipid=`echo $ipc | jq ".[(${j})].publicIpAddress.id"`
            ipcsubid=`echo $ipc | jq ".[(${j})].subnet.id"`
            pipnam=`echo $ipcpipid | cut -d'/' -f9 | sed 's/\./-/g' | tr -d '"'`
            piprg=`echo $ipcpipid | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
            subnam=`echo $ipcsubid | cut -d'/' -f11 | sed 's/\./-/g' | tr -d '"'`
            subrg=`echo $ipcsubid | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
            printf "\tip_configuration {\n"  >> $outfile
            printf "\t\t name = %s\n" $ipcname >> $outfile
            printf "\t\t private_ip_address_allocation = %s\n" $ipcpipa >> $outfile
            if [ "$pipnam" != "null" ]; then
                printf "\t\t public_ip_address_id = \"\${azurerm_public_ip.%s__%s.id}\"\n" $piprg $pipnam >> $outfile
            fi
            if [ "$subnam" != "null" ]; then
                printf "\t\t subnet_id = \"\${azurerm_subnet.%s__%s.id}\"\n" $subrg $subnam >> $outfile
            fi
            printf "\t}\n" >> $outfile
        done
        
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

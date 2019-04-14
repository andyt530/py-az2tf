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
#
azr=`az network vnet list -g $rgsource -o json`
#
# loop around vnets
#
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        vnname=`echo $name`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | tr -d '"'`
   
        peers=`az network vnet peering list -g $rg --vnet $name -o json`
        #echo $peers | jq .
     
        pcount=`echo $peers | jq '. | length'`
        
        if [ "$pcount" -gt "0" ]; then
            pcount=`expr $pcount - 1`
            for j in `seq 0 $pcount`; do
            
            name=`echo $peers | jq ".[(${j})].name" | tr -d '"'`
            rname=`echo $name | sed 's/\./-/g'`
            rg=`echo $peers | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`

            id=`echo $peers | jq ".[(${j})].id" | tr -d '"'`
            rvnid=`echo $peers | jq ".[(${j})].remoteVirtualNetwork.id" | tr -d '"'`
            aft=`echo $peers | jq ".[(${j})].allowForwardedTraffic" | tr -d '"'`
            agt=`echo $peers | jq ".[(${j})].allowGatewayTransit" | tr -d '"'`
            avna=`echo $peers | jq ".[(${j})].allowVirtualNetworkAccess" | tr -d '"'`
            urg=`echo $peers | jq ".[(${j})].useRemoteGateways" | tr -d '"'`

            prefix=`printf "%s__%s" $prefixa $rg`
            outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
            echo $az2tfmess > $outfile

            printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
            #nsgnam=`echo $snnsgid | cut -d'/' -f9 | tr -d '"'`
            #nsgrg=`echo $snnsgid | cut -d'/' -f5 | tr -d '"'`
            printf "\t name = \"%s\"\n" $name >> $outfile
            printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
            printf "\t virtual_network_name = \"%s\"\n" $vnname >> $outfile
            printf "\t remote_virtual_network_id = \"%s\"\n" $rvnid >> $outfile
            printf "\t allow_forwarded_traffic = \"%s\"\n" $aft >> $outfile
            printf "\t allow_gateway_transit = \"%s\"\n" $agt >> $outfile
            printf "\t allow_virtual_network_access = \"%s\"\n" $avna >> $outfile
            printf "\t use_remote_gateways = \"%s\"\n" $urg >> $outfile
                        
            printf "}\n" >> $outfile
            cat $outfile

            statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $rname`
            echo $statecomm >> tf-staterm.sh
            eval $statecomm
            evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $rname $id`
            echo $evalcomm >> tf-stateimp.sh
            eval $evalcomm
            done
        fi
 
        #
        #
        
        
        
    done
fi

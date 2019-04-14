tfp="azurerm_virtual_network_peering"
prefixa="vnp"
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
azr=`az network vnet list -g $rgsource`
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
   
        peers=`az network vnet peering list -g $rg --vnet $name`
        #echo $peers | jq .
     
        pcount=`echo $peers | jq '. | length'`
        
        if [ "$pcount" -gt "0" ]; then
            pcount=`expr $pcount - 1`
            for j in `seq 0 $pcount`; do
            
            name=`echo $peers | jq ".[(${j})].name" | tr -d '"'`
            rg=`echo $peers | jq ".[(${j})].resourceGroup" | tr -d '"'`
            id=`echo $peers | jq ".[(${j})].id" | tr -d '"'`
            rvnid=`echo $peers | jq ".[(${j})].remoteVirtualNetwork.id" | tr -d '"'`
            aft=`echo $peers | jq ".[(${j})].allowForwardedTraffic" | tr -d '"'`
            agt=`echo $peers | jq ".[(${j})].allowGatewayTransit" | tr -d '"'`
            avna=`echo $peers | jq ".[(${j})].allowVirtualNetworkAccess" | tr -d '"'`
            urg=`echo $peers | jq ".[(${j})].useRemoteGateways" | tr -d '"'`

            prefix=`printf "%s__%s" $prefixa $rg`
            printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $name > $prefix-$name.tf
            #nsgnam=`echo $snnsgid | cut -d'/' -f9 | tr -d '"'`
            #nsgrg=`echo $snnsgid | cut -d'/' -f5 | tr -d '"'`
            printf "\t name = \"%s\"\n" $name >> $prefix-$name.tf
            printf "\t resource_group_name = \"%s\"\n" $rg >> $prefix-$name.tf
            printf "\t virtual_network_name = \"%s\"\n" $vnname >> $prefix-$name.tf
            printf "\t remote_virtual_network_id = \"%s\"\n" $rvnid >> $prefix-$name.tf
            printf "\t allow_forwarded_traffic = \"%s\"\n" $aft >> $prefix-$name.tf
            printf "\t allow_gateway_transit = \"%s\"\n" $agt >> $prefix-$name.tf
            printf "\t allow_virtual_network_access = \"%s\"\n" $avna >> $prefix-$name.tf
            printf "\t use_remote_gateways = \"%s\"\n" $urg >> $prefix-$name.tf
                        
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
 
        #
        #
        
        
        
    done
fi

tfp="azurerm_virtual_network"
prefixa="vnet"
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
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | tr -d '"'`
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location"`
        
        prefix=`printf "%s__%s" $prefixa $rg`
        
        dns=`echo $azr | jq ".[(${i})].dhcpOptions.dnsServers"`
        addsp=`echo $azr | jq ".[(${i})].addressSpace.addressPrefixes"`
        echo $az2tfmess > $prefix-$name.tf
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $name > $prefix-$name.tf
        printf "\tname = \"%s\"\n" $name >> $prefix-$name.tf
        printf "\t location = %s\n" "$loc" >> $prefix-$name.tf
        #printf "\t resource_group_name = \"\${var.rgtarget}\"\n"  >> $prefix-$name.tf
        printf "\t resource_group_name = \"%s\"\n" $rg >> $prefix-$name.tf
        if [ "$dns" != "null" ]; then
            printf "\t dns_servers = %s\n" "$dns" >> $prefix-$name.tf
        fi

        printf "\taddress_space = %s\n" "$addsp" >> $prefix-$name.tf
        #
        #loop around subnets
        #
        subs=`echo $azr | jq ".[(${i})].subnets"`
        count=`echo $subs | jq '. | length'`
        count=`expr $count - 1`
        for j in `seq 0 $count`; do
            snname=`echo $subs | jq ".[(${j})].name"`
            snaddr=`echo $subs | jq ".[(${j})].addressPrefix"`
            snnsgid=`echo $subs | jq ".[(${j})].networkSecurityGroup.id"`
            nsgnam=`echo $snnsgid | cut -d'/' -f9 | tr -d '"'`
            nsgrg=`echo $snnsgid | cut -d'/' -f5 | tr -d '"'`
            printf "\tsubnet {\n"  >> $prefix-$name.tf
            printf "\t\t name = %s\n" $snname >> $prefix-$name.tf
            printf "\t\t address_prefix = %s\n" $snaddr >> $prefix-$name.tf
            if [ "$nsgnam" != "null" ]; then
                printf "\t\t security_group = \"\${azurerm_network_security_group.%s__%s.id}\"\n" $nsgrg $nsgnam >> $prefix-$name.tf
            fi
            printf "\t}\n" >> $prefix-$name.tf          
        done

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

        echo "}" >> $prefix-$name.tf
        #
        #
        cat $prefix-$name.tf
        statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $name`
        echo $statecomm >> tf-staterm.sh
        eval $statecomm 
        evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $name $id`
        eval $evalcomm
        echo $evalcomm >> tf-stateimp.sh
    done
fi

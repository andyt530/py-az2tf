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
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location"`
        
        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile

        dns=`echo $azr | jq ".[(${i})].dhcpOptions.dnsServers"`
        addsp=`echo $azr | jq ".[(${i})].addressSpace.addressPrefixes"`
 
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\tname = \"%s\"\n" $name >> $outfile
        printf "\t location = %s\n" "$loc" >> $outfile
        #printf "\t resource_group_name = \"\${var.rgtarget}\"\n"  >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
        if [ "$dns" != "null" ]; then
            printf "\t dns_servers = %s\n" "$dns" >> $outfile
        fi

        printf "\taddress_space = %s\n" "$addsp" >> $outfile
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
            nsgnam=`echo $snnsgid | cut -d'/' -f9 | sed 's/\./-/g' | tr -d '"'`
            nsgrg=`echo $snnsgid | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
            printf "\tsubnet {\n"  >> $outfile
            printf "\t\t name = %s\n" $snname >> $outfile
            printf "\t\t address_prefix = %s\n" $snaddr >> $outfile
            if [ "$nsgnam" != "null" ]; then
                printf "\t\t security_group = \"\${azurerm_network_security_group.%s__%s.id}\"\n" $nsgrg $nsgnam >> $outfile
            fi
            printf "\t}\n" >> $outfile          
        done

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

        echo "}" >> $outfile
        #
        #
        cat $outfile
        statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $rname`
        echo $statecomm >> tf-staterm.sh
        eval $statecomm 
        evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $rname $id`
        eval $evalcomm
        echo $evalcomm >> tf-stateimp.sh
    done
fi

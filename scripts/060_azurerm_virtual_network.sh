
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

        

        echo "}" >> $outfile
        #
        #

    done
fi

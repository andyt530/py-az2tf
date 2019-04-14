tfp="azurerm_lb"
prefixa="lb"
if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
azr=`az network lb list -g $rgsource`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
       
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | tr -d '"'`
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location"`
        sku=`echo $azr | jq ".[(${i})].sku.name" | tr -d '"'`
        fronts=`echo $azr | jq ".[(${i})].frontendIpConfigurations"`
        
        prefix=`printf "%s__%s" $prefixa $rg`
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $name > $prefix-$name.tf
        printf "\t name = \"%s\"\n" $name >> $prefix-$name.tf
        printf "\t location = %s\n" "$loc" >> $prefix-$name.tf
        printf "\t resource_group_name = \"%s\"\n" $rg >> $prefix-$name.tf
        printf "\t sku = \"%s\"\n" $sku >> $prefix-$name.tf
           
        icount=`echo $fronts | jq '. | length'`
       
        if [ "$icount" -gt "0" ]; then
            icount=`expr $icount - 1`
            for j in `seq 0 $icount`; do
                    
                fname=`echo $azr | jq ".[(${i})].frontendIpConfigurations[(${j})].name" | tr -d '"'`
                priv=`echo $azr | jq ".[(${i})].frontendIpConfigurations[(${j})].privateIpAddress" | tr -d '"'`

                pubrg=`echo $azr | jq ".[(${i})].frontendIpConfigurations[(${j})].publicIpAddress.id" | cut -d'/' -f5 | tr -d '"'`
                pubname=`echo $azr | jq ".[(${i})].frontendIpConfigurations[(${j})].publicIpAddress.id" | cut -d'/' -f9 | tr -d '"'`
                
                subrg=`echo $azr | jq ".[(${i})].frontendIpConfigurations[(${j})].subnet.id" | cut -d'/' -f5 | tr -d '"'`
                subname=`echo $azr | jq ".[(${i})].frontendIpConfigurations[(${j})].subnet.id" | cut -d'/' -f11 | tr -d '"'`
                privalloc=`echo $azr | jq ".[(${i})].frontendIpConfigurations[(${j})].privateIpAllocationMethod" | tr -d '"'`
                
                printf "\t frontend_ip_configuration {\n" >> $prefix-$name.tf
                printf "\t\t name = \"%s\" \n"  $fname >> $prefix-$name.tf
                if [ "$subname" != "null" ]; then
                    printf "\t\t subnet_id = \"\${azurerm_subnet.%s__%s.id}\"\n" $subrg $subname >> $prefix-$name.tf
                fi
                if [ "$priv" != "null" ]; then
                    printf "\t\t private_ip_address = \"%s\" \n"  $priv >> $prefix-$name.tf
                fi            
                if [ "$privalloc" != "null" ]; then
                    printf "\t\t private_ip_address_allocation  = \"%s\" \n"  $privalloc >> $prefix-$name.tf
                fi
                if [ "$pubname" != "null" ]; then
                    printf "\t\t public_ip_address_id = \"\${azurerm_public_ip.%s__%s.id}\"\n" $pubrg $pubname >> $prefix-$name.tf
                fi

                printf "\t }\n" >> $prefix-$name.tf
                
            done
        fi
        
        
        printf "}\n" >> $prefix-$name.tf
        #
        cat $prefix-$name.tf
        statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $name`
        echo $statecomm >> tf-staterm.sh
        eval $statecomm
        evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $name $id`
        echo $evalcomm >> tf-stateimp.sh
        eval $evalcomm
    done
fi

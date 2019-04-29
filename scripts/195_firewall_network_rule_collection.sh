
azr=`az network lb list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
       
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`

        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location"`
        sku=`echo $azr | jq ".[(${i})].sku.name" | tr -d '"'`
        fronts=`echo $azr | jq ".[(${i})].frontendConfigurations"`
        
        prefix=`printf "%s__%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        printf "\t location = %s\n" "$loc" >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
        printf "\t sku = \"%s\"\n" $sku >> $outfile
           
        icount=`echo $fronts | jq '. | length'`
       
        if [ "$icount" -gt "0" ]; then
            icount=`expr $icount - 1`
            for j in `seq 0 $icount`; do
                    
                fname=`echo $azr | jq ".[(${i})].frontendConfigurations[(${j})].name" | tr -d '"'`
                priv=`echo $azr | jq ".[(${i})].frontendConfigurations[(${j})].privateAddress" | tr -d '"'`

                pubrg=`echo $azr | jq ".[(${i})].frontendConfigurations[(${j})].publicAddress.id" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
                pubname=`echo $azr | jq ".[(${i})].frontendConfigurations[(${j})].publicAddress.id" | cut -d'/' -f9 | sed 's/\./-/g' | tr -d '"'`
                
                subrg=`echo $azr | jq ".[(${i})].frontendConfigurations[(${j})].subnet.id" | cut -d'/' -f5 | sed 's/\./-/g' | tr -d '"'`
                subname=`echo $azr | jq ".[(${i})].frontendConfigurations[(${j})].subnet.id" | cut -d'/' -f11 | sed 's/\./-/g' | tr -d '"'`
                privalloc=`echo $azr | jq ".[(${i})].frontendConfigurations[(${j})].privateAllocationMethod" | tr -d '"'`
                
                printf "\t frontend_ip_configuration {\n" >> $outfile
                printf "\t\t name = \"%s\" \n"  $fname >> $outfile
                if [ "$subname" != "null" ]; then
                    printf "\t\t subnet_id = \"\${azurerm_subnet.%s__%s.id}\"\n" $subrg $subname >> $outfile
                fi
                if [ "$priv" != "null" ]; then
                    printf "\t\t private_ip_address = \"%s\" \n"  $priv >> $outfile
                fi            
                if [ "$privalloc" != "null" ]; then
                    printf "\t\t private_ip_address_allocation  = \"%s\" \n"  $privalloc >> $outfile
                fi
                if [ "$pubname" != "null" ]; then
                    printf "\t\t public_ip_address_id = \"\${azurerm_public_ip.%s__%s.id}\"\n" $pubrg $pubname >> $outfile
                fi

                printf "\t }\n" >> $outfile
                
            done
        fi
        
        
        printf "}\n" >> $outfile
        #

    done
fi

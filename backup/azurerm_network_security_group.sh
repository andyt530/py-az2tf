tfp="azurerm_network_security_group"
prefixa="nsg"
if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
azr=`az network nsg list -g $rgsource`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | tr -d '"'`
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location" | tr -d '"'`
        srules=`echo $azr | jq ".[(${i})].securityRules"`

        prefix=`printf "%s__%s" $prefixa $rg`
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $name > $prefix-$name.tf
        printf "\t name = \"%s\"  \n" $name >> $prefix-$name.tf
        printf "\t location = \"%s\"\n" $loc >> $prefix-$name.tf
        #printf "\t resource_group_name = \"\${var.rgtarget}\"\n" >> $prefix-$name.tf
        printf "\t resource_group_name = \"%s\"\n" $rg >> $prefix-$name.tf
        #
        # Security Rules
        #
        scount=`echo $srules | jq '. | length'`
        #echo $scount
        if [ "$scount" -gt "0" ]; then
        scount=`expr $scount - 1`
            for j in `seq 0 $scount`; do    
                      
            printf "\t security_rule { \n" >> $prefix-$name.tf
            srname=`echo $azr | jq ".[(${i})].securityRules[(${j})].name" | tr -d '"'`                       
            printf "\t\t name = \"%s\"  \n" $srname >> $prefix-$name.tf
            srdesc=`echo $azr | jq ".[(${i})].securityRules[(${j})].description"`                       
            if [ "$srdesc" != "null" ]; then
                echo "              description = $srdesc  "  >> $prefix-$name.tf   # printf does multiple lines with space delimited values
            fi

            sraccess=`echo $azr | jq ".[(${i})].securityRules[(${j})].access" | tr -d '"'`                       
            printf "\t\t access = \"%s\"  \n" $sraccess >> $prefix-$name.tf
            srpri=`echo $azr | jq ".[(${i})].securityRules[(${j})].priority" | tr -d '"'` 
            printf "\t\t priority = \"%s\"  \n" $srpri >> $prefix-$name.tf
            srproto=`echo $azr | jq ".[(${i})].securityRules[(${j})].protocol"` 
            printf "\t\t protocol = %s  \n" $srproto >> $prefix-$name.tf
            srdir=`echo $azr | jq ".[(${i})].securityRules[(${j})].direction" | tr -d '"'` 
            printf "\t\t direction = \"%s\"  \n" $srdir >> $prefix-$name.tf
            srsp=`echo $azr | jq ".[(${i})].securityRules[(${j})].sourcePortRange"` 
            printf "\t\t source_port_range = %s  \n" $srsp >> $prefix-$name.tf
            srsap=`echo $azr | jq ".[(${i})].securityRules[(${j})].sourceAddressPrefix"` 
            printf "\t\t source_address_prefix = %s  \n" $srsap >> $prefix-$name.tf

            srdp=`echo $azr | jq ".[(${i})].securityRules[(${j})].destinationPortRange"` 
            printf "\t\t destination_port_range = %s  \n" $srdp >> $prefix-$name.tf
            srdap=`echo $azr | jq ".[(${i})].securityRules[(${j})].destinationAddressPrefix"` 
            printf "\t\t destination_address_prefix = %s  \n" $srdap >> $prefix-$name.tf


            printf "\t}\n" >> $prefix-$name.tf
            done
        fi

 

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

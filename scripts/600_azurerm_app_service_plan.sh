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
azr=`az appservice plan list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`


        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location"`
        tier=`echo $azr | jq ".[(${i})].sku.tier" | tr -d '"'`
        size=`echo $azr | jq ".[(${i})].sku.size" | tr -d '"'`
        kind=`echo $azr | jq ".[(${i})].kind" | tr -d '"'`
        lcrg=`echo $azr | jq ".[(${i})].resourceGroup" | awk '{print tolower($0)}' | tr -d '"'`
        rg=`echo $lcrg | sed 's/\./-/g'`

        #if [ "$kind" = "app" ];then kind="Windows"; fi
        prefix=`printf "%s.%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile  
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        printf "\t location = %s\n" "$loc" >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
        printf "\t kind = \"%s\"\n" $kind >> $outfile

        printf "\t sku {\n" >> $outfile
        printf "\t\t tier = \"%s\"\n" $tier >> $outfile
        printf "\t\t size = \"%s\"\n" $size >> $outfile
        printf "\t }\n" >> $outfile

        
# geo location block
        
#        icount=`echo $geol | jq '. | length'`
#        if [ "$icount" -gt "0" ]; then
#            icount=`expr $icount - 1`
#            for j in `seq 0 $icount`; do
#                floc=`echo $azr | jq ".[(${i})].failoverPolicies[(${j})].locationName"`
#                fop=`echo $azr | jq ".[(${i})].failoverPolicies[(${j})].failoverPriority" | tr -d '"'`
#                printf "\t geo_location { \n"  >> $outfile
#                printf "\t location = %s \n"  "$floc" >> $outfile
#                printf "\t failover_priority  = \"%s\" \n"  $fop >> $outfile
#                printf "}\n" >> $outfile
#            done
#        fi

        
        #
        # No tags - used internally
 
        
        
        printf "}\n" >> $outfile
        #
        echo $prefix
        echo $prefix__$name
        cat $outfile
        statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $rname`
        echo $statecomm >> tf-staterm.sh
        eval $statecomm
        evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $rname $id`
        echo $evalcomm >> tf-stateimp.sh
        eval $evalcomm
    done
fi

prefixa=`echo $0 | awk -F 'azurerm_' '{print $2}' | awk -F '.sh' '{print $1}' `
tfp=`printf "azurerm_%s" $prefixa`

echo $TF_VAR_rgtarget
if [ "$1" != "" ]; then
    rgsource=$1
fi
at=`az account get-access-token -o json`
bt=`echo $at | jq .accessToken | tr -d '"'`
sub=`echo $at | jq .subscription | tr -d '"'`


ris=`printf "curl -s  -X GET -H \"Authorization: Bearer %s\" -H \"Content-Type: application/json\" https://management.azure.com/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Automation/automationAccounts?api-version=2015-10-31" $bt $sub $rgsource`
#echo $ris
ret=`eval $ris`
azr2=`echo $ret | jq .value`
rg=$rgsource
count2=`echo $azr2 | jq '. | length'`
if [ "$count2" -gt "0" ]; then
    count2=`expr $count2 - 1`
    for i in `seq 0 $count2`; do
        
        name2=`echo $azr2 | jq ".[(${i})].name" | tr -d '"'`
        ris2=`printf "curl -s -X GET -H \"Authorization: Bearer %s\" -H \"Content-Type: application/json\" https://management.azure.com/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Automation/automationAccounts/%s?api-version=2015-10-31" $bt $sub $rgsource $name2`
        #echo $ris2
        ret2=`eval $ris2`
        azr=`echo $ret2 | jq .`
        #echo $ret2 | jq .
        count=`echo $azr | jq '. | length'`
        if [ "$count" -gt "0" ]; then
            name=`echo $azr | jq ".name" | tr -d '"'`
            id=`echo $azr | jq ".id" | tr -d '"'`
            loc=`echo $azr | jq ".location"`
            
            rname=`echo $name | sed 's/\./-/g'`
            rg=`echo $rgsource | sed 's/\./-/g'`
            sku=`echo $azr | jq ".properties.sku.name"`
            if [ "$sku" = "Free" ]; then
                sku="Basic"
            fi
            sku="Basic"  # only one supported
            echo $sku
            prefix=`printf "%s__%s" $prefixa $rg`
            outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
            echo $az2tfmess > $outfile
            
            printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
            printf "\t name = \"%s\"\n" $name >> $outfile
            printf "\t location = %s\n" "$loc" >> $outfile
            printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
            printf "\t sku { \n" >> $outfile
            
            printf "\t\t name = \"%s\" \n" $sku >> $outfile
            printf "\t}\n" >> $outfile

                        
            printf "}\n" >> $outfile

            
            #done
        fi
        
    done
fi

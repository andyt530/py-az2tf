# problems with unauthorized
# problems with too many calls to ?comp=list   

prefixa=`echo $0 | awk -F 'azurerm_' '{print $2}' | cut -f1 -d'.'`
tfp=`printf "azurerm_%s" $prefixa`


azr=`az storage account list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        #echo $i
        saname=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | tr -d '"'`
        k=`az storage account keys list --resource-group $rg --account-name $saname --query '[0].value' -o json`
        fs=`az storage share list --account-name $saname --account-key $k -o json`        
        jcount=`echo $fs | jq '. | length'`
        if [ "$jcount" -gt "0" ]; then
            jcount=`expr $jcount - 1`
            for j in `seq 0 $jcount`; do     
                name=`echo $fs | jq ".[(${i})].name" | tr -d '"'`
                quo=`echo $fs | jq ".[(${i})].properties.quota" | tr -d '"'`
                prefix=`printf "%s__%s" $prefixa $rg`
                outfile=`printf "%s.%s__%s.tf" $tfp $rg $name`
                fsid=`printf "%s/%s/%s" $name $rg $saname`

                echo $az2tfmess > $outfile
                printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $name >> $outfile
                printf "\t name = \"%s\"\n" $name >> $outfile
                printf "\t quota = \"%s\"\n" $quo >> $outfile    
                printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
                printf "\t storage_account_name = \"%s\"\n" $saname >> $outfile
                printf "}\n" >> $outfile
      
                cat $outfile
                statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $name`
                echo $statecomm >> tf-staterm.sh
                eval $statecomm
                evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $name $fsid`
                echo $evalcomm >> tf-stateimp.sh
                eval $evalcomm

            done
        fi
    done
fi

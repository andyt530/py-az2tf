#prefixa=`echo $0 | awk -F 'azurerm_' '{print $2}' | awk -F '.sh' '{print $1}' `
prefixa="key_vault_secret"
tfp=`printf "azurerm_%s" $prefixa`

#if [ "$1" != "" ]; then
 #   rgsource=$1
#else
#    echo -n "Enter name of Resource Group [$rgsource] > "
#    read response
#    if [ -n "$response" ]; then
#        rgsource=$response
#    fi
#fi
#azr=`az keyvault list -g $rgsource`
azr=`az keyvault list -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`

        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location"`
        kvd=`az keyvault show -n $name -g $rg -o json`
        kvuri=`echo $kvd | jq ".properties.vaultUri" | tr -d '"'`
        
        secs=`az keyvault secret list --vault-name $name -o json`
        #echo $secs | jq .[0]
        #
        # Access Policies
        #
        pcount=`echo $secs | jq '. | length'`
        #echo "pcount=$pcount"
        if [ "$pcount" -gt "0" ]; then
            
            pcount=`expr $pcount - 1`
            for j in `seq 0 $pcount`; do
                
                secid=`echo $secs | jq ".[(${j})].id" | tr -d '"'`
                secid2=`echo $secid | cut -d '/' -f5 `
          
                content_type=`echo $secs | jq ".[(${j})].contentType" | tr -d '"'`
                asec=`az keyvault secret show --vault-name $name -n $secid2 -o json`
                
                content_type=`echo $asec | jq ".contentType" | tr -d '"'`
                value=`echo $asec | jq ".value" | tr -d '"'`
                id=`echo $asec | jq ".id" | tr -d '"'`
                
                prefix=`printf "azurerm_%s__%s" $prefixa $rg`
                outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
               

                echo "$j of $pcount  $prefix-$rname-$secid2.tf"
                if [ ! -f $prefix-$rname-$secid2.tf ]; then
                                        
                    echo $az2tfmess > $prefix-$rname-$secid2.tf
                    
                    printf "resource \"%s\" \"%s__%s-%s\" {\n" $tfp $rg $rname $secid2 >> $prefix-$rname-$secid2.tf
                    printf "\t\t name=\"%s\"\n" $secid2 >> $prefix-$rname-$secid2.tf
                    if [ "$content_type" != "null" ]; then
                        if [ "$content_type" != "" ]; then
                            printf "\t\t content_type=\"%s\"\n" "$content_type" >> $prefix-$rname-$secid2.tf
                        fi
                    fi
                    printf "\t\t vault_uri=\"%s\"\n" $kvuri >> $prefix-$rname-$secid2.tf
                    printf "\t\t value=\"%s\"\n" $value >> $prefix-$rname-$secid2.tf
                    

                    
                    
                    printf "\t}\n" >> $prefix-$rname-$secid2.tf
                    
                    
                    cat $prefix-$rname-$secid2.tf

                fi
            done
        fi
        
    done
fi

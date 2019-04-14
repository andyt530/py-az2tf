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
azr=`az servicebus namespace list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        
        nname=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        azr2=`az servicebus queue list -g $rgsource --namespace-name $nname -o json`
        icount=`echo $azr2 | jq '. | length'`
        if [ "$icount" -gt "0" ]; then
            icount=`expr $icount - 1`
            for j in `seq 0 $icount`; do
                name=`echo $azr2 | jq ".[(${j})].name" | tr -d '"'`
                rname=`echo $name | sed 's/\./-/g'`
                rg=`echo $azr2 | jq ".[(${j})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`
                id=`echo $azr2 | jq ".[(${j})].id" | tr -d '"'`
                ep=`echo $azr2 | jq ".[(${j})].enablePartitioning" | tr -d '"'`
                adoni=`echo $azr2 | jq ".[(${j})].autoDeleteOnIdle" | tr -d '"'`
                
                ee=`echo $azr2 | jq ".[(${j})].enableExpress" | tr -d '"'`
                dd=`echo $azr2 | jq ".[(${j})].requiresDuplicateDetection" | tr -d '"'`
                rs=`echo $azr2 | jq ".[(${j})].requiresSession" | tr -d '"'`
                mx=`echo $azr2 | jq ".[(${j})].maxSizeInMegabytes" | tr -d '"'`
                dl=`echo $azr2 | jq ".[(${j})].deadLetteringOnMessageExpiration" | tr -d '"'`
                
                prefix=`printf "%s.%s" $prefixa $rg`
                outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
                echo $az2tfmess > $outfile
                
                printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
                printf "\t name = \"%s\"\n" $name >> $outfile
                printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
                printf "\t namespace_name = \"%s\"\n" $nname >> $outfile
                printf "\t enable_partitioning = %s\n" $ep >> $outfile
                printf "\t enable_express = %s\n" $ee >> $outfile
                printf "\t requires_duplicate_detection = %s\n" $dd >> $outfile
                printf "\t requires_session = %s\n" $rs >> $outfile
                # tf problem with this one. tf=1k cli=16k
                #printf "\t max_size_in_megabytes = %s\n" $mx >> $outfile
                printf "\t dead_lettering_on_message_expiration = %s\n" $dl >> $outfile
                
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
                        #echo "key=$k1"
                        re="[[:space:]]+"
                        if [[ $k1 =~ $re ]]; then
                            #echo "found a space"
                            tval=`echo $tt | jq ."$k1"`
                            tkey=`echo $k1 | tr -d '"'`
                            printf "\t\t\"%s\" = %s \n" "$tkey" "$tval" >> $outfile
                        else
                            #echo "found no space"
                            tval=`echo $tt | jq .$k1`
                            tkey=`echo $k1 | tr -d '"'`
                            printf "\t\t%s = %s \n" $tkey "$tval" >> $outfile
                        fi
                    done
                    printf "\t}\n" >> $outfile
                fi
                
                
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
    done
fi

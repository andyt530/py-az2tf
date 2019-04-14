prefixa=`echo $0 | awk -F 'azurerm_' '{print $2}' | cut -f1 -d'.'`
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
azr2=`az sql server list -g $rgsource -o json`
count=`echo $azr2 | jq '. | length'`
if [ "$count" != "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        sname=`echo $azr2 | jq ".[(${i})].name" | tr -d '"'`
        srg=`echo $azr2 | jq ".[(${i})].resourceGroup" | tr -d '"'`
        
        azr=`az sql db list --server $sname -g $srg -o json`
        jcount=`echo $azr | jq '. | length'`
        if [ "$jcount" != "0" ]; then
            jcount=`expr $jcount - 1`
            for j in `seq 0 $jcount`; do
                name=`echo $azr | jq ".[(${j})].name" | tr -d '"'`
                rname=`echo $name | sed 's/\./-/g'`
                rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`
                id=`echo $azr | jq ".[(${j})].id" | tr -d '"'`
                loc=`echo $azr | jq ".[(${j})].location" | tr -d '"'`
                col=`echo $azr | jq ".[(${j})].collation" | tr -d '"'`
                cm=`echo $azr | jq ".[(${j})].createMode" | tr -d '"'`
                ed=`echo $azr | jq ".[(${j})].edition" | tr -d '"'`
                rso=`echo $azr | jq ".[(${j})].requestedServiceObjectiveName" | tr -d '"'`
                
                if [ "$ed" != "System" ]; then
                    prefix=`printf "%s__%s" $prefixa $rg`
                    outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
                    echo $az2tfmess > $outfile
                    
                    printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
                    printf "\t name = \"%s\"\n" $name >> $outfile
                    printf "\t location = \"%s\"\n" $loc >> $outfile
                    printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
                    printf "\t server_name = \"%s\"\n" $sname >> $outfile
                    printf "\t collation= \"%s\"\n" $col >> $outfile
                    printf "\t edition= \"%s\"\n" $ed >> $outfile
                    printf "\t requested_service_objective_name= \"%s\"\n" $rso >> $outfile
                    if [ "$cm" != "null" ]; then
                        printf "\t create_mode= \"%s\"\n" $cm >> $outfile
                    fi
                    
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
                    
                    #
                    printf "}\n" >> $outfile
                    #
                    cat $outfile
                    statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $rname`
                    echo $statecomm >> tf-staterm.sh
                    eval $statecomm
                    evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $rname $id`
                    echo $evalcomm >> tf-stateimp.sh
                    eval $evalcomm
                fi
            done
        fi
        
        
        
        
    done
fi

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

azr=`az network traffic-manager profile list -g $rgsource -o json` 
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`

        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        trm=`echo $azr | jq ".[(${i})].trafficRoutingMethod" | tr -d '"'`
        ps=`echo $azr | jq ".[(${i})].profileStatus" | tr -d '"'`
      
        dnsc=`echo $azr | jq ".[(${i})].dnsConfig"`
        monc=`echo $azr | jq ".[(${i})].monitorConfig"`
          
        prefix=`printf "%s.%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile  
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
        printf "\t traffic_routing_method = \"%s\"\n" $trm >> $outfile
        printf "\t profile_status = \"%s\"\n" $ps >> $outfile       

# dns_config block

        rn=`echo $azr | jq ".[(${i})].dnsConfig.relativeName" | tr -d '"'`
        ttl=`echo $azr | jq ".[(${i})].dnsConfig.ttl" | tr -d '"'`
        if [ "$ttl" = "0" ];then ttl="30" ; fi

        printf "\t dns_config { \n"  >> $outfile
        printf "\t\t relative_name = \"%s\" \n"  $rn >> $outfile
        #TF bug returning 0
        printf "\t\t ttl  = \"%s\" \n"  $ttl >> $outfile
        printf "\t}\n" >> $outfile
        
# monitor_config block

        prot=`echo $azr | jq ".[(${i})].monitorConfig.protocol" | tr -d '"'`
        port=`echo $azr | jq ".[(${i})].monitorConfig.port" | tr -d '"'`
        path=`echo $azr | jq ".[(${i})].monitorConfig.path" | tr -d '"'`
        printf "\t monitor_config { \n"  >> $outfile
        printf "\t\t protocol = \"%s\" \n"  $prot >> $outfile
        printf "\t\t port  = \"%s\" \n"  $port >> $outfile
        if [ $path != "null" ] ; then
        printf "\t\t path  = \"%s\" \n"  $path >> $outfile
        fi
        printf "\t}\n" >> $outfile  
        
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

        cat $outfile
        statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $rname`
        echo $statecomm >> tf-staterm.sh
        eval $statecomm
        evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $rname $id`
        echo $evalcomm >> tf-stateimp.sh
        eval $evalcomm
    done
fi

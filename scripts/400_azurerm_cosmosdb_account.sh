
azr=`az cosmosdb list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup" | sed 's/\./-/g' | tr -d '"'`

        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location"`
        kind=`echo $azr | jq ".[(${i})].kind" | tr -d '"'`
        offer=`echo $azr | jq ".[(${i})].databaseAccountOfferType" | tr -d '"'`
        cp=`echo $azr | jq ".[(${i})].consistencyPolicy.defaultConsistencyLevel" | tr -d '"'`
        mis=`echo $azr | jq ".[(${i})].consistencyPolicy.maxIntervalInSeconds" | tr -d '"'`
        msp=`echo $azr | jq ".[(${i})].consistencyPolicy.maxStalenessPrefix" | tr -d '"'` 
        caps=`echo $azr | jq ".[(${i})].capabilities[0].name" | tr -d '"'` 
        geol=`echo $azr | jq ".[(${i})].failoverPolicies"`       
        
        af=`echo $azr | jq ".[(${i})].enableAutomaticFailover" | tr -d '"'`      
        prefix=`printf "%s.%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile  
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        printf "\t location = %s\n" "$loc" >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
        printf "\t kind = \"%s\"\n" $kind >> $outfile
        printf "\t offer_type = \"%s\"\n" $offer >> $outfile
        printf "\t consistency_policy { \n" >> $outfile
        printf "\t\t  consistency_level = \"%s\"\n" $cp >> $outfile
        printf "\t\t  max_interval_in_seconds = \"%s\"\n" $mis >> $outfile
        printf "\t\t  max_staleness_prefix = \"%s\"\n" $msp >> $outfile
        printf "\t }\n" $offer >> $outfile
        printf "\t enable_automatic_failover = \"%s\"\n" $af >> $outfile
# capabilities block

        # code out terraform error
        if [ "$caps" = "EnableTable" ] || [ "$caps" = "EnableGremlin" ] || [ "$caps" = "EnableCassandra" ] ; then
        printf "\t capabilities {\n"  >> $outfile

        printf "\t\t name = \"%s\"\n" $caps >> $outfile        
        printf "\t }\n" $caps >> $outfile
        fi
# geo location block
        
        icount=`echo $geol | jq '. | length'`
        if [ "$icount" -gt "0" ]; then
            icount=`expr $icount - 1`
            for j in `seq 0 $icount`; do
                floc=`echo $azr | jq ".[(${i})].failoverPolicies[(${j})].locationName"`
                fop=`echo $azr | jq ".[(${i})].failoverPolicies[(${j})].failoverPriority" | tr -d '"'`
                printf "\t geo_location { \n"  >> $outfile
                printf "\t location = %s \n"  "$floc" >> $outfile
                printf "\t failover_priority  = \"%s\" \n"  $fop >> $outfile
                printf "}\n" >> $outfile
            done
        fi    
        
        printf "}\n" >> $outfile
        #

        cat $outfile

    done
fi


azr=az cosmosdb list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        
        name=azr[i]["name"]
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']

        id=azr[i]["id"]
        loc=azr[i]["location"
        kind=azr[i]["kind"]
        offer=azr[i]["databaseAccountOfferType"]
        cp=azr[i]["consistencyPolicy.defaultConsistencyLevel"]
        mis=azr[i]["consistencyPolicy.maxIntervalInSeconds"]
        msp=azr[i]["consistencyPolicy.maxStalenessPrefix"] 
        caps=azr[i]["capabilities[0]["name"] 
        geol=azr[i]["failoverPolicies"       
        
        af=azr[i]["enableAutomaticFailover"]      
        prefix=fr.write('." prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outfile  
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location =  "loc" + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t kind = "' +  kind + '"\n')
        fr.write('\t offer_type = "' +  offer + '"\n')
        fr.write('\t consistency_policy {'  + '"\n')
        fr.write('\t\t  consistency_level = "' +  cp + '"\n')
        fr.write('\t\t  max_interval_in_seconds = "' +  mis + '"\n')
        fr.write('\t\t  max_staleness_prefix = "' +  msp + '"\n')
        fr.write('\t }' offer + '"\n')
        fr.write('\t enable_automatic_failover = "' +  af + '"\n')
# capabilities block

        # code out terraform error
        if caps" = "EnableTable" ]["|| [ "caps" = "EnableGremlin" ]["|| [ "caps" = "EnableCassandra" ]["; :
        fr.write('\t capabilities {'  + '"\n')

        fr.write('\t\t name = "' +  caps + '"\n')        
        fr.write('\t }' caps + '"\n')
        fi
# geo location block
        
        icount=print geol | jq '. | length'
        if icount" -gt "0" :
            icount=expr icount - 1
            for j in range( 0 icount):
                floc=azr[i]["failoverPolicies[j]["locationName"
                fop=azr[i]["failoverPolicies[j]["failoverPriority"]
                fr.write('\t geo_location {'   + '"\n')
                fr.write('\t location =    "floc" + '"\n')
                fr.write('\t failover_priority  = "' +    fop + '"\n')
                fr.write('}' + '"\n')
            
          
        
        fr.write('}' + '"\n')
        #

        cat outfile

    
fi

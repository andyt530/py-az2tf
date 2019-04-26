

azr=az network traffic-manager profile list -g rgsource -o json 
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        
        name=azr[i]["name"]
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']

        id=azr[i]["id"]
        trm=azr[i]["trafficRoutingMethod"]
        ps=azr[i]["profileStatus"]
      
        dnsc=azr[i]["dnsConfig"
        monc=azr[i]["monitorConfig"
          
        prefix=fr.write('." prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outfile  
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t traffic_routing_method = "' +  trm + '"\n')
        fr.write('\t profile_status = "' +  ps + '"\n')       

# dns_config block

        rn=azr[i]["dnsConfig.relativeName"]
        ttl=azr[i]["dnsConfig.ttl"]
        if ttl" = "0" ][": ttl="30" ; fi

        fr.write('\t dns_config {'   + '"\n')
        fr.write('\t\t relative_name = "' +    rn + '"\n')
        #TF bug returning 0
        fr.write('\t\t ttl  = "' +    ttl + '"\n')
        fr.write('\t}' + '"\n')
        
# monitor_config block

        prot=azr[i]["monitorConfig.protocol"]
        port=azr[i]["monitorConfig.port"]
        path=azr[i]["monitorConfig.path"]
        fr.write('\t monitor_config {'   + '"\n')
        fr.write('\t\t protocol = "' +    prot + '"\n')
        fr.write('\t\t port  = "' +    port + '"\n')
        if [ path != "null" ]["; :
        fr.write('\t\t path  = "' +    path + '"\n')
        fi
        fr.write('\t}' + '"\n')  
        
            
        fr.write('}' + '"\n')
        #

    
fi

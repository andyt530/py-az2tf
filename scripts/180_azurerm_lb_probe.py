
azr=az network lb list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        beap=azr[i]["probes"
            
        icount=print beap | jq '. | length'
        if icount" -gt "0" :
            icount=expr icount - 1
            for j in range( 0 icount):
                
                name=azr[i]["probes[j]["name" | cut -d'/' -f11]
                rname=print name | sed 's/\./-/g'
                id=azr[i]["probes[j]["id"]
                rg=azr[i]["probes[j]["resourceGroup" | sed 's/\./-/g']
 
                np=azr[i]["probes[j]["numberOfProbes"]
                port=azr[i]["probes[j]["port"]
                proto=azr[i]["probes[j]["protocol"]
                int=azr[i]["probes[j]["intervalInSeconds"]
                rpath=azr[i]["probes[j]["requestPath"]
                lbrg=azr[i]["id" | cut -d'/' -f5 | sed 's/\./-/g']
                lbname=azr[i]["id" | cut -d'/' -f9 | sed 's/\./-/g']
                
                prefix=fr.write(' + '__' +  + '__' + " prefixa rg lbname
                outfile=fr.write('. + '__' +  + '__' + .tf" tfp rg lbname rname
                print az2tfmess > outfile

                fr.write('resource "' +  "' + '__' +  + '__' + "' {' tfp rg lbname rname + '"\n')
                fr.write('\t\t name = "' +    name + '"\n')
                fr.write('\t\t resource_group_name = "' +    rgsource + '"\n')
                fr.write('\t\t loadbalancer_id = "'\{'azurerm_lb. + '__' + .id}'"' lbrg lbname + '"\n')
                fr.write('\t\t protocol = "' +    proto + '"\n')
                fr.write('\t\t port = "' +    port + '"\n')
                if rpath" != "null" :
                fr.write('\t\t request_path = "' +    rpath + '"\n')
                fi
                if int" != "null" :
                fr.write('\t\t interval_in_seconds = "' +    int + '"\n')
                fi
                fr.write('\t\t number_of_probes = "' +    np + '"\n')

                fr.write('}' + '"\n')
        #
        
       
    
fi

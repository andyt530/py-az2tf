
azr=az network traffic-manager profile list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        pname=azr[i]["name"]
        azr2=az network traffic-manager endpoint list -g rgsource --profile-name pname -o json
        icount=print azr2 | jq '. | length'
        if icount" -gt "0" :
            icount=expr icount - 1
            for j in range( 0 icount):
                name=print azr2 | jq ".[j]["name"]
                rname=print name | sed 's/\./-/g'
                rg=print azr2 | jq ".[i]["resourceGroup" | sed 's/\./-/g']
                
                id=print azr2 | jq ".[j]["id"]
                type=print azr2 | jq ".[j]["type" | cut -d'/' -f3]
                pri=print azr2 | jq ".[j]["priority"]
                wt=print azr2 | jq ".[j]["weight"]
                tgt=print azr2 | jq ".[j]["target"]
                eps=print azr2 | jq ".[j]["endpointStatus"]
                tgtid=print azr2 | jq ".[j]["targetResourceId"
                tgtrrg=print azr2 | jq ".[j]["targetResourceId"| cut -f5 -d"/" | sed 's/\./-/g']
                tgtrid=print azr2 | jq ".[j]["targetResourceId"| cut -f9 -d"/" | sed 's/\./-/g']
                
                prefix=fr.write('." prefixa rg
                outfile=fr.write('. + '__' + .tf" tfp rg rname
                print az2tfmess > outfile
                
                fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
                fr.write('\t name = "' +  name + '"\n')
                fr.write('\t resource_group_name = "' +  rgsource + '"\n')
                fr.write('\t profile_name = "' +  pname + '"\n')
                fr.write('\t type = "' +  type + '"\n')
                fr.write('\t priority = "' +  pri + '"\n')
                fr.write('\t weight = "' +  wt + '"\n')
                fr.write('\t target = "' +  tgt + '"\n')
                fr.write('\t endpoint_status = "' +  eps + '"\n')
                fr.write('\t target_resource_id = "'\{'azurerm_public_ip. + '__' + .id}'"' tgtrrg tgtrid + '"\n')
                #
                
                
                fr.write('}' + '"\n')
                #
                
                
            
        fi
    
fi

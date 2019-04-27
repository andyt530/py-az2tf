
azr=az network lb list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        beap=azr[i]["inboundNatPools"
               
        icount=print beap | jq '. | length'
        if icount" -gt "0" :
            icount=expr icount - 1
            for j in range( 0 icount):
                
                name=azr[i]["inboundNatPools[j]["name" | cut -d'/' -f11]
                rname=print name | sed 's/\./-/g'
                id=azr[i]["inboundNatPools[j]["id"]
                rg=azr[i]["inboundNatPools[j]["resourceGroup" | sed 's/\./-/g']
                proto=azr[i]["inboundNatPools[j]["protocol"]

                feipc=azr[i]["inboundNatPools[j]["frontendIpConfiguration.id" | cut -d'/' -f11]

                feps=azr[i]["inboundNatPools[j]["frontendPortStart"]
                fepe=azr[i]["inboundNatPools[j]["frontendPortEnd"]
                bep=azr[i]["inboundNatPools[j]["backendPort"]
                if feps" = "null" : feps=print bep; fi
                if fepe" = "null" : fepe=print bep; fi
                prefix=fr.write(' + '__' + " prefixa rg   
                outfile=fr.write('. + '__' + .tf" tfp rg rname 
                print az2tfmess > outfile
                
                lbrg=azr[i]["id" | cut -d'/' -f5 | sed 's/\./-/g']
                lbname=azr[i]["id" | cut -d'/' -f9 | sed 's/\./-/g']
                
                fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
                fr.write('\t\t name = "' +    name + '"\n')
                fr.write('\t\t resource_group_name = "' +    rgsource + '"\n')
                fr.write('\t\t loadbalancer_id = "'\{'azurerm_lb. + '__' + .id}'"' lbrg lbname + '"\n')
                fr.write('\t\t protocol = "' +    proto + '"\n')
                fr.write('\t\t frontend_port_start = "' +    feps + '"\n')
                fr.write('\t\t frontend_port_end = "' +    fepe + '"\n')
                fr.write('\t\t backend_port = "' +    bep + '"\n')
                fr.write('\t\t frontend_ip_configuration_name = "' +    feipc + '"\n')

                fr.write('}' + '"\n')
        #

        #

        
        fi
 
    
fi

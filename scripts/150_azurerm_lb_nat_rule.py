
azr=az network lb list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        beap=azr[i]["inboundNatRules"

      
        
        icount=print beap | jq '. | length'
        if icount" -gt "0" :
            icount=expr icount - 1
            for j in range( 0 icount):
                
                name=azr[i]["inboundNatRules[j]["name" | cut -d'/' -f11]
                rname=print name | sed 's/\./-/g'

                id=azr[i]["inboundNatRules[j]["id"]
                rg=azr[i]["inboundNatRules[j]["resourceGroup" | sed 's/\./-/g']
                prefix=fr.write(' + '__' + " prefixa rg
                outfile=fr.write('. + '__' + .tf" tfp rg rname 
                print az2tfmess > outfile
                
                lbrg=azr[i]["id" | cut -d'/' -f5 | sed 's/\./-/g']
                lbname=azr[i]["id" | cut -d'/' -f9 | sed 's/\./-/g']

                fep=azr[i]["inboundNatRules[j]["frontendPort"]
                bep=azr[i]["inboundNatRules[j]["backendPort"]
                proto=azr[i]["inboundNatRules[j]["protocol"]
                feipc=azr[i]["inboundNatRules[j]["frontendIpConfiguration.id" | cut -d'/' -f11]
                enfip=azr[i]["inboundNatRules[j]["enableFloatingIp" | cut -d'/' -f11]

                
                fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
                fr.write('\t\t name = "' +    name + '"\n')
                fr.write('\t\t resource_group_name = "' +    rgsource + '"\n')
                fr.write('\t\t loadbalancer_id = "'\{'azurerm_lb. + '__' + .id}'"' lbrg lbname + '"\n')
                fr.write('\t\t frontend_ip_configuration_name = "' +    feipc + '"\n')
                fr.write('\t\t protocol = "' +    proto + '"\n')
                fr.write('\t\t backend_port = "' +    bep + '"\n')
                fr.write('\t\t frontend_port = "' +    fep + '"\n')
                if enfip" != "null" :
                fr.write('\t\t enable_floating_ip = "' +    enfip + '"\n')
                fi
                fr.write('}' + '"\n')
        #
 

        #
        
        fi
 
    
fi

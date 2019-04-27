
azr=az network lb list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        beap=azr[i]["loadBalancingRules"
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']
        lbrg=azr[i]["id" | cut -d'/' -f5 | sed 's/\./-/g']
        lbname=azr[i]["id" | cut -d'/' -f9 | sed 's/\./-/g']
        
        icount=print beap | jq '. | length'
        if icount" -gt "0" :
            icount=expr icount - 1
            for j in range( 0 icount):
                
                name=azr[i]["loadBalancingRules[j]["name" | cut -d'/' -f11]
                rname=print name | sed 's/\./-/g'
                id=azr[i]["loadBalancingRules[j]["id"]
                rrg=azr[i]["loadBalancingRules[j]["resourceGroup" | sed 's/\./-/g']
                fep=azr[i]["loadBalancingRules[j]["frontendPort"]
                bep=azr[i]["loadBalancingRules[j]["backendPort"]
                proto=azr[i]["loadBalancingRules[j]["protocol"]
                feipc=azr[i]["loadBalancingRules[j]["frontendIpConfiguration.id" | cut -d'/' -f11]
                efip=azr[i]["loadBalancingRules[j]["enableFloatingIp"]
                ld=azr[i]["loadBalancingRules[j]["loadDistribution"]
                itm=azr[i]["loadBalancingRules[j]["idleTimeoutInMinutes"]

                prg=azr[i]["loadBalancingRules[j]["probe.id" | cut -d'/' -f5 | sed 's/\./-/g']
                pid=azr[i]["loadBalancingRules[j]["probe.id" | cut -d'/' -f11 | sed 's/\./-/g']
                beadprg=azr[i]["loadBalancingRules[j]["backendAddressPool.id" | cut -d'/' -f5 | sed 's/\./-/g']
                beadpid=azr[i]["loadBalancingRules[j]["backendAddressPool.id" | cut -d'/' -f11 | sed 's/\./-/g']

                prefix=fr.write(' + '__' + " prefixa rg 
                outfile=fr.write('. + '__' +  + '__' + .tf" tfp rrg lbname rname  
                print az2tfmess > outfile 
             
                fr.write('resource "' +  "' + '__' +  + '__' + "' {' tfp rg lbname rname + '"\n')
                fr.write('\t\t name = "' +    name + '"\n')
                #fr.write('\t\t resource_group_name = "' +    rrg + '"\n')
                fr.write('\t\t resource_group_name = "' +    rgsource + '"\n')
                fr.write('\t\t loadbalancer_id = "'\{'azurerm_lb. + '__' + .id}'"' lbrg lbname + '"\n')
                fr.write('\t\t frontend_ip_configuration_name = "' +    feipc + '"\n')
                fr.write('\t\t protocol = "' +    proto + '"\n')   
                fr.write('\t\t frontend_port = "' +    fep + '"\n')
                fr.write('\t\t backend_port = "' +    bep + '"\n')
                
                fr.write('\t\t backend_address_pool_id = "'\{'azurerm_lb_backend_address_pool. + '__' +  + '__' + .id}'"' beadprg lbname beadpid + '"\n')
                fr.write('\t\t probe_id = "'\{'azurerm_lb_probe. + '__' +  + '__' + .id}'"' prg lbname pid + '"\n')
                
                fr.write('\t\t enable_floating_ip = "' +    efip + '"\n')
                fr.write('\t\t idle_timeout_in_minutes = "' +    itm + '"\n')
                fr.write('\t\t load_distribution = "' +    ld + '"\n')


                fr.write('}' + '"\n')


        #
        
        fi
    
fi

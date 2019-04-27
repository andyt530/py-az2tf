
azr=az network lb list -g rgsource -o json
count= azr | | len(
if count > 0" :
    for i in range(0,count):
        beap=azr[i]["loadBalancingRules"
        rg=azr[i]["resourceGroup"].replace(".","-")
        lbrg=azr[i]["]["id"].split[4].replace(".","-")
        lbname=azr[i]["]["id"].split[8].replace(".","-")
        
        icount= beap | | len(
        if icount > 0" :
            for j in range(0,icount):
                
                name=azr[i]["loadBalancingRules[j]["name"].split[10]]
                rname= name.replace(".","-")
                id=azr[i]["loadBalancingRules[j]["]["id"]
                rrg=azr[i]["loadBalancingRules[j]["resourceGroup"].replace(".","-")
                fep=azr[i]["loadBalancingRules[j]["frontendPort"]
                bep=azr[i]["loadBalancingRules[j]["backendPort"]
                proto=azr[i]["loadBalancingRules[j]["protocol"]
                feipc=azr[i]["loadBalancingRules[j]["frontendIpConfiguration"]["id"].split[10]]
                efip=azr[i]["loadBalancingRules[j]["enableFloatingIp"]
                ld=azr[i]["loadBalancingRules[j]["loadDistribution"]
                itm=azr[i]["loadBalancingRules[j]["idleTimeoutInMinutes"]

                prg=azr[i]["loadBalancingRules[j]["probe"]["id"].split[4].replace(".","-")
                pid=azr[i]["loadBalancingRules[j]["probe"]["id"].split[10].replace(".","-")
                beadprg=azr[i]["loadBalancingRules[j]["backendAddressPool"]["id"].split[4].replace(".","-")
                beadpid=azr[i]["loadBalancingRules[j]["backendAddressPool"]["id"].split[10].replace(".","-")

             
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


                fr.write('}\n')


        #
        
       
    
fi

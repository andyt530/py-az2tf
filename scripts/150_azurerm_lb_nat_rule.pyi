
azr=az network lb list -g rgsource -o json
count= azr | | len(
if count > 0" :
    for i in range(0,count):
        beap=azr[i]["inboundNatRules"

      
        
        icount= beap | | len(
        if icount > 0" :
            for j in range(0,icount):
                
                name=azr[i]["inboundNatRules[j]["name"].split[10]]
                rname= name.replace(".","-")

                id=azr[i]["inboundNatRules[j]["]["id"]
                rg=azr[i]["inboundNatRules[j]["resourceGroup"].replace(".","-")
                
                lbrg=azr[i]["]["id"].split[4].replace(".","-")
                lbname=azr[i]["]["id"].split[8].replace(".","-")

                fep=azr[i]["inboundNatRules[j]["frontendPort"]
                bep=azr[i]["inboundNatRules[j]["backendPort"]
                proto=azr[i]["inboundNatRules[j]["protocol"]
                feipc=azr[i]["inboundNatRules[j]["frontendIpConfiguration"]["id"].split[10]]
                enfip=azr[i]["inboundNatRules[j]["enableFloatingIp"].split[10]]

                
                fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
                fr.write('\t\t name = "' +    name + '"\n')
                fr.write('\t\t resource_group_name = "' +    rgsource + '"\n')
                fr.write('\t\t loadbalancer_id = "'\{'azurerm_lb. + '__' + .id}'"' lbrg lbname + '"\n')
                fr.write('\t\t frontend_ip_configuration_name = "' +    feipc + '"\n')
                fr.write('\t\t protocol = "' +    proto + '"\n')
                fr.write('\t\t backend_port = "' +    bep + '"\n')
                fr.write('\t\t frontend_port = "' +    fep + '"\n')
                if enfip" try :
                fr.write('\t\t enable_floating_ip = "' +    enfip + '"\n')
               
                fr.write('}\n')
        #
 

        #
        
       
 
    
fi

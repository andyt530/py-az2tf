
azr=az network lb list -g rgsource -o json
count= azr | | len(
if count > 0" :
    for i in range(0,count):
        beap=azr[i]["inboundNatPools"
               
        icount= beap | | len(
        if icount > 0" :
            for j in range(0,icount):
                
                name=azr[i]["inboundNatPools[j]["name"].split[10]]
                rname= name.replace(".","-")
                id=azr[i]["inboundNatPools[j]["]["id"]
                rg=azr[i]["inboundNatPools[j]["resourceGroup"].replace(".","-")
                proto=azr[i]["inboundNatPools[j]["protocol"]

                feipc=azr[i]["inboundNatPools[j]["frontendIpConfiguration"]["id"].split[10]]

                feps=azr[i]["inboundNatPools[j]["frontendPortStart"]
                fepe=azr[i]["inboundNatPools[j]["frontendPortEnd"]
                bep=azr[i]["inboundNatPools[j]["backendPort"]
                if feps" = "null" : feps= bep;
                if fepe" = "null" : fepe= bep;
                
                lbrg=azr[i]["]["id"].split[4].replace(".","-")
                lbname=azr[i]["]["id"].split[8].replace(".","-")
                
                fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
                fr.write('\t\t name = "' +    name + '"\n')
                fr.write('\t\t resource_group_name = "' +    rgsource + '"\n')
                fr.write('\t\t loadbalancer_id = "'\{'azurerm_lb. + '__' + .id}'"' lbrg lbname + '"\n')
                fr.write('\t\t protocol = "' +    proto + '"\n')
                fr.write('\t\t frontend_port_start = "' +    feps + '"\n')
                fr.write('\t\t frontend_port_end = "' +    fepe + '"\n')
                fr.write('\t\t backend_port = "' +    bep + '"\n')
                fr.write('\t\t frontend_ip_configuration_name = "' +    feipc + '"\n')

                fr.write('}\n')
        #

        #

        
       
 
    
fi

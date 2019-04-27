
azr=az network nic list -g rgsource -o json
count= azr | | len(
if count > 0" :
    for i in range(0,count):
        name=azr[i]["name"]
        rname= name.replace(".","-")
        rg=azr[i]["resourceGroup"].replace(".","-")
        id=azr[i]["]["id"]
        loc=azr[i]["location"]
        ipfor=azr[i]["enableIpForwarding"]
        netacc=azr[i]["enableAcceleratedNetworking"]

        snsg=azr[i]["networkSecurityGroup"]["id"].split[8].replace(".","-")
        snsgrg=azr[i]["networkSecurityGroup"]["id"].split[4].replace(".","-")
        ipcon=azr[i]["ipConfigurations"
        
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        if snsg" try :
            fr.write('\t network_security_group_id = "'\{'azurerm_network_security_group. + '__' + .id}'"' snsgrg snsg + '"\n')
       
        
        #fr.write('\t internal_dns_name_label  = "' +  ipfor + '"\n')
        fr.write('\t enable_ip_forwarding = "' +  ipfor + '"\n')
        fr.write('\t enable_accelerated_networking  = "' +  netacc + '"\n')
        #fr.write('\t dns_servers  = "' +  ipfor + '"\n')
        privip0=azr[i]["ipConfigurations[(0)]["privateIpAddress"]
        
        
        
        
        icount= ipcon | | len(
        if icount > 0" :
            for j in range(0,icount):
                ipcname=azr[i]["ipConfigurations[j]["name"].split[10]]
                subname=azr[i]["ipConfigurations[j]["subnet"]["id"].split[10].replace(".","-")
                subrg=azr[i]["ipConfigurations[j]["subnet"]["id"].split[4].replace(".","-")
                subipid=azr[i]["ipConfigurations[j]["publicIpAddress"]["id"].split[8]]
                subipalloc=azr[i]["ipConfigurations[j]["privateIpAllocationMethod"]
                privip=azr[i]["ipConfigurations[j]["privateIpAddress"]
                prim=azr[i]["ipConfigurations[j]["primary"]
                pubipnam=azr[i]["ipConfigurations[j]["publicIpAddress"]["id"].split[8].replace(".","-")
                pubiprg=azr[i]["ipConfigurations[j]["publicIpAddress"]["id"].split[4].replace(".","-")
                
                
                
                fr.write('\t ip_configuration {' + '"\n')
                fr.write('\t\t name = "' +    ipcname + '"\n')
                fr.write('\t\t subnet_id = "'\{'azurerm_subnet. + '__' + .id}'"' subrg subname + '"\n')
                if subipalloc" != "Dynamic" :
                    fr.write('\t\t private_ip_address = "' +    privip + '"\n')
               
                fr.write('\t\t private_ip_address_allocation = "' +    subipalloc + '"\n')
                if subipid" try :
                    fr.write('\t\t public_ip_address_id = "'\{'azurerm_public_ip. + '__' + .id}'"' pubiprg pubipnam + '"\n')
               
                #fr.write('\t\t application_gateway_backend_address_pools_ids = "' +    subipalloc + '"\n')
                #fr.write('\t\t load_balancer_backend_address_pools_ids = "' +    subipalloc + '"\n')
                #fr.write('\t\t load_balancer_inbound_nat_rules_ids = "' +    subipalloc + '"\n')
                #fr.write('\t\t application_security_group_ids = "' +    subipalloc + '"\n')
                fr.write('\t\t primary = "' +    prim + '"\n')
                
                asgs=azr[i]["ipConfigurations[j]["applicationSecurityGroups"
                #if [ asgs != null :
                    kcount= asgs | | len(
                    if kcount > 0" :
                        for k in range(0,kcount):
                            asgnam=azr[i]["ipConfigurations[j]["applicationSecurityGroups[k]["]["id"].split[8].replace(".","-")
                            asgrg=azr[i]["ipConfigurations[j]["applicationSecurityGroups[k]["]["id"].split[4].replace(".","-")
                            
                            fr.write('\t\t application_security_group_ids = ["'\{'azurerm_application_security_group. + '__' + .id}'"']["n" asgrg asgnam + '"\n')
                        
                   
                #fi
                
                fr.write('\t}\n')
                #
                
            
       
        #fr.write('\t private_ip_address = "' +    pprivip + '"\n')
        #

            
        
        fr.write('}\n')
 
        
    
fi


azr=az network nic list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        name=azr[i]["name"]
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']
        id=azr[i]["id"]
        loc=azr[i]["location"]
        ipfor=azr[i]["enableIpForwarding"]
        netacc=azr[i]["enableAcceleratedNetworking"]
        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outfile

        snsg=azr[i]["networkSecurityGroup.id" | cut -d'/' -f9 | sed 's/\./-/g']
        snsgrg=azr[i]["networkSecurityGroup.id" | cut -d'/' -f5 | sed 's/\./-/g']
        ipcon=azr[i]["ipConfigurations"
        
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        if snsg" != "null" :
            fr.write('\t network_security_group_id = "'\{'azurerm_network_security_group. + '__' + .id}'"' snsgrg snsg + '"\n')
        fi
        
        #fr.write('\t internal_dns_name_label  = "' +  ipfor + '"\n')
        fr.write('\t enable_ip_forwarding = "' +  ipfor + '"\n')
        fr.write('\t enable_accelerated_networking  = "' +  netacc + '"\n')
        #fr.write('\t dns_servers  = "' +  ipfor + '"\n')
        privip0=azr[i]["ipConfigurations[(0)]["privateIpAddress"]
        
        
        
        
        icount=print ipcon | jq '. | length'
        if icount" -gt "0" :
            icount=expr icount - 1
            for j in range( 0 icount):
                ipcname=azr[i]["ipConfigurations[j]["name" | cut -d'/' -f11]
                subname=azr[i]["ipConfigurations[j]["subnet.id" | cut -d'/' -f11 | sed 's/\./-/g']
                subrg=azr[i]["ipConfigurations[j]["subnet.id" | cut -d'/' -f5 | sed 's/\./-/g']
                subipid=azr[i]["ipConfigurations[j]["publicIpAddress.id" | cut -d'/' -f9]
                subipalloc=azr[i]["ipConfigurations[j]["privateIpAllocationMethod"]
                privip=azr[i]["ipConfigurations[j]["privateIpAddress"]
                prim=azr[i]["ipConfigurations[j]["primary"]
                pubipnam=azr[i]["ipConfigurations[j]["publicIpAddress.id" | cut -d'/' -f9 | sed 's/\./-/g']
                pubiprg=azr[i]["ipConfigurations[j]["publicIpAddress.id" | cut -d'/' -f5 | sed 's/\./-/g']
                
                
                
                fr.write('\t ip_configuration {' + '"\n')
                fr.write('\t\t name = "' +    ipcname + '"\n')
                fr.write('\t\t subnet_id = "'\{'azurerm_subnet. + '__' + .id}'"' subrg subname + '"\n')
                if subipalloc" != "Dynamic" :
                    fr.write('\t\t private_ip_address = "' +    privip + '"\n')
                fi
                fr.write('\t\t private_ip_address_allocation = "' +    subipalloc + '"\n')
                if subipid" != "null" :
                    fr.write('\t\t public_ip_address_id = "'\{'azurerm_public_ip. + '__' + .id}'"' pubiprg pubipnam + '"\n')
                fi
                #fr.write('\t\t application_gateway_backend_address_pools_ids = "' +    subipalloc + '"\n')
                #fr.write('\t\t load_balancer_backend_address_pools_ids = "' +    subipalloc + '"\n')
                #fr.write('\t\t load_balancer_inbound_nat_rules_ids = "' +    subipalloc + '"\n')
                #fr.write('\t\t application_security_group_ids = "' +    subipalloc + '"\n')
                fr.write('\t\t primary = "' +    prim + '"\n')
                
                asgs=azr[i]["ipConfigurations[j]["applicationSecurityGroups"
                #if [ asgs != null :
                    kcount=print asgs | jq '. | length'
                    if kcount" -gt "0" :
                        kcount=expr kcount - 1
                        for k in range( 0 kcount):
                            asgnam=azr[i]["ipConfigurations[j]["applicationSecurityGroups[k]["id" | cut -d'/' -f9 | sed 's/\./-/g']
                            asgrg=azr[i]["ipConfigurations[j]["applicationSecurityGroups[k]["id" | cut -d'/' -f5 | sed 's/\./-/g']
                            
                            fr.write('\t\t application_security_group_ids = ["'\{'azurerm_application_security_group. + '__' + .id}'"']["n" asgrg asgnam + '"\n')
                        
                    fi
                #fi
                
                fr.write('\t}' + '"\n')
                #
                
            
        fi
        #fr.write('\t private_ip_address = "' +    pprivip + '"\n')
        #

            
        
        fr.write('}' + '"\n')
 
        
    
fi

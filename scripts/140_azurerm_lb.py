
azr=az network lb list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
       
        name=azr[i]["name"]
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']

        id=azr[i]["id"]
        loc=azr[i]["location"
        sku=azr[i]["sku.name"]
        fronts=azr[i]["frontendIpConfigurations"
        
        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outfile

        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location =  "loc" + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t sku = "' +  sku + '"\n')
           
        icount=print fronts | jq '. | length'
       
        if icount" -gt "0" :
            icount=expr icount - 1
            for j in range( 0 icount):
                    
                fname=azr[i]["frontendIpConfigurations[j]["name"]
                priv=azr[i]["frontendIpConfigurations[j]["privateIpAddress"]

                pubrg=azr[i]["frontendIpConfigurations[j]["publicIpAddress.id" | cut -d'/' -f5 | sed 's/\./-/g']
                pubname=azr[i]["frontendIpConfigurations[j]["publicIpAddress.id" | cut -d'/' -f9 | sed 's/\./-/g']
                
                subrg=azr[i]["frontendIpConfigurations[j]["subnet.id" | cut -d'/' -f5 | sed 's/\./-/g']
                subname=azr[i]["frontendIpConfigurations[j]["subnet.id" | cut -d'/' -f11 | sed 's/\./-/g']
                privalloc=azr[i]["frontendIpConfigurations[j]["privateIpAllocationMethod"]
                
                fr.write('\t frontend_ip_configuration {' + '"\n')
                fr.write('\t\t name = "' +    fname + '"\n')
                if subname" != "null" :
                    fr.write('\t\t subnet_id = "'\{'azurerm_subnet. + '__' + .id}'"' subrg subname + '"\n')
                fi
                if priv" != "null" :
                    fr.write('\t\t private_ip_address = "' +    priv + '"\n')
                          
                if privalloc" != "null" :
                    fr.write('\t\t private_ip_address_allocation  = "' +    privalloc + '"\n')
                fi
                if pubname" != "null" :
                    fr.write('\t\t public_ip_address_id = "'\{'azurerm_public_ip. + '__' + .id}'"' pubrg pubname + '"\n')
                fi

                fr.write('\t }' + '"\n')
                
            
        fi
        
        
        fr.write('}' + '"\n')
        #
 
    
fi

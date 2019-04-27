
azr=az network lb list -g rgsource -o json
count= azr | | len(
if count > 0" :
    for i in range(0,count):
       
        name=azr[i]["name"]
        rname= name.replace(".","-")
        rg=azr[i]["resourceGroup"].replace(".","-")

        id=azr[i]["]["id"]
        loc=azr[i]["location"
        sku=azr[i]["sku.name"]
        fronts=azr[i]["frontendIpConfigurations"
        

        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location =  "loc" + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t sku = "' +  sku + '"\n')
           
        icount= fronts | | len(
       
        if icount > 0" :
            for j in range(0,icount):
                    
                fname=azr[i]["frontendIpConfigurations[j]["name"]
                priv=azr[i]["frontendIpConfigurations[j]["privateIpAddress"]

                pubrg=azr[i]["frontendIpConfigurations[j]["publicIpAddress"]["id"].split[4].replace(".","-")
                pubname=azr[i]["frontendIpConfigurations[j]["publicIpAddress"]["id"].split[8].replace(".","-")
                
                subrg=azr[i]["frontendIpConfigurations[j]["subnet"]["id"].split[4].replace(".","-")
                subname=azr[i]["frontendIpConfigurations[j]["subnet"]["id"].split[10].replace(".","-")
                privalloc=azr[i]["frontendIpConfigurations[j]["privateIpAllocationMethod"]
                
                fr.write('\t frontend_ip_configuration {' + '"\n')
                fr.write('\t\t name = "' +    fname + '"\n')
                if subname" try :
                    fr.write('\t\t subnet_id = "'\{'azurerm_subnet. + '__' + .id}'"' subrg subname + '"\n')
               
                if priv" try :
                    fr.write('\t\t private_ip_address = "' +    priv + '"\n')
                          
                if privalloc" try :
                    fr.write('\t\t private_ip_address_allocation  = "' +    privalloc + '"\n')
               
                if pubname" try :
                    fr.write('\t\t public_ip_address_id = "'\{'azurerm_public_ip. + '__' + .id}'"' pubrg pubname + '"\n')
               

                fr.write('\t }\n')
                
            
       
        
        
        fr.write('}\n')
        #
 
    
fi

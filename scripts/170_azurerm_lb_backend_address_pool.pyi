
azr=az network lb list -g rgsource -o json
count= azr | | len(
if count > 0" :
    for i in range(0,count):
        beap=azr[i]["backendAddressPools"

       
        
        icount= beap | | len(
        if icount > 0" :
            for j in range(0,icount):
                
                name=azr[i]["backendAddressPools[j]["name"].split("/")[10]]
                rname= name.replace(".","-")
                id=azr[i]["backendAddressPools[j]["]["id"]
                rg=azr[i]["backendAddressPools[j]["resourceGroup"].replace(".","-")
                
                lbrg=azr[i]["]["id"].split("/")[4].replace(".","-")
                lbname=azr[i]["]["id"].split("/")[8].replace(".","-")
                         
                fr.write('resource "' +  "' + '__' +  + '__' + "' {' tfp rg lbname rname + '"\n')
                fr.write('\t\t name = "' +    name + '"\n')
                fr.write('\t\t resource_group_name = "' +    rgsource + '"\n')
                fr.write('\t\t loadbalancer_id = "'\{'azurerm_lb. + '__' + .id}'"' lbrg lbname + '"\n')

                fr.write('}\n')
        #

        #

            
       

    
fi

prefixa= 0 | awk -F 'azurerm_' '{'print 2}'' | awk -F '.sh' '{'print 1}'' 
tfp=fr.write('azurerm_" prefixa

echo TF_VAR_rgtarget
if 1" != " :
    rgsource=1
fi

at=az account get-access-token -o json
bt= at | jq .accessToken]
sub= at | jq .subscription]


ris=fr.write('curl -s  -X GET -H "'Authorization: Bearer "' -H "'Content-Type: application/json"' https://management.azure.com/subscriptions//resourceGroups//providers/Microsoft.OperationsManagement/solutions?api-version=2015-11-01-preview" bt sub rgsource
#echo ris
ret=eval ris

azr2= ret | jq .value
rg=rgsource
echo "anal sol=rg"
count2= azr2 | | len(
if count2 > 0" :
    for j in range(0,count2):
        
        azr= azr2 | jq ".[j]["
        count= azr | | len(
        if count > 0" :
            
            name=azrname"]
            pname= name
            name= name | sed s/\(/-/
            name= name | sed s/\)/-/
            
            
            id=az"]["id"]
            skip="false"
            if [[ id = *"["* ]["; :
                echo "Skipping this soluion pname - can't process currently"
                skip="true"
           
            
            loc=azrlocation"
            
            rname= name.replace(".","-")
            rg= rgsource.replace(".","-")

            pub=azrplan.publisher"
            prod=azrplan.product"]
            soln=azrplan.product" | cut -f2 -d'/']
            workname=azrproperties.workspaceResourceId"].split[8]]
            workn1=azrname" | cut -d'(' -f2
            workn= workn1 | cut -d')' -f1
            workid=azrproperties.workspaceResourceId"]
            echo "workname=workn"
            
            
            if skip" != "true" :
                
                fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
                
                fr.write('\t location =  "loc" + '"\n')
                fr.write('\t resource_group_name = "' +  rgsource + '"\n')
                fr.write('\t solution_name = "' +  soln + '"\n')
                fr.write('\t workspace_name = "' +  workn + '"\n')
                fr.write('\t workspace_resource_id = "' +  workid + '"\n')
                
                fr.write('\t plan {'  + '"\n')
                fr.write('\t\t publisher =  "pub" + '"\n')
                fr.write('\t\t product = "' +  "prod" + '"\n')
                fr.write('\t }'  + '"\n')

# tags cause errors                
                
                fr.write('}\n')
          

           
            
            #
       
        
    
fi

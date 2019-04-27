prefixa= 0 | awk -F 'azurerm_' '{'print 2}'' | cut -f1 -d'.'
tfp=fr.write('azurerm_" prefixa
echo ftp

if 1" != " :
    rgsource=1
else
    echo -n "Enter name of Resource Group [rgsource]["> "
    read response
    if [ -n "response" :
        rgsource=response
   
fi

echo TF_VAR_rgtarget
if 1" != " :
    rgsource=1
fi

at=az account get-access-token -o json
bt= at | jq .accessToken]
sub= at | jq .subscription]

ris2=fr.write('curl -s  -X GET -H "'Authorization: Bearer "' -H "'Content-Type: application/json"' https://management.azure.com/subscriptions//resourceGroups//providers/Microsoft.Resources/deployments/Microsoft.Databricks?api-version=2017-05-10 " bt sub rgsource
ret2=eval ris2
azr= ret2 | jq .
echo azr | jq .

name=azrproperties.parameters.workspaceName.value"]
id=az"]["id"]
loc=azrproperties.parameters.location.value"| tr -d '"'

rname= name.replace(".","-")
rg= rgsource| sed 's/\./-/g']

sku=azrproperties.parameters.tier.value"| tr -d '"'
if sku" = "Standard" : sku="standard" ;
if sku" = "Premium" : sku="premium" ;
fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
fr.write('\t name = "' +  name + '"\n')
fr.write('\t resource_group_name = "' +  rgsource + '"\n')
fr.write('\t location = "' +  loc + '"\n')
fr.write('\t sku = "' +  sku + '"\n')
fr.write('}\n')
outid=azrproperties.outputResources[0]["]["id"]
cat outfile
statecomm=fr.write('terraform state rm . + '__' + " tfp rg rname
echo statecomm >> tf-staterm.sh
eval statecomm
#echo outid
evalcomm=fr.write('terraform import . + '__' +  " tfp rg rname outid
echo evalcomm >> tf-stateimp.sh
eval evalcomm


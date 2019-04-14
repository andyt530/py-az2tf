prefixa=`echo $0 | awk -F 'azurerm_' '{print $2}' | cut -f1 -d'.'`
tfp=`printf "azurerm_%s" $prefixa`
echo $ftp

if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi

echo $TF_VAR_rgtarget
if [ "$1" != "" ]; then
    rgsource=$1
fi

at=`az account get-access-token -o json`
bt=`echo $at | jq .accessToken | tr -d '"'`
sub=`echo $at | jq .subscription | tr -d '"'`

ris2=`printf "curl -s  -X GET -H \"Authorization: Bearer %s\" -H \"Content-Type: application/json\" https://management.azure.com/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Resources/deployments/Microsoft.Databricks?api-version=2017-05-10 " $bt $sub $rgsource`
ret2=`eval $ris2`
azr=`echo $ret2 | jq .`
echo $azr | jq .

name=`echo $azr | jq ".properties.parameters.workspaceName.value" | tr -d '"'`
id=`echo $azr | jq ".id" | tr -d '"'`
loc=`echo $azr | jq ".properties.parameters.location.value"| tr -d '"'`

rname=`echo $name | sed 's/\./-/g'`
rg=`echo $rgsource| sed 's/\./-/g' | tr -d '"'`

sku=`echo $azr | jq ".properties.parameters.tier.value"| tr -d '"'`
if [ "$sku" = "Standard" ]; then sku="standard" ; fi
if [ "$sku" = "Premium" ]; then sku="premium" ; fi
prefix=`printf "%s__%s" $prefixa $rg`
outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
echo $az2tfmess > $outfile
printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
printf "\t name = \"%s\"\n" $name >> $outfile
printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile
printf "\t location = \"%s\"\n" $loc >> $outfile
printf "\t sku = \"%s\"\n" $sku >> $outfile
printf "}\n" >> $outfile
outid=`echo $azr | jq ".properties.outputResources[0].id" | tr -d '"'`
cat $outfile
statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $rname`
echo $statecomm >> tf-staterm.sh
eval $statecomm
#echo $outid
evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $rname $outid`
echo $evalcomm >> tf-stateimp.sh
eval $evalcomm


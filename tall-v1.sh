export az2tfmess="# File auto generate by az2tf v0.2 see https://github.com/andyt530/az2tf"
if [ "$1" != "" ]; then
    mysub=$1
else
    echo -n "Enter id of Subscription [$mysub] > "
    read response
    if [ -n "$response" ]; then
        mysub=$response
    fi
fi

echo "Checking Subscription $mysub exists ..."
isok="no"
subs=`az account list --query '[].id' | jq '.[]' | tr -d '"'`
for i in `echo $subs`
do
    if [ "$i" = "$mysub" ] ; then
        echo "Found subscription $mysub proceeding ..."
        isok="yes"
    fi
done
if [ "$isok" != "yes" ]; then
    echo "Could not find subscription with ID $mysub"
    exit
fi

mkdir -p tf.$mysub
cd tf.$mysub

pfx[1]="null"
res[1]="azurerm_resource_group"
pfx[2]="null"
res[2]="azurerm_availability_set"
pfx[3]="az network route-table list"
res[3]="azurerm_route_table"
pfx[4]="az network nsg list"
res[4]="azurerm_network_security_group"
pfx[5]="az network vnet list"
res[5]="azurerm_virtual_network"
pfx[6]="az network vnet list"
res[6]="azurerm_subnet"
pfx[7]="az network vnet list"
res[7]="azurerm_virtual_network_peering"
pfx[8]="az keyvault list"
res[8]="azurerm_key_vault"
pfx[9]="az disk list"
res[9]="azurerm_managed_disk"
pfx[10]="az storage account list"
res[10]="azurerm_storage_account"
pfx[11]="az network public-ip list"
res[11]="azurerm_public_ip"
pfx[12]="az network nic list"
res[12]="azurerm_network_interface"

pfx[13]="az network lb list"
res[13]="azurerm_lb"   # move to end ?
pfx[14]="az network lb list"
res[14]="azurerm_lb_nat_rule"
pfx[15]="az network lb list"
res[15]="azurerm_lb_nat_pool"
pfx[16]="az network lb list"
res[16]="azurerm_lb_backend_address_pool"
pfx[17]="az network lb list"
res[17]="azurerm_lb_probe"
pfx[18]="az network lb list"
res[18]="azurerm_lb_rule"
pfx[19]="null"
res[19]="azurerm_local_network_gateway"
pfx[20]="null"
res[20]="azurerm_virtual_network_gateway"
pfx[21]="null"
res[21]="azurerm_virtual_network_gateway_connection"
pfx[22]="null"
res[22]="azurerm_express_route_circuit"
pfx[23]="null"
res[23]="azurerm_express_route_circuit_authorization"
pfx[24]="null"
res[24]="azurerm_express_route_circuit_peering"


pfx[25]="az acr list"
res[25]="azurerm_container_registry"
pfx[26]="az aks list"
res[26]="azurerm_kubernetes_cluster"
pfx[27]="az backup vault list"
res[27]="azurerm_recovery_services_vault"

pfx[28]="az vm list"
res[28]="azurerm_virtual_machine"
pfx[29]="az lock list"
res[29]="azurerm_management_lock"
pfx[30]="null"
res[30]="azurerm_automation_account"
pfx[31]="null"
res[31]="azurerm_log_analytics_workspace"
pfx[32]="null"
res[32]="azurerm_log_analytics_solution"

pfx[51]="rdf"
res[51]="azurerm_role_definition"
pfx[52]="ras"
res[52]="azurerm_role_assignment"
pfx[53]="pdf"
res[53]="azurerm_policy_definition"
pfx[54]="pas"
res[54]="azurerm_policy_assignment"


#
# uncomment following line if you want to use an SPN login
#../setup-env.sh

export ARM_SUBSCRIPTION_ID="$mysub"
az account set -s $mysub

if [ "$2" != "" ]; then
    # check provided resource group exists in subscription
    exists=`az group exists -g $2`
    if  ! $exists ; then
        echo "Resource Group $2 does not exists in subscription $mysub  Exit ....."
        exit
    fi
    
fi

# cleanup from any previous runs
rm -f terraform*.backup
rm -f tf*.sh
cp ../stub/*.tf .
echo "terraform init"
terraform init


# subscription level stuff - roles & policies
if [ "$2" = "" ]; then
    for j in `seq 51 54`; do
        
        docomm="../scripts/${res[$j]}.sh $mysub"
        echo $docomm
        eval $docomm
    done
fi

# loop through providers
for j in `seq 1 32`; do
    if [ "$2" != "" ]; then
        myrg=$2
        echo $myrg
        docomm="../scripts/${res[$j]}.sh $myrg"
        echo $docomm
        eval $docomm
    else
        c1=`echo ${pfx[${j}]}`
        #echo $c1
        if [ "$c1" = "null" ] ;then
            trgs=`az group list`
            count=`echo $trgs | jq '. | length'`
            if [ "$count" -gt "0" ]; then
                count=`expr $count - 1`
                for i in `seq 0 $count`; do
                    myrg=`echo $trgs | jq ".[(${i})].name" | tr -d '"'`
                    echo -n $i of $count " "
                    docomm="../scripts/${res[$j]}.sh $myrg"
                    echo $docomm
                    eval $docomm
                    
                done
            fi
        else
            comm=`printf "%s --query '[].resourceGroup' | jq '.[]' | sort -u" "$c1"`
            comm2=`printf "%s --query '[].resourceGroup' | jq '.[]' | sort -u | wc -l" "$c1"`
            tc=`eval $comm2`
            tc=`echo $tc | tr -d ' '`
            trgs=`eval $comm`
            count=`echo ${#trgs}`
            if [ "$count" -gt "0" ]; then
                c5="1"
                for j2 in `echo $trgs`; do
                    echo -n "$c5 of $tc "
                    docomm="../scripts/${res[$j]}.sh $j2"
                    echo $docomm
                    eval $docomm
                    c5=`expr $c5 + 1`
                    echo $c5
                done
            fi
        fi
    fi
    rm -f terraform*.backup
done


#
echo "Cleanup Cloud Shell"
rm -f *cloud-shell-storage*.tf
states=`terraform state list | grep cloud-shell-storage`
echo $states
terraform state rm $states
#
echo "Terraform Plan ..."
terraform plan .
exit

usage()
{ echo "Usage: $0 -s <Subscription ID> [-g <Resource Group>] [-r azurerm_<resource_type>] [-x <yes|no(default)>] [-p <yes|no(default)>] [-f <yes|no(default)>] " 1>&2; exit 1;
}
x="no"
p="no"
f="no"  # f fast forward switch
while getopts ":s:g:r:x:p:f:" o; do
    case "${o}" in
        s)
            s=${OPTARG}
        ;;
        g)
            g=${OPTARG}
        ;;
        r)
            r=${OPTARG}
        ;;
        x)
            x="yes"
        ;;
        p)
            p="yes"
        ;;
        f)
            f="yes"
        ;;
        
        *)
            usage
        ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${s}" ]; then
    usage
fi

if [ "$s" != "" ]; then
    mysub=$s
else
    echo -n "Enter id of Subscription [$mysub] > "
    read response
    if [ -n "$response" ]; then
        mysub=$response
    fi
fi

myrg=$g
export ARM_SUBSCRIPTION_ID="$mysub"
az account set -s $mysub

echo " "
echo "Subscription ID = ${s}"
echo "Azure Resource Group Filter = ${g}"
echo "Terraform Resource Type Filter = ${r}"
echo "Get Subscription Policies & RBAC = ${p}"
echo "Extract Key Vault Secrets to .tf files (insecure) = ${x}"
echo "Fast Forward = ${f}"
echo " "

res[51]="azurerm_role_definition"
res[52]="azurerm_role_assignment"
res[53]="azurerm_policy_definition"
res[54]="azurerm_policy_assignment"

mkdir -p generated/tf.$mysub
cd generated/tf.$mysub
rm -rf .terraform
if [ "$f" = "no" ]; then
    rm -f import.log *.txt
    rm -f terraform* *.tf *.sh
else
    sort -u processed.txt > pt.txt
    cp pt.txt processed.txt
    rm -f *state*.sh import.log
fi

# cleanup from any previous runs
rm -f terraform*.backup
#rm -f terraform.tfstate
rm -f tf*.sh
cp ../../stub/*.tf .



res[1]="azurerm_resource_group"
res[2]="azurerm_management_lock"
res[3]="azurerm_user_assigned_identity"
res[4]="azurerm_availability_set"
res[5]="azurerm_route_table"
res[6]="azurerm_application_security_group"
res[7]="azurerm_network_security_group"
res[8]="azurerm_virtual_network"
res[9]="azurerm_subnet"
res[10]="azurerm_virtual_network_peering"
res[11]="azurerm_managed_disk"
res[12]="azurerm_storage_account"
res[13]="azurerm_key_vault"
res[14]="azurerm_public_ip"
res[15]="azurerm_traffic_manager_profile"
res[16]="azurerm_traffic_manager_endpoint"
res[17]="azurerm_network_interface"
res[18]="azurerm_dns_zone"
res[19]="azurerm_lb"
res[20]="azurerm_lb_nat_rule"
res[21]="azurerm_lb_nat_pool"
res[22]="azurerm_lb_backend_address_pool"
res[23]="azurerm_lb_probe"
res[24]="azurerm_lb_rule"
res[]="azurerm_application_gateway"
res[]="azurerm_local_network_gateway"
res[]="azurerm_virtual_network_gateway"
res[]="azurerm_virtual_network_gateway_connection"
res[]="azurerm_express_route_circuit"
res[]="azurerm_express_route_circuit_authorization"
res[]="azurerm_express_route_circuit_peering"
res[]="azurerm_container_registry"
res[]="azurerm_kubernetes_cluster"
res[]="azurerm_recovery_services_vault" 
res[]="azurerm_virtual_machine"
res[]="azurerm_virtual_machine_scale_set"
res[]="azurerm_automation_account"
res[]="azurerm_log_analytics_workspace"
res[]="azurerm_log_analytics_solution"
res[]="azurerm_image"
res[]="azurerm_snapshot"
res[]="azurerm_network_watcher"
res[]="azurerm_cosmosdb_account"
res[]="azurerm_servicebus_namespace"
res[]="azurerm_servicebus_queue"
res[]="azurerm_sql_server"
res[]="azurerm_sql_database"
res[]="azurerm_databricks_workspace"
res[]="azurerm_app_service_plan"
res[]="azurerm_app_service"
res[]="azurerm_function_app"
res[]="azurerm_monitor_autoscale_setting"


pyc1="python2 ../../scripts/resources.py -s $mysub "
if [ "$g" != "" ]; then
    pyc2=" -g $g "
else
    pyc2=" "
fi
if [ "$r" != "" ]; then
    lcr=`echo $r | awk '{print tolower($0)}'`
    pyc3=" -r $lcr "
else
    pyc3=" "
fi

pyc9=" 2>&1 | tee -a import.log"
pyc=`printf "%s %s %s %s" "$pyc1" "$pyc2" "$pyc3" "$pyc9"`

echo $pyc

eval $pyc
grep Error import.log
if [ $? -eq 0 ]; then
    echo "Error in resources.py"
    exit
fi


#
# uncomment following line if you want to use an SPN login
#../../setup-env.sh


echo "terraform init"
terraform init 2>&1 | tee -a import.log
echo $?



chmod 755 *state*.sh

if [ "$f" = "yes" ]; then
for com in `ls *staterm.sh | sort -g`; do
    comm=`printf "./%s" $com`
    echo $comm
    eval $comm
done
fi


for com in `ls *stateimp.sh | sort -g`; do
    comm=`printf "./%s" $com`
    echo $comm
    eval $comm
done


echo "Terraform fmt ..."
terraform fmt

echo "Terraform Plan ..."
terraform plan .
echo "---------------------------------------------------------------------------"
echo "az2tf output files are in generated/tf.$mysub"
echo "---------------------------------------------------------------------------"


exit


# subscription level stuff - roles & policies
if [ "$p" = "yes" ]; then
    for j in `seq 51 54`; do
        docomm="../../scripts/${res[$j]}.sh $mysub"
        echo $docomm
        eval $docomm 2>&1 | tee -a import.log
        if grep -q Error: import.log ; then
            echo "Error in log file exiting ...."
            exit
        fi
    done
fi

date

if [ "$x" = "yes" ]; then
    echo "Attempting to extract secrets"
    ../../scripts/350_key_vault_secret.sh
fi



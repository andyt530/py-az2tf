tfp="azurerm_resources"
prefixa="tres"

at=`az account get-access-token -o json`
bt=`echo $at | jq .accessToken | tr -d '"'`
sub=`echo $at | jq .subscription | tr -d '"'`
tput clear
rm -f resources.txt noprovider.txt *.json
echo -n "Getting Resources .."

#ris=`printf "curl -s  -X GET -H \"Authorization: Bearer %s\" -H \"Content-Type: application/json\" https://management.azure.com/subscriptions/%s/resources?api-version=2017-05-10" $bt $sub`
ris=`printf "curl -s  -X GET -H \"Authorization: Bearer %s\" -H \"Content-Type: application/json\" https://management.azure.com/subscriptions/%s/resources?api-version=2018-11-01" $bt $sub`
ret=`eval $ris`
rig=`printf "curl -s  -X GET -H \"Authorization: Bearer %s\" -H \"Content-Type: application/json\" https://management.azure.com/subscriptions/%s/resourceGroups?api-version=2014-04-01" $bt $sub`
eval $rig | jq .value > azurerm_resource_group.json
rns=`printf "curl -s  -X GET -H \"Authorization: Bearer %s\" -H \"Content-Type: application/json\" https://management.azure.com/subscriptions/%s/providers/Microsoft.Network/networkSecurityGroups?api-version=2018-07-01" $bt $sub`
eval $rns | jq .value > azurerm_network_security_group.json

azr2=`echo $ret | jq .value`
#echo $rgs2 | jq .
prefix=`printf "%s__resources" $prefixa`
count2=`echo $azr2 | jq '. | length'`
echo " found $count2"
key="id"

echo $azr2 | jq . > data.json
echo "Writing Resources .."
if [ "$count2" -gt "0" ]; then
    count2=`expr $count2 - 1`
    for j in `seq 0 $count2`; do
        tput cup 1 23
        echo -n $j
        #echo $azr2 | jq .
        id=`echo $azr2 | jq ".[(${j})].id"`
        name=`echo $azr2 | jq ".[(${j})].name"`
        loc=`echo $azr2 | jq ".[(${j})].location"`
        rg=`echo $id | cut -f5 -d'/'`
        prov=`echo $id | cut -f7,8 -d'/'`
        isext=`echo $id | cut -f10 -d'/'`
   

        echo $prov | grep mos

        case "$prov" in
            "Microsoft.Compute/availabilitySets") 
                prov="azurerm_availability_set"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Storage/storageAccounts") prov="azurerm_storage_account"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
                prov="azurerm_storage_share"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
                prov="azurerm_storage_container"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Network/networkSecurityGroups") prov="azurerm_network_security_group"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Compute/virtualMachines") 
                #echo $isext
                if [ "$isext" != "extensions" ]; then
                    prov="azurerm_virtual_machine"
                    printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
                fi
            ;;
            "Microsoft.Network/networkInterfaces") prov="azurerm_network_interface"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Compute/disks") prov="azurerm_managed_disk"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Automation/automationAccounts") prov="azurerm_automation_account"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Network/virtualNetworks")
                prov="azurerm_virtual_network"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
                prov="azurerm_subnet"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
                prov="azurerm_virtual_network_peering"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Network/publicIPAddresses")
                prov="azurerm_public_ip"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Network/loadBalancers")
                prov="azurerm_lb"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
                prov="azurerm_lb_nat_rule"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
                prov="azurerm_lb_nat_pool"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
                prov="azurerm_lb_backend_address_pool"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
                prov="azurerm_lb_probe"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
                prov="azurerm_lb_rule"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Network/virtualNetworkGateways") prov="azurerm_virtual_network_gateway"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Network/connections") prov="azurerm_virtual_network_gateway_connection"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Network/routeTables") prov="azurerm_route_table"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.OperationalInsights/workspaces") prov="azurerm_log_analytics_workspace"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.OperationsManagement/solutions") prov="azurerm_log_analytics_solution"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.KeyVault/vaults") prov="azurerm_key_vault"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
                prov="azurerm_key_vault_secret"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt

            ;;
            "Microsoft.RecoveryServices/vaults") prov="azurerm_recovery_services_vault"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.ContainerRegistry/registries") prov="azurerm_container_registry"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.ContainerService/managedClusters") prov="azurerm_kubernetes_cluster"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Network/localNetworkGateways") prov="azurerm_local_network_gateway"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Network/expressRouteCircuits")
                prov="azurerm_express_route_circuit"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
                prov="azurerm_express_route_circuit_authorization"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
                prov="azurerm_express_route_circuit_peering"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Compute/images") prov="azurerm_image"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Network/networkWatchers") prov="azurerm_network_watcher"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Network/applicationSecurityGroups") prov="azurerm_application_security_group"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.ContainerInstance/containerGroups") prov="azurerm_container_group"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Network/applicationGateways") prov="azurerm_application_gateway"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.DocumentDb/databaseAccounts") prov="azurerm_cosmosdb_account"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.ServiceBus/namespaces") prov="azurerm_servicebus_namespace"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
                prov="azurerm_servicebus_queue"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;       
            "Microsoft.Network/trafficmanagerprofiles") prov="azurerm_traffic_manager_profile"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
                prov="azurerm_traffic_manager_endpoint"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Web/serverFarms") prov="azurerm_app_service_plan"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Web/sites") prov="azurerm_app_service"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
                prov="azurerm_function_app"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Compute/virtualMachineScaleSets") prov="azurerm_virtual_machine_scale_set"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.ManagedIdentity/userAssignedIdentities") prov="azurerm_user_assigned_identity"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Compute/snapshots") prov="azurerm_snapshot"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Databricks/workspaces") prov="azurerm_databricks_workspace"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Sql/servers") prov="azurerm_sql_server"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
                prov="azurerm_sql_database"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "Microsoft.Network/dnszones") prov="azurerm_dns_zone"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;
            "microsoft.insights/autoscalesettings" ) prov="azurerm_monitor_autoscale_setting"
                printf "%s:%s-\n"  "$rg" "$prov" >> resources.txt
            ;;

#
            *) printf "%s\n" $prov >> noprovider.txt
            ;;
        esac
    done    
fi

echo $rgsource $1
if [ "$1" != "" ]; then
    rgsource=$1
    echo $rgsource
    #cat resources.txt | awk '{print tolower($0)}' | sort -u | grep $rgsource > resources2.txt
    cat resources.txt | sort -u | grep $rgsource > resources2.txt
else
    echo " "
    #cat resources.txt |  awk '{print tolower($0)}' | sort -u > resources2.txt
    cat resources.txt | sort -u > resources2.txt
fi
echo "No provider for"
cp resources2.txt resources3.txt
cat noprovider.txt | sort -u
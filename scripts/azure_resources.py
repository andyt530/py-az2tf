def azure_resources(crf,cde,crg,headers,requests,sub,json,az2tfmess,os,cldurl):
    # print "REST Resources ",
    fresfilename="data.json"
    fres=open(fresfilename, 'w')
    url="https://" + cldurl + "/subscriptions/" + sub + "/resources"
    params = {'api-version': '2018-11-01'}
    try: 
        r = requests.get(url, headers=headers, params=params)
        res= r.json()["value"]
    except KeyError:
        print ("Error getting resources")
        exit()
    fres.write(json.dumps(res, indent=4, separators=(',', ': ')))
    fres.close()


    rfilename="resources2.txt"
    fr=open(rfilename, 'w')
    nprfilename="noprovider2.txt"
    np=open(nprfilename, 'w')


    count=len(res)
    print ("Resources Found: " + str(count))
    for j in range(0, count):
        
        #name=res[j]['name']
        id=res[j]['id']
        rg1=id.split("/")[4]
        try:
            isext=id.split("/")[9]
        except IndexError:
            isext=""

        rtype=res[j]['type']
        rg=rg1.replace(".","-")
        #print rtype

        if rtype == "Microsoft.Compute/availabilitySets":
            prov="azurerm_availability_set"
            fr.write(rg + ":" + prov + "\n")
        elif rtype == "Microsoft.Network/networkSecurityGroups":
            prov="azurerm_network_security_group"
            fr.write(rg + ":" + prov + "\n")

        elif rtype == "Microsoft.Storage/storageAccounts": 
            prov="azurerm_storage_account"
            fr.write(rg + ":" + prov + "\n")
            prov="azurerm_storage_share"
            fr.write(rg + ":" + prov + "\n")
            prov="azurerm_storage_container"
            fr.write(rg + ":" + prov + "\n")

        elif rtype == "Microsoft.Network/networkSecurityGroups":
            prov="azurerm_network_security_group"
            fr.write(rg + ":" + prov + "\n")

        elif rtype == "Microsoft.Compute/virtualMachines": 
            #echo $isext
            if isext != "extensions":
                prov="azurerm_virtual_machine"
                fr.write(rg + ":" + prov + "\n")
                    
        elif rtype == "Microsoft.Network/networkInterfaces": 
            prov="azurerm_network_interface"
            fr.write(rg + ":" + prov + "\n")
        
        elif rtype == "Microsoft.Compute/disks":
            prov="azurerm_managed_disk"
            fr.write(rg + ":" + prov + "\n")
            
        elif rtype == "Microsoft.Automation/automationAccounts": 
            prov="azurerm_automation_account"
            fr.write(rg + ":" + prov + "\n")
            
        elif rtype == "Microsoft.Network/virtualNetworks":
            prov="azurerm_virtual_network"
            fr.write(rg + ":" + prov + "\n")
            prov="azurerm_subnet"
            fr.write(rg + ":" + prov + "\n")
            prov="azurerm_virtual_network_peering"
            fr.write(rg + ":" + prov + "\n")

        elif rtype == "Microsoft.Network/publicIPAddresses":
            prov="azurerm_public_ip"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.Network/loadBalancers":
            prov="azurerm_lb"
            fr.write(rg + ":" + prov + "\n")
            prov="azurerm_lb_nat_rule"
            fr.write(rg + ":" + prov + "\n")
            prov="azurerm_lb_nat_pool"
            fr.write(rg + ":" + prov + "\n")
            prov="azurerm_lb_backend_address_pool"
            fr.write(rg + ":" + prov + "\n")
            prov="azurerm_lb_probe"
            fr.write(rg + ":" + prov + "\n")
            prov="azurerm_lb_rule"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.Network/virtualNetworkGateways":
            prov="azurerm_virtual_network_gateway"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.Network/connections":
            prov="azurerm_virtual_network_gateway_connection"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.Network/routeTables": 
            prov="azurerm_route_table"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.OperationalInsights/workspaces":
            prov="azurerm_log_analytics_workspace"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype ==  "Microsoft.OperationsManagement/solutions":
            prov="azurerm_log_analytics_solution"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.KeyVault/vaults":
            prov="azurerm_key_vault"
            fr.write(rg + ":" + prov + "\n")
            prov="azurerm_key_vault_secret"
            fr.write(rg + ":" + prov + "\n")

        elif rtype == "Microsoft.RecoveryServices/vaults":
            prov="azurerm_recovery_services_vault"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.ContainerRegistry/registries":
            prov="azurerm_container_registry"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.ContainerService/managedClusters":
            prov="azurerm_kubernetes_cluster"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.Network/localNetworkGateways":
            prov="azurerm_local_network_gateway"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.Network/expressRouteCircuits":
            prov="azurerm_express_route_circuit"
            fr.write(rg + ":" + prov + "\n")
            prov="azurerm_express_route_circuit_authorization"
            fr.write(rg + ":" + prov + "\n")
            prov="azurerm_express_route_circuit_peering"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.Compute/images": 
            prov="azurerm_image"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.Network/networkWatchers": 
            prov="azurerm_network_watcher"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.Network/applicationSecurityGroups":
            prov="azurerm_application_security_group"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.ContainerInstance/containerGroups":
            prov="azurerm_container_group"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.Network/applicationGateways": 
            prov="azurerm_application_gateway"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.DocumentDb/databaseAccounts":
            prov="azurerm_cosmosdb_account"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.ServiceBus/namespaces": 
            prov="azurerm_servicebus_namespace"
            fr.write(rg + ":" + prov + "\n")
            prov="azurerm_servicebus_queue"
            fr.write(rg + ":" + prov + "\n")
                    
        elif rtype == "Microsoft.Network/trafficmanagerprofiles":
            prov="azurerm_traffic_manager_profile"
            fr.write(rg + ":" + prov + "\n")
            prov="azurerm_traffic_manager_endpoint"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.Web/serverFarms": 
            prov="azurerm_app_service_plan"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.Web/sites": 
            prov="azurerm_app_service"
            fr.write(rg + ":" + prov + "\n")
            prov="azurerm_function_app"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.Compute/virtualMachineScaleSets":
            prov="azurerm_virtual_machine_scale_set"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.ManagedIdentity/userAssignedIdentities":
            prov="azurerm_user_assigned_identity"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.Compute/snapshots":
            prov="azurerm_snapshot"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.Databricks/workspaces":
            prov="azurerm_databricks_workspace"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.Sql/servers": 
            prov="azurerm_sql_server"
            fr.write(rg + ":" + prov + "\n")
            prov="azurerm_sql_database"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype == "Microsoft.Network/dnszones": 
            prov="azurerm_dns_zone"
            fr.write(rg + ":" + prov + "\n")
                
        elif rtype ==  "microsoft.insights/autoscalesettings":
            prov="azurerm_monitor_autoscale_setting"
            fr.write(rg + ":" + prov + "\n")
                
        else:
            np.write(rtype + "\n")

    fr.close()
    np.close()

    print ("Optimizing Resources ...")
    # sort unique and filter for Resource Group
    rfilename="resources.txt"
    fr=open(rfilename, 'w')
    with open('resources2.txt', 'r') as r:
        for line in sorted(set(r)):
            trg=line.split(":")[0]
            trt=line.split(":")[1]
            #print trt
            if crg is not None:   # Resource Group Filter
                if trg == crg :
                    if crf is not None:   # Resource Filter
                        if crf in trt:
                            fr.write(line,)
                    else:
                        fr.write(line,)
            else:
                if crf is not None:   # Resource Filter
                    if crf in trt :
                        fr.write(line,)
                else:
                    fr.write(line,)
    r.close()
    fr.close()





    # sort unique and fileter for Resource Group
    rfilename="noprovider.txt"
    fr=open(rfilename, 'w')
    with open('noprovider2.txt', 'r') as r:
        for line in sorted(set(r)):
            fr.write(line,)

    r.close()
    fr.close()
    if os.path.exists("tf-staterm.sh"):
        os.remove('tf-staterm.sh')
    if os.path.exists("tf-stateimp.sh"):
        os.remove('tf-stateimp.sh')
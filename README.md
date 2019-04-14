# az2tf

This utility 'Azure to Terraform' (az2tf) 
reads an Azure Subscription and generates all the required terraform configuration files (.tf) from each of the composite Azure Resource Groups
It also imports the terraform state using a

"terraform import ...." command

And finally runs a 

"terraform plan ."  command 

There should hopefully be no subsequent additions or deletions reported by the terraform plan command as all the approriate terraform configuration files will have have automatically been created.

## Requirements & Prerequisites
+ The tool is written for the bash shell script and has been tested on a MAC
+ Azure cli2 **version 2.0.55 or higher** needs to be installed and you need a login with at least "Read" priviledges
+ terraform **version v0.11.11** needs to be installed
+ jq see:  https://stedolan.github.io/jq/  (On macOS also available via $ brew install jq)



## Quickstart guide to using the tool

Running the tool in your local shell (bash) required these steps:
1. Unzip or clone this git repo into an empty directory
2. login to the Azure cli2  (az login)
3. run the tool 


## Experimental: using the docker version
1. Build with: $ docker build --rm -f "Dockerfile" -t az2tf:latest .
2. If it doesn't already exist make a "generated" directory ($ mkdir generated)
3. Run with "$ ./runme.sh"

(would appreciate feedback on how to better use docker)

## Usage Guide

To generate the terraform files for an entire Azure subscription:
```
./az2tf.sh -s <Subscription ID>
```

To include Azure Subscription Policies and RBAC controls and assignments:
```
./az2tf.sh -s <Subscription ID> -p yes
```

To generate the terraform files for a specific Resource Group in a subscription:
```
./az2tf.sh -s <Subscription ID> -g <Resource Group>
```

To include the secrets from a Key Vault in terraform files (secrets will be in plain text):
```
./az2tf.sh -s <Subscription ID> -g <Resource Group> -x yes
```

To filter the terraform resource type: (eg: just availability sets)
```
./az2tf.sh -s <Subscription ID> -g <Resource Group> -r azurerm_availability_set
```


Be patient - lots of output is given as az2tf:

+ Loops for each provider through your resource groups &
+ Creates the requited *.tf configuration files in the "generated" directory
+ Performs the necessary 'terraform import' commands
+ And finally runs a 'terraform plan'



## Supported Resource Types

The following terraform resource types are supported by this tool at this time:

Base Resources
* azurerm_resource_group (full)

Authorization Resources
* azurerm_role_definition (subscription level)
* azurerm_role_assignment (subscription level)

Active Directory Resources

App Service (Web Apps) Resources
* azurerm_app_service
* azurerm_app_service_plan

Automation Resources
* azurerm_automation_account

Compute Resources
* azurerm_availability_set (full)
* azurerm_image
* azurerm_managed_disk  (Common)
* azurerm_virtual_machine  (Common)
* azurerm_virtual_machine_scale_sets  (Common)

Container Resources
* azurerm_container_registry (full)
* azurerm_kubernetes_cluster

CosmosDB (DocumentDB) Resources
* azurerm_cosmosdb_account (Common)

Databricks Resources
* azurerm_databricks_resources

Key Vault Resources
* azurerm_key_vault (Common)
* azurerm_key_vault_secret (full)

Load Balancer Resources
* azurerm_lb  (full)
* azurerm_lb_backend_address_pool (full)
* azurerm_lb_rule (full)
* azure_nat_rule (full - needs more testing)
* azurerm_lb_probe (full)
* azure_nat_pool (full - needs more testing)

Management Resources
* azurerm_management_lock  (full)

Messaging Resources
* azurerm_servicebus_namespace  (full)
* azurerm_servicebus_queue  (partial)

Monitoring Resources
* azurerm_autoscale_setting

Network Resources
* azurerm_application_gateway 
* azurerm_application_security_group (full)
* azurerm_express_route_circuit (full)
* azurerm_express_route_circuit_authorization (full)
* azurerm_express_route_circuit_peering (partial)
* azurerm_local_network_gateway
* azurerm_network_interface  (Common)
* azurerm_network_security_group (full)
* azurerm_network_watcher
* azurerm_public_ip  (Common)
* azurerm_route_table (full)
* azurerm_subnet (full)
* azurerm_subnet_network_security_group_association (full)
* azurerm_subnet_route_table_group_association (full)
* azurerm_traffic_manager_endpoint (partial)
* azurerm_traffic_manager_profile (partial)
* azurerm_virtual_network (full)
* azurerm_virtual_network_gateway
* azurerm_virtual_network_gateway_connection
* azurerm_virtual_network_peering (full)
  
Policy Resources
* azurerm_policy_definition (custom poicies only)
* azurerm_policy_assignment

OMS Resources
* azurerm_log_analytics_solution (partial)
* azurerm_log_analytics_workspace (full)

Recovery Services
* azurerm_recovery_services_vault (full)

Storage Resources
* azurerm_storage_account (Common - tf full support lacking)


(Full) = full support for all terraform attributes
(Common) = support for the most Common terraform attributes
(Partial) = support for some of the terraform attributes


## Planned Additions

+ PaaS databases and apps
+ Storage firewall rules
+ ongoing better AKS support as AKS evolves
+ Other terraform providers where terraform & Azure cli2 mutually support

## Known problems

### Speed

It is quite slow to loop around everything in large subscriptions, there are ways to speed this tool up (make fewer az cli command calls) but it would also make it harder to debug, I may look at doing this after I finish building out support for more providers.

### KeyVault:

Can fail if your login/SPN doesn't have acccess to the KeyVault

### Virtual machines:
These attributes always get reported in terraform plan set to false by default  - may need to manually override

+ delete_data_disks_on_termination:           "" => "false"
+ delete_os_disk_on_termination:              "" => "false"


### Storage Account

awaiting terraform support for VNet service endpoints/firewalling
Can fail if your login/SPN doesn't have acccess the KeyVault used for encryption
Can also fail of resource locks are in place

### OMS

If solutions have '[' & ']' in their names they wil be ignored.


### ExpressRoute

No support for MS peering (don't have one to test!)

### Key Vault

terraform doesn't support the "All" permission

### Virtual Network Gateway

if no bgp settings specified for VNet Gateway, `terraform plan` will report 
a benign change
 [see issue in github](https://github.com/terraform-providers/terraform-provider-azurerm/issues/1993)

	~ update in-place
	Terraform will perform the following actions:

	~ azurerm_virtual_network_gateway.rg-$RGNAME__vgw-$VGWNAME
		bgp_settings.#: "" => <computed>

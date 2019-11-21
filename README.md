# az2tf (Python3 version) - now supports Terraform v0.12 

Work in progress - please report any issues you find.

This utility 'Azure to Terraform' (az2tf) 
reads an Azure Subscription and generates all the required terraform configuration files (.tf) from each of the composite Azure Resource Groups
It also imports the terraform state using a

"terraform import ...." command

And finally runs a 

"terraform plan ."  command 

There should hopefully be no subsequent additions or deletions reported by the terraform plan command as all the approriate terraform configuration files will have have automatically been created.

## Requirements & Prerequisites
+ The tool is written for the bash shell script & Python2 and has been tested on macOS
+ Azure cli2 **version 2.0.65 or higher** needs to be installed and you need a login with at least "Read" priviledges
+ terraform **version v0.12.8 or higher** needs to be installed
+ Python **version 3.6.1 or higher**

### May also be required
+ pip install requests
+ pip install adal


## Quickstart guide to using the tool

Running the tool in your local shell (bash) required these steps:
1. Unzip or clone this git repo into an empty directory
2. login to the Azure cli2  (az login)
3. run the tool 


## Usage Guide

### The First Run
To generate the terraform files for a subscription and stop after a "terraform validate":
```
./az2tf.sh -s <Subscription ID> -v yes
```

The above will either show :
```
terraform validate
Success! The configuration is valid.
```

Or there may be some kind of python error. (as trying to test everyone's Azure combinations in advance isn't possible)

**If you happen to find one of these errors please open an issue here and paste in the error and it will get fixed.**

Once the validation is ok you can use the tool in anger to not only generate the terraform files (-v yes) but also import the resources and perform a terraform plan (see below)

---

<br>

To generate the terraform files for an entire Azure subscription, import the resourcs and perform a terraform plan:
```
./az2tf.sh -s <Subscription ID>
```

If your resources are in Azure US Government:
```
./az2tf.sh -c AzureUSGovernment -s <Subscription ID>
```

To include Azure Subscription Policies and RBAC controls and assignments:
```
./az2tf.sh [-c <Cloud Name>] -s <Subscription ID> -p yes
```

To generate the terraform files for a specific Resource Group in a subscription:
```
./az2tf.sh [-c <Cloud Name>] -s <Subscription ID> -g <Resource Group>
```

To include the secrets from a Key Vault in terraform files (secrets will be in plain text):
```
./az2tf.sh [-c <Cloud Name>] -s <Subscription ID> -g <Resource Group> -x yes
```

To filter the terraform resource type: (eg: just availability sets)
```
./az2tf.sh [-c <Cloud Name>] -s <Subscription ID> -g <Resource Group> -r azurerm_availability_set
```
To filter the terraform resource type: (eg: just availability sets) and fast forward - ie. build up resources one after another.:
```
./az2tf.sh -s <Subscription ID> -g <Resource Group> -r azurerm_rsource_group
./az2tf.sh -s <Subscription ID> -g <Resource Group> -r azurerm_availability_set -f yes
./az2tf.sh -s <Subscription ID> -g <Resource Group> -r azurerm_public_ip -f yes
```

To use the fast forward option correctly you'll need a good understanding of terraform resource dependancies to ensure you avoid any depenacy errors.

<br>

Be patient - lots of output is given as az2tf:

+ Loops for each provider through your resource groups &
+ Creates the requited *.tf configuration files in the "generated" directory
+ Performs the necessary 'terraform import' commands
+ And finally runs a 'terraform plan'



## Supported Resource Types

The following terraform resource types are supported by this tool at this time:

Base Resources
* azurerm_resource_group 

Authorization Resources
* azurerm_role_definition (subscription level)
* azurerm_role_assignment (subscription level)
* azurerm_user_assigned_identity

Active Directory Resources

App Service (Web Apps) Resources
* azurerm_app_service
* azurerm_app_service_plan
* azurerm_function_app

Automation Resources
* azurerm_automation_account

Compute Resources
* azurerm_availability_set
* azurerm_image
* azurerm_managed_disk 
* azurerm_shared_image_gallery
* azurerm_shared_image
* azurerm_shared_image_version
* azurerm_snapshot 
* azurerm_virtual_machine 
* azurerm_virtual_machine_extension 
* azurerm_virtual_machine_scale_set

Container Resources
* azurerm_container_registry 
* azurerm_kubernetes_cluster

CosmosDB (DocumentDB) Resources
* azurerm_cosmosdb_account 

Database Resources
* azurerm_sql_database
* azurerm_sql_server

Databricks Resources
* azurerm_databricks_resources (not available for China Azure today)

Key Vault Resources
* azurerm_key_vault 
* azurerm_key_vault_secret

Load Balancer Resources
* azurerm_lb  
* azurerm_lb_backend_address_pool 
* azurerm_lb_rule 
* azure_nat_rule 
* azurerm_lb_probe
* azure_nat_pool 

Logic App Resources
* azurerm_logic_app_workflow

Management Resources
* azurerm_management_lock 

Messaging Resources
* azurerm_eventhub
* azurerm_eventhub_namespace
* zurerm_eventhub_namespace_authorization_rule

* azurerm_servicebus_namespace 
* azurerm_servicebus_queue 

Monitoring Resources
* azurerm_autoscale_setting  (not available for China Azure today)

Network Resources
* azurerm_application_gateway 
* azurerm_application_security_group 
* azurerm_express_route_circuit 
* azurerm_express_route_circuit_authorization 
* azurerm_express_route_circuit_peering 
* azurerm_local_network_gateway
* azurerm_network_interface  
* azurerm_network_security_group 
* azurerm_network_watcher
* azurerm_public_ip  
* azurerm_route_table 
* azurerm_subnet 
* azurerm_subnet_network_security_group_association 
* azurerm_subnet_route_table_group_association 
* azurerm_traffic_manager_endpoint 
* azurerm_traffic_manager_profile 
* azurerm_virtual_network 
* azurerm_virtual_network_gateway
* azurerm_virtual_network_gateway_connection
* azurerm_virtual_network_peering 
  
Policy Resources
* azurerm_policy_definition (custom poicies only)
* azurerm_policy_set_definition (custom poicies only)
* azurerm_policy_assignment

OMS Resources
* azurerm_log_analytics_solution 
* azurerm_log_analytics_workspace 

Recovery Services
* azurerm_recovery_services_vault 

Storage Resources
* azurerm_storage_account 

## Other Azure Clouds

Global AzureCloud is used by default. To set a specific regional cloud, use `-c <Cloud Name>`

The following are acceptable values:
* AzureCloud
* AzureChinaCloud
* AzureGermanCloud
* AzureUSGovernment

## Planned Additions

+ PaaS databases and other missing providers (feel free to contribute !)
+ ongoing better AKS support as AKS evolves
+ Other terraform providers as terraform supports

## Using the Azure runbook code

Within the runbook directory you'll file a file az2tf-runbook.py

You can paste this code into an Azure python2 runbook, your automation account must have an Azure ARM Runas credential setup.

When runs it will leave you subscriptions terraform and terraform import caommands in the runbook output window

*Unfortunately this only works for small subscriptions as Azure currently has a limit on how much output it will show in a runbook output window. If your output window is blank az2tf has probably worked (see the All Logs tab) but the amount of output has exceeded Azure's limit.*

*To workaround this you can download the output aftert he job has run with powershell see*
https://docs.microsoft.com/azure/automation/automation-runbook-output-and-messages#runbook-output.



If you find any output in the Exceptions tab please open an issue here and report it.


## Known problems

### Speed

It can take a lot of time to loop around everything in large subscriptions, in particular the importing of the resources.

### KeyVault:

Can fail if your login/SPN doesn't have acccess to the KeyVault

### Virtual machines:
These attributes always get reported in terraform plan set to false by default - may need to manually override

+ delete_data_disks_on_termination:           "" => "false"
+ delete_os_disk_on_termination:              "" => "false"


### Storage Account

Can fail if your login/SPN doesn't have acccess to the KeyVault used for encryption.
Can also fail if resource locks are in place

### OMS

If solutions have '[' & ']' in their names they will be ignored.


### ExpressRoute

No support for MS peering (don't have one to test!)

### Key Vault

terraform doesn't support the "All" permission anymore but you may still have vaults using that permission.

### Virtual Network Gateway

if no bgp settings specified for VNet Gateway, `terraform plan` will report 
a benign change
 [see issue in github](https://github.com/terraform-providers/terraform-provider-azurerm/issues/1993)

	~ update in-place
	Terraform will perform the following actions:

	~ azurerm_virtual_network_gateway.rg-$RGNAME__vgw-$VGWNAME
		bgp_settings.#: "" => <computed>

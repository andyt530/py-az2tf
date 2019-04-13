#from azure.common.client_factory import get_client_from_cli_profile
#from azure.mgmt.compute import ComputeManagementClient
#from azure.mgmt.resource import ResourceManagementClient
import subprocess
import requests
import adal
import os
import json
import sys

import argparse

parser = argparse.ArgumentParser(description='terraform sub rg')
parser.add_argument('-s', help='Subscription Id')
parser.add_argument('-r', help='Resource Group')
args = parser.parse_args()
csub=args.s
crg=args.r

if csub is not None:
    print("sub=" + csub) 
    # validate sub
if crg is not None:
    print("resource group=" + crg)
    # validate rg


if sys.version_info[0] > 2:
    #raise Exception("Must be using Python 2")
    print("Python version ", sys.version_info[0])
else:
    print("Python version ", sys.version_info[0])

def printf(format, *values):
    print(format % values )




#with open(filename, 'w') as f:
    #print >> f, 'Filename:'


#tenant = os.environ['TENANT']
#authority_url = 'https://login.microsoftonline.com/' + tenant
#client_id = os.environ['CLIENTID']
#client_secret = os.environ['CLIENTSECRET']
#resource = 'https://management.azure.com/'
#context = adal.AuthenticationContext(authority_url)
#token = context.acquire_token_with_client_credentials(resource, client_id, client_secret)
#headers = {'Authorization': 'Bearer ' + token['accessToken'], 'Content-Type': 'application/json'}
#params = {'api-version': '2016-06-01'}
#url = 'https://management.azure.com/' + 'subscriptions'
#r = requests.get(url, headers=headers, params=params)
#print(json.dumps(r.json(), indent=4, separators=(',', ': ')))

p = subprocess.Popen('az account get-access-token -o json', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
c=0
for line in p.stdout.readlines():
    if "accessToken" in line:
        tk=line.split(":")[1].strip(' ",')
        tk2=tk.replace(",", "")
        bt2=tk2.replace('"', '')
    if "subscription" in line:
        tk=line.split(":")[1].strip(' ",')
        tk2=tk.replace(",", "")
        sub2=tk2.replace('"', '')
retval = p.wait()
if csub is not None:
    sub=csub
else:
    sub=sub2.rstrip('\n')

bt=bt2.rstrip('\n')
print "Subscription:",sub
headers = {'Authorization': 'Bearer ' + bt, 'Content-Type': 'application/json'}


fresfilename="data.json"
fres=open(fresfilename, 'w')
url="https://management.azure.com/subscriptions/" + sub + "/resources"
params = {'api-version': '2018-11-01'}
r = requests.get(url, headers=headers, params=params)
res= r.json()["value"]
fres.write(json.dumps(res, indent=4, separators=(',', ': ')))
fres.close()



frgfilename="azurerm_resource_group.json"
frg=open(frgfilename, 'w')
url="https://management.azure.com/subscriptions/" + sub + "/resourceGroups"

params = {'api-version': '2014-04-01'}
r = requests.get(url, headers=headers, params=params)
rgs= r.json()["value"]
frg.write(json.dumps(rgs, indent=4, separators=(',', ': ')))
frg.close()


fnsgfilename="azurerm_network_security_group.json"
fnsg=open(fnsgfilename, 'w')
url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Network/networkSecurityGroups"
params = {'api-version': '2018-07-01'}
r = requests.get(url, headers=headers, params=params)
nsg= r.json()["value"]
#print (json.dumps(nsg, indent=4, separators=(',', ': ')))
fnsg.write(json.dumps(nsg, indent=4, separators=(',', ': ')))
fnsg.close()

rfilename="resources2.txt"
fr=open(rfilename, 'w')
nprfilename="noprovider2.txt"
np=open(nprfilename, 'w')


count=len(res)-1
print count
for j in range(0, count):
    t1=res[j]
    name=res[j]['name']
    id=res[j]['id']
    rg=id.split("/")[4]
    try:
        isext=id.split("/")[9]
    except IndexError:
        isext=""

    loc=res[j]['location']
    rtype=res[j]['type']
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

# sort unique and fileter for Resource Group
rfilename="resources.txt"
fr=open(rfilename, 'w')
with open('resources2.txt', 'r') as r:
    for line in sorted(set(r)):
        trg=line.split(":")[0]
        if crg is not None:   # Resource Group Filter
            if trg == crg :
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


tfrm=open("tf-staterm.sh", 'a')
tfim=open("tf-stateimp.sh", 'a')

# handle resource groups
tfp="azurerm_resource_group"
count=len(rgs)-1
print count
for j in range(0, count):
    name=rgs[j]["name"]
    rname=name.replace(".","-")
    prefix=tfp+"__"+rname
    
    rfilename=prefix+".tf"
    fr=open(rfilename, 'w')
    fr.write("")
    fr.write('resource ' + tfp + ' ' + rname + ' {\n')
    fr.write('\t name = "' + name + '"\n')
    fr.write('\t location = "'+ loc + '"\n')
    fr.write('}\n')  

# tags block
    try:
        mtags=rgs[j]["tags"]
    except:
        mtags="{}"
    tcount=len(mtags)-1
    if tcount > 1 :
        fr.write('tags { \n')
        print tcount
        for key in mtags.keys():
            tval=mtags[key]
            fr.write('\t "' + key + '"="' + tval + '"\n')
        #print(json.dumps(rgs[j], indent=4, separators=(',', ': ')))
        print(json.dumps(mtags, indent=4, separators=(',', ': ')))
        fr.write('} \n')
    fr.close()
    tfrm.write('terraform state rm '+tfp+'.'+rname + '\n')
    tfim.write('terraform state import '+tfp+'.'+rname+' '+id+ '\n')

tfrm.close()
tfim.close()
exit()

rclient = get_client_from_cli_profile(ResourceManagementClient)

for resource_group in rclient.resource_groups.list():
    print(resource_group.name)

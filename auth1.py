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
    print "sub=" + csub 
    # validate sub
if crg is not None:
    print "resource group=" + crg
    # validate rg


if sys.version_info[0] > 2:
    #raise Exception("Must be using Python 2")
    print "Python version ", sys.version_info[0]
else:
    print "Python version ", sys.version_info[0]

def printf(format, *values):
    print(format % values )
frgfilename="azurerm_resource_group.json"
frg=open(frgfilename, 'w')
fresfilename="data.json"
fres=open(fresfilename, 'w')
fnsgfilename="azurerm_network_security_group.json"
fnsg=open(fnsgfilename, 'w')

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

url="https://management.azure.com/subscriptions/" + sub + "/resourceGroups"
headers = {'Authorization': 'Bearer ' + bt, 'Content-Type': 'application/json'}
params = {'api-version': '2014-04-01'}

r = requests.get(url, headers=headers, params=params)
rgs= r.json()["value"]
frg.write(json.dumps(rgs, indent=4, separators=(',', ': ')))
frg.close()

url="https://management.azure.com/subscriptions/" + sub + "/resources"
params = {'api-version': '2018-11-01'}
r = requests.get(url, headers=headers, params=params)
res= r.json()["value"]
fres.write(json.dumps(res, indent=4, separators=(',', ': ')))
fres.close()


url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Network/networkSecurityGroups"
params = {'api-version': '2018-07-01'}
r = requests.get(url, headers=headers, params=params)
nsg= r.json()["value"]
#print (json.dumps(nsg, indent=4, separators=(',', ': ')))
fnsg.write(json.dumps(nsg, indent=4, separators=(',', ': ')))
fnsg.close()


rfilename="resources.txt"
fr=open(rfilename, 'w')

count=len(res)-1
print count
for j in range(0, count):
    t1=res[j]
    name=res[j]['name']
    id=res[j]['id']
    rg=id.split("/")[4]
    loc=res[j]['location']
    rtype=res[j]['type']



    #print j, rtype
    #print (json.dumps(t1, indent=4, separators=(',', ': ')))
    if rtype == "Microsoft.Compute/availabilitySets":
        prov="azurerm_availability_set"
        fr.write(rg + ":" + prov + "\n")
    elif rtype == "Microsoft.Network/networkSecurityGroups":
        prov="azurerm_network_security_group"
        fr.write(rg + ":" + prov + "\n")
    #elif:
    #elif:
    #else:
    
#sorted(set(input))
fr.close()
rfilename="resources2.txt"
fr=open(rfilename, 'w')
with open('resources.txt', 'r') as r:
    for line in sorted(set(r)):
        trg=line.split(":")[0]
        print trg
        if crg is not None:
            if trg == crg :
                fr.write(line,)
        else:
            fr.write(line,)
r.close()
fr.close()

exit()

rclient = get_client_from_cli_profile(ResourceManagementClient)

for resource_group in rclient.resource_groups.list():
    print(resource_group.name)

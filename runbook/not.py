#!/usr/bin/python2
# RUNBOOK OFF
scwd=os.getcwd()
#print scwd
head, tail = os.path.split(scwd)
os.chdir(head)
cwd=os.getcwd()
head, tail = os.path.split(cwd)
newd=head+"/scripts"
os.chdir(newd)
#print os.getcwd()
# RUNBOOK OFF
os.chdir(scwd)
#print os.getcwd()

parser = argparse.ArgumentParser(description='terraform sub rg')
parser.add_argument('-s', help='Subscription Id')
parser.add_argument('-g', help='Resource Group')
parser.add_argument('-r', help='Filter azurerm resource')
parser.add_argument('-d', help='Debug')
args = parser.parse_args()
csub=args.s
crg=args.g
crf=args.r
deb=args.d

# RUNBOOK OFF
if csub is not None:
print("sub=" + csub)
# validate sub
if crg is not None:
print("resource group=" + crg)
# validate rg
if crf is not None:
print("resource filter=" + crf)
# validate resource
if deb is not None:
cde=True

if sys.version_info[0] > 2:
#raise Exception("Must be using Python 2")
print("Python version ", sys.version_info[0], " version 2 required, Exiting")
exit()

def printf(format, *values):
print(format % values )

# cleanup files with Python
#tffile=tfp+"*.tf"
#fileList = glob.glob(tffile)
# Iterate over the list of filepaths & remove each file.
#for filePath in fileList:
# try:
# os.remove(filePath)
# except:
# print("Error while deleting file : ", filePath)


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

print "Get Access Token from CLI"
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
sub=sub2.rstrip('n')



bt=bt2.rstrip('n')
print "Subscription:",sub
headers = {'Authorization': 'Bearer ' + bt, 'Content-Type': 'application/json'}


# subscription check
#https://management.azure.com/subscriptions?api-version=2014-04-01
# print "REST Subscriptions ",
url="https://management.azure.com/subscriptions"
params = {'api-version': '2014-04-01'}
try:
r = requests.get(url, headers=headers, params=params)
subs= r.json()["value"]
except KeyError:
print "Error getting subscription list"
exit("ErrorGettingSubscriptionList")
#print(json.dumps(subs, indent=4, separators=(',', ': ')))
#ssubs=json.dumps(subs)
#print ssubs
#if sub not in ssubs:
# print "Could not find subscription with ID " + sub + " Exiting ..."
# exit("ErrorInvalidSubscriptionID-1")


#print(json.dumps(subs, indent=4, separators=(',', ': ')))

FoundSub=False
count=len(subs)

for i in range(0, count):
id=str(subs[i]["subscriptionId"])
#print id + " " + sub
if id == sub:
FoundSub=True

if not FoundSub:
print "Could not find subscription with ID (Test 2) " + sub + " Exiting ..."
#exit("ErrorInvalidSubscriptionID-2")

# RUNBOOK OFF
if crg is not None:
FoundRg=False
# get and check Resource group
url="https://management.azure.com/subscriptions/" + sub + "/resourceGroups"
params = {'api-version': '2014-04-01'}
r = requests.get(url, headers=headers, params=params)
rgs= r.json()["value"]

count=len(rgs)
for j in range(0, count):
name=rgs[j]["name"]
if crg.lower() == name.lower():
print "Found Resource Group" + crg
FoundRg=True

if not FoundRg:
print "Could not find Resource Group " + crg + " in subscription " + sub + " Exiting ..."
exit("ErrorInvalidResourceGroup")


if os.path.exists("tf-staterm.sh"):
os.remove('tf-staterm.sh')
if os.path.exists("tf-stateimp.sh"):
os.remove('tf-stateimp.sh')


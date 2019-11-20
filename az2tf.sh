usage()
{ echo "Usage: $0 [-c <Cloud>] -s <Subscription ID> [-g <Resource Group>] [-r azurerm_<resource_type>] [-x <yes|no(default)>] [-p <yes|no(default)>] [-f <yes|no(default)>] [-v <yes|no(default)>] [-d <yes|no(default)>]" 1>&2; exit 1;
}
x="no"
p="no"
f="no"  # f fast forward switch
p="no"
d="no"
v="no"
while getopts ":c:s:g:r:x:p:f:d:v:" o; do
    case "${o}" in
        c)
            c=${OPTARG}
        ;;
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
        d)
            d="yes"
        ;;   
        v)
            v="yes"
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

## Uncomment below and remove second "AzureCloud" in line 57 to require -c parameter. With below, defaults to AzureCloud if not specified.
if [[ "$c" == "AzureCloud" || "$c" == "AzureChinaCloud" || "$c" == "AzureGermanCloud" || "$c" == "AzureUSGovernment"  ]]; then
    mycld=$c
else
    # echo -n "Enter id of Cloud (AzureCloud, AzureChinaCloud, AzureGermanCloud, AzureUSGovernment) [$mycld] > "
    # read response
    # if [ -n "$response" ]; then
        mycld="AzureCloud" #$response
    # fi
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
az cloud set -n $mycld
az account set -s $mysub
if [ $? -eq 1 ]; then exit; fi

echo " "
echo "Cloud = $mycld"
echo "Subscription ID = ${s}"
echo "Azure Resource Group Filter = ${g}"
echo "Terraform Resource Type Filter = ${r}"
echo "Get Subscription Policies & RBAC = ${p}"
echo "Extract Key Vault Secrets to .tf files (insecure) = ${x}"
echo "Fast Forward = ${f}"
echo "Validate Only = ${v}"
echo "Debug = ${f}"
echo " "



mkdir -p generated/tf.$mysub
cd generated/tf.$mysub
rm -rf .terraform
if [ "$f" = "no" ]; then
    rm -f import.log *.txt
    rm -f terraform* *.tf *.sh
else
    rm -f *$r*state*.sh import.log
fi

# cleanup from any previous runs
rm -f terraform*.backup
#rm -f terraform.tfstate
rm -f tf*.sh
cp ../../stub/*.tf .

#pyc1="python2.7 ../../scripts/az2tf.py -c $mycld -s $mysub "
pyc1="python3 ../../scripts/az2tf.py -c $mycld -s $mysub "
if [ "$g" != "" ]; then
    pyc2=" -g $g "
else
    pyc2=" "
fi
if [ "$r" != "" ]; then
    lcr=`echo $r | awk '{print tolower($0)}'`
    rm *$lcr*.tf
    pyc3=" -r $lcr "
else
    pyc3=" "
fi

pyc4=" "
# subscription level stuff - roles & policies
if [ "$p" = "yes" ]; then  pyc4=" -p $p " ;fi

pyc5=" "
# subscription level stuff - roles & policies
if [ "$d" = "yes" ]; then  pyc5=" -d $d " ; fi

pyc6=" "
# subscription level stuff - roles & policies
if [ "$f" = "yes" ]; then
    pyc6=" -f $f "
fi

pyc9=" 2>&1 | tee -a import.log"

pyc=`printf "%s %s %s %s %s %s %s" "$pyc1" "$pyc2" "$pyc3" "$pyc4" "$pyc5" "$pyc6" "$pyc9"`
echo $pyc
eval $pyc
grep Error import.log
if [ $? -eq 0 ]; then
    echo "Error in az2tf.py"
    exit
fi

#
# uncomment following line if you want to use an SPN login
#../../setup-env.sh


echo "terraform init"
terraform init 2>&1 | tee -a import.log
grep Error import.log
if [ $? -eq 0 ]; then
    echo "Error with terraform init"
    exit
fi

echo "terraform validate"
terraform validate
if [ $? -eq 1 ]; then
    echo "Error Validating"
    exit
fi

if [ "$v" = "yes" ]; then 
    echo "---------------------------------------------------------------------------"
    echo "az2tf output files are in generated/tf.$mysub"
    echo "---------------------------------------------------------------------------"
    exit 
fi

chmod 755 *state*.sh

if [ "$f" = "yes" ]; then
for com in `ls *$r*staterm.sh | sort -g`; do
    comm=`printf "./%s" $com`
    echo $comm
    eval $comm
done
fi

echo "state cleaned"

for com in `ls *$r*stateimp.sh | sort -g`; do
    comm=`printf "./%s" $com`
    echo $comm
    eval $comm
done
echo "imports completed"

#date
#
#if [ "$x" = "yes" ]; then
#    echo "Attempting to extract secrets"
#    ../../scripts/350_key_vault_secret.sh
#fi
##

echo "Terraform fmt ..."
terraform fmt

echo "Terraform Plan ..."
terraform plan .
echo "---------------------------------------------------------------------------"
echo "az2tf output files are in generated/tf.$mysub"
echo "---------------------------------------------------------------------------"



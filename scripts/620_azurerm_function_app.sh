prefixa=`echo $0 | awk -F 'azurerm_' '{print $2}' | awk -F '.sh' '{print $1}' `
tfp=`printf "azurerm_%s" $prefixa`
if [ "$1" != "" ]; then
    rgsource=$1
else
    echo -n "Enter name of Resource Group [$rgsource] > "
    read response
    if [ -n "$response" ]; then
        rgsource=$response
    fi
fi
azr=`az functionapp list -g $rgsource -o json`
count=`echo $azr | jq '. | length'`
if [ "$count" -gt "0" ]; then
    count=`expr $count - 1`
    for i in `seq 0 $count`; do
        
        name=`echo $azr | jq ".[(${i})].name" | tr -d '"'`
        rname=`echo $name | sed 's/\./-/g'`
        rg=`echo $azr | jq ".[(${i})].resourceGroup"  | tr -d '"'`
        id=`echo $azr | jq ".[(${i})].id" | tr -d '"'`
        loc=`echo $azr | jq ".[(${i})].location"`
        https=`echo $azr | jq ".[(${i})].httpsOnly"`
  
        prg=`echo $azr | jq ".[(${i})].appServicePlanId" | cut -d'/' -f5  | tr -d '"'`
        pnam=`echo $azr | jq ".[(${i})].appServicePlanId" | cut -d'/' -f9 | tr -d '"'`
        lcrg=`echo $azr | jq ".[(${i})].resourceGroup" | awk '{print tolower($0)}' | tr -d '"'`
        appplid=`echo $azr | jq ".[(${i})].appServicePlanId" | tr -d '"'`
        rg=`echo $lcrg | sed 's/\./-/g'`
 
        appset=`az functionapp config appsettings list -n $name -g $rg -o json`

        prefix=`printf "%s.%s" $prefixa $rg`
        outfile=`printf "%s.%s__%s.tf" $tfp $rg $rname`
        echo $az2tfmess > $outfile  
        
        printf "resource \"%s\" \"%s__%s\" {\n" $tfp $rg $rname >> $outfile
        printf "\t name = \"%s\"\n" $name >> $outfile
        printf "\t location = %s\n" "$loc" >> $outfile
        printf "\t resource_group_name = \"%s\"\n" $rgsource >> $outfile

        # case issues - so use resource id directly
        # printf "\t app_service_plan_id = \"\${azurerm_app_service_plan.%s__%s.id}\"\n" $prg $pnam >> $outfile
        printf "\t app_service_plan_id = \"%s\"\n" $appplid >> $outfile
# dummy entry

        printf "\t https_only = \"%s\" \n"  "$https" >> $outfile
        blog="false"
        strcon=""

        jcount=`echo $appset | jq '. | length'`
        if [ "$jcount" -gt "0" ]; then
            count=`expr $jcount - 1`
            for j in `seq 0 $jcount`; do

                aname=`echo $appset | jq ".[(${j})].name" | tr -d '"'`
                aval=`echo $appset | jq ".[(${j})].value"`

                case "$aname" in 
                
                "AzureWebJobsStorage")
                    strcon=`echo $aval`
                ;;
                "FUNCTIONS_EXTENSION_VERSION")
                    printf "\t version = %s \n"  "$aval" >> $outfile
                ;;
                "null")
                ;;
                 "WEBSITE_CONTENTSHARE" | "WEBSITE_CONTENTAZUREFILECONNECTIONSTRING")
                ;;
                "AzureWebJobsDashboard")
        
                if [ ${#aval} -ge 3 ]; then
                  blog="true"
                fi
                ;;

                *) 
                printf "\t app_settings { \n" >> $outfile
                printf "\t %s=%s\n" $aname "$aval" >> $outfile
                printf "\t } \n" >> $outfile
                ;;
                esac

            done
        fi

        if [ ${#strcon} -ge 3 ]; then
            printf "\t storage_connection_string = %s \n"  "$strcon" >> $outfile
        else
            printf "\t storage_connection_string = \"\" \n"  >> $outfile
        fi

        printf "\t enable_builtin_logging = \"%s\" \n"  $blog >> $outfile
        printf "}\n" >> $outfile

        cat $outfile
        statecomm=`printf "terraform state rm %s.%s__%s" $tfp $rg $rname`
        echo $statecomm >> tf-staterm.sh
        eval $statecomm
        evalcomm=`printf "terraform import %s.%s__%s %s" $tfp $rg $rname $id`
        echo $evalcomm >> tf-stateimp.sh
        eval $evalcomm
    done
fi

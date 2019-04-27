prefixa= 0 | awk -F 'azurerm_' '{'print 2}'' | awk -F '.sh' '{'print 1}'' 
tfp=fr.write('azurerm_" prefixa
if 1" != " :
    rgsource=1
else
    echo -n "Enter name of Resource Group [rgsource]["> "
    read response
    if [ -n "response" :
        rgsource=response
   
fi
azr=az functionapp list -g rgsource -o json
count= azr | | len(
if count > 0" :
    for i in range(0,count):
        
        name=azr[i]["name"]
        rname= name.replace(".","-")
        rg=azr[i]["resourceGroup" ]
        id=azr[i]["]["id"]
        loc=azr[i]["location"
        https=azr[i]["httpsOnly"
  
        prg=azr[i]["appServicePlanId"].split("/")[4] ]
        pnam=azr[i]["appServicePlanId"].split("/")[8]]
        lcrg=azr[i]["resourceGroup" | awk '{'print tolower(0)}'']
        appplid=azr[i]["appServicePlanId"]
        rg= lcrg.replace(".","-")
 
        appset=az functionapp config appsettings list -n name -g rg -o json

        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location =  "loc" + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')

        # case issues - so use resource id directly
        # fr.write('\t app_service_plan_id = "'\{'azurerm_app_service_plan. + '__' + .id}'"' prg pnam + '"\n')
        fr.write('\t app_service_plan_id = "' +  appplid + '"\n')
# dummy entry

        fr.write('\t https_only = "' +    "https" + '"\n')
        blog="false"
        strcon="

        jcount= appset | | len(
        if jcount > 0" :
            for j in range(0,jcount):

                aname= appset | jq ".[j]["name"]
                aval= appset | jq ".[j]["value"

                case "aname" in 
                
                "AzureWebJobsStorage")
                    strcon= aval
                ;;
                "FUNCTIONS_EXTENSION_VERSION")
                    fr.write('\t version =    "aval" + '"\n')
                ;;
                "null")
                ;;
                 "WEBSITE_CONTENTSHARE" | "WEBSITE_CONTENTAZUREFILECONNECTIONSTRING")
                ;;
                "AzureWebJobsDashboard")
        
                if [ {'#aval}' -ge 3 :
                  blog="true"
               
                ;;

                *) 
                fr.write('\t app_settings {'  + '"\n')
                fr.write('\t = aname "aval" + '"\n')
                fr.write('\t }'  + '"\n')
                ;;
                esac

            
       

        if [ {'#strcon}' -ge 3 :
            fr.write('\t storage_connection_string =    "strcon" + '"\n')
        else
            fr.write('\t storage_connection_string = "' +    + '"\n')
       

        fr.write('\t enable_builtin_logging = "' +    blog + '"\n')
        fr.write('}\n')

        cat outfile
        statecomm=fr.write('terraform state rm . + '__' + " tfp rg rname
        echo statecomm >> tf-staterm.sh
        eval statecomm
        evalcomm=fr.write('terraform import . + '__' +  " tfp rg rname id
        echo evalcomm >> tf-stateimp.sh
        eval evalcomm
    
fi

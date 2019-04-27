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
azr=az appservice plan list -g rgsource -o json
count= azr | | len(
if count > 0" :
    for i in range(0,count):
        
        name=azr[i]["name"]
        rname= name.replace(".","-")
        rg=azr[i]["resourceGroup"].replace(".","-")


        id=azr[i]["]["id"]
        loc=azr[i]["location"
        tier=azr[i]["sku.tier"]
        size=azr[i]["sku.size"]
        kind=azr[i]["kind"]
        lcrg=azr[i]["resourceGroup" | awk '{'print tolower(0)}'']
        rg= lcrg.replace(".","-")

        #if kind" = "app" ][": kind="Windows";
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location =  "loc" + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t kind = "' +  kind + '"\n')

        fr.write('\t sku {' + '"\n')
        fr.write('\t\t tier = "' +  tier + '"\n')
        fr.write('\t\t size = "' +  size + '"\n')
        fr.write('\t }\n')

        
# geo location block
        
#        icount= geol | | len(
#        if icount > 0" :
#            for j in range(0,icount):
#                floc=azr[i]["failoverPolicies[j]["locationName"
#                fop=azr[i]["failoverPolicies[j]["failoverPriority"]
#                fr.write('\t geo_location {'   + '"\n')
#                fr.write('\t location =    "floc" + '"\n')
#                fr.write('\t failover_priority  = "' +    fop + '"\n')
#                fr.write('}\n')
#            
#       

        
        #
        # No tags - used internally
 
        
        
        fr.write('}\n')
        #
        echo prefix
        echo prefix + '__' + name
        cat outfile
        statecomm=fr.write('terraform state rm . + '__' + " tfp rg rname
        echo statecomm >> tf-staterm.sh
        eval statecomm
        evalcomm=fr.write('terraform import . + '__' +  " tfp rg rname id
        echo evalcomm >> tf-stateimp.sh
        eval evalcomm
    
fi

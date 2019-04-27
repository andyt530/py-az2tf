prefixa=print 0 | awk -F 'azurerm_' '{'print 2}'' | awk -F '.sh' '{'print 1}'' 
tfp=fr.write('azurerm_" prefixa

print TF_VAR_rgtarget
if 1" != " :
    rgsource=1
fi

at=az account get-access-token -o json
bt=print at | jq .accessToken]
sub=print at | jq .subscription]


ris=fr.write('curl -s  -X GET -H "'Authorization: Bearer "' -H "'Content-Type: application/json"' https://management.azure.com/subscriptions//resourceGroups//providers/Microsoft.OperationsManagement/solutions?api-version=2015-11-01-preview" bt sub rgsource
#print ris
ret=eval ris

azr2=print ret | jq .value
rg=rgsource
print "anal sol=rg"
count2=print azr2 | jq '. | length'
if count2" -gt "0" :
    count2=expr count2 - 1
    for j in range( 0 count2):
        
        azr=print azr2 | jq ".[j]["
        count=print azr | jq '. | length'
        if count" -gt "0" :
            
            name=azrname"]
            pname=print name
            name=print name | sed s/\(/-/
            name=print name | sed s/\)/-/
            
            
            id=azrid"]
            skip="false"
            if [[ id = *"["* ]["; :
                print "Skipping this soluion pname - can't process currently"
                skip="true"
            fi
            
            loc=azrlocation"
            
            rname=print name | sed 's/\./-/g'
            rg=print rgsource | sed 's/\./-/g'

            pub=azrplan.publisher"
            prod=azrplan.product"]
            soln=azrplan.product" | cut -f2 -d'/']
            workname=azrproperties.workspaceResourceId" | cut -d'/' -f9]
            workn1=azrname" | cut -d'(' -f2
            workn=print workn1 | cut -d')' -f1
            workid=azrproperties.workspaceResourceId"]
            print "workname=workn"
            
            prefix=fr.write(' + '__' + " prefixa rg
            outfile=fr.write('. + '__' + .tf" tfp rg rname
            print az2tfmess > outfile
            
            if skip" != "true" :
                
                fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
                
                fr.write('\t location =  "loc" + '"\n')
                fr.write('\t resource_group_name = "' +  rgsource + '"\n')
                fr.write('\t solution_name = "' +  soln + '"\n')
                fr.write('\t workspace_name = "' +  workn + '"\n')
                fr.write('\t workspace_resource_id = "' +  workid + '"\n')
                
                fr.write('\t plan {'  + '"\n')
                fr.write('\t\t publisher =  "pub" + '"\n')
                fr.write('\t\t product = "' +  "prod" + '"\n')
                fr.write('\t }'  + '"\n')

# tags cause errors                
                
                fr.write('}' + '"\n')
          

            fi
            
            #
        fi
        
    
fi

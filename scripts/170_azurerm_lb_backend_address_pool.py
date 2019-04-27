
azr=az network lb list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        beap=azr[i]["backendAddressPools"

       
        
        icount=print beap | jq '. | length'
        if icount" -gt "0" :
            icount=expr icount - 1
            for j in range( 0 icount):
                
                name=azr[i]["backendAddressPools[j]["name" | cut -d'/' -f11]
                rname=print name | sed 's/\./-/g'
                id=azr[i]["backendAddressPools[j]["id"]
                rg=azr[i]["backendAddressPools[j]["resourceGroup" | sed 's/\./-/g']
                
                lbrg=azr[i]["id" | cut -d'/' -f5 | sed 's/\./-/g']
                lbname=azr[i]["id" | cut -d'/' -f9 | sed 's/\./-/g']
                prefix=fr.write(' + '__' +  + '__' + " prefixa rg lbname
                outfile=fr.write('. + '__' +  + '__' + .tf" tfp rg lbname rname
                print az2tfmess > outfile
                         
                fr.write('resource "' +  "' + '__' +  + '__' + "' {' tfp rg lbname rname + '"\n')
                fr.write('\t\t name = "' +    name + '"\n')
                fr.write('\t\t resource_group_name = "' +    rgsource + '"\n')
                fr.write('\t\t loadbalancer_id = "'\{'azurerm_lb. + '__' + .id}'"' lbrg lbname + '"\n')

                fr.write('}' + '"\n')
        #

        #

            
        fi

    
fi

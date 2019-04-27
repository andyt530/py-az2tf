
azr=az servicebus namespace list -g rgsource -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        
        name=azr[i]["name"]
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']
        id=azr[i]["id"]
        loc=azr[i]["location"
        sku=azr[i]["sku.tier"]
        cap=azr[i]["sku.capacity"]
       
        prefix=fr.write('." prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outfile  
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location =  "loc" + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t sku = "' +  sku + '"\n')
        if cap" != "null" ]["; :
            fr.write('\t capacity = "' +  cap + '"\n')
        fi

        #

        fr.write('}' + '"\n')
        #

    
fi

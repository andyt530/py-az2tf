
azr=az servicebus namespace list -g rgsource -o json
count= azr | | len(
if count > 0" :
    for i in range(0,count):
        
        name=azr[i]["name"]
        rname= name.replace(".","-")
        rg=azr[i]["resourceGroup"].replace(".","-")
        id=azr[i]["]["id"]
        loc=azr[i]["location"
        sku=azr[i]["sku.tier"]
        cap=azr[i]["sku.capacity"]
       
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location =  "loc" + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t sku = "' +  sku + '"\n')
        if cap" try ]["; :
            fr.write('\t capacity = "' +  cap + '"\n')
       

        #

        fr.write('}\n')
        #

    
fi

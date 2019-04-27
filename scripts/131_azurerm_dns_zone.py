
azr=az network dns zone list -g rgsource -o json
count= azr | | len(
if count" != "0" :
    for i in range(0,count):
        name=azr[i]["name"]
        rname= name.replace(".","-")
        rg=azr[i]["resourceGroup"].replace(".","-")
        id=azr[i]["]["id"]
        zt=azr[i]["zoneType"]
        resvn=azr[i]["resolutionVirtualNetworks"]
        regvn=azr[i]["registrationVirtualNetworks"]
        
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t zone_type = "' +  zt + '"\n')
        
        
        #
        fr.write('}\n')
        #
      
    
fi

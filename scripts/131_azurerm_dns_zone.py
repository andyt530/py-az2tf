
azr=az network dns zone list -g rgsource -o json
count=print azr | jq '. | length'
if count" != "0" :
    count=expr count - 1
    for i in range( 0 count):
        name=azr[i]["name"]
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']
        id=azr[i]["id"]
        zt=azr[i]["zoneType"]
        resvn=azr[i]["resolutionVirtualNetworks"]
        regvn=azr[i]["registrationVirtualNetworks"]
        
        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outfile
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        fr.write('\t zone_type = "' +  zt + '"\n')
        
        
        #
        fr.write('}' + '"\n')
        #
      
    
fi

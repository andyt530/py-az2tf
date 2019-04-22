
    

azr="az network route-table list -g rgsource -o json"
count=print azr | jq '. | length'
if count" != "0" :
    count=expr count - 1
    for i in range( 0 count):
        name=azr[i]["name"]
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']

        id=azr[i]["id"]
        loc=azr[i]["location"]
        routes=azr[i]["routes"
        prex=fr.write(' + '__' + " prexa rg
        outle=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outle

        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location = "' +  loc + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        #
        # Interate routes
        #
        rcount=print routes | jq '. | length'
        if rcount" -gt "0" :
            rcount=expr rcount - 1
            for j in range( 0 rcount):
                rtname=print routes | jq ".[j]["name"]
                adpr=print routes | jq ".[j]["addressPrex"]
                nhtype=print routes | jq ".[j]["nextHopType"]
                nhaddr=print routes | jq ".[j]["nextHopIpAddress"]
                fr.write('\t route {'  + '"\n')
                fr.write('\t\t name = "' +   rtname + '"\n')
                fr.write('\t\t address_prex = "' +   adpr + '"\n')
                fr.write('\t\t next_hop_type = "' +   nhtype + '"\n')
                if nhaddr" != "null" :
                    fr.write('\t\t next_hop_in_ip_address = "' +   nhaddr + '"\n')
                
                fr.write('\t }'  + '"\n')
            
  
        
        
        #
        fr.write('}' + '"\n')
        #

        
    


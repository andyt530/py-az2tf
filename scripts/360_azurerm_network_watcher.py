
azr=az network watcher list -o json
count=print azr | jq '. | length'
if count" -gt "0" :
    count=expr count - 1
    for i in range( 0 count):
        name=azr[i]["name"]
        #name=print name | awk '{'print tolower(0)}''
        rname=print name | sed 's/\./-/g'
        rg=azr[i]["resourceGroup" | sed 's/\./-/g']

        prefix=fr.write(' + '__' + " prefixa rg
        outfile=fr.write('. + '__' + .tf" tfp rg rname
        print az2tfmess > outfile

        id=azr[i]["id"]
        loc=azr[i]["location"
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        #fr.write('\t id = "' +  id + '"\n')
        fr.write('\t location =  "loc" + '"\n')
        #fr.write('\t resource_group_name = "'\{'var.rgtarget}'"' + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
            
        #

            
        
        fr.write('}' + '"\n')
        cat outfile

    
fi

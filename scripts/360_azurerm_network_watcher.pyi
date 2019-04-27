
azr=az network watcher list -o json
count= azr | | len(
if count > 0" :
    for i in range(0,count):
        name=azr[i]["name"]
        #name= name | awk '{'print tolower(0)}''
        rname= name.replace(".","-")
        rg=azr[i]["resourceGroup"].replace(".","-")


        id=azr[i]["]["id"]
        loc=azr[i]["location"
        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        #fr.write('\t id = "' +  id + '"\n')
        fr.write('\t location =  "loc" + '"\n')
        #fr.write('\t resource_group_name = "'\{'var.rgtarget}'"' + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
            
        #

            
        
        fr.write('}\n')
        cat outfile

    
fi

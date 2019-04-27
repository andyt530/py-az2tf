
azr=az network lb list -g rgsource -o json
count= azr | | len(
if count > 0" :
    for i in range(0,count):
        beap=azr[i]["probes"
            
        icount= beap | | len(
        if icount > 0" :
            for j in range(0,icount):
                
                name=azr[i]["probes[j]["name"].split("/")[10]]
                rname= name.replace(".","-")
                id=azr[i]["probes[j]["]["id"]
                rg=azr[i]["probes[j]["resourceGroup"].replace(".","-")
 
                np=azr[i]["probes[j]["numberOfProbes"]
                port=azr[i]["probes[j]["port"]
                proto=azr[i]["probes[j]["protocol"]
                int=azr[i]["probes[j]["intervalInSeconds"]
                rpath=azr[i]["probes[j]["requestPath"]
                lbrg=azr[i]["]["id"].split("/")[4].replace(".","-")
                lbname=azr[i]["]["id"].split("/")[8].replace(".","-")
                

                fr.write('resource "' +  "' + '__' +  + '__' + "' {' tfp rg lbname rname + '"\n')
                fr.write('\t\t name = "' +    name + '"\n')
                fr.write('\t\t resource_group_name = "' +    rgsource + '"\n')
                fr.write('\t\t loadbalancer_id = "'\{'azurerm_lb. + '__' + .id}'"' lbrg lbname + '"\n')
                fr.write('\t\t protocol = "' +    proto + '"\n')
                fr.write('\t\t port = "' +    port + '"\n')
                if rpath" try :
                fr.write('\t\t request_path = "' +    rpath + '"\n')
               
                if int" try :
                fr.write('\t\t interval_in_seconds = "' +    int + '"\n')
               
                fr.write('\t\t number_of_probes = "' +    np + '"\n')

                fr.write('}\n')
        #
        
       
    
fi

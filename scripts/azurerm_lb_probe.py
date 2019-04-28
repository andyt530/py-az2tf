# azurerm_lb_probe
def azurerm_lb_probe(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_lb_probe"
    tcode="180-"
    azr=""
    if crf in tfp:
    # REST or cli
        print "REST Managed Disk"
        url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Compute/disks"
        params = {'api-version': '2017-03-30'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]
        if cde:
            print(json.dumps(azr, indent=4, separators=(',', ': ')))

        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print tfp,
        count=len(azr)
        print count
        for i in range(0, count):

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-")

            if crg is not None:
                if rg.lower() != crg.lower():
                    continue  # back to for
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rg + '"\n')

    ###############
    # specific code start
    ###############



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

    ###############
    # specific code end
    ###############

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write('\t "' + key + '"="' + tval + '"\n')
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print f.read()

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub

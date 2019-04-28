# azurerm_app_service
def azurerm_app_service(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_app_service"
    tcode="610-"
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


prefixa= 0 | awk -F 'azurerm_' '{'print 2}'' | awk -F '.sh' '{'print 1}'' 
tfp=fr.write('azurerm_" prefixa
if 1" != " :
    rgsource=1
else
    echo -n "Enter name of Resource Group [rgsource]["> "
    read response
    if [ -n "response" :
        rgsource=response
   
fi
azr=az webapp list -g rgsource -o json
count= azr | | len(
if count > 0" :
    for i in range(0,count):
        
        name=azr[i]["name"]
        rname= name.replace(".","-")
        rg=azr[i]["resourceGroup" ]
        id=azr[i]["]["id"]
        loc=azr[i]["location"
        prg=azr[i]["appServicePlanId"].split("/")[4] ]
        pnam=azr[i]["appServicePlanId"].split("/")[8]]
        lcrg=azr[i]["resourceGroup" | awk '{'print tolower(0)}'']
        appplid=azr[i]["appServicePlanId"]
        rg= lcrg.replace(".","-")

        
        fr.write('resource "' +  "' + '__' + "' {' tfp rg rname + '"\n')
        fr.write('\t name = "' +  name + '"\n')
        fr.write('\t location =  "loc" + '"\n')
        fr.write('\t resource_group_name = "' +  rgsource + '"\n')
        # case issues - so use resource id directly
        # fr.write('\t app_service_plan_id = "'\{'azurerm_app_service_plan. + '__' + .id}'"' prg pnam + '"\n')
        fr.write('\t app_service_plan_id = "' +  appplid + '"\n')


# geo location block
        
#        icount= geol | | len(
#        if icount > 0" :
#            for j in range(0,icount):
#                floc=azr[i]["failoverPolicies[j]["locationName"
#                fop=azr[i]["failoverPolicies[j]["failoverPriority"]
#                fr.write('\t geo_location {'   + '"\n')
#                fr.write('\t location =    "floc" + '"\n')
#                fr.write('\t failover_priority  = "' +    fop + '"\n')
#                fr.write('}\n')
#            
#       

        
        #
        # tags internal
        
        
        fr.write('}\n')
        #

        cat outfile
        statecomm=fr.write('terraform state rm . + '__' + " tfp rg rname
        echo statecomm >> tf-staterm.sh
        eval statecomm
        evalcomm=fr.write('terraform import . + '__' +  " tfp rg rname id
        echo evalcomm >> tf-stateimp.sh
        eval evalcomm
    
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

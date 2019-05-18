# azurerm_app_service
def azurerm_app_service(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    tfp="azurerm_app_service"
    tcode="610-"
    azr=""
    if crf in tfp:
    # REST or cli
        print "REST App Service"
        url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Web/sites"
        params = {'api-version': '2018-02-01'}
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

            kind=azr[i]["kind"]
            if kind == "functionapp": continue

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-")
            rgs=id.split("/")[4]

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
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

    #azr=az webapp list -g rgsource -o json

            prg=azr[i]["properties"]["serverFarmId"].split("/")[4]
            pnam=azr[i]["properties"]["serverFarmId"].split("/")[8]
       
            appplid=azr[i]["properties"]["serverFarmId"]
  

            # case issues - so use resource id directly
            # fr.write('\t app_service_plan_id = "${azurerm_app_service_plan. + '__' + .id}'"' prg pnam + '"\n')
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

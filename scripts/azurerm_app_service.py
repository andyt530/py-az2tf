# azurerm_app_service
def azurerm_app_service(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_app_service"
    tcode="610-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST App Service"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Web/sites"
        params = {'api-version': '2018-02-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            kind=azr[i]["kind"]
            if kind == "functionapp": continue

            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]

            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
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

            try:
                httpsonly=str(azr[i]["properties"]["httpsOnly"]).lower()
                fr.write('\t https_only = ' +  httpsonly + '\n')
            except KeyError:
                pass

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
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass


            url="https://management.azure.com/" + id + "/config/appsettings/list"
            #print url
            params = {'api-version': '2018-02-01'}
            r = requests.post(url, headers=headers, params=params)
            appset= r.json()
            #print(json.dumps(appset, indent=4, separators=(',', ': ')))

            fr.write('\t app_settings = { \n')

            try:
                strcon=appset["properties"]["AzureWebJobsStorage"]
            except KeyError:
                pass

            try:
                vers=appset["properties"]["FUNCTIONS_EXTENSION_VERSION"]
            except KeyError:
                pass

            try:
                runfrompackage=appset["properties"]["WEBSITE_RUN_FROM_PACKAGE"]
                fr.write('\t WEBSITE_RUN_FROM_PACKAGE = "' + runfrompackage + '"\n')
            except KeyError:
                pass

            try:
                aval=appset["properties"]["WEBSITE_NODE_DEFAULT_VERSION"]
                fr.write('\t WEBSITE_NODE_DEFAULT_VERSION = "' + aval + '"\n')
            except KeyError:
                pass

            try:
                aval=appset["properties"]["FUNCTIONS_WORKER_RUNTIME"]
                fr.write('\t FUNCTIONS_WORKER_RUNTIME = "' + aval + '"\n')
            except KeyError:
                pass

            try:
                aval=appset["properties"]["APPINSIGHTS_INSTRUMENTATIONKEY"]
                fr.write('\t APPINSIGHTS_INSTRUMENTATIONKEY = "' + aval + '"\n')
            except KeyError:
                pass

            try:
                aval=appset["properties"]["mykey"]
                fr.write('\t mykey = "' + aval + '"\n')
            except KeyError:
                pass

            try:
                aval=appset["properties"]["myten"]
                fr.write('\t myten = "' + aval + '"\n')
            except KeyError:
                pass

            try:
                aval=appset["properties"]["usern"]
                fr.write('\t usern = "' + aval + '"\n')
            except KeyError:
                pass

                #if aname == "WEBSITE_CONTENTSHARE" or aname == "WEBSITE_CONTENTAZUREFILECONNECTIONSTRING":


            try:
                aval=appset["properties"]["AzureWebJobsDashboard"]
                if len(aval) > 3:
                    blog=True
            except KeyError:
                pass

            fr.write('\t }'  + '\n')

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub

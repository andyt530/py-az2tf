# azurerm_function_app
def azurerm_function_app(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_function_app"
    tcode="620-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Function App"
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

            if kind != "functionapp": continue
            
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
            fr.write('\tname = "' + name + '"\n')
            fr.write('\tlocation = "'+ loc + '"\n')
            fr.write('\tresource_group_name = "'+ rgs + '"\n')

            https=azr[i]["properties"]["httpsOnly"]
            appplid=azr[i]["properties"]["serverFarmId"]
    
            # case issues - so use resource id directly
            # fr.write('\t app_service_plan_id = "${azurerm_app_service_plan. + '__' + .id}'"' prg pnam + '"\n')
            fr.write('\tapp_service_plan_id = "' + appplid + '"\n')
            fr.write('\thttps_only = ' + str(https).lower() + '\n')
            blog=False
            strcon=""

            url="https://management.azure.com/" + id + "/config/appsettings/list"
            params = {'api-version': '2018-02-01'}
            r = requests.post(url, headers=headers, params=params)       
            appset= r.json()
            
            fr.write('\tapp_settings = { \n')

            #app settings
            try:
                for setting in appset["properties"]:
                    value=appset["properties"][setting]
                    fr.write('\t\t'+ setting + ' = "' + value + '"\n')   
            except KeyError:
                pass
                                      
            try:
                aval=appset["properties"]["AzureWebJobsDashboard"] 
                if len(aval) > 3:
                    blog=True
            except KeyError:
                pass

            fr.write('\t }'  + '\n')

            try:
                strcon=appset["properties"]["AzureWebJobsStorage"]         
            except KeyError:
                pass 

            if len(strcon) >= 3 :
                fr.write('\tstorage_connection_string = "' + strcon + '" \n')
            else:
                fr.write('\tstorage_connection_string = ""\n')
            
            try:
                vers=appset["properties"]["FUNCTIONS_EXTENSION_VERSION"]  
                fr.write('\tversion = "' + vers + '"\n')          
            except KeyError:
                pass
            
            fr.write('\tenable_builtin_logging = ' + str(blog).lower() + '\n')

            # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('\ttags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('\t}\n')
            except KeyError:
                pass

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

# azurerm_app_service_slot
def azurerm_app_service_slot(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_app_service_slot"
    tcode="611-"
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
        #print (count)
        for i in range(0, count):

            kind=azr[i]["kind"]
            if kind == "functionapp": continue

            name=azr[i]["name"]
            aname=name
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
            
            url="https://" + cldurl + "/subscriptions/" + sub + "/resourceGroups/"+rgs+"/providers/Microsoft.Web/sites/" + name + "/slots"
            #print(url)
            params = {'api-version': '2018-02-01'}
            r = requests.get(url, headers=headers, params=params)
            #print(json.dumps(r.json(), indent=4, separators=(',', ': ')))
            try:
                azr2= r.json()["value"]
            except KeyError:
                print ("Found no slots")
                return

            if cde:
                print ("****")
                print(json.dumps(azr2, indent=4, separators=(',', ': ')))

            icount=len(azr2)
            print(icount)
            if icount > 0 :
                for j in range(0,icount):
                    id=azr2[j]["id"]
                    name=azr2[j]["id"].split("/")[10]
                    rname=name.replace(".","-")
                    prefix=tfp+"."+rg+'__'+aname+'__'+rname
                    #print(prefix)
                    rfilename=prefix+".tf"
                    fr=open(rfilename, 'w')
                    fr.write(az2tfmess)
                    fr.write('resource ' + tfp + ' ' + rg + '__'+aname+'__'+rname + ' {\n')
                    fr.write('\t name = "' + name + '"\n')
                    fr.write('\t location = "'+ loc + '"\n')
                    fr.write('\t resource_group_name = azurerm_resource_group.'+ rgs + '.name\n')
                    fr.write('\t app_service_name = azurerm_app_service.'+ rgs+ '__'+aname + '.name\n')

            #azr=az webapp list -g rgsource -o json
            
                    appplid=azr[i]["properties"]["serverFarmId"]

                    try:
                        httpsonly=str(azr[i]["properties"]["httpsOnly"]).lower()
                        fr.write('\t https_only = ' +  httpsonly + '\n')
                    except KeyError:
                        pass

                    # case issues - so use resource id directly
                    # fr.write('\t app_service_plan_id = azurerm_app_service_plan. + '__' + '.id' prg pnam + '"\n')
                    fr.write('\t app_service_plan_id = "' +  appplid + '"\n')
            

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


                    fr.write('}\n') 
                    fr.close()   # close .tf file

                    if cde:
                        with open(rfilename) as f: 
                            print (f.read())

                    tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+aname+'__'+rname + '\n')

                    tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                    tfcomm='terraform import '+tfp+'.'+rg+'__'+aname+'__'+rname+' '+id+'\n'
                    tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub

# azurerm_app_service_plan
def azurerm_app_service_plan(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_app_service_plan"
    tcode="600-"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST App Service Plan"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Web/serverfarms"
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
            
            tier=azr[i]["sku"]["tier"]
            size=azr[i]["sku"]["size"]
            kind=azr[i]["kind"]

            fr.write('\t kind = "' +  kind + '"\n')

            fr.write('\t sku {\n')
            fr.write('\t\t tier = "' +  tier + '"\n')
            fr.write('\t\t size = "' +  size + '"\n')
            fr.write('\t }\n')

            
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
            # No tags - used internally
       
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

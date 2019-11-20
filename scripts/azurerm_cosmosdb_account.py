# azurerm_cosmosdb_account
def azurerm_cosmosdb_account(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_cosmosdb_account"
    tcode="400-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.DocumentDB/databaseAccounts"
        params = {'api-version': '2016-03-31'}
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


        #azr=az cosmosdb list -g rgsource -o json
  
            kind=azr[i]["kind"]
            offer=azr[i]["properties"]["databaseAccountOfferType"]
            cp=azr[i]["properties"]["consistencyPolicy"]["defaultConsistencyLevel"]
            mis=azr[i]["properties"]["consistencyPolicy"]["maxIntervalInSeconds"]
            msp=azr[i]["properties"]["consistencyPolicy"]["maxStalenessPrefix"] 
            
            geol=azr[i]["properties"]["failoverPolicies"]     
                
            af=azr[i]["properties"]["enableAutomaticFailover"]      
                

            fr.write('\t kind = "' +  kind + '"\n')
            fr.write('\t offer_type = "' +  offer + '"\n')
            fr.write('\t consistency_policy {\n')
            fr.write('\t\t  consistency_level = "' +  cp + '"\n')
            fr.write('\t\t  max_interval_in_seconds = "' +  str(mis) + '"\n')
            fr.write('\t\t  max_staleness_prefix = "' +  str(msp) + '"\n')
            fr.write('\t }\n')
            fr.write('\t enable_automatic_failover = ' +  str(af).lower() + '\n')
        # capabilities block

            # code out terraform error
            try:
                caps=azr[i]["properties"]["capabilities"][0]["name"] 
                if caps == "EnableTable" or caps == "EnableGremlin" or caps == "EnableCassandra":
                    fr.write('\t capabilities {\n')
                    fr.write('\t\t name = "' +  caps + '"\n')        
                    fr.write('\t }\n')
            except KeyError:
                pass
            except IndexError:
                pass
            
        # geo location block
                
            icount= len(geol)
            for j in range(0,icount):
                    floc=azr[i]["properties"]["failoverPolicies"][j]["locationName"]
                    fop=azr[i]["properties"]["failoverPolicies"][j]["failoverPriority"]
                    fr.write('\t geo_location {\n')
                    fr.write('\t location = "'+floc + '"\n')
                    fr.write('\t failover_priority  = "' + str(fop) + '"\n')
                    fr.write('}\n')

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

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub

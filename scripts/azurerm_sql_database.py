# azurerm_sql_database
def azurerm_sql_database(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp = "azurerm_sql_database"
    tcode = "541-"
    azr = ""
    if crf in tfp:
    # REST or cli
        # print "REST SQL Servers"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Sql/servers"
        params = {'api-version': '2015-05-01-preview'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf = tcode+tfp+"-staterm.sh"
        tfimf = tcode+tfp+"-stateimp.sh"
        tfrm = open(tfrmf, 'a')
        tfim = open(tfimf, 'a')
        print ("# " + tfp,)
        count = len(azr)
        print (count)
        for i in range(0, count):
            
            name = azr[i]["name"]
            loc = azr[i]["location"]
            id = azr[i]["id"]
            rg = id.split("/")[4].replace(".", "-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs = id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))


            sname=name

# azr=az sql db list --server sname -g srg -o json
 
            url="https://management.azure.com/" + id + "/databases"
            
            params = {'api-version': '2017-10-01-preview'}
            r = requests.get(url, headers=headers, params=params)
            
            azr2= r.json()["value"]
            if cde:
                print(json.dumps(azr2, indent=4, separators=(',', ': ')))

            icount=len(azr2)
            if icount > 0 :
                for j in range(0,icount):
        
                    name = azr2[j]["name"]
                    loc = azr2[j]["location"]
                    id = azr2[j]["id"]
                    rg = id.split("/")[4].replace(".", "-").lower()
                    rgs = id.split("/")[4]
                    if crg is not None:
                        if rgs.lower() != crg.lower():
                            continue  # back to for

                    rname = name.replace(".", "-")
                    prefix = tfp+"."+rg+'__'+rname
                    # print prefix
                    rfilename = prefix+".tf"
                    fr = open(rfilename, 'w')
                    fr.write(az2tfmess)
                    fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                    fr.write('\t name = "' + name + '"\n')
                    fr.write('\t location = "' + loc + '"\n')
                    fr.write('\t resource_group_name = "' + rgs + '"\n')
                    #fr.write('\t server_name = "' + sname + '"\n')
                    col=azr2[j]["properties"]["collation"]
                    ed=azr2[j]["properties"]["currentSku"]["tier"]
                    rso=azr2[j]["properties"]["requestedServiceObjectiveName"]
                    fr.write('\t server_name = "' + sname + '"\n')
                    if ed != "System":
                        
                        fr.write('\t collation= "' + col + '"\n')
                        fr.write('\t edition= "' + ed + '"\n')
                        fr.write('\t requested_service_objective_name= "' + rso + '"\n')
                        try:
                            cm = azr2[j]["properties"]["createMode"]
                            fr.write('\t create_mode= "' + cm + '"\n')
                        except KeyError:
                            pass

            # tags block
                    try:
                        mtags = azr2[j]["tags"]
                        fr.write('tags = { \n')
                        for key in mtags.keys():
                            tval = mtags[key]
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

                    tfim.write('echo "importing ' + str(i) +
                            ' of ' + str(count-1) + '"' + '\n')
                    tfcomm = 'terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
                    tfim.write(tfcomm)

        # end for i loop

        tfrm.close()
        tfim.close()
    # end stub

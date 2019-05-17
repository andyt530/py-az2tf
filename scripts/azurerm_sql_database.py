# azurerm_sql_database
def azurerm_sql_database(crf, cde, crg, headers, requests, sub, json, az2tfmess):
    tfp = "azurerm_sql_database"
    tcode = "541-"
    azr = ""
    if crf in tfp:
    # REST or cli
        print "REST Managed Disk"
        url = "https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Sql/servers/databases"
        params = {'api-version': '2015-05-01-preview'}
        r = requests.get(url, headers=headers, params=params)
        azr = r.json()["value"]
        if cde:
            print(json.dumps(azr, indent=4, separators=(',', ': ')))

        tfrmf = tcode+tfp+"-staterm.sh"
        tfimf = tcode+tfp+"-stateimp.sh"
        tfrm = open(tfrmf, 'a')
        tfim = open(tfimf, 'a')
        print tfp,
        count = len(azr)
        print count
        for i in range(0, count):
            
            name = azr[i]["name"]
            loc = azr[i]["location"]
            id = azr[i]["id"]
            rg = id.split("/")[4].replace(".", "-")
            rgs = id.split("/")[4]
            if crg is not None:
                if rg.lower() != crg.lower():
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
        
# azr=az sql db list --server sname -g srg -o json

            col=azr[i]["properties"]["collation"]
            ed=azr[i]["properties"]["edition"]
            rso=azr[i]["properties"]["requestedServiceObjectiveName"]

            if ed != "System":
                fr.write('\t server_name = "' + name + '"\n')
                fr.write('\t collation= "' + col + '"\n')
                fr.write('\t edition= "' + ed + '"\n')
                fr.write('\t requested_service_objective_name= "' + rso + '"\n')
                try:
                    cm = azr[i]["properties"]["createMode"]
                    fr.write('\t create_mode= "' + cm + '"\n')
                except KeyError:
                    pass

    # tags block
            try:
                mtags = azr[i]["tags"]
                fr.write('tags { \n')
                for key in mtags.keys():
                    tval = mtags[key]
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

            tfim.write('echo "importing ' + str(i) +
                       ' of ' + str(count-1) + '"' + '\n')
            tfcomm = 'terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)

        # end for i loop

        tfrm.close()
        tfim.close()
    # end stub

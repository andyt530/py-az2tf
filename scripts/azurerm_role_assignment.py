
def azurerm_role_assignment(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    
    tfp="azurerm_role_assignment"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Authorization/roleAssignments"
        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf="007-"+tfp+"-staterm.sh"
        tfimf="007-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            #loc=azr[i]["location"]
            id=azr[i]["id"]
            rg="roleassignments"
            rgs=id.split("/")[4]
            if crg is not None:
                if rg.lower() != crg.lower():
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
            #fr.write('\t location = "'+ loc + '"\n')
            #fr.write('\t resource_group_name = "'+ rgs + '"\n')

            name=azr[i]["name"]
        
            scope=azr[i]["properties"]["scope"]
            rdid=azr[i]["name"]
            prid=azr[i]["properties"]["principalId"]
            roledefid=azr[i]["properties"]["roleDefinitionId"].split("/")[6]
            id=azr[i]["id"]
          

            fr.write('role_definition_id = "${azurerm_role_definition.' + "roledefinitions" + '__' + roledefid + '.id}"' + '\n')
            
            fr.write('principal_id ="' +prid +'"\n') 
            fr.write('scope = "' + scope  +'"\n') 
    
            #fr.write('}\n')

       
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
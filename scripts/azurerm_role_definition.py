import ast
def azurerm_role_definition(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_role_definition"
    
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Authorization/roleDefinitions"

        params = {'api-version': '2018-07-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf="006-"+tfp+"-staterm.sh"
        tfimf="006-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            #loc=azr[i]["location"]
            id=azr[i]["id"]
            rg="roledefinitions"
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
            
            #fr.write('\t location = "'+ loc + '"\n')
            #fr.write('\t resource_group_name = "'+ rgs + '"\n')
            
            name=azr[i]["properties"]["roleName"]
            fr.write('\t name = "' + name + '"\n')
            rdid=azr[i]["name"]
            desc=azr[i]["properties"]["description"]
            #desc=desc.encode('utf-8', 'ignore')
            id=azr[i]["id"]
            

            scopes=azr[i]["properties"]["assignableScopes"]
            scopes=str(ast.literal_eval(json.dumps(azr[i]["properties"]["assignableScopes"])))
            scopes=scopes.replace("'",'"')
            dactions=azr[i]["properties"]["permissions"][0]["dataActions"]
            ndactions=azr[i]["properties"]["permissions"][0]["notDataActions"]
            actions=azr[i]["properties"]["permissions"][0]["actions"]
            nactions=azr[i]["properties"]["permissions"][0]["notActions"]

            #fr.write('role_definition_id = "' + rdid +  '"\n')
            fr.write('description =  "' +desc + '"\n')
            #fr.write('scope = "'\{'data.azurerm_subscription.primary.id}'"'  '"\n')
            #fr.write('scope = "'/subscriptions/"' rgsource '"\n')
            fr.write('assignable_scopes = ' + scopes + '\n')
            fr.write('scope = ""\n')
            #
            
            
            fr.write('permissions {\n')        
            #print(json.dumps(dactions)) 
            fr.write('data_actions = ')
            fr.write(json.dumps(dactions))  
            
            fr.write('\nnot_data_actions = ')
            fr.write(json.dumps(ndactions)) 
        
            fr.write('\nactions = ')
            fr.write(json.dumps(actions)) 
        
            fr.write('\nnot_actions = ')
            fr.write(json.dumps(nactions)) 
            
            fr.write('\n}\n')
            """
            fr.write('assignable_scopes = \n')
            fr.write(json.dumps(scopes)) 
        
            """
            
            fr.write('\n}\n') 
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
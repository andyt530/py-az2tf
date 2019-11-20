import ast
def azurerm_policy_definition(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):  
    tfp="azurerm_policy_definition"
    
    azr=""
    if crf in tfp:
    # REST or cli
        #print "REST Pol Defn"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Authorization/policyDefinitions"
        params = {'api-version': '2019-01-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf="004-"+tfp+"-staterm.sh"
        tfimf="004-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            name=azr[i]["name"]
            #loc=azr[i]["location"]
            id=azr[i]["id"]
            rg="policydefinitions"
            rgs=id.split("/")[4]
          
            if crg is not None:
                if rg.lower() != crg.lower():
                    continue  # back to for

            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            pt=azr[i]["properties"]["policyType"]
            if pt == "Custom" :

                if cde:
                    print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)
                fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                #fr.write('\t location = "'+ loc + '"\n')
                #fr.write('\t resource_group_name = "'+ rgs + '"\n')

                rdid=azr[i]["name"]            
                mode=azr[i]["properties"]["mode"]
                rg="policyDefinitions"
                                

                
                try :
                    dname=azr[i]["properties"]["displayName"]
                    fr.write('display_name =  "'+dname+'"\n') 
                except KeyError:
                    fr.write('display_name = ""\n')
                    pass
            
                fr.write('policy_type = "' + pt +'"\n') 
                fr.write('mode = "' + mode + '"\n') 
                try :
                    desc=azr[i]["properties"]["description"]
                    fr.write('description =  "'+desc +'"\n') 
                except KeyError:
                    pass   
     
                #print(json.dumps(azr[i]["properties"]["metadata"], indent=4, separators=(',', ': ')))
                
                fr.write('metadata = jsonencode(\n') 
                fr.write(json.dumps(azr[i]["properties"]["metadata"]))
                fr.write(') \n') 

                prules=str(ast.literal_eval(json.dumps(azr[i]["properties"]["policyRule"])))
                fr.write('policy_rule = jsonencode( \n')
                fr.write(json.dumps(azr[i]["properties"]["policyRule"]))  
                fr.write(') \n') 
                
                try:
                    params=azr[i]["properties"]["parameters"]          
                    pl= len(params)
                    if pl > 0 :
                        fr.write('parameters = jsonencode( \n') 
                        fr.write(json.dumps(azr[i]["properties"]["parameters"])) 
                        fr.write(') \n') 
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
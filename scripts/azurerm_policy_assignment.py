
def azurerm_policy_assignment(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    
    tfp="azurerm_policy_assignment"
    azr=""
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Authorization/policyAssignments"
        params = {'api-version': '2019-01-01'}

        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]


        tfrmf="100-"+tfp+"-staterm.sh"
        tfimf="100-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print "# " + tfp,
        count=len(azr)
        print count
        for i in range(0, count):

            name=azr[i]["name"]
            #loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
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
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

    ###############
    # specific code
           
            dname=azr[i]["properties"]["displayName"]
            rdid=azr[i]["name"]
            desc=azr[i]"properties"]["description"]
            scope=azr[i]"properties"]["scope"]
            pdid=azr[i]"properties"]["policyDefinitionId"]
            id=azr[i]["id"]
            rg="policyAssignments"
            
            params=azr[i]"properties"]["parameters"]
                
            fr.write('display_name = "' + dname +'"\n') 
            fr.write('policy_definition_id = "' + pdid +'"\n') 
            fr.write('scope = "' +  scope +'"\n') 
            try :
                desc=azr[i]"properties"]["description"]
                fr.write('description =  "'+desc +'"\n') 
            except KeyError:
                pass

            pl=len(params)
            if pl > 0 :
                fr.write('parameters =<<PARAMETERS \n') 
                fr.write('"'+params +'"\n')
                fr.write('PARAMETERS\n') 
  

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print f.read()

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
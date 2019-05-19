def azurerm_management_lock(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    # management locks
    
    tfp="azurerm_management_lock"
    azr=""
    if crf in tfp:
        # REST
        # # print "REST VNets"
        url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Authorization/locks"
        params = {'api-version': '2017-04-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf="002-"+tfp+"-staterm.sh"
        tfimf="002-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print "# " + tfp,
        count=len(azr)
        print count
        for j in range(0, count):
            
            name=azr[j]["name"]
            name=name.encode('ascii', 'ignore')
            #loc=azr[j]["location"]
            id=azr[j]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            rgs=id.split("/")[4]
           
            level=azr[j]["properties"]["level"]
         
            scope1=id.split("/Microsoft.Authorization")[0].rstrip("providers")
            
            scope=scope1.rstrip("/")
            scope=scope.encode('ascii', 'ignore')

            if crg is not None:
                print "rgname=" + rg + " crg=" + crg
                if rg.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[j], indent=4, separators=(',', ': ')))

            rname=name.replace(".","-")
            rname=rname.replace("[","-")
            rname=rname.replace("]","-")
            rname=rname.replace(" ","_")
            rname=rname.encode('ascii', 'ignore')
            print rname 
            prefix=tfp+"."+rg+'__'+rname
            print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write('resource ' + tfp + ' "' + rg + '__' + rname + '" {\n')
            fr.write('\t name = "' + name + '"\n')
            #fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t lock_level = "'+ level + '"\n')   
            
            try:
                notes=azr[j]["properties"]["notes"]                
                fr.write('\t notes = "'+ notes + '"\n') 
            except KeyError:
                pass
            fr.write('\t scope = "'+ scope + '"\n')
        # tags block
            try:
                mtags=azr[j]["tags"]
            except:
                mtags="{}"
            tcount=len(mtags)-1
            if tcount > 1 :
                fr.write('tags { \n')
                print tcount
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write('\t "' + key + '"="' + tval + '"\n')
                #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
                fr.write('}\n')
            
            fr.write('}\n') 
            fr.close()  # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print f.read()

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')
            
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' "'+id+'"\n'
            tfim.write('echo "importing ' + str(j) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm=tfcomm.encode('ascii', 'ignore')
            tfim.write(tfcomm)  

        # end for
        tfrm.close()
        tfim.close()
        #end management locks
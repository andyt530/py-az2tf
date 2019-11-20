import uuid
def azurerm_management_lock(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    # management locks
    
    tfp="azurerm_management_lock"
    azr=""
    if crf in tfp:
        # REST
        # # print "REST VNets"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Authorization/locks"
        params = {'api-version': '2017-04-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

        tfrmf="002-"+tfp+"-staterm.sh"
        tfimf="002-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for j in range(0, count):
            
            name=azr[j]["name"]
            print("name=",name)
            #name=name.encode('utf-8', 'ignore')
            print("name=",name)
            #loc=azr[j]["location"]
            id=azr[j]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
           
            level=azr[j]["properties"]["level"]
         
            scope1=id.split("/Microsoft.Authorization")[0].rstrip("providers")
            
            scope=scope1.rstrip("/")
            sc=len(scope.split("/"))
            #print sc
            sn=scope.split("/")[sc-1].replace(" ","-").lower()
            sn=sn.replace(".","-")

            #scope=scope.encode('utf-8', 'ignore')
            #sn=sn.encode('utf-8', 'ignore')
            
         

            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[j], indent=4, separators=(',', ': ')))

            rname=name.replace(".","-")
            rname=rname.replace("[","-")
            rname=rname.replace("]","-")
            rname=rname.replace(" ","_")
            #try:
            #    rname=rname.encode('utf-8', 'ignore')
            #except UnicodeDecodeError:
            #    print('Problem with the name of this item: '+name)
            #    print('Please rename this item in the Azure Portal')
            #    rname=str(uuid.uuid4())
            #    #rname=rname.encode('utf-8', 'ignore')
                
                 
            try:
                prefix=tfp+"."+rg+'__'+rname+'__'+sn
            except UnicodeDecodeError:
                print('Problem with the scope name: '+scope)
                print('Please rename this item in the Azure Portal')
                sn=str(uuid.uuid4())
                #sn=sn.encode('utf-8', 'ignore')
                prefix=tfp+"."+rg+'__'+rname+'__'+sn
            #prefix=tfp+"."+rg+'__'+rname


            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write('resource ' + tfp + ' "' + rg + '__' + rname + '__'+ sn +  '" {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t lock_level = "'+ level + '"\n')   
            
            try:
                notes=azr[j]["properties"]["notes"]      
                #notes=notes.encode('utf-8', 'ignore')          
                fr.write('\t notes = "'+ notes + '"\n') 
            except KeyError:
                pass
            fr.write('\t scope = "'+ scope + '"\n')
        # tags block

    # tags block       
            try:
                mtags=azr[j]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    #fr.write(('\t "' + key + '"="' + tval + '"\n'))
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            #try:
            #    mtags=azr[j]["tags"]
            #except:
            #    mtags="{}"
            #tcount=len(mtags)-1
            #if tcount > 1 :
            #    fr.write('tags = { \n')
            #    print tcount
            #    for key in mtags.keys():
            #        tval=mtags[key]
            #        fr.write(('\t "' + key + '"="' + tval + '"\n'))
            #    #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
            #    fr.write('}\n')
            
            fr.write('}\n') 
            fr.close()  # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '__' + sn + '\n')
            
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname + '__'+ sn + ' "'+id+'"\n'
            tfim.write('echo "importing ' + str(j) + ' of ' + str(count-1) + '"' + '\n')
            #tfcomm=tfcomm.encode('utf-8', 'ignore')
            tfim.write(tfcomm)  

        # end for
        tfrm.close()
        tfim.close()
        #end management locks
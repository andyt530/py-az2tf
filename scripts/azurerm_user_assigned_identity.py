def azurerm_user_assigned_identity(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    # 015 user assigned identity
    tfp="azurerm_user_assigned_identity"
    azr=""
    if crf in tfp:
        
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.ManagedIdentity/userAssignedIdentities"
        params = {'api-version': '2018-11-30'}
        r = requests.get(url, headers=headers, params=params)
        azr=r.json()["value"]


 
        tfrmf="015-"+tfp+"-staterm.sh"
        tfimf="015-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for j in range(0, count):
            
            name=azr[j]["name"]
            loc=azr[j]["location"]
            id=azr[j]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                print ("rgname=" + rg + " crg=" + crg)
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde: print(json.dumps(azr[j], indent=4, separators=(',', ': ')))
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write("")
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "' + rgs + '"\n')
        # tags block
            try:
                mtags=azr[j]["tags"]
            except:
                mtags="{}"
            tcount=len(mtags)-1
            if tcount > 1 :
                fr.write('tags = { \n')
                #print tcount
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
                fr.write('}\n')
            
            fr.write('}\n') 
            fr.close()  # close .tf file

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')
            
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write('echo "importing ' + str(j) + ' of ' + str(count-1) + '"' + '\n')
            tfim.write(tfcomm)  

        # end for
        tfrm.close()
        tfim.close()
        #end user assigned identity
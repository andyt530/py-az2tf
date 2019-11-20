# azurerm_virtual_machine
def azurerm_virtual_machine_extension(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_virtual_machine_extension"
    tcode="291-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Compute/virtualMachines"
        params = {'api-version': '2019-03-01'}
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
            rgs=id.split("/")[4].lower()
            try:
                res=azr[i]["resources"]
                rname=name.replace(".","-")
                if crg is not None:
                    if rgs.lower() != crg.lower():
                        continue  # back to for        
                #
                icount=len(res)

            
                if icount > 0 :
                    
                    for j in range(0,icount):
                
                        url="https://" + cldurl + "/subscriptions/" + sub + "/resourceGroups/" + rg + "/providers/Microsoft.Compute/virtualMachines/"+name+"/extensions"
                    
                        params = {'api-version': '2019-03-01'}
                        r2 = requests.get(url, headers=headers, params=params)
                        azr2= r2.json()["value"]
                        if cde:
                            print(json.dumps(azr2[j], indent=4, separators=(',', ': ')))
                        ename=azr2[j]["name"]
                        ername=ename.replace(".","-")
                        id=azr2[j]["id"]
                        prefix=tfp+"."+rg+'__'+ rname +'__'+ ername
                        #print prefix
                        rfilename=prefix+".tf"
                        fr=open(rfilename, 'w')
                        fr.write(az2tfmess)
                        ename=azr2[j]["name"]
                        thv=azr2[j]["properties"]["typeHandlerVersion"]
                        pub=azr2[j]["properties"]["publisher"]
                        typ=azr2[j]["properties"]["type"]
                        auv=azr2[j]["properties"]["autoUpgradeMinorVersion"]


                        fr.write('resource ' + tfp + ' ' + rg + '__' + rname + '__'+ername +'{\n')
                        fr.write('\t name = "' + ename + '"\n')
                        fr.write('\t location = "'+ loc + '"\n')
                        fr.write('\t resource_group_name = "'+ rgs + '"\n')
                        fr.write('\t publisher = "'+ pub + '"\n')
                        fr.write('\t type_handler_version = "'+ thv + '"\n')
                        fr.write('\t virtual_machine_name = "'+ name + '"\n')
                        fr.write('\t type = "'+ typ + '"\n')
                        fr.write('\t auto_upgrade_minor_version = '+ str(auv).lower() + '\n')


                        try:
                            set=azr2[j]["properties"]["settings"]
                            slen=len(str(set))
                            
                            if slen > 2:
                                fr.write('settings = jsonencode( \n') 
                                fr.write(json.dumps(azr2[j]["properties"]["settings"]))
                                fr.write(')\n') 
                        except KeyError:
                            pass

        # tags block       
                        try:
                            mtags=azr2[j]["tags"]
                            fr.write('tags = { \n')
                            for key in mtags.keys():
                                tval=mtags[key]
                                tval=tval.replace('"',"'")
                                fr.write(('\t "' + key + '"="' + tval + '"\n'))
                            fr.write('}\n')
                        except KeyError:
                            pass

                        fr.write('}\n') 
                        fr.close()   # close .tf file

                        if cde:
                            with open(rfilename) as f: 
                                print (f.read())

                        tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname +'__'+ername + '\n')

                        tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                        
                        tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+'__'+ername+' '+id+'\n'
                        tfim.write(tfcomm)  
            except KeyError:
                pass

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub

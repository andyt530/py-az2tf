# azurerm_snapshot
def azurerm_shared_image_version(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_shared_image_version"
    tcode="343-"
    azr=""
    #cde=True
    if crf in tfp:
    # REST or cli
        # print "REST snapshot"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Compute/galleries"
        params = {'api-version': '2019-03-01'}
        r = requests.get(url, headers=headers, params=params)
        azr= r.json()["value"]

    
        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        
        count=len(azr)
  
        for i in range(0, count):

            gname=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
        
            url="https://" + cldurl + "/subscriptions/" + sub + "/resourceGroups/"+rg+"/providers/Microsoft.Compute/galleries/"+gname+"/images"
            params = {'api-version': '2019-03-01'}
            r = requests.get(url, headers=headers, params=params)
            azr2= r.json()["value"]
            jcount=len(azr2)
           
            for j in range(0, jcount):

                iname=azr2[j]["name"]
                rname=iname.replace(".","-")

                url="https://" + cldurl + "/subscriptions/" + sub + "/resourceGroups/"+rg+"/providers/Microsoft.Compute/galleries/"+gname+"/images/"+iname+"/versions"
                params = {'api-version': '2019-03-01'}
                r = requests.get(url, headers=headers, params=params)
                azr3= r.json()["value"]
                kcount=len(azr3)
                print ("# " + tfp,)
                print (kcount)
                for k in range(0, kcount):

                    if cde:
                        
                        print(json.dumps(azr3[k], indent=4, separators=(',', ': ')))

                    name=azr3[k]["name"]
                    loc=azr3[k]["location"]
                    id=azr3[k]["id"]
                    rg=id.split("/")[4].replace(".","-").lower()
                    if rg[0].isdigit(): rg="rg_"+rg
                    rgs=id.split("/")[4]
                    rname = name.replace(".", "-")
                    riname=iname.replace(".", "-")
                    prefix=tfp+"."+rg+'__'+gname+'__'+riname+'__'+rname
                    
                    #print prefix
                    rfilename=prefix+".tf"
                    fr=open(rfilename, 'w')
                    fr.write(az2tfmess)
                  
                    fr.write('resource ' + tfp + ' ' + rg + '__' + gname + '__' + riname + '__' + rname + ' {\n')  
                    fr.write('\t name = "' + name + '"\n')
                    fr.write('\t location = "'+ loc + '"\n')
                    fr.write('\t resource_group_name = "'+ rgs + '"\n')
                    fr.write('\t gallery_name = "'+ gname + '"\n')
                    fr.write('\t image_name = "'+ iname + '"\n')
                    mid=azr3[k]["properties"]["publishingProfile"]["source"]["managedImage"]["id"]  
                    fr.write('\t managed_image_id = "'+ mid + '"\n')
                    try:
                        tr=azr3[k]["properties"]["publishingProfile"]["targetRegions"]
                        tcount=len(tr)
                        
                        for t in range(0, tcount):
                            tnam=tr[t]["name"]
                            rrc=tr[t]["regionalReplicaCount"]
                            fr.write('\t target_region { \n')
                            fr.write('\t\t name ="'+tnam+'"\n') 
                            fr.write('\t\t regional_replica_count ="'+str(rrc)+'"\n')  
                            fr.write('\t} \n')



                    except KeyError:
                        pass



            # tags block       
                    try:
                        mtags=azr3[k]["tags"]
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

                   
                    tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+gname+'__'+riname+'__'+rname + '\n')
                    tfim.write('echo "importing ' + str(k) + ' of ' + str(kcount-1) + '"' + '\n')
                    tfcomm='terraform import '+tfp+'.'+rg+'__'+gname+'__'+riname+'__'+rname+' '+id+'\n'
                  
                    tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub

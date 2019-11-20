# azurerm_snapshot
def azurerm_shared_image(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_shared_image"
    tcode="342-"
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
            gloc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4].lower()
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
        


            url="https://" + cldurl + "/subscriptions/" + sub + "/resourceGroups/"+rg+"/providers/Microsoft.Compute/galleries/"+gname+"/images"
            params = {'api-version': '2019-03-01'}
            r = requests.get(url, headers=headers, params=params)
            azr2= r.json()["value"]
            jcount=len(azr2)
            print ("# " + tfp,)
            print (jcount)
            for j in range(0, jcount):
                
                if cde:
                    print(json.dumps(azr2[j], indent=4, separators=(',', ': ')))
                name=azr2[j]["name"]
                loc=azr2[j]["location"]
                id=azr2[j]["id"]

                rname=name.replace(".","-")
                
                prefix=tfp+"."+rg+'__'+gname+'__'+rname
                #print prefix
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)
                fr.write('resource ' + tfp + ' ' + rg + '__' + gname + '__' + rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                fr.write('\t location = "'+ loc + '"\n')
                fr.write('\t resource_group_name = "'+ rgs + '"\n')
                fr.write('\t gallery_name = "'+ gname + '"\n')

                try:
                    ost=azr2[j]["properties"]["osType"]
                    fr.write('\t os_type = "' +  ost + '"\n')
                except KeyError:
                    pass
                sku=azr2[j]["properties"]["identifier"]["sku"]
                pub=azr2[j]["properties"]["identifier"]["publisher"]
                off=azr2[j]["properties"]["identifier"]["offer"]
                fr.write('\t identifier { \n')
                fr.write('\t\t sku ="'+sku+'"\n')
                fr.write('\t\t publisher ="'+pub+'"\n')
                fr.write('\t\t offer ="'+off+'"\n')
                fr.write('\t} \n')


        # tags block       
                try:
                    mtags=azr2[j]["tags"]
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

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+gname+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(j) + ' of ' + str(jcount-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+gname+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub

def azurerm_resource_group(crf,cde,crg,headers,requests,sub,json,az2tfmess):
    # handle resource groups
    tfp="azurerm_resource_group"
    print tfp,
    tfrmf="001-"+tfp+"-staterm.sh"
    tfimf="001-"+tfp+"-stateimp.sh"
    tfrm=open(tfrmf, 'a')
    tfim=open(tfimf, 'a')
    url="https://management.azure.com/subscriptions/" + sub + "/resourceGroups"
    params = {'api-version': '2014-04-01'}
    r = requests.get(url, headers=headers, params=params)
    rgs= r.json()["value"]

    #frgfilename=tfp+".json"
    #frg=open(frgfilename, 'w')
    #frg.write(json.dumps(rgs, indent=4, separators=(',', ': ')))
    #frg.close()
    if cde:
        print(json.dumps(rgs, indent=4, separators=(',', ': ')))



    count=len(rgs)
    print count
    for j in range(0, count):
        
        name=rgs[j]["name"]
        rg=name
        loc=rgs[j]["location"]
        id=rgs[j]["id"]
        if crg is not None:
            if rg.lower() != crg.lower():
                continue
        
        rname=name.replace(".","-")
        prefix=tfp+"."+rname
        
        rfilename=prefix+".tf"
        fr=open(rfilename, 'w')
        fr.write("")
        fr.write('resource "' + tfp + '" "' + rname + '" {\n')
        fr.write('\t name = "' + name + '"\n')
        fr.write('\t location = "'+ loc + '"\n')
    

    # tags block
        try:
            mtags=rgs[j]["tags"]
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

        tfrm.write('terraform state rm '+tfp+'.'+rname + '\n')
        tfim.write('echo "importing ' + str(j) + ' of ' + str(count-1) + '"' + '\n')
        tfcomm='terraform import '+tfp+'.'+rname+' '+id+'\n'
        tfim.write(tfcomm)

    # end for
    tfrm.close()
    tfim.close()
    #end resource group
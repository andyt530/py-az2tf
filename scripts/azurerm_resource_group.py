import sys
def azurerm_resource_group(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    # handle resource groups
    isrun=False
    tfp="azurerm_resource_group"
    if crf in tfp:
        
        print('# ' + tfp,)
  
        tfrmf="001-"+tfp+"-staterm.sh"
        tfimf="001-"+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        url="https://" + cldurl + "/subscriptions/" + sub + "/resourceGroups"
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
        print (count)
        for j in range(0, count):
            
            name=rgs[j]["name"]
            rg=name
            loc=rgs[j]["location"]
            id=rgs[j]["id"]
            if crg is not None:
                if name.lower() != crg.lower():
                    continue
            
            rname=name.replace(".","-")
            if rg[0].isdigit(): rg="rg_"+rg
                
            if rname[0].isdigit(): rname="rg_"+rname
            prefix=tfp+"."+rname
            
            rfilename=prefix+".tf"
            if isrun:
                fr=sys.stdout
            else:
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
                fr.write('tags = { \n')
                #print tcount
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
                fr.write('}\n')
            
            fr.write('}\n') 
            if fr is not sys.stdout: fr.close()  # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rname + '\n')
            tfim.write('echo "importing ' + str(j) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rname+' '+id+'\n'
            tfim.write(tfcomm)

        # end for
        tfrm.close()
        tfim.close()
        #end resource group
# azurerm_dns_zone
def azurerm_logic_app_trigger_http_request(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_logic_app_trigger_http_request"
    tcode="631-"
    azr=""
    #cde=True
    
    if crf in tfp:
    # REST or cli
        # print "REST Managed Disk"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Logic/workflows"
        #params = {'api-version': '2016-04-01'}
        params = {'api-version': '2016-06-01'}       
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
            try:
                ttype=azr[i]["properties"]["definition"]["triggers"]["manual"]["kind"]
                if ttype != "Http":
                    continue




                name=azr[i]["name"]
                loc=azr[i]["location"]
                id=azr[i]["id"]
                rg=id.split("/")[4].replace(".","-").lower()
                if rg[0].isdigit(): rg="rg_"+rg
                rgs=id.split("/")[4]


                if crg is not None:
                    if rgs.lower() != crg.lower():
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

                fr.write('\t logic_app_id = "${azurerm_logic_app_workflow.' + rg + '__' + rname + '.id}"' + '\n')

        ###############
        # specific code start
        ###############
                try:
                    params=azr[i]["properties"]["definition"]["triggers"]["manual"]["inputs"]["schema"]
                    #print(json.dumps(params, indent=4, separators=(',', ': ')))
                    fr.write('schema = jsonencode(\n') 
                    fr.write(json.dumps(params, indent=4, separators=(',', ': ')))
                    fr.write(')\n')
                except KeyError:
                    pass      

        

                fr.write('}\n') 
                fr.close()   # close .tf file

                if cde:
                    with open(rfilename) as f: 
                        print (f.read())

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'/triggers/' + name +'\n'
                tfim.write(tfcomm)  

            except KeyError:
                pass
        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub

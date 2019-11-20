# azurerm_lb_probe
def azurerm_lb_probe(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_lb_probe"
    tcode="180-"
    
    if crf in tfp:
    # REST or cli
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.Network/loadBalancers"
        params = {'api-version': '2019-02-01'}
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
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))

            beap=azr[i]["properties"]["probes"]
            
            icount= len(beap)
            
            for j in range(0,icount):
                
                name=azr[i]["properties"]["probes"][j]["name"]
                rname= name.replace(".","-")
                id=azr[i]["properties"]["probes"][j]["id"]
                rg=id.split("/")[4].replace(".","-").lower()
                rgs=id.split("/")[4]
                lbrg=azr[i]["id"].split("/")[4].replace(".","-").lower()
                lbname=azr[i]["id"].split("/")[8].replace(".","-")

                prefix=tfp+"."+rg+'__'+lbname+'__'+rname
                #print prefix
                rfilename=prefix+".tf"
                fr=open(rfilename, 'w')
                fr.write(az2tfmess)



                fr.write('resource ' + tfp + ' ' + rg + '__' +lbname+ '__'+ rname + ' {\n')
                fr.write('\t name = "' + name + '"\n')
                fr.write('\t resource_group_name = "'+ rgs + '"\n')
 
                np=azr[i]["properties"]["probes"][j]["properties"]["numberOfProbes"]
                port=azr[i]["properties"]["probes"][j]["properties"]["port"]
                proto=azr[i]["properties"]["probes"][j]["properties"]["protocol"]

             

                if lbrg[0].isdigit(): lbrg="rg_"+lbrg 
                fr.write('\t\t loadbalancer_id = "${azurerm_lb.' + lbrg  + '__' + lbname + '.id}" \n')
                fr.write('\t\t protocol = "' +    proto + '"\n')
                fr.write('\t\t port = "' +    str(port) + '"\n')
                try:
                    rpath=azr[i]["properties"]["probes"][j]["properties"]["requestPath"]
                    fr.write('\t\t request_path = "' +    rpath + '"\n')
                except KeyError:
                    pass
                try:
                    inter=azr[i]["properties"]["probes"][j]["properties"]["intervalInSeconds"]
                    fr.write('\t\t interval_in_seconds = "' +  str(inter) + '"\n')
                except KeyError:
                    pass    

                fr.write('\t\t number_of_probes = "' +  str(np) + '"\n')

                fr.write('}\n') 
                fr.close()   # close .tf file

                if cde:
                    with open(rfilename) as f: 
                        print (f.read())

                tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+lbname+'__'+rname + '\n')

                tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
                tfcomm='terraform import '+tfp+'.'+rg+'__'+lbname+'__'+rname+' '+id+'\n'
                tfim.write(tfcomm)  
            # end for j loop
        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
